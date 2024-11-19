
import json
import vertexai
import base64
import requests
import time
import vertexai.preview.generative_models as generative_models
from vertexai.generative_models import GenerativeModel, Part, Content
from google.oauth2 import service_account
from google.cloud import aiplatform_v1, aiplatform, storage
from google.protobuf import struct_pb2
from typing import List, Union, Sequence, NamedTuple, Dict
from ..config import get_settings, GOOGLE_APPLICATION_CREDENTIALS
from .prompt import system_prompt, user_prompt
from ..services.firebase import FirebaseService
from loguru import logger

GOALS = system_prompt()
class EmbeddingResponse(NamedTuple):
  image_embedding: Sequence[float]

class EndpointType:
    FRONT = 'front'
    LOWER = 'lower'
    UPPER = 'upper'
class EmbeddingPredictionClient:
  _instance = None

  def __new__(cls):
    """
    Create a new instance of the class if it doesn't 
    exist, otherwise return the existing instance.
    """
    if cls._instance is None:
        cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self):
    self._settings= get_settings()
    self.client = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": self._settings.api_regional_endpoint}
    )

    self.endpoint = (f"projects/{self._settings.google_project_id}/locations/{self._settings.google_location_id}"
      "/publishers/google/models/multimodalembedding@001")
    
  def get_embedding(
    self,
    image_bytes : bytes = None
  ):
    if not image_bytes:
      raise ValueError('At least one of text or image_bytes must be specified.')

    instance = struct_pb2.Struct()

    if image_bytes:
      encoded_content = base64.b64encode(image_bytes).decode("utf-8")
      image_struct = instance.fields['image'].struct_value
      image_struct.fields['bytesBase64Encoded'].string_value = encoded_content

    instances = [instance]
    response = self.client.predict(endpoint=self.endpoint, instances=instances)

    image_embedding = None
    if image_bytes:    
      image_emb_value = response.predictions[0]['imageEmbedding']
      image_embedding = [v for v in image_emb_value]

    return EmbeddingResponse(
      image_embedding=image_embedding
    )

class VectorSearchService:
  _instance = None
  _settings = None

  def __new__(cls):
      """
      Create a new instance of the class if it doesn't 
      exist, otherwise return the existing instance.
      """
      if cls._instance is None:
          cls._instance = super().__new__(cls)
      return cls._instance
  
  def __init__(self):
    try:
      self._settings = get_settings()
      vertexai.init(
         project=self._settings.google_project_id, 
         location=self._settings.google_location_id
      )
      self.model = GenerativeModel(
          self._settings.gemini_model_name,
          system_instruction=[GOALS]
      )
      self.generation_config = {
          "max_output_tokens": 8192,
          "temperature": 0.6,
          "top_p": 0.95,
      }
      self.client = EmbeddingPredictionClient()

      self.safety_settings = {
          generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
          generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
      }
    except Exception as ex:
      logger.error(f"Error with Agent: {ex}")
  
  @property
  def credentials(self):
    if not self.credentials:
        try:
            self.credentials = service_account.Credentials.from_service_account_file(
              GOOGLE_APPLICATION_CREDENTIALS
            )
        except Exception as ex:
            print(f"Error: {ex}")

    return self.credentials
  
  @property
  def bucket(self):
    if not self.bucket:
      storage_client = storage.Client()
      self.bucket = storage_client.get_bucket(self._settings.cloud_storage_bucket)

    return self.bucket 

  def get_endpoint(self, type: EndpointType = EndpointType.FRONT) -> tuple:
    """Retrieve the endpoints based on the type provided."""
    endpoint_mapping = {
        EndpointType.FRONT: (self._settings.api_endpoint_v1, self._settings.index_endpoint_v1, self._settings.deploy_index_id_v1),
        EndpointType.LOWER: (self._settings.api_endpoint_v2, self._settings.index_endpoint_v2, self._settings.deploy_index_id_v2),
        EndpointType.UPPER: (self._settings.api_endpoint_v3, self._settings.index_endpoint_v3, self._settings.deploy_index_id_v3)
    }
    
    # Add error handling for missing keys
    if type not in endpoint_mapping:
      raise ValueError(f"Invalid endpoint type: {type}")
    
    api_endpoint, index_endpoint, deployed_index_id = endpoint_mapping[type]

    return api_endpoint, index_endpoint, deployed_index_id
  
  def parse_response(self, response_text: str):
    response_text = response_text.replace("```json", "").replace("```", "")
    try:
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        logger.debug(f"response_text: {response_text}")
        print(f"JSON decode error: {e}")
        return {}
  
  def parse_vertext_search_response(self, response, user_input: str = None):
    output = []
    cloud_bucket_uri = f"gs://{self._settings.cloud_storage_bucket}/{self._settings.cloud_storage_bucket_obj}"
    for r in response.nearest_neighbors:
      for n in r.neighbors:
        datapoint_id = n.datapoint.datapoint_id
        
        # Improved handling to avoid IndexError
        parts = datapoint_id.split("'")
        path = parts[1] if len(parts) > 1 else parts[0]

        if path:
            try:
              image_uri = f"{cloud_bucket_uri}/{path}.jpg"
              text = self.extract_teeth_info(document_id=path)
              
              output.append((
                Part.from_uri(mime_type="image/jpeg", uri=image_uri),
                text
              ))
            except Exception as e:
              logger.error(f"Unexpected error during vector search: {e}")

    if user_input:
      output.append((
        Part.from_uri(mime_type="image/jpeg", uri=user_input),
        ""
      ))
    
    return output
  
  def load_image_bytes(self, image_uri: str) -> bytes:
    """Load image bytes from a remote or local URI."""
    image_bytes = None

    if image_uri.startswith("http://") or image_uri.startswith("https://"):
        response = requests.get(image_uri, stream=True)
        if response.status_code == 200:
            image_bytes = response.content

    elif image_uri.startswith('gs://'):
      _ , blob_name = self._parse_gcs_uri(image_uri)
      bucket_ = self.bucket()
      blob = bucket_.blob(blob_name)
      # Download the image bytes from the GCS bucket
      image_bytes = blob.download_as_bytes()
    
    # Handle local file paths
    else:
        image_bytes = open(image_uri, "rb").read()
    return image_bytes
  
  def _parse_gcs_uri(self, gcs_uri: str) -> tuple:
    """Parse the GCS URI into bucket name and blob name."""
    parts = gcs_uri.replace("gs://", "").split("/", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid GCS URI: {gcs_uri}")
    return parts[0], parts[1]
  
  def _parse_to_gcs(self, image_uri: str) -> str:
    gs_prefix = "https://storage.googleapis.com/"
    if image_uri.startswith(gs_prefix):
        image_uri = f"gs://{image_uri[len(gs_prefix):]}"
    return image_uri
  
  def extract_feature_vector(self, image_path):
    """
    Extracts a feature vector from the given image.

    Args:
        image (PIL.Image.Image): An image from which to extract the feature vector.

    Returns:
        list: A list representing the feature vector.
    """
    # This is a placeholder example. Replace with actual feature extraction logic.
    # Load image
    try:
      image_bytes = self.load_image_bytes(image_path)
      feature_vector = self.client.get_embedding(image_bytes=image_bytes)
    except Exception as e:
        raise ValueError(f"Unable to open image at {image_path}: {e}")
    
    if hasattr(feature_vector, 'image_embedding'):
       return feature_vector.image_embedding
    
    return None

  def extract_teeth_info(self, document_id: str) -> Dict[str, int]:
      """Extract teeth information from a document."""
      callable = FirebaseService()
      doc = callable.fetch_one(document_id=document_id)

      if not doc:
          return {}

      fields = {
          'calculusGrade': 'calculus',
          'cariesGrade': 'caries',
          'gingivitisGrade': 'gingivitis',
          'mouthUlcerGrade': 'mouthUlcer',
          'discolorationGrade': 'discoloration'
      }

      output = {field: doc.get(key, 0) for key, field in fields.items()}
      return output
  
  def search_vector_by_image(
    self, 
    image_path, 
    neighbor_count=3,
    type: str = EndpointType.FRONT
  ) -> aiplatform_v1.FindNeighborsResponse:
    """
    Searches for vectors similar to the one extracted from the given image.

    Args:
        image_path (str): The path to the image file.
        neighbor_count (int): The number of nearest neighbors to retrieve. Default is 3.

    Returns:
        response: The response from the find_neighbors request.
    """
    
    # Extract feature vector from image
    feature_vector = self.extract_feature_vector(image_path)
    
    # Perform vector search using the extracted feature vector
    response = self.vector_search(feature_vector, neighbor_count, type)

    return response
  
  def vector_search(
    self,
    feature_vector: List[Union[int, float]],
    neighbor_count: int = 3,
    type: str = EndpointType.FRONT
  ) -> aiplatform_v1.FindNeighborsResponse:
    try:
        # Configure Vector Search client
        api_endpoint, index_endpoint, deploy_index_id = self.get_endpoint(type=type)
        client_options = {
            "api_endpoint": api_endpoint
        }

        vector_search_client = aiplatform_v1.MatchServiceClient(
            client_options=client_options
        )

        # Build FindNeighborsRequest object
        datapoint = aiplatform_v1.IndexDatapoint(
            feature_vector=feature_vector
        )

        query = aiplatform_v1.FindNeighborsRequest.Query(
            datapoint=datapoint,
            neighbor_count=neighbor_count  # The number of nearest neighbors to be retrieved
        )

        request = aiplatform_v1.FindNeighborsRequest(
            index_endpoint=index_endpoint,
            deployed_index_id=deploy_index_id,
            queries=[query],  # Request can have multiple queries
            return_full_datapoint=False,
        )
        
        # Execute the request
        response = vector_search_client.find_neighbors(request)

    except Exception as e:
        logger.error(f"Client error during vector search: {e}")
        raise

    return response
     
  def predict(self, image_path: str, type: str = EndpointType.FRONT):
    """
    Predict content based on an image.
    Retry if parse_response encounters JSON decode errors.

    Parameters:
    image_path (str): The path to the image file.

    Returns:
    dict: Parsed response content or empty dictionary if unsuccessful.
    """
    def clean_and_parse_json(response_text: str):
        """
        Clean the response text by removing code block markers and parse it as JSON.

        Parameters:
        response_text (str): The raw response text from the model.

        Returns:
        dict: Parsed JSON data.
        """
        cleaned_text = response_text.replace("```json", "").replace("```", "")
        return json.loads(cleaned_text)
    
    def generate_content_with_retries(prompt: str, retries: int = 3):
        """
        Generate content with retries in case of parsing errors.

        Parameters:
        prompt (str): The prompt to pass to the model.
        retries (int): The number of retries for generating content.

        Returns:
        dict: Parsed JSON data or None if unsuccessful after retries.
        """
        for attempt in range(retries):
            response = self.model.generate_content(
                [prompt],
                generation_config=self.generation_config,
                safety_settings=self.safety_settings,
                stream=False,
            )
            trace = ''
            try:
                if hasattr(response, 'text'):
                    trace = response.text
                    return clean_and_parse_json(trace)

                for candidate in response.candidates:
                    for part in getattr(candidate.content, 'parts', []):
                        if hasattr(part, 'text'):
                            trace = part.text
                            return clean_and_parse_json(trace)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error:: {trace},  error: {e}")
                if attempt < retries - 1:
                    time.sleep(1)  # Wait for a second before retrying

        return None
    
    # Step 1: Search for vectors using the image
    response = self.search_vector_by_image(image_path=image_path, neighbor_count=3, type=type)

    # Step 2: Convert the local image path to a GCS URI
    image_uri = self._parse_to_gcs(image_path)

    # Step 3: Parse response from vector search to find pairs
    pairs = self.parse_vertext_search_response(response, user_input=image_uri)

    # Step 4: If pairs are found, generate content using the model
    if pairs:
      prompt = user_prompt(pairs)
      result = generate_content_with_retries(prompt)
      if result:
          return result
    
    # Step 5: Return empty dictionary if no valid response is found
    return {}
  
  def calculator(self, results):
    """Choose max value from each item in array results and update a report."""
    if not results:
        return {}
    best_choice = {}
    for result in results:
        for key, value in result.items():
            if isinstance(value, int):
                if key not in best_choice or value > best_choice[key]:
                    best_choice[key] = value
    
    return best_choice

    
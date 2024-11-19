import os
import time
import asyncio

from app.model.data_consent_train import DataConsentTrain
from app.services.generate_report import render_reports
from app.utils.calculate_score import OralHealthScoreCalculator
from app.utils.date_time_utils import DateTimeUtils
from app.utils.helpers import Helpers
from ...subscription import Subscription
from app.constants import Constants
from app.core.client import VectorSearchService
from app.services.firebase import FirebaseService
from loguru import logger


TOPIC_ID = os.environ.get('PUBSUB_TOPIC_ID', 'AI-Colgate-Topic')
IS_TESTING = os.environ.get('IS_TESTING', 'false')
utils = Helpers()
dt_utils = DateTimeUtils()
calculator = OralHealthScoreCalculator()


class TaskAI(Subscription):
    topic = TOPIC_ID
    
    def __init__(self):
        self._func = self.handler
        super().__init__(self._func, self.topic)
    
    
    def handler(self, data, **kwargs):
        queue_type = data.get('queue_type')
        document_id = data.get('document_id')
        session_id = data.get('session_id')
        version = data.get('version', 1)
        logger.info(f"Calling Queue Type {queue_type} with version {version}")
        
        if queue_type == Constants.QUEUE_PREDICT:
            callable_service = VectorSearchService()
            consent_data = data.get('consent')
            self.handle_queue_predict(callable_service, data, document_id, consent_data)
        
        elif queue_type == Constants.QUEUE_GENERATE_REPORT:
            if document_id and session_id:
                result = asyncio.run(render_reports(document_id, session_id))
                return result
        
        elif queue_type == Constants.QUEUE_UPLOAD_IMAGE:
            image_id = data.get('image_id')
            file_name = data.get('file_name')
            start_time = time.time()
            
            if not (document_id and session_id):
                logger.error("Invalid document_id or session_id")
                return
            
            try:
                res_image = utils.get_retrieve_media_url(image_id)
                if not res_image:
                    logger.error(f"Failed to retrieve media URL for image_id: {image_id}")
                    return
                blob_name = f"{Constants.BUCKET_NAME}/{document_id}/{session_id}/{file_name}.jpg"
                payload = utils.upload_image(blob_name, res_image.get("url"))
                if not payload:
                    logger.error("Failed to upload image")
                    return
                
                client = FirebaseService()
                client.update_image(document_id, session_id, payload, file_name)
                if file_name == Constants.BUCKET_NAME_FRONT_TEETH_IMAGE:
                    user_data = client.get_user_data_by_sessions(document_id, session_id)
                    consent_data = client.get_consent_action(document_id)
                    utils.gemini_process(document_id, session_id, user_data, consent_data)
                
                logger.info(f"Firebase state extraction took {time.time() - start_time:.2f} seconds")
            
            except Exception as e:
                logger.debug(f"Error extracting Firebase state: {e}")
        elif queue_type == Constants.QUEUE_UPDATE_DATA_CONSENT_TRAIN:
            try:
                consent_data = data.get('consent')
                self.update_data_consent_train(document_id, consent_data)
                logger.info(f"Update consent success")

            except Exception as e:
                logger.debug(f"Error extracting Firebase state: {e}")
                
        elif queue_type == Constants.QUEUE_DELETE_USER_INFORMATION:
            try:
                utils.delete_user_information(document_id)
                logger.info(f"Delete user information success")
            except Exception as e:
                logger.debug(f"Error extracting Firebase state: {e}")
    
    
    def handle_queue_predict(self, callable_service, data, document_id, consent_data):
        images = data.get('images')
        full_path = data.get('full_path')
        if not images:
            return
        
        results = self.process_images(images, full_path, callable_service, document_id, consent_data)
        
        if document_id:
            session_id = data.get('session_id', document_id)
            try:
                best_choice = callable_service.calculator(results)
                self.update_report_to_firebase(document_id, session_id, best_choice)
            except Exception as e:
                logger.error(f"Error calculating best choice: {e}")
    
    def process_images(self, images, full_path, callable_service, document_id, consent_data):
        results = []
        for type_, image_path in images.items():
            start_time = time.time()
            try:
                response = self.predict_image(callable_service, image_path, type_)
                print("response: " + str(response))
                self.add_data_consent_train(document_id, response, type_, full_path, consent_data)
                results.append(response)
                elapsed_time = time.time() - start_time
                logger.info(f"Prediction for {type_} took {elapsed_time:.2f} seconds")
            except Exception as e:
                logger.error(f"Error predicting image {type_}: {e}")
        
        return results
    
    def predict_image(self, callable_service, image_path, type_):
        logger.info(f"Handling prediction for image type '{type_}' with IS_TESTING = {IS_TESTING}")
        
        if IS_TESTING == 'true':
            return Constants.FAKE_DUMMY
        
        return callable_service.predict(image_path=image_path, type=type_)
    
    def update_report_to_firebase(self, document_id, session_id, best_choice):
        try:
            client = FirebaseService()
            client.update_report(
                document_id=document_id,
                session_id=session_id,
                payload=best_choice
            )
            score_scenario = calculator.calculate_total_score(best_choice)
            print(f"score_scenario: {score_scenario}")

            client.set_user_score(document_id, score_scenario)
            logger.info(f"Collect best choice data received: {str(best_choice)}")
        except Exception as e:
            logger.error(f"Error updating report to firebase: {e}")
    
    def add_data_consent_train(self, document_id, response, type_, full_path, consent_data):
        try:
            print("full_path: " + str(full_path))
            client = FirebaseService()
            data_consent_train = DataConsentTrain(
                user_id=document_id,
                calculus_grade=response.get("calculus"),
                caries_grade=response.get("caries"),
                discoloration_grade=response.get("discoloration"),
                gingivitis_grade=response.get("gingivitis"),
                mouth_ulcer_grade=response.get("mouthUlcer"),
                consent=consent_data,
                created_at=dt_utils.get_current_datetime(),
                image_path=full_path.get(type_),
                pov=f"{type_}Teeth"
            )
            client.add_data_consent(data_consent_train)
            logger.info(f"Collect consent data received: {str(data_consent_train)}")
        except Exception as e:
            logger.error(f"Error updating report to firebase: {e}")
    
    def update_data_consent_train(self, document_id, consent_data):
        try:
            # Initialize the Firebase service client
            client = FirebaseService()
            
            # Create a DataConsentTrain object with the provided document_id and consent_data
            data_consent_train = DataConsentTrain(
                user_id=document_id,
                consent=consent_data
            )
            
            # Update the consent data in the Firestore using the client
            client.update_data_consent(document_id, data_consent_train)
            
            # Log a detailed success message with consent information
            logger.info(f"Successfully updated consent data for user ID: {document_id}. Consent data: {data_consent_train.dict(by_alias=True)}")
        except Exception as e:
            # Log an error message if there was an issue updating the consent data in Firestore
            logger.error(f"Error updating consent data for user ID: {document_id}. Exception: {e}")

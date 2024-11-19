import base64
import logging
import re
import datetime
import threading
import uuid
from typing import Optional, Dict, Any
from fastapi import (
    HTTPException
)
# from firebase_admin import credentials, firestore, storage  # type: ignore
from google.cloud import firestore, storage
from google.cloud.firestore_v1.base_query import FieldFilter

from google.oauth2 import service_account

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

from app.constants import Constants
from app.core.welcome_states import WelcomeStates
from ..config import get_settings, GOOGLE_APPLICATION_CREDENTIALS
from ..model.data_consent_log import DataConsentLog
from ..utils.date_time_utils import DateTimeUtils


logger = logging.getLogger()
dt_utils = DateTimeUtils()


class FirebaseService:
    _instance = None
    
    _collection = None
    _collection_audit_trail = None
    _helpers = None
    bucket = None
    baseUrl: str
    _instance: Optional['FirebaseService'] = None
    _listeners = {}
    
    def __new__(cls) -> 'FirebaseService':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            self._settings = get_settings()
            # Use google.oauth2 for authentication
            credentials = service_account.Credentials.from_service_account_file(
                GOOGLE_APPLICATION_CREDENTIALS
            )
            self.client = firestore.Client(credentials=credentials, project=credentials.project_id)
            self.collection = self._settings.firestore_collection
            
            # Initialize Cloud Storage client
            self.storage_client = storage.Client(credentials=credentials)
            self.bucket = self.storage_client.bucket(Constants.PRIVATE_BUCKET)
            
            self._collection = self.client.collection(Constants.COLLECTION_NAME)
            self._collection_audit_trail = self.client.collection(Constants.COLLECTION_AUDIT_TRAIL_LOG)
            self._collection_training_data = self.client.collection(Constants.COLLECTION_TRAINING_DATA)
            self.baseUrl = f"https://storage.googleapis.com/{Constants.BUCKET_NAME}"
            
            self.key = self._settings.aes_secret_key.encode('utf-8')
            self.iv = self._settings.aes_iv_key.encode('utf-8')
            self.backend = default_backend()
            self._initialized = True
    
    
    def generate_session_id(self):
        return f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}"
    
    def get_user_state(self, user_id):
        try:
            user_ref = self._collection.document(user_id)
            session_id = self.get_latest_session_id(user_ref)
            if session_id:
                doc_ref = user_ref.collection('sessions').document(session_id)
                doc = doc_ref.get()
                if doc.exists:
                    return doc.to_dict().get('state')
            return None
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error getting user state: {str(e)}"
            )
    
    
    def delete_user(self, user_id):
        try:
            user_ref = self._collection.document(user_id)
            user_ref.delete()
            print("User successfully deleted")
            return {"message": "User successfully deleted"}
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500,
                detail=f"Error deleting user: {str(e)}"
            )
    
    def get_user_data(self, user_id):
        try:
            user_ref = self._collection.document(user_id)
            session_id = self.get_latest_session_id(user_ref)
            if session_id:
                doc_ref = user_ref.collection('sessions').document(session_id)
                doc = doc_ref.get()
                if doc.exists:
                    return doc.to_dict()
            return None
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error getting user state: {str(e)}"
            )
    
    
    def get_user_data_by_sessions(self, user_id, session_id):
        try:
            user_ref = self._collection.document(user_id)
            doc_ref = user_ref.collection('sessions').document(session_id)
            doc = doc_ref.get()
            return doc.to_dict()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error getting user state: {str(e)}"
            )
    
    def save_user_state(self, user_id, state):
        try:
            user_ref = self._collection.document(user_id)
            session_id = self.get_latest_session_id(user_ref)
            if session_id:
                doc_ref = user_ref.collection('sessions').document(session_id)
                doc_ref.update({'state': state})
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error saving user state: {str(e)}"
            )
    
    def save_user_data(self, user_id, data):
        try:
            print("save_user_data: " + str(data))
            user_ref = self._collection.document(user_id)
            session_id = self.get_latest_session_id(user_ref)
            if session_id:
                doc_ref = user_ref.collection('sessions').document(session_id)
                doc_ref.update(data)
        except Exception as e:
            print(e)

    def set_user_score(self, user_id, score):
        try:
            user_ref = self._collection.document(user_id)
            session_id = self.get_latest_session_id(user_ref)
            if session_id:
                doc_ref = user_ref.collection('sessions').document(session_id)
                # Check if the document exists
                if doc_ref.get().exists:
                    # Get the existing score
                    current_score = doc_ref.get().to_dict().get("final_score", 0)
                    # Add the new score to the existing score
                    final_score = round(current_score + score, 1)
                    # Update the document with the new final score
                    doc_ref.update({"final_score": final_score})
                else:
                    # If the document does not exist, create it with the initial score
                    doc_ref.set({"final_score": round(score, 1)})
            return None
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error updating user score: {str(e)}"
            )

    def reset_user_score(self, user_id):
        try:
            user_ref = self._collection.document(user_id)
            session_id = self.get_latest_session_id(user_ref)
            if session_id:
                doc_ref = user_ref.collection('sessions').document(session_id)
                # Retrieve the score from the document
                if doc_ref.get().exists:
                    doc_ref.update({"final_score": 0})
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving user score: {str(e)}"
            )
    def log_consent_action(self, user_id, action_type):
        try:
            user_ref = self._collection.document(user_id)
            session_id = self.get_latest_session_id(user_ref)
            
            consent_log = DataConsentLog(
                user_id=user_id,
                action_type=action_type,
                session_id=session_id,
                timestamp=dt_utils.get_current_datetime()
            )
            doc_ref = user_ref.collection('consent_logs').document(session_id)
            if doc_ref.get().exists:
                doc_ref.update(consent_log.dict(by_alias=True))
            else:
                doc_ref.set(consent_log.dict(by_alias=True))
        except Exception as e:
            print(e)
    
    def set_audit_trail_log(self, user_id, data_audit_trail_log):
        try:
            # Query to check if a document with the specific user_id exists
            query = self._collection_audit_trail.where(filter=FieldFilter('user_id', '==', user_id))
            results = query.stream()
            
            # Convert results to a list to check if any documents exist
            results_list = list(results)
            
            if results_list:
                # If a document exists, update it
                for result in results_list:
                    result.reference.update(data_audit_trail_log.dict(by_alias=True, exclude_none=True))
            else:
                # If no document exists, create a new one
                user_ref = self._collection_audit_trail.document()
                user_ref.set(data_audit_trail_log.dict(by_alias=True, exclude_none=True))
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def set_consent_action(self, user_id, action_type):
        try:
            user_ref = self._collection.document(user_id)
            consent_status = True if action_type.lower() == Constants.ACTION_TYPE_CONSENT else False
            user_ref.set({"consent_image_train_model": consent_status}, merge=True)
            print(f"Consent status set to {consent_status} for user {user_id}.")
        except Exception as e:
            print(f"Error setting consent action for user {user_id}: {e}")
    
    def get_consent_action(self, user_id):
        try:
            user_ref = self._collection.document(user_id)
            doc = user_ref.get()
            if doc.exists:
                return doc.to_dict().get("consent_image_train_model", None)
            else:
                print(f"No document found for user {user_id}.")
                return None
        except Exception as e:
            print(f"Error retrieving consent action for user {user_id}: {e}")
            return None
    
    def add_data_consent(self, data_consent_train):
        try:
            user_ref = self._collection_training_data.document(None)
            user_ref.set(data_consent_train.dict(by_alias=True, exclude_none=True))
        except Exception as e:
            print(f"Error setting consent action : {e}")
    
    def update_data_consent(self, user_id, data_consent_train):
        try:
            # Query to check if a document with the specific user_id exists
            query = self._collection_training_data.where(filter=FieldFilter('userId', '==', user_id))
            results = query.stream()
            
            # Convert results to a list to check if any documents exist
            results_list = list(results)
            
            if results_list:
                # If a document exists, update it
                for result in results_list:
                    result.reference.update(data_consent_train.dict(by_alias=True, exclude_none=True))
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def save_user_history(self, user_id, message: str, auth: str):
        try:
            user_ref = self._collection.document(user_id)
            session_id = self.get_latest_session_id(user_ref)
            timestamp = int(datetime.datetime.now().timestamp())
            data = {f"{timestamp}_{auth}": message}
            print(data)
            user_ref = self._collection.document(user_id)
            doc_ref = user_ref.collection('history').document(session_id)
            # Check if the document exists
            if doc_ref.get().exists:
                doc_ref.update(data)
            else:
                doc_ref.set(data)
        except Exception as e:
            print(e)
    
    def user_exists(self, user_id):
        try:
            user_ref = self._collection.document(user_id)
            session_id = self.get_latest_session_id(user_ref)
            if session_id:
                doc_ref = user_ref.collection('sessions').document(session_id)
                doc = doc_ref.get()
                return doc.exists
            return False
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error checking if user exists: {str(e)}"
            )
    
    def create_user(self, user_id):
        try:
            session_id = self.generate_session_id()
            user_ref = self._collection.document(user_id).collection('sessions').document(session_id)
            user_ref.set({'state': WelcomeStates.WELCOME_PRIVACY_POLICY})
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error creating user: {str(e)}"
            )
    
    def get_latest_session_id_by_phone(self, user_id):
        user_ref = self._collection.document(user_id)
        session_id = self.get_latest_session_id(user_ref)
        return session_id
    
    def get_latest_session_id(self, user_ref):
        # Get the latest session ID based on the timestamp
        sessions = list(user_ref.collection('sessions').stream())
        latest_session = max(sessions, key=lambda s: s.id, default=None)
        return latest_session.id if latest_session else None
    
    def upload(self, image: str, blob_name: str):
        """Upload image to google cloud storage"""
        try:
            blob = self.bucket.blob(blob_name)
            codec = self.pre_format_base64code(image)
            decoded_image_data = base64.decodebytes(codec)
            blob.upload_from_string(decoded_image_data,
                                    content_type="image/jpg")
            
            url = blob.generate_signed_url(
                version="v4",
                # This URL is valid for 12 hours
                expiration=datetime.timedelta(hours=12),
                # Allow GET requests using this URL.
                method="GET",
            )
            data = {
                "file_name": blob_name,
                "url": url,
                "size": blob.size
            }
            
            return data
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Error")
    
    def delete_files_with_pattern(self, directory_prefix, pattern):
        try:
            # List all blobs (files) in the bucket
            blobs = self.bucket.list_blobs(prefix=directory_prefix)
            
            # Filter blobs that match the pattern and delete them
            for blob in blobs:
                if pattern in blob.name:
                    print(f"Deleting file: {blob.name}")
                    blob.delete()
                    print(f"File {blob.name} deleted successfully.")
            
            print("All matching files have been deleted.")
            return True
        
        except Exception as e:
            print(f"Error occurred while deleting files: {e}")
            return False
    
    def delete_folder(self, folder_name: str):
        try:
            # List all objects in the folder
            blobs = self.bucket.list_blobs(prefix=folder_name)
            
            # Delete all objects in the folder
            for blob in blobs:
                print(f"Deleting {blob.name}")
                blob.delete()
            
            print(f"Folder '{folder_name}' and its contents have been deleted successfully.")
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def delete_documents_by_user_id(self, user_id):
        try:
            # Query to find all documents with the specified user_id
            query = self._collection_training_data.where('userId', '==', user_id)
            results = query.stream()
        
            # Convert results to a list to check if any documents exist
            results_list = list(results)
        
            if results_list:
                # If documents exist, delete each one
                for result in results_list:
                    result.reference.delete()
                print(f"Deleted {len(results_list)} documents for user_id: {user_id}")
            else:
                print(f"No documents found for user_id: {user_id}")
    
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def remove(self, file_name):
        try:
            self.bucket.delete_blob(blob_name=file_name)
            return {"message": "Success in delete {} file".format(file_name)}
        except Exception:
            raise HTTPException(status_code=500, detail="Internal Error")
    
    def upload_to_firebase(self, pdf_path_local: str, blob_name: str):
        blob = self.bucket.blob(blob_name)
        blob.upload_from_filename(pdf_path_local)
        url = blob.generate_signed_url(
            version="v4",
            # This URL is valid for 2 hours
            expiration=datetime.timedelta(hours=2),
            # Allow GET requests using this URL.
            method="GET",
        )
        return url
    
    def pre_format_base64code(self, codec: str) -> str:
        base64_data = re.sub('^data:image/.+;base64,', '', codec)
        return base64_data.encode("utf-8")
    
    def update_data_by_session_id(
        self,
        document_id: str,
        session_id: str,
        payload,
    ) -> None:
        doc_ref = self._collection.document(document_id)
        try:
            session_ref = doc_ref.collection('sessions').document(session_id)
            print(f"{session_ref.get().exists}")
            if session_ref.get().exists:
                session_ref.update(payload)
        except Exception as e:
            logging.error(f"Failed to update report for document_id {document_id}: {e}")
     
    def update_image(
        self,
        document_id: str,
        session_id: str,
        payload: Dict,
        file_name: str
    ) -> None:
        doc_ref = self._collection.document(document_id)
        try:
            session_ref = doc_ref.collection('sessions').document(session_id)
            if session_ref.get().exists:
                session_ref.update({file_name: payload})
        except Exception as e:
            logging.error(f"Failed to update report for document_id {document_id}: {e}")
    
    def update_report(
        self,
        document_id: str,
        session_id: str,
        payload: Dict[str, Any],
        field: str = 'gemini_data'
    ) -> None:
        doc_ref = self._collection.document(document_id)
        try:
            session_ref = doc_ref.collection('sessions').document(session_id)
            if session_ref.get().exists:
                session_ref.update({
                    field: payload
                })
        except Exception as e:
            logging.error(f"Failed to update report for document_id {document_id}: {e}")
    
    def listen_document(
        self,
        document_id: str,
        session_id: str,
        reports_messages,
        send_message_callback,
    ) -> None:
        if self.is_listening(document_id, session_id):
            print(f"Already listening to document {document_id} and session {session_id}")
            return
        
        doc_ref = self._collection.document(document_id)
        try:
            # Create a callback on_snapshot function to capture changes
            def on_snapshot(doc_snapshot, changes, read_time):
                for doc in doc_snapshot:
                    print(f"Received document snapshot: {doc.id}")
                    send_message_callback(document_id, session_id, reports_messages, doc.to_dict())
            
            docs = doc_ref.collection('sessions').document(session_id)
            # Watch the document
            doc_watch = docs.on_snapshot(on_snapshot)
            
            # Store the listener for later unsubscription
            self._listeners[(document_id, session_id)] = doc_watch
        except Exception as e:
            
            logging.error(f"Failed to update report for document_id {document_id}: {e}")

    def generate_signed_url(self, blob_name, expiration_time=3600):
        blob = self.bucket.blob(blob_name)
    
        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(seconds=expiration_time),  # 1 hour
            method="GET",
        )
    
        return url
    
    def unsubscribe(self, document_id: str, session_id: str) -> None:
        try:
            # Unsubscribe from the snapshot listener
            listener = self._listeners.pop((document_id, session_id), None)
            if listener:
                listener.unsubscribe()
                print(f"Unsubscribed from document {document_id} and session {session_id}")
            else:
                print(f"No listener found for document {document_id} and session {session_id}")
        except Exception as e:
            print(f"Failed to update report for document_id {document_id}: {e}")
     
    def is_listening(self, document_id: str, session_id: str) -> bool:
        # Check if there's an active listener for the given document and session
        return (document_id, session_id) in self._listeners
    
    def fetch_one(self, document_id: str) -> firestore.DocumentSnapshot:
        doc_ref = self.client.collection(self.collection).document(document_id)
        
        try:
            doc = doc_ref.get()
            return doc.to_dict() if doc.exists else None
        except Exception as e:
            logging.error(f"Failed to fetch document with ID {document_id}: {e}")
            return None
    
    def _pad(self, data):
        # Manual padding to make data length a multiple of 16 bytes
        pad_length = 16 - (len(data) % 16)
        return data + (chr(pad_length) * pad_length).encode()
    
    def _unpad(self, data):
        # Remove padding
        pad_length = data[-1]
        return data[:-pad_length]
    
    def encrypt(self, raw_data):
        # Ensure the input data is in bytes
        if isinstance(raw_data, str):
            raw_data = raw_data.encode('utf-8')
        
        # Manually pad the data
        padded_data = self._pad(raw_data)
        
        # Encrypt the data
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=self.backend)
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Encode to base64 to make it easily storable
        return base64.b64encode(encrypted_data).decode('utf-8')
    
    def decrypt(self, enc_data):
        # Decode base64 encoded data
        encrypted_data = base64.b64decode(enc_data)
        
        # Decrypt the data
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=self.backend)
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # Remove the padding
        unpadded_data = self._unpad(decrypted_data)
        
        return unpadded_data.decode('utf-8')

import os
import time
import asyncio
from typing import Dict, Any, Optional

from app.model.data_consent_train import DataConsentTrain
from app.services.generate_report import render_reports
from app.utils.calculate_score import OralHealthScoreCalculator
from app.utils.date_time_utils import DateTimeUtils
from app.utils.helpers import Helpers
from app.constants import Constants
from app.core.client import VectorSearchService
from app.services.firebase import FirebaseService
from loguru import logger
from threading import Lock

class QueueProcessor:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(QueueProcessor, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.topic_id: str = os.getenv('PUBSUB_TOPIC_ID', 'AI-Colgate-Topic')
        self.is_testing: bool = os.getenv('IS_TESTING', 'false') == 'true'

        # Utility instances
        self.helpers: Helpers = Helpers()
        self.date_time_utils: DateTimeUtils = DateTimeUtils()
        self.score_calculator: OralHealthScoreCalculator = OralHealthScoreCalculator()
        self.vector_service: VectorSearchService = VectorSearchService()
        self.firebase_client: FirebaseService = FirebaseService()

    def handle(self, data: Dict[str, Any]) -> Optional[Any]:
        queue_type = data.get('queue_type')
        document_id = data.get('document_id')
        session_id = data.get('session_id')
        version = data.get('version', 1)

        logger.info(f"Processing Queue Type: {queue_type} (Version: {version})")

        if queue_type == Constants.QUEUE_PREDICT:
            self.handle_queue_predict(data, document_id, data.get('consent'))

        elif queue_type == Constants.QUEUE_GENERATE_REPORT:
            return self.generate_report(document_id, session_id)

        elif queue_type == Constants.QUEUE_UPLOAD_IMAGE:
            self.upload_image(data, document_id, session_id)

        elif queue_type == Constants.QUEUE_UPDATE_DATA_CONSENT_TRAIN:
            self.update_data_consent_train_handler(document_id, data.get('consent'))

        elif queue_type == Constants.QUEUE_DELETE_USER_INFORMATION:
            self.delete_user_information(document_id)

        logger.info(f"End process Queue Type: {queue_type} (Version: {version})")
        return True

    def generate_report(self, document_id: str, session_id: str) -> Optional[Any]:
        if document_id and session_id:
            return asyncio.run(render_reports(document_id, session_id))
        logger.error("Invalid document_id or session_id for report generation")
        return None

    def upload_image(self, data: Dict[str, Any], document_id: str, session_id: str) -> None:
        image_id = data.get('image_id')
        file_name = data.get('file_name')
        start_time = time.time()

        if not (document_id and session_id):
            logger.error("Invalid document_id or session_id")
            return

        try:
            media_url = self.helpers.get_retrieve_media_url(image_id)
            if not media_url:
                logger.error(f"Failed to retrieve media URL for image_id: {image_id}")
                return

            blob_name = f"{Constants.BUCKET_NAME}/{document_id}/{session_id}/{file_name}.jpg"
            upload_payload = self.helpers.upload_image(blob_name, media_url.get("url"))
            if not upload_payload:
                logger.error("Failed to upload image")
                return

            self.firebase_client.update_image(document_id, session_id, upload_payload, file_name)

            if file_name == Constants.BUCKET_NAME_FRONT_TEETH_IMAGE:
                user_data = self.firebase_client.get_user_data_by_sessions(document_id, session_id)
                consent_data = self.firebase_client.get_consent_action(document_id)
                self.helpers.gemini_process(document_id, session_id, user_data, consent_data)

            logger.info(f"Firebase state extraction took {time.time() - start_time:.2f} seconds")

        except Exception as e:
            logger.error(f"Error during image upload: {e}")

    def update_data_consent_train_handler(self, document_id: str, consent_data) -> None:
        try:
            self.update_data_consent_train(document_id, consent_data)
            logger.info("Update consent success")
        except Exception as e:
            logger.error(f"Error updating consent data: {e}")

    def delete_user_information(self, document_id: str) -> None:
        try:
            self.helpers.delete_user_information(document_id)
            logger.info("Delete user information success")
        except Exception as e:
            logger.error(f"Error deleting user information: {e}")

    def handle_queue_predict(self, data: Dict[str, Any], document_id: str, consent_data) -> None:
        images = data.get('images')
        full_path = data.get('full_path')
        if not images:
            logger.warning("No images provided for prediction.")
            return

        results = self.process_images(images, full_path, document_id, consent_data)

        if document_id:
            session_id = data.get('session_id', document_id)
            try:
                best_choice = self.vector_service.calculator(results)
                self.update_report_to_firebase(document_id, session_id, best_choice)
            except Exception as e:
                logger.error(f"Error calculating best choice: {e}")

    def process_images(self, images: Dict[str, str], full_path: Dict[str, str], document_id: str, consent_data) -> list:
        results = []
        for image_type, image_path in images.items():
            start_time = time.time()
            try:
                response = self.predict_image(image_path, image_type)
                self.add_data_consent_train(document_id, response, image_type, full_path, consent_data)
                results.append(response)
                logger.info(f"Prediction for {image_type} took {time.time() - start_time:.2f} seconds")
            except Exception as e:
                logger.error(f"Error predicting image {image_type}: {e}")

        return results

    def predict_image(self, image_path: str, image_type: str) -> Any:
        logger.info(f"Handling prediction for image type '{image_type}' with IS_TESTING = {self.is_testing}")
        return Constants.FAKE_DUMMY if self.is_testing else self.vector_service.predict(image_path=image_path, type=image_type)

    def update_report_to_firebase(self, document_id: str, session_id: str, best_choice: Any) -> None:
        try:
            self.firebase_client.update_report(document_id=document_id, session_id=session_id, payload=best_choice)
            score_scenario = self.score_calculator.calculate_total_score(best_choice)
            self.firebase_client.set_user_score(document_id, score_scenario)
            logger.info(f"Best choice data received: {str(best_choice)}")
        except Exception as e:
            logger.error(f"Error updating report to firebase: {e}")

    def add_data_consent_train(self, document_id: str, response: Dict[str, Any], image_type: str, full_path: Dict[str, str], consent_data) -> None:
        try:
            data_consent_train = DataConsentTrain(
                user_id=document_id,
                calculus_grade=response.get("calculus"),
                caries_grade=response.get("caries"),
                discoloration_grade=response.get("discoloration"),
                gingivitis_grade=response.get("gingivitis"),
                mouth_ulcer_grade=response.get("mouthUlcer"),
                consent=consent_data,
                created_at=self.date_time_utils.get_current_datetime(),
                image_path=full_path.get(image_type),
                pov=f"{image_type}Teeth"
            )
            self.firebase_client.add_data_consent(data_consent_train)
            logger.info(f"Consent data collected: {str(data_consent_train)}")
        except Exception as e:
            logger.error(f"Error adding data consent train: {e}")

    def update_data_consent_train(self, document_id: str, consent_data) -> None:
        try:
            data_consent_train = DataConsentTrain(user_id=document_id, consent=consent_data)
            self.firebase_client.update_data_consent(document_id, data_consent_train)
            logger.info(f"Successfully updated consent data for user ID: {document_id}. Consent data: {data_consent_train.dict(by_alias=True)}")
        except Exception as e:
            logger.error(f"Error updating consent data for user ID: {document_id}. Exception: {e}")

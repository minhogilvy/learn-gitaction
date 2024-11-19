import base64
import os
from typing import List, Optional

import requests
import logging
import functools

from app.constants import Constants
from app.core.publisher import publisher
from app.model.model_reports import DataReports, parse_data
from app.schemas.data_country import CountryDetail
from app.services.firebase import FirebaseService
import datetime
import time
import tracemalloc
import random

from playwright.async_api import async_playwright

from .date_time_utils import DateTimeUtils
from ..config import get_settings
from ..model.data_audit_trail_log import DataAuditTrailLog

import hashlib
import hmac


logger = logging.getLogger()
dt_utils = DateTimeUtils()
STORAGE_BASE_URL = "https://storage.googleapis.com/"


class Helpers:
    def __init__(self):
        self.firebase = FirebaseService()
        self._settings = get_settings()
    
    
    def upload_image(self, blob_name: str, image_url):
        # Download the image from the URL
        response = requests.get(image_url, headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {Constants.API_TOKEN}'})
        # Get image content
        image_content = response.content
        image_base64 = base64.b64encode(image_content).decode('utf-8')
        return self.firebase.upload(image_base64, blob_name)
    
    def delete_files_with_pattern(self, directory_prefix, pattern):
        return self.firebase.delete_files_with_pattern(directory_prefix, pattern)
    
    def upload_to_firebase(self, pdf_path, user_id: str, folder_name: str):
        name = "oral_basic_report"
        blob_name = f"{Constants.BUCKET_NAME}/{user_id}/{folder_name}/{name}.pdf"
        return self.firebase.upload_to_firebase(pdf_path, blob_name)
    
    def get_user_data(self, user_id: str, session_id: str):
        data = self.firebase.get_user_data_by_sessions(user_id, session_id)
        return parse_data(data)
    
    def parser_data_firebase(self, data):
        return parse_data(data)
    
    def delete_local_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
    
    def get_public_url(self, url: str) -> str:
        url = url.replace("gs://", STORAGE_BASE_URL)
        return url
    
    def pre_format_base64code(self, image: str) -> bytes:
        if isinstance(image, str):
            image = image.split(',')[1] if ',' in image else image
            return image.encode('utf-8')
        raise ValueError("Image must be a base64 encoded string")
    
    def get_retrieve_media_url(self, image_id: str):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {Constants.API_TOKEN}'
        }
        response = requests.get(f"{Constants.MEDIA_WHATSAPP_API_URL}{image_id}",
                                headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    def check_and_remove_process(self, input_string: str):
        if "_process" in input_string:
            output_string = input_string.replace("_process", "")
            return output_string
        else:
            return input_string
    
    def count_total_characters(self, input_string: str) -> int:
        return len(input_string)
    
    def get_date(self):
        return datetime.datetime.now().strftime('%m/%d/%Y')
    
    def get_message_string(self, message):
        messages = ""
        if hasattr(message, 'interactive') and message.interactive:
            if message.interactive.button_reply:
                messages = message.interactive.button_reply.title
            elif message.interactive.list_reply:
                messages = message.interactive.list_reply.title
        elif hasattr(message, 'text') and message.text:
            messages = message.text.body.lower()
        elif hasattr(message, 'image') and message.image:
            messages = f"image: {message.image.id}"
        return messages
    
    def get_country_by_name(self,
                            country_name: str,
                            valid_countries: List[CountryDetail]) -> Optional[CountryDetail]:
        # Find and return the country dictionary by its name
        for country in valid_countries:
            if country.name.lower() == country_name.lower():
                return country
        return None
    
    def generate_report(self, user_id, session_id):
        payload = {
            'queue_type': Constants.QUEUE_GENERATE_REPORT,
            'document_id': user_id,
            'session_id': session_id
        }
        publisher(payload)
    
    def gemini_process(self, user_id, session_id, user_data, consent_data):
        payload = {
            'queue_type': Constants.QUEUE_PREDICT,
            'document_id': user_id,
            'session_id': session_id,
            'consent': consent_data,
            'images': {
                'front': user_data.get("front_teeth").get("url"),
                'lower': user_data.get("lower_jaw").get("url"),
                'upper': user_data.get("upper_jaw").get("url")
            },
            'full_path': {
                'front': user_data.get("front_teeth").get("file_name"),
                'lower': user_data.get("lower_jaw").get("file_name"),
                'upper': user_data.get("upper_jaw").get("file_name"),
            }
        }
        response = publisher(payload)
    
    async def render_with_playwright(self, html_content):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.set_content(html_content, wait_until='load')
            start_time = time.time()
            tracemalloc.start()
            pdf_path = "playwright_output.pdf"
            await page.pdf(path=pdf_path, print_background=True, scale=1)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            end_time = time.time()
            await browser.close()
            return pdf_path, end_time - start_time, peak / 10 ** 6  # Convert to MB
    
    def encrypt(self, raw_data):
        return self.firebase.encrypt(raw_data)
    
    def decrypt(self, enc_data):
        return self.firebase.decrypt(enc_data)
    
    def set_consent_action(self, user_id, action_type):
        self.firebase.set_consent_action(user_id, action_type)
        self.firebase.log_consent_action(user_id, action_type)
        payload = {
            'queue_type': Constants.QUEUE_UPDATE_DATA_CONSENT_TRAIN,
            'document_id': user_id,
            'consent': True if action_type == Constants.ACTION_TYPE_CONSENT else False
        }
        response = publisher(payload)
        print("response: " + str(response))
    
    def set_audit_trail_log(self, user_id, data_audit_trail_log):
        self.firebase.set_audit_trail_log(user_id, data_audit_trail_log)
    
    def delete_user_information(self, user_id):
        self.firebase.delete_user(user_id)
        self.firebase.delete_documents_by_user_id(user_id)
        self.firebase.delete_folder(user_id)
        current_time_readable = dt_utils.get_current_datetime()
        data_audit_trail_log = DataAuditTrailLog(
            user_id=user_id,
            system_delete=current_time_readable
        )
        self.set_audit_trail_log(user_id, data_audit_trail_log)
        
    def verify_signature(self, secret: str, payload: bytes, signature: str) -> bool:
        """Verifies the HMAC SHA1 signature."""
        hash_ = hmac.new(secret.encode('utf-8'), payload, hashlib.sha1).hexdigest()
        return hmac.compare_digest(f'sha1={hash_}', signature)

    def random_bool(self):
        return random.choice([Constants.ACTION_TYPE_CONSENT, Constants.ACTION_TYPE_DE_CONSENT])

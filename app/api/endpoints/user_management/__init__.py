from google.cloud import firestore
from app.core.config import SERVICE_ACCOUNT_KEY_FILE_PATH

USER_MANAGEMENT_TAG = "User Management"
USER_MANAGEMENT_TAG_V2 = "User Management V2"

firestore_client = firestore.Client.from_service_account_json(SERVICE_ACCOUNT_KEY_FILE_PATH)

USER_DETAILS = {
    "id": "Agfrt234dfg",
    "email": "abc@gmail.com",
    "password": "Password@123",
    "mobile_no": "9700000000",
    "first_name": "Abc",
    "last_name": "Xyz"
}

CREATE_USER_REQUEST_BODY_EXAMPLE = {
    "email": "abc@gmail.com",
    "password": "Password@123",
    "mobile_no": "9700000000",
    "first_name": "Abc",
    "last_name": "Xyz"
}

UPDATE_USER_REQUEST_BODY_EXAMPLE = {
    "email": "abc@gmail.com",
    "password": "Password@123",
}
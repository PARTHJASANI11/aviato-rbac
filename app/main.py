from fastapi import FastAPI
from app.api.api import router
from app.db.connector import db_connector
from app.middleware.auth_middleware import AuthMiddleware
from openapi.custom_api_spec import tags_metadata

# FastAPI App
app = FastAPI(
    title="Aviato RBAC",
    version="1.0.0",
    openapi_tags=tags_metadata,
    description="Role Based Access Control Endpoints",
)

app.add_middleware(AuthMiddleware)
app.add_event_handler(
    "startup", db_connector.create_database_connection
)
app.add_event_handler(
    "shutdown", db_connector.close_database_connection
)
app.include_router(router)

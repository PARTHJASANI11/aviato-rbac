from fastapi import APIRouter
from app.api import API_PREFIX

from app.api.endpoints.user_management.post_user import router as post_user
from app.api.endpoints.user_management.get_user import router as get_user
from app.api.endpoints.user_management.delete_user import router as delete_user
from app.api.endpoints.user_management.update_user import router as update_user

router = APIRouter(prefix=API_PREFIX)

router.include_router(post_user)
router.include_router(get_user)
router.include_router(delete_user)
router.include_router(update_user)
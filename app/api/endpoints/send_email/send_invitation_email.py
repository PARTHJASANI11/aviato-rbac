from fastapi import APIRouter, status, BackgroundTasks, Header
from app.api import SEND_INVITATION_EMAIL
from app.api.endpoints.send_email import SEND_EMAIL_TAG
from app.schemas.send_email import SendInvitationEmailRequest, SendInvitationEmailResponse
from app.core.logger import logger
from jinja2 import Environment, FileSystemLoader
from app.core.config import TEMPLATES_DIR, MAIL_CONF
from fastapi_mail import MessageSchema, FastMail
from openapi.custom_api_spec import send_invitation_email_responses
 
router = APIRouter()

@router.post(
    SEND_INVITATION_EMAIL,
    tags=[SEND_EMAIL_TAG],
    description="Send an invitation email",
    status_code=status.HTTP_200_OK,
    response_model=SendInvitationEmailResponse,
    responses={**send_invitation_email_responses},
)
async def send_invitation_email(
    send_invitation_email_payload: SendInvitationEmailRequest,
    background_tasks: BackgroundTasks,
    secret_key: str = Header(),
):
    """ 
    Endpoint to send an invitation email

    :param background_tasks: To make the email sending as background task
    """
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("invitation_template.html.j2")

    html_content = template.render(
        redoc_link=send_invitation_email_payload.redoc_url, 
        github_url=send_invitation_email_payload.github_url)
    
    message = MessageSchema(
        subject="Invitation to View API Documentation by Parth Jasani",
        recipients=send_invitation_email_payload.emails,
        body=html_content,
        subtype="html"
    )

    fastapi_mail = FastMail(MAIL_CONF)

    await fastapi_mail.send_message(message)

    logger.info("Email sent successfully to the users: %s" % send_invitation_email_payload.emails)
    
    return {"message": "Email sent successfully"}
    
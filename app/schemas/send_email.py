from pydantic import BaseModel, conlist, constr

class SendInvitationEmailRequest(BaseModel):
    """
    Request body for send invitation email endpoint
    """
    emails: conlist(str, min_length=1)
    redoc_url: constr(strip_whitespace=True)
    github_url: constr(strip_whitespace=True)

class SendInvitationEmailResponse(BaseModel):
    """
    Response for send invitation email endpoint 
    """
    message: str
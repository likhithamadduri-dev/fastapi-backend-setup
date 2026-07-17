from pydantic import BaseModel
from typing import Optional


class UpdateOrganizationProfileRequest(BaseModel):

    organization_name: Optional[str] = None
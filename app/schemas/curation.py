from typing import Dict, Optional

from pydantic import BaseModel


class CurationResponseSchema(BaseModel):
    status: str
    result: Optional[Dict]

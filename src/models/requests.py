from pydantic import BaseModel

class InsertRequest(BaseModel):
    metadata: list[dict[str, str | int | float]]

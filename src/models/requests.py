from pydantic import BaseModel

class InsertRequest(BaseModel):
    metadata: dict[str, str | int | float | dict[str, str | int | float]]

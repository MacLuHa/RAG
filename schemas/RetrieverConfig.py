from pydantic import BaseModel, field_validator

class RetrieverConfig(BaseModel):
    api_key: str | None 
    model: str

    @field_validator('api_key')
    def validate_api_key(cls, value):
        if value is None:
            raise ValueError(
                'Api key not set - Embedder'
            )
        return value 

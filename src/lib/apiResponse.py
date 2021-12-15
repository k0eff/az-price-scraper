from pydantic import Field, BaseModel

class apiResponse(BaseModel):
    hello: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
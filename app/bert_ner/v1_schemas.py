from typing import List, Any

from pydantic import BaseModel, Field

from app import api_settings


class ErrorMessage(BaseModel):
    detail: str = Field(description="Human-readable error message.")


class RequestModel(BaseModel):
    text: str = Field(...,
                      description="Original text input. May contain multiple sentences.",
                      example="Tere, Mari!",
                      max_length=api_settings.max_input_length)

    def __init__(self, **data: Any):
        super(RequestModel, self).__init__(**data)


class ResponseToken(BaseModel):
    word: str = Field(...,
                      description="Original word.",
                      example="Mari")
    ner: str = Field(...,
                     description="Named entity tag.",
                     example="B-PER")


class ResponseModel(BaseModel):
    result: List[List[ResponseToken]] = Field(...,
                                              description="List of sentences, each containing a list of words with "
                                                          "named entity tags.")

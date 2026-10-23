
from pydantic import BaseModel, Field, field_validator


class AskRequest(BaseModel):
    question: str = Field(min_length=1)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Question cannot be empty")
        return value


class SourceItem(BaseModel):
    text: str
    metadata: dict[str, str | int | float]
    distance: float


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceItem]

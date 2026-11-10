from pydantic import BaseModel, Field

class SummaryResponse(BaseModel):
    summary: str = Field(
        min_length = 20,
        description = "A concise summary of the input text"
    )

    keywords: list[str] = Field(
        min_length = 5,
        max_length = 5,
        description = "Exactly 5 important keywords"
    )
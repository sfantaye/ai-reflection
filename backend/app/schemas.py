from pydantic import BaseModel, Field
from typing import List

# Request and Response Models
class JournalEntry(BaseModel):
    entry: str

class ReflectionResponse(BaseModel):
    reflection: str
    affirmation: str
    follow_ups: List[str]
    
class ReflectionModel(BaseModel):
    reflection: str = Field(description="Empathetic response to the journal entry")
    followup: str = Field(description="Thought-provoking question based on reflection")

class AffirmationModel(BaseModel):
    affirmation: str = Field(description="Supportive statement based on journal entry")
    followup: str = Field(description="Uplifting question to reinforce affirmation")
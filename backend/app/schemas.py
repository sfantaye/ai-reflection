from pydantic import BaseModel

# Request and Response Models
class JournalEntry(BaseModel):
    entry: str

class ReflectionResponse(BaseModel):
    reflection: str
    affirmation: str
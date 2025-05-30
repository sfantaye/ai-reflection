from fastapi import APIRouter, HTTPException
from app.schemas import JournalEntry, ReflectionResponse
from app.agents import build_graph

router = APIRouter()
graph = build_graph()

@router.post("/reflect", response_model=ReflectionResponse)
async def reflect(entry: JournalEntry):
    if not entry.entry.strip():
        raise HTTPException(status_code=400, detail="Journal entry is empty.")
    
    result = graph.invoke({"user_input": entry.entry})
    return result["final_response"]

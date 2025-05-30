from typing import TypedDict, Any
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from app.config import settings 

from app.schemas import JournalEntry, ReflectionResponse

# --- Define the State Schema ---
class GraphState(TypedDict):
    user_input: str             
    intake: str                 
    reflection: str            
    affirmation: str            
    final_response: ReflectionResponse 



def intake_agent(state: GraphState) -> dict[str, Any]:
    user_input = state["user_input"]
    return {"intake": user_input.strip()} 
def reflection_agent(state: GraphState) -> dict[str, Any]:
    intake_content = state["intake"]
    prompt = PromptTemplate.from_template(
        "Given the journal entry: '{entry}', provide a short empathetic reflection (1-2 sentences)."
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", 
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0.7, 
    )
    chain = prompt | llm
    result = chain.invoke({"entry": intake_content})
    return {"reflection": result.content.strip()}

def affirmation_agent(state: GraphState) -> dict[str, Any]:
    intake_content = state["intake"]
    prompt = PromptTemplate.from_template(
        "Based on the following journal entry: '{entry}', return a brief, supportive affirmation."
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", 
        google_api_key=settings.GEMINI_API_KEY,
        temperature=0.7
    )
    chain = prompt | llm
    result = chain.invoke({"entry": intake_content})
    return {"affirmation": result.content.strip()}


def orchestrator(state: GraphState) -> dict[str, Any]:
    reflection_content = state["reflection"]
    affirmation_content = state["affirmation"]
    response = ReflectionResponse(reflection=reflection_content, affirmation=affirmation_content)
    return {"final_response": response}



def build_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("process_intake", intake_agent)
    workflow.add_node("generate_reflection", reflection_agent)
    workflow.add_node("generate_affirmation", affirmation_agent)
    workflow.add_node("compile_response", orchestrator)

    workflow.set_entry_point("process_intake")
    workflow.add_edge("process_intake", "generate_reflection")
    workflow.add_edge("generate_reflection", "generate_affirmation")
    workflow.add_edge("generate_affirmation", "compile_response")
    workflow.add_edge("compile_response", END)

    return workflow.compile()
from typing import TypedDict, Any, List, Literal
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from app.config import settings
from app.schemas import ReflectionResponse, ReflectionModel, AffirmationModel

# --- Shared LLM Setup ---
def get_gemini_llm(temperature: float = 0.7):
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=settings.GEMINI_API_KEY,
        temperature=temperature,
    )





REFLECTION_PROMPT = PromptTemplate.from_template(
    """Given the journal entry: '{entry}', provide:
1. A short empathetic reflection (1-2 sentences)
2. One thoughtful follow-up question

{format_instructions}"""
).partial(format_instructions=JsonOutputParser(pydantic_object=ReflectionModel).get_format_instructions())

AFFIRMATION_PROMPT = PromptTemplate.from_template(
    """Based on the following journal entry: '{entry}', provide:
1. A brief, supportive affirmation
2. One uplifting follow-up question

{format_instructions}"""
).partial(format_instructions=JsonOutputParser(pydantic_object=AffirmationModel).get_format_instructions())

FOLLOW_UP_PROMPT = PromptTemplate.from_template(
    """Journal Entry: {intake}
Reflection: {reflection}
Affirmation: {affirmation}

Based on the above, generate exactly two thought-provoking follow-up questions that encourage deeper self-reflection.
Make them personal, empathetic, and relevant to the content of the journal.

Return only the questions, each on a new line."""
)

class GraphState(TypedDict):
    user_input: str            
    intake: str                 
    reflection: str             
    reflection_followup: str    
    affirmation: str            
    affirmation_followup: str   
    follow_ups: List[str]       
    final_response: ReflectionResponse  


def intake_agent(state: GraphState) -> dict[str, Any]:
    user_input = state["user_input"]
    return {"intake": user_input.strip()}

def reflection_agent(state: GraphState) -> dict[str, Any]:
    intake_content = state["intake"]
    parser = JsonOutputParser(pydantic_object=ReflectionModel)
    llm = get_gemini_llm()
    chain = REFLECTION_PROMPT | llm | parser
    result = chain.invoke({"entry": intake_content})
    return {
        "reflection": result["reflection"],
        "reflection_followup": result["followup"]
    }

def affirmation_agent(state: GraphState) -> dict[str, Any]:
    intake_content = state["intake"]
    parser = JsonOutputParser(pydantic_object=AffirmationModel)
    llm = get_gemini_llm()
    chain = AFFIRMATION_PROMPT | llm | parser
    result = chain.invoke({"entry": intake_content})
    return {
        "affirmation": result["affirmation"],
        "affirmation_followup": result["followup"]
    }

def followup_agent(state: GraphState) -> dict[str, Any]:
    intake = state["intake"]
    reflection = state["reflection"]
    affirmation = state["affirmation"]

    llm = get_gemini_llm()
    chain = FOLLOW_UP_PROMPT | llm

    result = chain.invoke({
        "intake": intake,
        "reflection": reflection,
        "affirmation": affirmation
    })

    follow_ups = [line.strip() for line in result.content.strip().split("\n") if line.strip()]
    
    return {"follow_ups": follow_ups[:2]} 

def orchestrator(state: GraphState) -> dict[str, Any]:
    response = ReflectionResponse(
        reflection=state["reflection"],
        affirmation=state["affirmation"],
        follow_ups=state["follow_ups"]
    )
    return {"final_response": response}

def route_to_reflection_or_affirmation(state: GraphState) -> Literal["generate_reflection", "generate_affirmation"]:
    return ["generate_reflection", "generate_affirmation"]

def build_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("process_intake", intake_agent)
    workflow.add_node("generate_reflection", reflection_agent)
    workflow.add_node("generate_affirmation", affirmation_agent)
    workflow.add_node("generate_followups", followup_agent)
    workflow.add_node("compile_response", orchestrator)

    workflow.set_entry_point("process_intake")
    
    # Fan-out to run reflection and affirmation in parallel
    workflow.add_conditional_edges(
        "process_intake",
        route_to_reflection_or_affirmation,
    )
    
    workflow.add_edge("generate_reflection", "generate_followups")
    workflow.add_edge("generate_affirmation", "generate_followups")
    workflow.add_edge("generate_followups", "compile_response")
    workflow.add_edge("compile_response", END)

    return workflow.compile()
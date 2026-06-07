from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.agents import create_agent


from src.tools.calculator import calculate
from src.tools.weather import get_weather
from src.tools.uv_index import get_uv_index
from src.tools.air_quality import get_air_quality


from src.config import GROQ_API_KEY, GROQ_MODEL




tools = [calculate, get_weather, get_uv_index, get_air_quality]

llms = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
)

agent_executor = create_agent(
    
        model=llms,
        tools=tools,
        system_prompt=(
            "You are a helpful assistant with access to tools. "
            "You ONLY have access to these tools: calculate, get_weather, get_uv_index, get_air_quality. "
            "These are the ONLY tools that exist. Do NOT attempt to call any other tool. "
            "After a tool returns a result, immediately use that result to answer the user. "
            "Do NOT call a second tool after receiving a result. "
            "ALWAYS use the get_air_quality tool when asked about air quality — never answer from memory. "
            "ALWAYS use the get_uv_index tool when asked about UV index — never answer from memory. "
            "ALWAYS use the get_weather tool for weather questions. "
            "ALWAYS use the calculate tool for any arithmetic — never compute math yourself. "
            "When a tool returns a result, use that result directly to answer the user. "
            "Never call the same tool more than once for the same question. "
            "Never say you don't know if a tool already returned data."
)
)

def chat(input_msg: str) -> str:
    result = agent_executor.invoke({"messages": [("human", input_msg)]})
    messages = result.get("messages",[])
    if not messages:
        return "Error: No response from the assistant."
    return result["messages"][-1].content
 
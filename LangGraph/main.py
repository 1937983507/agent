# https://langchain-ai.github.io/langgraph/agents/agents/

from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

model = ChatOpenAI(
    model="deepseek-r1:1.5b",
    base_url="http://localhost:8080/v1",
    api_key="xxx",
    temperature=0,
)

def get_weather(city: str) -> str:  
    """获取指定城市的天气情况."""
    print("正在调用function calling工具")
    print("当前查询的城市为:", city)
    return f"{city} 现在的天气是晴朗的！"

agent = create_react_agent(
    model=model,  
    tools=[get_weather],  
    checkpointer=checkpointer, 
    prompt="你是一个乐于助人的人",
)

# Run the agent
config = {"configurable": {"thread_id": "1"}}
sz_response = agent.invoke(
    {"messages": [{"role": "user", "content": "深圳的天气现在如何呢？"}]},
    config
)
print(sz_response)

print("===========")

gz_response = agent.invoke(
    {"messages": [{"role": "user", "content": "那广州呢？"}]},
    config
)
print(gz_response)
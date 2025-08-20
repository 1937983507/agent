import asyncio
from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
    function_tool,
)

BASE_URL = "http://localhost:8080/v1"
API_KEY = "xxx"
MODEL_NAME = "deepkseek-r1:1.5b"


set_default_openai_api("chat_completions")
set_default_openai_client(AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY))
# 该示例中禁止使用追踪
#如需使用自定义追踪处理器，请参考：https://openai.github.io/openai-agents-python/tracing/#external-tracing-processors-list to use the custom spans.
set_tracing_disabled(disabled=True)

@function_tool
def get_weather(city: str) -> str:
    print("正在调用function tool")
    print("输入参数为：", city)
    return f"{city}目前的天气是晴朗的"

agent = Agent(
    name="机器人",
    instructions="你是一个乐于助人的机器人",
    tools=[get_weather],
    model=MODEL_NAME,
)

async def main():
    result = await Runner.run(agent, input="深圳的天气如何呢?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
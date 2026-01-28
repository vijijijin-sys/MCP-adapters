# RUN IN A SECOND TERMINAL - uv run servers/weather_server.py
import asyncio
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv


load_dotenv()


async def main():
    # Manual weather client (SSE)
    weather_client = MultiServerMCPClient(
        {
            "weather": {
                "url": "http://127.0.0.1:8000/sse",
                "transport": "sse",
            },
        }
    )

    # Get tools
    weather_tools = await weather_client.get_tools()
    print(f"Weather tools: {[t.name for t in weather_tools]}")

    llm = ChatOpenAI(model="gpt-4o-mini")
    agent = create_agent(llm, weather_tools)

    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Weather in NYC in celsius ?"}]}
    )
    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())

# RUN IN A SECOND TERMINAL - uv run servers/weather_server.py
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


async def main():
    print("Hello MCP")
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                # Make sure to update to the full absolute path to your math_server.py file
                "args": [
                    "C:/Users/Viji/OneDrive - mentis-consulting.be/Documents/Mentis/Udemy/LangChainLangGraph/EdenMarco/MCP_Adapters/mcp-crash-course/servers/math_server.py"
                ],
                "transport": "stdio",
            },
            "weather": {
                # Make sure you start your weather server on port 8000
                # "url": "http://localhost:8000/mcp",
                "url": "http://127.0.0.1:8000/sse",
                "transport": "sse",
            },
        }
    )
    tools = await client.get_tools()
    agent = create_agent(llm, tools)
    math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
    weather_response = await agent.ainvoke({"messages": "what is the weather in nyc?"})
    print(f"math_response: {math_response['messages'][-1].content}")
    print(f"weather_response: {weather_response['messages'][-1].content}")

    # print(weather_response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())

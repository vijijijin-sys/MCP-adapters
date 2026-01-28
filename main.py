import asyncio
from dotenv import load_dotenv

# Create server parameters for stdio connection
from langchain_openai import ChatOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent

# Create an stdio client
# needs to know 2 things - How to run the mcp server, how to communicate with it.

# Initialize stdio server parameters
stdio_server_params = StdioServerParameters(
    command="python",
    # Make sure to update to the full absolute path to your math_server.py file
    args=[
        "C:/Users/Viji/OneDrive - mentis-consulting.be/Documents/Mentis/Udemy/LangChainLangGraph/EdenMarco/MCP_Adapters/mcp-crash-course/servers/math_server.py"
    ],
)

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


# create stdio client context manager
async def main():
    print("Hello from mcp-crash-course!")
    async with stdio_client(stdio_server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            print("Session initialized")

            # Get tools
            tools = await load_mcp_tools(
                session
            )  # chage cp tool obj to langchain tool object
            # print(tools)

            # Create and run the agent
            agent = create_agent(llm, tools)
            response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
            print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())

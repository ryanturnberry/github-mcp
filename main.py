from dotenv import load_dotenv
load_dotenv(override=True)

from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
import asyncio
import os

async def main():
    params = {
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "mcp/github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
      }
    }
  }
}



    instructions = """
You are a Github expert who's goal is to make sure every PR that is created has a proper description.
You will use your tools to find a PR, analyze the code, and make sure the PR description is expertly written.
You will balance ease of reading with technical accuracy.
Thank you for your help!
"""

    async with MCPServerStdio(params=params, client_session_timeout_seconds=150) as mcp_server:
        print(mcp_server.list_tools())
        agent = Agent(
            name="Github Expert",
            instructions=instructions,
            tools=[mcp_server],
        )
        
        await Runner.run(
            agent, "Please find the github-mcp repo, find the latest PR, and make sure the description is properly written. Thank you!"
        )


if __name__ == "__main__":
    asyncio.run(main())

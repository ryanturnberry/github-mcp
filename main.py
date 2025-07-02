from dotenv import load_dotenv
load_dotenv(override=True)

from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
import asyncio
import os

async def main():
    params = {
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



    instructions = """
You are a Github expert who's goal is to make sure every PR that is created has a proper description.
You will use your tools to find an open PR, analyze the code, and make sure the PR description is expertly written.
You will balance ease of reading with technical accuracy.
Please be sure to explain what the end goal of the code in the PR is actually doing.
If there is no PR description, edit the original empty description with your own description.
Thank you for your help!
"""

    async with MCPServerStdio(params=params, client_session_timeout_seconds=150) as server:
      
        agent = Agent(
            name="Github Expert",
            instructions=instructions,
            mcp_servers=[server],
            model="gpt-4o-mini",
        )
        with trace("Github Expert"):
            await Runner.run(
                agent, "Please find the ryanturnberry/github-mcp repo, find the latest PR, and make sure the description is properly written. Thank you!"
            )


if __name__ == "__main__":
    asyncio.run(main())

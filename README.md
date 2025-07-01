# GitHub MCP

This repository contains an implementation that uses agents to interact with the GitHub API through a multi-agent communication protocol (MCP).

## Overview
The main function runs an agent called "Github Expert" that utilizes an MCP server via stdio with Docker, using a provided GitHub Personal Access Token for authentication. The agent's instructions are to ensure every Pull Request (PR) in the GitHub repository has a proper, expertly written description.

## Details
- The agent searches for the latest open PR in the `ryanturnberry/github-mcp` repository.
- If a PR lacks a description or has an incomplete one, the agent analyzes the PR's code changes and updates the description.
- The description balances readability and technical accuracy.

## Purpose
The goal is to automate the process of maintaining high-quality PR descriptions, ensuring they clearly explain what the PR does, why changes were made, and any relevant technical context.

## Dependencies
- Python 3.13
- `openai-agents` package
- `mcp` package
- `dotenv` for environment variable loading
- Docker (for running the MCP server)

## Testing
The script runs asynchronously, invoking an MCP server in Docker and communicating with the agent to execute the PR description update process.

## Next Steps
- Extend the agent's capabilities to review multiple PRs concurrently.
- Add detailed logging and error handling.
- Create test cases to validate accuracy of PR descriptions generated.
- Integrate with GitHub Actions or other CI pipeline for automated execution.

---

### Code snippet reference (`main.py`):
```python
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
```

This provides a comprehensive view of what this PR adds and the functionality it implements.
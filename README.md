# AI Coding Agent

A modular AI coding agent built with Python, FastAPI, SQLite, pytest, and the OpenAI Responses API.

The project supports both a deterministic `MockProvider` for free local development, demonstrations, and automated testing, and a real `OpenAIProvider` that uses LLM function calling to interact with controlled development tools.

The OpenAI provider requires the user to configure their own OpenAI API key and have available API credits. The project can be developed, tested, and demonstrated locally with the `MockProvider` without making paid API calls.

## Features

* Modular provider architecture
* OpenAI Responses API integration
* LLM tool/function calling
* File reading and writing
* Workspace file listing
* Restricted workspace access
* Python command execution
* Automated pytest execution
* CLI interface
* FastAPI backend
* SQLite-based conversation/history storage
* Deterministic mock provider for local development
* Automated test suite

## Architecture

```text
User
  ↓
CLI / Web Interface
  ↓
CodingAgent
  ↓
BaseProvider
  ├── MockProvider
  └── OpenAIProvider
          ↓
      OpenAI Responses API
          ↓
      Function / Tool Calls
          ↓
      ToolRegistry
          ↓
  ┌───────┼───────────┐
  ↓       ↓           ↓
Files   Python      pytest
Tools   Execution    Tests
  ↓
Restricted Workspace
```

## How It Works

The `CodingAgent` receives a user request and passes it to the configured provider.

With the `MockProvider`, responses are deterministic and no external API call is required.

With the `OpenAIProvider`, the request is sent to the OpenAI Responses API. The model can decide whether it needs to use one of the available development tools.

For example:

```text
User Request
    ↓
OpenAI Provider
    ↓
Model decides to use a tool
    ↓
ToolRegistry
    ↓
read_file / write_file / run_python / run_tests
    ↓
Tool Result
    ↓
Model receives the result
    ↓
Final response or another tool call
```

This allows the agent to interact with a controlled development environment instead of only generating text responses.

## Available Tools

### File Tools

The agent can:

* List files in the workspace
* Read files
* Write files
* Reject access outside the configured workspace

Example operations:

```text
list_files
read_file
write_file
```

Path traversal attempts are blocked so the agent cannot freely access files outside its restricted workspace.

### Python Execution

The agent can execute Python code or Python files through the controlled terminal tool.

Example:

```text
run_python
```

Execution output, errors, and return codes can be returned to the agent.

### Automated Tests

The agent can execute the project's test suite using pytest.

Example:

```text
run_tests
```

This allows the agent to inspect code, make changes, run tests, and evaluate whether the changes work correctly.

## Project Structure

```text
ai-coding-agent/
│
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── api.py
│   ├── config.py
│   ├── database.py
│   ├── exceptions.py
│   ├── main.py
│   │
│   ├── providers/
│   │   ├── base.py
│   │   ├── mock_provider.py
│   │   └── openai_provider.py
│   │
│   └── tools/
│       ├── file_tools.py
│       ├── registry.py
│       ├── terminal_tools.py
│       └── test_tools.py
│
├── data/
│
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── style.css
│
├── tests/
│   ├── test_agent.py
│   ├── test_api.py
│   ├── test_file_tools.py
│   ├── test_openai_provider.py
│   ├── test_terminal_tools.py
│   └── test_test_tools.py
│
├── workspace/
│
├── .env.example
├── .gitignore
├── LICENSE
├── pytest.ini
├── requirements.txt
└── README.md
```

The project is organized around a modular provider and tool architecture. The `CodingAgent` coordinates requests, providers decide how requests should be handled, and the `ToolRegistry` controls which development tools can be executed. The OpenAI provider uses LLM function calling, while the mock provider allows deterministic local testing without paid API usage.

## Installation

Clone the repository:

```bash
git clone https://github.com/goktugparlak/ai-coding-agent.git
cd ai-coding-agent
```

Create a virtual environment:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root.

You can copy `.env.example`:

```bash
cp .env.example .env
```

On Windows, you can also create the file manually.

Example configuration:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=your_model_here
```

Never commit your real API key to GitHub.

The `.env` file should remain excluded through `.gitignore`.

## Running the Agent

Start the CLI application:

```bash
python -m app.main
```

Example:

```text
AI Coding Agent
Provider: openai
Model: your-configured-model
Type 'exit' to quit.

You: List the files in the workspace and explain what the project contains.
```

When the OpenAI provider is enabled, live API requests require:

* A valid OpenAI API key
* Available API credits

Without API credits, the OpenAI provider may return a quota or billing error.

## Mock Provider

The project also includes a deterministic `MockProvider`.

The mock provider is useful for:

* Local development
* Automated testing
* Demonstrations
* Testing agent logic without paid API calls
* Testing tool execution independently from an external LLM

This means the main architecture and tool system can be tested without sending requests to a paid AI service.

## Running the Tests

Run the complete test suite:

```bash
python -m pytest -v
```

Current test status:

```text
15 passed
```

The test suite covers areas including:

* Agent commands
* Conversation history
* FastAPI endpoints
* File reading and writing
* File listing
* Path traversal protection
* OpenAI provider tool execution
* Python execution
* Python error handling
* Successful pytest execution
* Failed pytest execution

Example:

```text
tests/test_agent.py::test_agent_lists_files PASSED
tests/test_agent.py::test_agent_reads_file PASSED
tests/test_agent.py::test_agent_unknown_command PASSED
tests/test_agent.py::test_agent_history PASSED
tests/test_api.py::test_health PASSED
tests/test_api.py::test_chat_help PASSED
tests/test_file_tools.py::test_write_and_read_file PASSED
tests/test_file_tools.py::test_missing_file PASSED
tests/test_file_tools.py::test_path_traversal_is_blocked PASSED
tests/test_file_tools.py::test_list_files PASSED
tests/test_openai_provider.py::test_openai_provider_executes_tool PASSED
tests/test_terminal_tools.py::test_run_python PASSED
tests/test_terminal_tools.py::test_run_python_error PASSED
tests/test_test_tools.py::test_run_tests_success PASSED
tests/test_test_tools.py::test_run_tests_failure PASSED
```

## Example Agent Workflow

A typical coding-agent workflow can look like this:

```text
User asks for a code change
        ↓
Agent analyzes the request
        ↓
Agent reads relevant project files
        ↓
Agent determines the required change
        ↓
Agent writes or modifies code
        ↓
Agent runs automated tests
        ↓
Agent checks the result
        ↓
Agent returns the final response
```

Conceptually, this follows an:

```text
inspect → plan → edit → test
```

workflow.

## Why This Is an Agent

A traditional chatbot mainly generates text responses.

This project can also interact with an external environment through tools.

The agent can:

```text
read files
      ↓
inspect code
      ↓
execute tools
      ↓
run tests
      ↓
receive tool results
      ↓
continue its reasoning
```

The ability to select and execute tools is what allows it to perform coding-related tasks rather than only discuss them.

## Safety and Workspace Restrictions

Tool access is intentionally restricted.

The agent should operate only inside the configured workspace.

The project includes protection against directory traversal attempts such as:

```text
../../some-file
```

This reduces the risk of the agent accessing unrelated files on the host system.

Command execution is also separated behind controlled tool interfaces instead of giving the language model unrestricted direct system access.

## API

The project includes a FastAPI backend that can expose agent functionality through HTTP endpoints.

FastAPI can be used to connect the agent to:

* A browser-based frontend
* Another application
* A development dashboard
* External services

The API layer is separate from the core agent logic, which keeps the architecture modular.

## Technologies

### Backend

* Python
* FastAPI
* Pydantic

### AI

* OpenAI Responses API
* LLM function/tool calling
* Provider abstraction

### Data

* SQLite

### Testing

* pytest
* FastAPI TestClient

### Development

* Virtual environments
* Environment variables
* Git
* GitHub

## Design Goals

The project focuses on:

* Modular architecture
* Separation of agent logic and providers
* Controlled tool execution
* Testability
* Safe workspace interaction
* Easy replacement of AI providers
* Reproducible local development

The provider abstraction makes it possible to use deterministic testing logic independently from the real OpenAI integration.

## Current Status

The core agent architecture is implemented.

Current functionality includes:

```text
Agent orchestration        ✅
Mock provider              ✅
OpenAI provider            ✅
LLM tool calling           ✅
File tools                 ✅
Restricted workspace       ✅
Python execution           ✅
pytest execution           ✅
FastAPI integration        ✅
SQLite integration         ✅
Automated tests            ✅
15 automated tests passing ✅
```

Live OpenAI requests require the user's own API key and available API credits.

## Future Improvements

Possible future improvements include:

* Additional development tools
* More advanced command validation
* Improved multi-step planning
* Streaming responses
* Web-based user interface
* Git integration
* Code diff previews
* Approval before sensitive operations
* More extensive integration testing
* Support for additional LLM providers

## Disclaimer

This project is intended as a learning and portfolio project demonstrating agent architecture, tool calling, backend development, automated testing, and controlled code execution.

Any external API usage depends on the user's own API credentials and provider account configuration.

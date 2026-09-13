# AI Coding Agent Prototype

A portfolio-ready coding-agent prototype built with Python, FastAPI, pytest, SQLite, and a lightweight HTML/CSS/JavaScript interface.

> **Important:** this version intentionally does **not** connect to an LLM or paid AI API.  
> It uses a deterministic `MockProvider` to demonstrate agent architecture, tool orchestration, testing, persistence, and a replaceable provider layer.

## Why this project exists

The goal is to understand how coding agents are structured around a model:

```text
User
  ↓
Interface (CLI / Web)
  ↓
CodingAgent
  ↓
Provider
  ↓
Tool plan
  ↓
ToolRegistry
  ↓
File / Python / pytest tools
  ↓
Workspace
```

A future OpenAI or local-model provider can replace `MockProvider` without redesigning the tool layer.

## Features

- Interactive terminal interface
- FastAPI backend
- Browser-based chat UI
- Provider abstraction (`BaseProvider`)
- Free deterministic `MockProvider`
- File discovery, reading, and writing
- Workspace path-traversal protection
- Restricted Python execution tool
- Automated pytest execution
- SQLite command/response history
- Tool registry and orchestration layer
- Automated test suite
- Example workspace project
- No API key required

## Project structure

```text
ai-coding-agent/
├── app/
│   ├── agent.py
│   ├── api.py
│   ├── config.py
│   ├── database.py
│   ├── exceptions.py
│   ├── main.py
│   ├── providers/
│   │   ├── base.py
│   │   └── mock_provider.py
│   └── tools/
│       ├── file_tools.py
│       ├── registry.py
│       ├── terminal_tools.py
│       └── test_tools.py
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── style.css
├── tests/
├── workspace/
├── data/
├── requirements.txt
├── pytest.ini
└── README.md
```

## Setup

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, you can still use the virtual environment directly:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run the CLI

```powershell
python -m app.main
```

Example:

```text
AI Coding Agent Prototype
Mock provider mode — no paid AI API is connected.

You: check project

Agent:
Running a small project check.

Workspace files
- README.md
- calculator.py
- tests/test_calculator.py

Test results
Tests passed.
2 passed
```

## Run the web interface

```powershell
python -m uvicorn app.api:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

FastAPI docs are available at:

```text
http://127.0.0.1:8000/docs
```

## Supported commands

```text
help
list files
read <filename>
inspect <filename>
write <filename> :: <content>
run python <filename>
run tests
check project
history
```

Examples:

```text
read calculator.py
write demo.py :: print("Hello")
run python demo.py
run tests
check project
```

## Run tests

```powershell
python -m pytest -v
```

The test suite covers:

- file reads/writes
- path-traversal blocking
- workspace file listing
- Python execution
- successful and failing pytest runs
- agent routing
- history persistence
- FastAPI health/chat endpoints

## Design decisions

### 1. Provider abstraction

`CodingAgent` does not depend directly on OpenAI or another model provider.

```text
CodingAgent
    ↓
BaseProvider
    ↓
MockProvider today
    ↓
OpenAIProvider / LocalModelProvider later
```

This keeps the project testable and free during development.

### 2. Tool registry

The provider chooses *what should happen*.  
The registry controls *what the application is actually allowed to execute*.

That separation is central to agent architecture.

### 3. Workspace restriction

File tools resolve requested paths and reject paths that escape `workspace/`.

Example:

```text
../app/main.py
```

is rejected.

### 4. Restricted command execution

This prototype does not expose arbitrary shell execution.  
The runtime tool only executes a Python file selected inside the workspace.

This reduces risk, but it is **not a full security sandbox**. Python code executed inside the workspace can still access resources permitted by the operating system.

## What this project demonstrates

- Python project architecture
- OOP and abstractions
- AI-agent architecture concepts
- tool/function orchestration
- provider interfaces
- exception handling
- file-system safety
- subprocess management
- automated testing
- FastAPI / REST APIs
- frontend-backend communication
- SQLite persistence
- Git-friendly project organization

## Future improvements

- OpenAI Responses API provider
- Local-model provider
- structured tool calling
- multi-step autonomous planning
- Git diff / checkpoint / rollback tools
- user approval before file changes
- stronger isolated execution sandbox
- repository indexing / RAG
- streaming responses
- authentication

## Portfolio description

**AI Coding Agent Prototype** — Built a modular coding-agent architecture in Python with a replaceable model-provider layer, controlled file and execution tools, pytest-based verification, SQLite history, FastAPI REST endpoints, and a browser interface. Implemented a deterministic mock provider so the complete system can be developed and demonstrated without paid API access.

## License

MIT

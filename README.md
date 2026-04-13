# 🤖 CLI-AIGENT

> An autonomous AI coding agent that runs directly in your terminal — powered by Google Gemini.

---

## What is CLI-AIGENT?

CLI-AIGENT is a command-line AI agent that takes a natural language prompt and autonomously plans and executes coding tasks. It can explore your project files, read code, run Python scripts, and write or modify files — all without manual intervention.

Built on **Google Gemini 2.0 Flash**, it uses function-calling to iteratively act on your codebase until the task is complete.

---

## ✨ Features

- 🧠 **Autonomous planning** — the agent breaks down tasks and decides which tools to call
- 📁 **File exploration** — list files and directories in your project
- 📖 **File reading** — inspect the contents of any file
- ▶️ **Python execution** — run Python scripts with optional arguments
- ✍️ **File writing** — create or overwrite files with generated content
- 🔁 **Iterative reasoning** — loops up to 20 iterations until the task is resolved
- 🔍 **Verbose mode** — optional detailed logging of every function call and result

---

## 📦 Prerequisites

- Python 3.9+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

---

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/siddhu5pute/CLI-AIGENT.git
cd CLI-AIGENT

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up your environment
cp .env.example .env
# Add your Gemini API key to .env:
# GEMINI_API_KEY=your_key_here
```

---

## 🛠️ Usage

```bash
# Basic usage
python main.py "Your task or question here"

# With verbose output (shows each function call and result)
python main.py "Your task or question here" --verbose
```

### Examples

```bash
# Explore the project structure
python main.py "List all the files in the project"

# Understand the codebase
python main.py "Read main.py and explain what it does"

# Fix a bug
python main.py "Run calculator.py and fix any errors you find"

# Generate code
python main.py "Write a Python function that sorts a list of dictionaries by a key"
```

---

## 📁 Project Structure

```
CLI-AIGENT/
├── main.py                  # Entry point — agent loop & orchestration
├── .env                     # Environment variables (API key)
├── calculator/              # Working directory used by the agent
└── functions/
    ├── get_files_info.py    # Tool: list files and directories
    ├── get_file_content.py  # Tool: read file contents
    ├── run_python_file.py   # Tool: execute Python scripts
    └── write_file.py        # Tool: write or overwrite files
```

---

## ⚙️ How It Works

1. You provide a natural language prompt via the CLI
2. The agent sends it to **Gemini 2.0 Flash** along with available tool definitions
3. Gemini responds with a function call plan
4. The agent executes the appropriate tool and feeds the result back to Gemini
5. This loop continues until Gemini returns a final text response (or hits the 20-iteration limit)

```
You → Prompt → Gemini → Function Call → Tool Execution → Result → Gemini → ... → Final Answer
```

---

## 🔧 Available Tools

| Tool | Description |
|---|---|
| `get_files_info` | List files and subdirectories at a given path |
| `get_file_content` | Read the full contents of a file |
| `run_python_file` | Execute a Python file with optional arguments |
| `write_file` | Write or overwrite a file with specified content |

> All file paths are resolved relative to the `./calculator` working directory. The working directory is injected automatically for security.

---

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Your Google Gemini API key (required) |

---

## 📄 License

This project is open source. See [LICENSE](LICENSE) for details.

---

## 🙌 Author

Made by [siddhu5pute](https://github.com/siddhu5pute)

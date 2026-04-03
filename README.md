# 🐹 Hamster Claude Code

A ComfyUI custom node that runs **Claude Code CLI** directly inside your workflow.
If you can run Claude Code in your terminal, you can use it in ComfyUI right away.
Supports both **local** and **server** environments.

---

# 📦 Included Nodes

## 🐹 Claude Code

Execute Claude Code CLI from within a ComfyUI node. Pass a prompt and an optional file path, and get Claude's response as a string output.

### Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `prompt` | STRING | ✅ | Instructions for Claude |
| `file_path` | STRING | optional | Path to a local file to process (`.txt`, `.py`, `.md`, etc.) |
| `api_key_if_server` | STRING | optional | `ANTHROPIC_API_KEY` for server use (leave empty for local) |
| `model` | dropdown | optional | Model to use (default uses CLI setting) |
| `continue_session` | BOOLEAN | optional | Continue from the previous session |
| `working_directory` | STRING | optional | Working directory (defaults to file's directory or home) |

### Outputs

| Output | Description |
|---|---|
| `output` | Claude's response text |
| `metadata` | Model name, duration, cost, token count, session ID, etc. |

### Notes

- **Local use**: Run `claude login` once — no API key needed in the node.
- **Server use**: Enter your `ANTHROPIC_API_KEY` in the `api_key_if_server` field, or set it as a system environment variable.
- `file_path` accepts any file type (`.txt`, `.py`, `.md`, etc.) — read directly by Claude CLI with no file size bottleneck on the ComfyUI side. Supports files up to ~200,000 tokens.

---

# 🛠 Installation

## Method 1 — Git Clone

Open your terminal in `ComfyUI/custom_nodes/` and run:

```bash
git clone https://github.com/hamster-poodle/ComfyUI_Hamster_ClaudeCode
```

Then restart **ComfyUI**.

---

# 📋 Dependencies

This node requires the **Claude Code CLI**:

```bash
npm install -g @anthropic-ai/claude-code
```

Node.js must be installed beforehand. No additional Python packages are required.

---

# 🔐 Authentication

### Local

```bash
claude login
```

Browser-based OAuth. Run once — credentials are stored locally.

### Server (e.g. AWS EC2)

Set the environment variable before starting ComfyUI:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Or enter it directly in the `api_key_if_server` field in the node.

> ⚠️ Avoid hardcoding API keys in workflow `.json` files — use system environment variables for production.

---

# 💡 Use Cases

- Translating or rewriting text files in batch workflows
- Summarizing or analyzing documents as part of a pipeline
- Generating prompts or captions using file content
- Any task where Claude's reasoning should be embedded in a ComfyUI workflow

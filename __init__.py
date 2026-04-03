from .claude_code_node import ClaudeCodeNode

NODE_CLASS_MAPPINGS = {
    "Hamster_ClaudeCode": ClaudeCodeNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Hamster_ClaudeCode": "🐹 Claude Code",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

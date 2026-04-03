import subprocess
import re
import os
import json
import time


def strip_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


class ClaudeCodeNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "以下のファイルを処理してください。",
                    "tooltip": "Claudeへの指示（プロンプト）"
                }),
            },
            "optional": {
                "file_path": ("STRING", {
                    "default": "",
                    "tooltip": "処理対象のtxtファイルのパス（例: C:/Users/paras/Documents/sample.txt）"
                }),
                "api_key_if_server": ("STRING", {
                    "default": "",
                    "placeholder": "your ANTHROPIC_API_KEY",
                    "tooltip": "For server use: enter your ANTHROPIC_API_KEY. For local use: leave empty (claude login credentials will be used)"
                }),
                "model": (["default", "claude-opus-4-6", "claude-sonnet-4-6", "claude-haiku-4-5-20251001"], {
                    "default": "default",
                    "tooltip": "使用するモデル（defaultはCLIのデフォルト設定）"
                }),
                "continue_session": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "直前のセッションを継続してコンテキストを保持する"
                }),
                "working_directory": ("STRING", {
                    "default": "",
                    "tooltip": "作業ディレクトリ（空の場合はfile_pathのディレクトリ、またはホームディレクトリ）"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("output", "metadata")
    FUNCTION = "run"
    CATEGORY = "Claude Code"
    OUTPUT_NODE = False

    def run(self, prompt, file_path="", api_key_if_server="", model="default", continue_session=False, working_directory=""):
        # ファイルパスが指定されている場合はプロンプトに付加
        fp = file_path.strip()
        if fp:
            if not os.path.isfile(fp):
                return (
                    f"[ERROR] ファイルが見つかりません: {fp}",
                    "status: error"
                )
            full_prompt = f"{prompt}\n\nファイル: {fp}"
        else:
            full_prompt = prompt

        # 作業ディレクトリの決定
        if working_directory.strip():
            cwd = working_directory.strip()
        elif fp:
            cwd = os.path.dirname(os.path.abspath(fp))
        else:
            cwd = os.path.expanduser("~")

        # コマンド構築
        cmd = ["claude", "-p", full_prompt, "--output-format", "json"]
        if model != "default":
            cmd.extend(["--model", model])
        if continue_session:
            cmd.append("--continue")

        # 環境変数の構築
        env = os.environ.copy()
        if api_key_if_server.strip():
            env["ANTHROPIC_API_KEY"] = api_key_if_server.strip()

        wall_start = time.time()
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                cwd=cwd,
                env=env,
                shell=False,
            )
            wall_elapsed = time.time() - wall_start
            raw = strip_ansi(result.stdout).strip()

            if result.returncode != 0:
                stderr = strip_ansi(result.stderr).strip()
                output = f"[ERROR] returncode={result.returncode}\n{stderr}\n{raw}"
                metadata = f"wall_time: {wall_elapsed:.2f}s\nstatus: error"
            else:
                try:
                    data = json.loads(raw)
                    output = data.get("result", raw)

                    lines = []
                    if "model" in data:
                        lines.append(f"model: {data['model']}")
                    duration_ms = data.get("duration_ms")
                    if duration_ms is not None:
                        lines.append(f"duration: {duration_ms / 1000:.2f}s")
                    lines.append(f"wall_time: {wall_elapsed:.2f}s")
                    cost = data.get("cost_usd")
                    if cost is not None:
                        lines.append(f"cost: ${cost:.6f}")
                    in_tok = data.get("total_input_tokens")
                    out_tok = data.get("total_output_tokens")
                    if in_tok is not None and out_tok is not None:
                        lines.append(f"tokens: {in_tok} in / {out_tok} out")
                    session_id = data.get("session_id")
                    if session_id:
                        lines.append(f"session_id: {session_id}")
                    if fp:
                        lines.append(f"file: {os.path.basename(fp)}")
                    lines.append(f"cwd: {cwd}")
                    lines.append(f"status: {data.get('subtype', 'unknown')}")
                    metadata = "\n".join(lines)
                except json.JSONDecodeError:
                    output = raw
                    metadata = f"wall_time: {wall_elapsed:.2f}s\nstatus: ok (JSON parse failed)"

        except FileNotFoundError:
            output = "[ERROR] `claude` コマンドが見つかりません。PATHを確認してください。"
            metadata = f"wall_time: {time.time() - wall_start:.2f}s\nstatus: error"
        except Exception as e:
            output = f"[ERROR] {e}"
            metadata = f"wall_time: {time.time() - wall_start:.2f}s\nstatus: error"

        return (output, metadata)


NODE_CLASS_MAPPINGS = {
    "Hamster_ClaudeCode": ClaudeCodeNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Hamster_ClaudeCode": "🐹 Claude Code",
}

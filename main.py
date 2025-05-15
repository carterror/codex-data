# codex_agent.py

import subprocess
import re
import os
import pandas as pd

# --- Prompt Builder ---
def build_prompt(user_instruction: str, context: dict) -> str:
    return f"""
You are a data engineering assistant.

Context:
- Available files: {context['files']}
- Schemas:
{context['schemas']}

Instruction: {user_instruction}

Generate Python code using Pandas. Do not explain the code.
"""

# --- Codex CLI Adapter ---
def query_codex(prompt: str) -> str:
    result = subprocess.run(
        ["codex", "--provider", "gemini", "--approval-mode", "full-auto", prompt],
        capture_output=True, text=True
    )
    print(result)
    return result.stdout

# --- Response Parser ---
def extract_code(response: str) -> str:
    match = re.search(r"```python\n(.*?)```", response, re.DOTALL)
    return match.group(1).strip() if match else response.strip()

# --- Context Provider ---
def get_context_from_csvs(data_dir: str = "./data") -> dict:
    files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
    schemas = ""
    for f in files:
        try:
            df = pd.read_csv(os.path.join(data_dir, f), nrows=5)
            schemas += f"\n- {f}:\n  Columns: {list(df.columns)}\n  Sample: {df.head(1).to_dict(orient='records')[0]}\n"
        except Exception as e:
            schemas += f"\n- {f}: ERROR reading CSV: {e}\n"
    return {"files": files, "schemas": schemas}

# --- Codex Agent ---
class CodexAgent:
    def __init__(self, data_dir="./data"):
        self.data_dir = data_dir

    def handle_instruction(self, instruction: str) -> str:
        context = get_context_from_csvs(self.data_dir)
        prompt = build_prompt(instruction, context)
        raw_response = query_codex(prompt)
        code = extract_code(raw_response)
        return code

    def run_code(self, code: str, globals_dict=None) -> dict:
        try:
            exec_env = globals_dict or {"pd": pd, "__name__": "__main__"}
            exec(code, exec_env)
            return {"success": True, "env": exec_env}
        except Exception as e:
            return {"success": False, "error": str(e)}

# --- CLI Entry Point ---
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Codex Agent instruction.")
    parser.add_argument("instruction", type=str, help="Natural language instruction to execute")
    parser.add_argument("--data-dir", type=str, default="./data", help="Path to CSV folder")
    args = parser.parse_args()

    agent = CodexAgent(data_dir=args.data_dir)
    code = agent.handle_instruction(args.instruction)

    print("\n--- Generated Code ---\n")
    print(code)

    print("\n--- Execution Result ---\n")
    result = agent.run_code(code)
    if result["success"]:
        print("Execution completed successfully.")
    else:
        print(f"Error: {result['error']}")

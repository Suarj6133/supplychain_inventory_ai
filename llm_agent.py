from prompt_builder import build_prompt

import subprocess
import re

def get_sql_from_llama(user_input: str) -> str:
    prompt = build_prompt(user_input)

    process = subprocess.Popen(
    ["ollama", "run", "phi3:3.8b"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    encoding='utf-8'  # ✅ FIX: avoids UnicodeDecodeError
)


    output, error = process.communicate(input=prompt)



    if process.returncode != 0:
        raise RuntimeError(f"Ollama failed: {error}")

    # Remove triple backticks or SQL markdown blocks
    cleaned = re.sub(r"```.*?```", lambda m: m.group(0).strip("`"), output.strip(), flags=re.DOTALL)

    # Optional: remove remaining ` or ``` if present
    cleaned = cleaned.replace("```", "").strip("`").strip()

    # Split the string into lines
    lines = cleaned.split('\n')
    
    #  Check the first line for common language labels
    if lines and lines[0].strip().lower() in ['sql', 'sqlite', 'markdown']:
        lines = lines[1:] # Remove the first line
    
    #  Join the lines back together
    cleaned = '\n'.join(lines).strip()

    return cleaned
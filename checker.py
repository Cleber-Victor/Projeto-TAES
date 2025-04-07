import sys
import subprocess
from build_sol import gen_sol
from build_tester import gen_tester

def run_script(script_name: str) -> str:
    try:
        subprocess.run([sys.executable, script_name], check=True, capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        return "Error: Script execution timed out after 10 seconds."
    except subprocess.CalledProcessError as e:
        return e.stderr
    return "pass"

def process_attempt(llm_attempt: str, problem: dict) -> str:
    # escreve solução da LLM em arquivo sol.py
    gen_sol(llm_attempt)

    # implementa script (tester.py) que vai verificar sol.py
    gen_tester(problem)

    # retorna mensagem de erro ou string 'pass'
    result = run_script("tester.py")

    return result
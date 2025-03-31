from human_eval.data import read_problems
import re

def extract_check_func(text: str) -> str:
    match = re.search(r'def (.*)$', text, re.DOTALL)
    return "def " + match.group(1) if match else ""

def write_tester(check_func: str, entry_point: str):
    with open("tester.py", "w") as file:
        
        # import funcao 
        file.write(f"from sol import {entry_point}\n\n")

        # definiçao da função check
        file.write(f"{check_func}\n\n")
        
        # chamada da função check
        file.write(f"check({entry_point})\n")

        file.close()

# escreve tester.py completo
def gen_tester(problem: dict):
    check_function = extract_check_func(problem["test"])
    entry_point = problem["entry_point"]
    write_tester(check_function, entry_point)
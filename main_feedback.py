"""
    Esse script passa o statement para a LLM e registra a solução do modelo
    guardando a saída do modelo em 'samples.json'.
    porém não faz avaliação de corretude.

    A avaliação é feita por outro script que precisará ser implementado
    pois o output está em formato diferente do human eval original
"""

from human_eval.data import write_jsonl, read_problems
from llm_gen import get_completion, get_completion_with_feedback
from checker import process_attempt
import time
import sys
import re

problems: dict = read_problems()

NUM_TASKS: int = 164
NUM_ATTEMPTS: int = 3

def extract_python_code(text: str) -> str:
    match = re.search(r'```python\n(.*?)(```|$)', text, re.DOTALL)
    if match:
        return match.group(1)
    else:
        match = re.search(r'```\n(.*?)(```|$)', text, re.DOTALL)
    return match.group(1) if match else text

samples: list[dict] = []
full_samples: list[dict] = []

MODEL = sys.argv[1]

counter: int = 0
# id é string no formato 'HumanEval/0'
for id in problems:
    # enunciado do problema
    enunciado = problems[id]["prompt"]

    previous_attempt = ""
    tester_feedback = ""

    for attempt in range(NUM_ATTEMPTS):

        print("tentativa no. ",attempt+1)

        # chama API do groq, obtém solução gerada pela llm
        if (attempt == 0):
            solucao_llm = get_completion(enunciado, MODEL)
        else:
            solucao_llm = get_completion_with_feedback(enunciado, previous_attempt, tester_feedback, MODEL)

        print("solução gerada")

        # guardando saída completa, que pode incluir linguagem natural e não apenas código
        full_samples.append(dict(task_id=id,completion=solucao_llm))

        # extrai script python, sem qualquer linguagem natural
        solucao_llm = extract_python_code(solucao_llm)

        # não só enunciado, dict completo
        problem_dict = problems[id]

        print()

        # obtém veredito ('pass' ou mensagem de erro)
        verdict = process_attempt(solucao_llm, problem_dict)
        passed_tests = True if verdict == "pass" else False

        # salva script feito anteriormente + feedback do tester
        previous_attempt = solucao_llm
        tester_feedback = verdict

        samples.append(dict(task_id=id,completion=solucao_llm,attempt_no=attempt+1,passed_tests=passed_tests))

        time.sleep(5)

        if (passed_tests):
            break

    print(f"Modelo: {MODEL} - processando task no.{counter}")
    
    counter += 1

    if (counter == NUM_TASKS):
        break

OUTPUT_FILE = "samples_" + MODEL + ".jsonl"
FULL_OUTPUT_FILE = "full_samples_" + MODEL + ".jsonl"

write_jsonl(OUTPUT_FILE, samples)
write_jsonl(FULL_OUTPUT_FILE, full_samples)
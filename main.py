"""
    Esse script passa o statement para a LLM e registra a solução do modelo
    guardando a saída do modelo em 'samples.json'.
    porém não faz avaliação de corretude.

    A avaliação é feita com a seguinte chamada no terminal:

    $ evaluate_functional_correctness samples.jsonl
"""

from human_eval.data import write_jsonl, read_problems
from llm_gen import get_completion
import time
import sys
import re

problems: dict = read_problems()

NUM_SAMPLES_PER_TASK: int = 1
NUM_TASKS: int = 165
NUM_LOOPS: int = 0 # número de vezes que o mecanismo de feedback roda

# problema com human eval: apenas ~5 testes por problema.
# se o loop reporta o caso teste que tá falhando em cada iteração, 
# basta o modelo rodar 5 vezes que ele consegue responder

# podemos adicionar problemas no mesmo padrão jsonl que tem no arquivo 'human-eval-v2....'
# e fazer o experimento nesse padrão

# outra possibilidade é gerar mais exemplos desses mesmos problemas com o canonical solution
# e aí evita esse problema de 'filar'

# adicionar traceback também

# não fiz nada das recomendações de segurança do artigo...

# TODO
# 1.rodar avaliações sem nenhum feedback.
    # verificar que pipeline está funcionando

# 2. incorporar feedback
    # primeiro caso teste que não pegar.

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
    # chama API do groq, obtém código gerado pela llm 
    solucao_llm = get_completion(enunciado, MODEL)

    full_samples.append(dict(task_id=id,completion=solucao_llm))

    # extrai script sem mais nada
    solucao_llm = extract_python_code(solucao_llm)
    
    samples.append(dict(task_id=id,completion=solucao_llm))
    
    time.sleep(5)
    # limite 30 requisições/6k tokens por minuto, com isso parece seguro não ultrapassar
    # ~50k tokens pra rodar 1 vez os 165 problemas
    # ~16 minutos pra rodar 1 vez os 165 problemas
    # ~3k tokens e 12 reqs por minuto, margem ok.

    print(f"Modelo: {MODEL} - processando task no.{counter}")
    
    counter += 1

    if (counter == NUM_TASKS):
        break

OUTPUT_FILE = "samples_" + MODEL + ".jsonl"
FULL_OUTPUT_FILE = "full_samples_" + MODEL + ".jsonl"

write_jsonl(OUTPUT_FILE, samples)
write_jsonl(FULL_OUTPUT_FILE, full_samples)

#"""
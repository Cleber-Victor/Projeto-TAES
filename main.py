"""
    Esse script passa o statement para a LLM e registra a solução do modelo
    guardando a saída do modelo em 'samples.json'.
    porém não faz avaliação de corretude.

    A avaliação é feita com a seguinte chamada no terminal:

    $ evaluate_functional_correctness samples.jsonl
"""

from human_eval.data import write_jsonl, read_problems
from llm_gen import get_completion

problems: dict = read_problems()

NUM_SAMPLES_PER_TASK: int = 1
NUM_TASKS: int = 1 # não rodar todos os problemas pra evitar 
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

# gambiarra: llm retorna resposta no formato: 
    # ```python
    # <código>
    # ```
# posso tirar a primeira e última linha pra ficar só o código
def remove_first_and_last_line(text):
    lines = text.splitlines()
    return "\n".join(lines[1:-1]) if len(lines) > 2 else ""


samples: list[dict] = []

counter: int = 0
# id é string no formato 'HumanEval/0'
for id in problems:
    # enunciado do problema
    enunciado = problems[id]["prompt"]
    # chama API do groq, obtém código gerado pela llm 
    solucao_llm = get_completion(enunciado)

    solucao_llm = remove_first_and_last_line(solucao_llm)
    
    samples.append(dict(task_id=id,completion=solucao_llm))
    
    counter += 1
    
    if (counter == NUM_TASKS):
        break

write_jsonl("samples.jsonl", samples)


# samples = [
#     dict(task_id=task_id, completion=generate_one_completion(problems[task_id]["prompt"]))
#     for task_id in problems
#     for _ in range(num_samples_per_task)
# ]
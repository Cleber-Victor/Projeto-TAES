# gera o script com a solução da LLM
def gen_sol(llm_sol: str):

    with open("sol.py", "w") as file:
        file.write(llm_sol)
        file.close()

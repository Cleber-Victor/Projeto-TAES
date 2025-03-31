#!/bin/bash

# llama-3.3-70b-versatile e llama-3.1-8b-instant já foram testados, 
# para replicar os resultados completos, incluir os dois na lista

#args=("llama3-8b-8192" "llama3-70b-8192" "llama-guard-3-8b" "gemma2-9b-it")

args=("llama3-8b-8192" "llama-guard-3-8b" "gemma2-9b-it")

for arg in "${args[@]}"; do
    python3 main.py "$arg"
done
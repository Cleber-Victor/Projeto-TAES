#!/bin/bash

args=("llama3-8b-8192" "llama3-70b-8192" "gemma2-9b-it" \
      "llama-3.3-70b-versatile" "llama-3.1-8b-instant")

for arg in "${args[@]}"; do
    python3 main_feedback.py "$arg"
done
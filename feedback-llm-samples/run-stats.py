import json
from collections import defaultdict

def compute_stats(file_path: str):
    attempts = defaultdict(list)
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            if data["passed_tests"]:
                attempts[data["task_id"].split("/")[-1]].append(data["attempt_no"])
    
    num_pass_1 = sum(1 for v in attempts.values() if min(v) == 1)
    num_pass_2 = sum(1 for v in attempts.values() if min(v) <= 2)
    num_pass_3 = sum(1 for v in attempts.values() if min(v) <= 3)
    avg_attempts = sum(min(v) for v in attempts.values()) / len(attempts) if attempts else 0
    
    return {
        "pass_1_abs": num_pass_1,
        "pass_1_rel": num_pass_1 / 164,
        "pass_2_abs": num_pass_2,
        "pass_2_rel": num_pass_2 / 164,
        "pass_3_abs": num_pass_3,
        "pass_3_rel": num_pass_3 / 164,
        "avg_attempts": avg_attempts
    }

def process_models(models):
    results = {}
    for model in models:
        file_path = f"samples_{model}.jsonl"
        results[model] = compute_stats(file_path)
    
    with open("model_stats.json", "w", encoding="utf-8") as out_file:
        json.dump(results, out_file, indent=4)

# Example usage
models = [ "llama-3.3-70b-versatile",
           "llama-3.1-8b-instant",
           "llama3-70b-8192",
           "llama3-8b-8192",
           "gemma2-9b-it"
         ]
process_models(models)

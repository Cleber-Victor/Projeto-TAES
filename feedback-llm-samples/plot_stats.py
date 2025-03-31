import json
import numpy as np
import matplotlib.pyplot as plt

def plot_stats(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    models = list(data.keys())
    categories = ["pass_1_rel", "pass_2_rel", "pass_3_rel"]
    category_labels = ["1 Attempt", "≤2 Attempts", "≤3 Attempts"]
    
    x = np.arange(len(models))
    width = 0.2  # Width of each bar
    
    fig, ax = plt.subplots(figsize=(12, 6))  # Set larger figure size
    
    for i, category in enumerate(categories):
        values = [data[model][category] for model in models]
        ax.bar(x + i * width, values, width, label=category_labels[i])
    
    ax.set_xticks(x + width)
    ax.set_xticklabels(models)
    ax.set_ylabel("Pass Rate")
    ax.set_title("Pass Rate per Model")
    ax.legend()
    
    plt.savefig("model_stats.png", dpi=300, bbox_inches='tight')  # Save as large PNG
    plt.show()

# Example usage
plot_stats("model_stats.json")
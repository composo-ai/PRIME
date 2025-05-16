import requests
import json
import time
from tqdm import tqdm
import concurrent.futures
import threading

# Load configuration
with open("config.json", "r") as f:
    config = json.load(f)

API_KEY = config["api"]["key"]
url = config["api"]["url"]
headers = {
    "API-Key": API_KEY
}

with open(config["input_file"], "r") as f:
    data = json.load(f)

results = []
results_lock = threading.Lock()

max_items = config["max_items"]
data = data[:max_items] if max_items > 0 else data

def evaluate_item(item):
    a_payload = {
        "messages": [
            {"role": "user", "content": item["prompt"]},
            {"role": "assistant", "content": item["a_only_response"]}
        ],
        "evaluation_criteria": item["criterion_a"]
    }
    
    try:
        max_retries = config["max_retries"]
        retry_delay = config["retry_delay"]

        for attempt in range(max_retries):
            try:
                a_response = requests.post(url, headers=headers, json=a_payload)
                a_response.raise_for_status()
                break
            except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
                print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    print("Max retries reached, request failed")
                    raise
        a_result = a_response.json()
        a_score = a_result.get('score', None)
        a_explanation = a_result.get('explanation', 'No feedback provided.')
    except Exception as e:
        a_score = None
        a_explanation = f"Error: {str(e)}"
    
    b_payload = {
        "messages": [
            {"role": "user", "content": item["prompt"]},
            {"role": "assistant", "content": item["b_only_response"]}
        ],
        "evaluation_criteria": item["criterion_a"]
    }
    
    try:
        for attempt in range(max_retries):
            try:
                b_response = requests.post(url, headers=headers, json=b_payload)
                b_response.raise_for_status()
                break
            except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
                print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    print("Max retries reached, request failed")
                    raise
        b_result = b_response.json()
        b_score = b_result.get('score', None)
        b_explanation = b_result.get('explanation', 'No feedback provided.')
    except Exception as e:
        b_score = None
        b_explanation = f"Error: {str(e)}"
    
    result = {
        "prompt": item["prompt"],
        "criterion_a": item["criterion_a"],
        "criterion_b": item["criterion_b"],
        "a_only_response": item["a_only_response"],
        "b_only_response": item["b_only_response"],
        "a_score_on_criterion_a": a_score,
        "a_explanation": a_explanation,
        "b_score_on_criterion_a": b_score,
        "b_explanation": b_explanation,
        "score_difference": a_score - b_score if a_score is not None and b_score is not None else None,
        "a_better_on_criterion_a": "Yes" if a_score is not None and b_score is not None and a_score > b_score else "No"
    }
    
    with results_lock:
        results.append(result)
        if len(results) % 10 == 0:
            with open(config["output_file"], "w") as f:
                json.dump(results, f, indent=2)
    
    return result

with concurrent.futures.ThreadPoolExecutor(max_workers=config["max_workers"]) as executor:
    future_to_item = {executor.submit(evaluate_item, item): item for item in data}
    
    for future in tqdm(concurrent.futures.as_completed(future_to_item), total=len(future_to_item)):
        try:
            future.result()
        except Exception as exc:
            print(f'Exception occurred during evaluation: {exc}')

with open(config["output_file"], "w") as f:
    json.dump(results, f, indent=2)

a_better_count = sum(1 for r in results if r["a_better_on_criterion_a"] == "Yes")
b_better_count = sum(1 for r in results if r["a_better_on_criterion_a"] == "No")
error_cases = sum(1 for r in results if r["score_difference"] is None)

print(f"Total evaluated: {len(results)}")
print(f"A-optimized responses better on criterion A: {a_better_count} ({a_better_count/len(results)*100:.2f}%)")
print(f"B-optimized responses better on criterion A: {b_better_count} ({b_better_count/len(results)*100:.2f}%)")
print(f"Error cases: {error_cases} ({error_cases/len(results)*100:.2f}%)")

print("\nResults by criterion type:")
criteria_types = {}
for r in results:
    criterion_a = r["criterion_a"]
    if criterion_a not in criteria_types:
        criteria_types[criterion_a] = {"total": 0, "a_better": 0}
    
    criteria_types[criterion_a]["total"] += 1
    if r["a_better_on_criterion_a"] == "Yes":
        criteria_types[criterion_a]["a_better"] += 1

for criterion, stats in criteria_types.items():
    a_better_rate = stats["a_better"] / stats["total"] * 100 if stats["total"] > 0 else 0
    print(f"Criterion: '{criterion[:70]}...'")
    print(f"  A-optimized better: {stats['a_better']}/{stats['total']} ({a_better_rate:.2f}%)")

if len([r for r in results if r["score_difference"] is not None]) > 0:
    avg_diff = sum(r["score_difference"] for r in results if r["score_difference"] is not None) / len([r for r in results if r["score_difference"] is not None])
    print(f"\nAverage score difference (A - B on criterion A): {avg_diff:.4f}")
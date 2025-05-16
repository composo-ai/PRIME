import json

# Load configuration
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        file_config = config['file_config']
        output_file = config['output_file']
        key_fields = config['key_fields']
        dataset_path = config['dataset_path']
except Exception as e:
    print(f"Error loading configuration: {e}")
    exit(1)

# Load dataset mapping
dataset_mapping = {}
try:
    with open(dataset_path, 'r', encoding='utf-8') as f:
        dataset_data = json.load(f)
        for item in dataset_data:
            key = (
                item.get("prompt"),
                item.get("a_only_response"),
                item.get("b_only_response"),
                item.get("criterion_a"),
                item.get("criterion_b")
            )
            if all(key):  # Only add if all fields are present
                dataset_mapping[key] = item.get("data_source")
except Exception as e:
    print(f"Error loading dataset mapping: {e}")

merged_data = {}

for file_path, config in file_config.items():
    suffix = config["suffix"]
    is_base_file = config["is_base"]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f) 
            if not isinstance(data, list):
                print(f"Warning: Expected a list of objects in {file_path}, but got {type(data)}. Skipping this file.")
                continue

            for item in data:
                # Create a unique key for this item
                try:
                    current_key_tuple = tuple(item.get(k) for k in key_fields)
                except TypeError: 
                    print(f"Warning: Could not create a hashable key for an item in {file_path}. Item: {item}. Skipping this item.")
                    continue
                
                # If this key hasn't been seen, initialize it with common key fields
                if current_key_tuple not in merged_data:
                    # Initialize with None values for all scores
                    merged_data[current_key_tuple] = {
                        "prompt": item.get("prompt"),
                        "criterion": item.get("criterion_a"),
                        "chosen": item.get("a_only_response"),
                        "rejected": item.get("b_only_response"),
                        "chosen_composo": None,
                        "rejected_composo": None,
                        "chosen_openai": None,
                        "rejected_openai": None,
                        "chosen_claude": None,
                        "rejected_claude": None
                    }
                    
                    # Add datasource information if available in mapping
                    mapping_key = (
                        item.get("prompt"),
                        item.get("a_only_response"),
                        item.get("b_only_response"),
                        item.get("criterion_a"),
                        item.get("criterion_b")
                    )
                    if mapping_key in dataset_mapping:
                        merged_data[current_key_tuple]["datasource"] = dataset_mapping[mapping_key]
                
                # Add scores based on the source file
                if is_base_file:  # From "composo" file
                    if "a_score_on_criterion_a" in item and "b_score_on_criterion_a" in item and \
                       isinstance(item["a_score_on_criterion_a"], (int, float)) and \
                       isinstance(item["b_score_on_criterion_a"], (int, float)):
                        merged_data[current_key_tuple]["chosen_composo"] = item["a_score_on_criterion_a"]
                        merged_data[current_key_tuple]["rejected_composo"] = item["b_score_on_criterion_a"]
                        # Add explanations for composo
                        if "a_explanation" in item:
                            merged_data[current_key_tuple]["chosen_composo_explanation"] = item["a_explanation"]
                        if "b_explanation" in item:
                            merged_data[current_key_tuple]["rejected_composo_explanation"] = item["b_explanation"]
                
                if suffix == "_openai":  # From "openai" file
                    if "a_score_on_criterion_a" in item and "b_score_on_criterion_a" in item and \
                       isinstance(item["a_score_on_criterion_a"], (int, float)) and \
                       isinstance(item["b_score_on_criterion_a"], (int, float)):
                        merged_data[current_key_tuple]["chosen_openai"] = item["a_score_on_criterion_a"]
                        merged_data[current_key_tuple]["rejected_openai"] = item["b_score_on_criterion_a"]
                
                if suffix == "_claude":  # From "claude" file
                    if "a_score_on_criterion_a" in item and "b_score_on_criterion_a" in item and \
                       isinstance(item["a_score_on_criterion_a"], (int, float)) and \
                       isinstance(item["b_score_on_criterion_a"], (int, float)):
                        merged_data[current_key_tuple]["chosen_claude"] = item["a_score_on_criterion_a"]
                        merged_data[current_key_tuple]["rejected_claude"] = item["b_score_on_criterion_a"]

    except FileNotFoundError:
        print(f"Error: File not found {file_path}")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred while processing {file_path}: {e}")

# Convert the dictionary of merged items back to a list and filter out invalid records
final_merged_list = []
for record in merged_data.values():
    # Only keep records that have valid scores from all sources
    if all(isinstance(record.get(field), (int, float)) for field in [
        "chosen_composo", "rejected_composo",
        "chosen_openai", "rejected_openai",
        "chosen_claude", "rejected_claude"
    ]):
        final_merged_list.append(record)
    else:
        print(f"Skipping record due to missing or invalid scores: {record.get('prompt', '')[:100]}...")

# Add win fields
for record in final_merged_list:
    # Calculate composo_win
    chosen_composo = record.get("chosen_composo")
    rejected_composo = record.get("rejected_composo")
    if chosen_composo is not None and rejected_composo is not None:
        record["composo_win"] = chosen_composo > rejected_composo
    else:
        record["composo_win"] = False

    # Calculate claude_win
    chosen_claude = record.get("chosen_claude")
    rejected_claude = record.get("rejected_claude")
    if chosen_claude is not None and rejected_claude is not None:
        record["claude_win"] = chosen_claude > rejected_claude
    else:
        record["claude_win"] = False

    # Calculate openai_win
    chosen_openai = record.get("chosen_openai")
    rejected_openai = record.get("rejected_openai")
    if chosen_openai is not None and rejected_openai is not None:
        record["openai_win"] = chosen_openai > rejected_openai
    else:
        record["openai_win"] = False

# Write the merged data to the output file
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_merged_list, f, indent=2, ensure_ascii=False)
    print(f"Successfully merged data into {output_file}")
    print(f"Number of merged records: {len(final_merged_list)}")

    # Calculate and print win rates
    if final_merged_list:
        total_records = len(final_merged_list)
        composo_wins = sum(1 for record in final_merged_list if record.get("composo_win", False))
        claude_wins = sum(1 for record in final_merged_list if record.get("claude_win", False))
        openai_wins = sum(1 for record in final_merged_list if record.get("openai_win", False))

        print(f"\nCriterion A Win Rates:")
        print(f"Composo Win Rate: {composo_wins/total_records:.2%} ({composo_wins}/{total_records})")
        print(f"Claude Win Rate: {claude_wins/total_records:.2%} ({claude_wins}/{total_records})")
        print(f"OpenAI Win Rate: {openai_wins/total_records:.2%} ({openai_wins}/{total_records})")
    else:
        print("No records found to calculate win rates.")

except Exception as e:
    print(f"Error writing merged data to {output_file}: {e}") 
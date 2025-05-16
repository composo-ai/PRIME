# LLMAAJ - LLM Answer Analysis and Judgment

A tool for evaluating and comparing LLM responses based on specific criteria.

## Features

- Support for both Anthropic Claude and OpenAI GPT models
- Parallel processing for efficient evaluation
- Detailed analysis of response quality
- Configurable evaluation criteria
- Progress tracking and result statistics

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/LLMAAJ.git
cd LLMAAJ
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your API keys:
   - Copy `config.example.py` to `config.py`
   - Copy `config.example.json` to `config.json` (if using JSON configuration)
   - Add your API keys in the respective configuration files
   - Never commit your actual configuration files to version control

## Security

- Never commit files containing API keys or sensitive information
- Keep your configuration files (config.py, config.json) in your local environment only
- Use environment variables for sensitive data in production environments
- The .gitignore file is configured to prevent accidental commits of sensitive files

## Usage

1. Prepare your input data in JSON format with the following structure:
```json
[
    {
        "prompt": "Your question here",
        "criterion_a": "Evaluation criterion A",
        "criterion_b": "Evaluation criterion B",
        "a_only_response": "Response A",
        "b_only_response": "Response B"
    }
]
```

2. Update the input file path in your configuration file

3. Run the evaluation:
```bash
python LLMAAJ.py
```

## Configuration

You can configure the following settings in your configuration file:
- API keys
- Model provider (Anthropic or OpenAI)
- Model name
- Input/output file paths
- Maximum number of items to process

## Output

The tool generates a JSON file containing:
- Individual scores for each response
- Score differences
- Statistical analysis
- Error cases

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Security Policy

If you discover any security-related issues, please email security@example.com instead of using the issue tracker. 

# Evaluation Data Merger

This script merges multiple evaluation JSON files into a single consolidated file, comparing different evaluation methods (Composo, Claude, and OpenAI) for criterion-based assessment.

## Features

- Merges multiple evaluation JSON files
- Compares evaluation results from different sources (Composo, Claude, OpenAI)
- Calculates win rates for each evaluation method
- Handles data validation and error cases
- Supports custom configuration

## Requirements

- Python 3.6+
- Required packages listed in `requirements.txt`

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your evaluation JSON files in the `data` directory
2. Configure the file paths in `config.json`
3. Run the script:
```bash
python merge_script.py
```

## Configuration

Edit `config.json` to specify:
- Input file paths
- Output file path
- Key fields for merging
- Dataset mapping file path

## Output

The script generates a merged JSON file containing:
- Combined evaluation results
- Win rates for each evaluation method
- Detailed statistics

## License

MIT License 
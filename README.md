# PrimeBench: Practical Real World Industry and Multi Domain Evaluation Benchmark

A comprehensive dataset and evaluation framework for analyzing and comparing LLM responses in real-world industry scenarios across multiple domains, with support for merging evaluation results from different sources.

## Features

- Support for both Anthropic Claude and OpenAI GPT models
- Parallel processing for efficient evaluation
- Detailed analysis of response quality
- Configurable evaluation criteria
- Progress tracking and result statistics
- Merging and comparing evaluation results from different sources (Composo, Claude, OpenAI)
- Win rate calculation for each evaluation method
- Real-world industry scenarios
- Multi-domain evaluation capabilities

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/PRIMEBENCH.git
cd PRIMEBENCH
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

## Dataset Structure

The PRIMEBENCH dataset is organized as follows:

```
PRIMEBENCH/
├── data/
│   ├── raw/              # Raw evaluation data
│   ├── processed/        # Processed evaluation results
│   └── merged/          # Merged evaluation results
├── scripts/
│   ├── evaluation/      # Evaluation scripts
│   └── analysis/        # Analysis scripts
└── results/             # Final evaluation results and statistics
```

## Usage

### Evaluation

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
python scripts/evaluation/evaluate.py
```

### Merging Evaluation Results

1. Place your evaluation JSON files in the `data/processed` directory
2. Configure the file paths in `config.json`
3. Run the merge script:
```bash
python scripts/analysis/merge_results.py
```

## Configuration

You can configure the following settings in your configuration file:
- API keys
- Model provider (Anthropic or OpenAI)
- Model name
- Input/output file paths
- Maximum number of items to process
- Key fields for merging
- Dataset mapping file path

## Output

The tools generate JSON files containing:
- Individual scores for each response
- Score differences
- Statistical analysis
- Error cases
- Combined evaluation results
- Win rates for each evaluation method

## Dataset Citation

If you use PrimeBench in your research, please cite our work:

```bibtex
@misc{primebench2024,
    title={PrimeBench: Practical Real World Industry and Multi Domain Evaluation Benchmark},
    author={Your Name},
    year={2024},
    publisher={GitHub},
    journal={GitHub repository},
    howpublished={\url{https://github.com/yourusername/PRIMEBENCH}}
}
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Security Policy

If you discover any security-related issues, please email security@example.com instead of using the issue tracker. 
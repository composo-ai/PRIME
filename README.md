# PrimeBench: Practical Real-World Industry and Multi-Domain Evaluation Benchmark

## Overview

**Problem:** Current evaluation datasets focus on overall quality (e.g., [RewardBench](https://huggingface.co/datasets/allenai/reward-bench)) or single aspects (e.g., [Anthropic HH-RLHF](https://github.com/anthropics/hh-rlhf)). However, these datasets are not practical for real-world use cases, which are more complex, domain-specific, and business-oriented. These existing datasets are insufficient for evaluating models against multiple specific criteria such as "Reward responses that demonstrate creativity." in real world scenarios. 

**Solution:** PrimeBench provides paired responses edited along conflicting criteria (Comprehensive/Concise, Hallucinated/Factual, Technical/Simple) to test whether evaluation models can distinguish nuanced differences.

## Dataset Design

1. **Source:** Real-world datasets (FinQA, XSUM, PubMed, TechQA) with questions and corresponding context
2. **Baseline:** Generates initial answers using the original context
3. **Criteria Pairs:**
   - Comprehensive vs Concise
   - Hallucinated vs Factual
   - Technical vs Simple
4. **Modification:**: Create two responses that align with the given criteria pair.
5. **Evaluation:** Score both chosen and rejected answers using LLM judges and Composo models.
6. **Comparison:** If the score for the chosen answer is higher than the rejected answer, this data point is considered a pass; otherwise, it's a fail. The pass rate across all data points represents the performance of the evaluation approach.

## Quick Start

```bash
# Clone and install
git clone https://github.com/composo-ai/PRIME
cd PRIME
pip install -r requirements.txt

# Configure (copy and edit with your API keys)
# For Composo API key, please email contact@composo.ai
cp config.example.json config.json

# Run evaluation
python scripts/evaluate.py

# Show results
python scripts/show_results.py
```

## Data Format

```json
{
    "prompt": "The input containing user question and context",
    "criterion": "The evaluation criteria being tested",
    "chosen": "The response that should score higher according to the criterion",
    "rejected": "The response that should score lower according to the criterion",
    "datasource": "The source dataset (e.g., FINQA, XSUM, PubMed, TechQA)"
}
```


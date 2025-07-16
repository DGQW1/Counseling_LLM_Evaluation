# Counseling LLM Evaluation

Automated evaluation pipeline for counseling LLM research using ChatGPT 4o API to evaluate generated counseling questions.

**Scripts included:**
- `evaluate_questions.py` - Main evaluation script using ChatGPT 4o API
- `extract_evaluations.py` - Extract evaluation results to readable markdown files

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment**
   ```bash
   # Create .env file with your OpenAI API key
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

3. **Run evaluation**
   ```bash
   # Process all JSON files
   python evaluate_questions.py

   # Process only first 100 questions per file
   python evaluate_questions.py --max-questions 100

   # Process a specific file independently
   python evaluate_questions.py --file llm_generated_questions_claude_without_explanation.json
   ```

4. **Extract evaluations to markdown** (after running evaluations)
   ```bash
   # Extract all evaluation results to markdown files
   python extract_evaluations.py

   # Extract specific result file
   python extract_evaluations.py --file llm_evaluated_response_claude_without_explanation.json
   ```

## What it does

- Processes all JSON files in `data/` folder
- Evaluates questions using the prompt template in `prompt.md`
- Calls ChatGPT 4o API for each successful data point
- Saves results to `results/` folder with format: `llm_evaluated_response_{model}_without_explanation.json`
- Extract evaluations to readable markdown files

## Options

### Evaluation Script (`evaluate_questions.py`)
- `--file`: Process a specific JSON file independently (e.g., `llm_generated_questions_claude_without_explanation.json`)
- `--max-questions`: Limit questions per file (e.g., 100)
- `--data-dir`: Custom data directory (default: "data")
- `--results-dir`: Custom results directory (default: "results")

### Extraction Script (`extract_evaluations.py`)
- `--file`: Extract a specific JSON result file (e.g., `llm_evaluated_response_claude_without_explanation.json`)
- `--results-dir`: Custom results directory (default: "results")

## Features

### Evaluation Features
- Process all files or target specific files independently
- Only processes entries where `metadata.success = true`
- Automatic error handling and retry logic
- Progress tracking and rate limiting
- Skips already processed files

### Extraction Features
- Converts JSON evaluation results to readable markdown format
- Creates individual `.md` files for each model's evaluations
- Generates a comprehensive summary with statistics
- Includes success/failure tracking and token usage
- Formats evaluations with context, questions, and responses
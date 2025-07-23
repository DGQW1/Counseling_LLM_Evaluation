# Counseling LLM Evaluation

Automated evaluation pipeline for counseling LLM research using ChatGPT 4o API to evaluate generated counseling questions.

**Scripts included:**
- `evaluate_questions.py` - Main evaluation script using ChatGPT 4o API
- `extract_evaluations.py` - Extract evaluation results to readable markdown files
- `analyze_evaluations.py` - Analyze evaluation results with visualizations and statistics

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
   # Process all files from 500_4_Models dataset (default)
   python evaluate_questions.py

   # Process all files from 100_4_Models_5_Times dataset (trial runs)
   python evaluate_questions.py --dataset 100_4_Models_5_Times

   # Process only first 100 questions per file
   python evaluate_questions.py --max-questions 100

   # Process a specific file from 500_4_Models dataset
   python evaluate_questions.py --file llm_generated_questions_claude_without_explanation.json

   # Process a specific trial file from 100_4_Models_5_Times dataset
   python evaluate_questions.py --dataset 100_4_Models_5_Times --file claude_first_trial.json
   ```

4. **Extract evaluations to markdown** (after running evaluations)
   ```bash
   # Extract all evaluation results to markdown files
   python extract_evaluations.py

   # Extract specific result file
   python extract_evaluations.py --file llm_evaluated_response_claude_without_explanation.json
   ```

5. **Analyze evaluation results** (after running evaluations)
   ```bash
   # Generate comprehensive analysis with visualizations and statistics
   python analyze_evaluations.py

   # Specify custom directories
   python analyze_evaluations.py --results-dir results --output-dir analysis
   ```

## What it does

- **Evaluation**: Processes all JSON files in `data/` folder and evaluates questions using ChatGPT 4o API
- **Data Processing**: Uses the prompt template in `prompt.md` and properly separates questions from explanations
- **Results Storage**: Saves evaluation results to `results/` folder in JSON format
- **Markdown Export**: Extracts evaluations to readable markdown files with proper formatting
- **Statistical Analysis**: Generates comprehensive analysis with visualizations and summary statistics
- **Model Comparison**: Compares performance across different LLMs and explanation variants

## Options

### Evaluation Script (`evaluate_questions.py`)
- `--dataset`: Choose dataset type: `500_4_Models` (default) or `100_4_Models_5_Times` (trial runs)
- `--file`: Process a specific JSON file independently
- `--max-questions`: Limit questions per file (e.g., 100)
- `--data-dir`: Custom data directory (default: "data")
- `--results-dir`: Custom results directory (default: "results")

### Extraction Script (`extract_evaluations.py`)
- `--file`: Extract a specific JSON result file (e.g., `llm_evaluated_response_claude_without_explanation.json`)
- `--results-dir`: Custom results directory (default: "results")

### Analysis Script (`analyze_evaluations.py`)
- `--results-dir`: Directory containing evaluation results (default: "results")
- `--output-dir`: Directory to save analysis output (default: "analysis")

## Features

### Evaluation Features
- Process all files or target specific files independently
- Only processes entries where `metadata.success = true`
- Automatic error handling and retry logic
- Progress tracking and rate limiting
- Skips already processed files
- Separates questions from explanations for accurate evaluation

### Extraction Features
- Converts JSON evaluation results to readable markdown format
- Creates individual `.md` files for each model's evaluations
- Generates a comprehensive summary with statistics
- Includes success/failure tracking and token usage
- Formats evaluations with context, questions, and responses
- Properly separates questions and explanations in display

### Analysis Features
- **Visualizations**: Distribution plots, box plots, heatmaps, and category analysis
- **Model Comparison**: Compare rating distributions across different LLMs
- **Cross-Comparison Analysis**: Detailed with/without explanation comparison by model
- **Interaction Analysis**: Model × Explanation interaction heatmaps for each metric
- **Statistical Summary**: Comprehensive markdown report with key insights
- **Metric Extraction**: Parses tone, relevance, clarity, toxicity, and assumption ratings
- **Category Analysis**: Analyzes question format, purpose, and depth classifications
- **Model-Specific Insights**: Individual model performance with explanation impact analysis
- **Auto-generated Reports**: Creates detailed summary statistics and visual analysis
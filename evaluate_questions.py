#!/usr/bin/env python3
"""
Script to evaluate counseling questions using ChatGPT 4o API.

This script processes JSON files containing LLM-generated questions and evaluates them
using the prompt template. It calls ChatGPT 4o API for each valid data point.
"""

import json
import os
import argparse
import time
from typing import Dict, List, Any
from pathlib import Path
import openai
from openai import OpenAI
from dotenv import load_dotenv

def load_prompt_template() -> str:
    """Load and prepare the prompt template from prompt.md"""
    with open('prompt.md', 'r', encoding='utf-8') as f:
        prompt = f.read()
    return prompt

def load_json_data(file_path: str) -> List[Dict[str, Any]]:
    """Load data from a JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def filter_successful_data(data: List[Dict[str, Any]], max_questions: int = None) -> List[Dict[str, Any]]:
    """Filter data points that have success: true and limit to max_questions if specified"""
    successful_data = [item for item in data if item.get('metadata', {}).get('success', False)]
    
    if max_questions is not None:
        successful_data = successful_data[:max_questions]
    
    return successful_data

def call_chatgpt_api(client: OpenAI, prompt: str, max_retries: int = 3) -> Dict[str, Any]:
    """Call ChatGPT 4o API with retry logic"""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            return {
                "response": response.choices[0].message.content,
                "model": "gpt-4o",
                "success": True,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "tokens_used": response.usage.total_tokens if response.usage else None
            }
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt) 
            else:
                return {
                    "response": f"ERROR: API call failed after {max_retries} attempts - {str(e)}",
                    "model": "gpt-4o",
                    "success": False,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "error": str(e)
                }

def extract_model_name(filename: str) -> str:
    """Extract model name from filename"""
    # Remove file extension and prefix
    name = filename.replace('.json', '').replace('llm_generated_questions_', '')
    
    # Extract model name (everything before _with_explanation or _without_explanation)
    if '_with_explanation' in name:
        return name.replace('_with_explanation', '')
    elif '_without_explanation' in name:
        return name.replace('_without_explanation', '')
    else:
        return name

def parse_question_from_generated_text(generated_question: str, has_explanation: bool) -> str:
    """Extract just the question part from the generated text"""
    if not has_explanation:
        return generated_question.strip()
    
    # Try to extract only the question part from "Question(s): ... Explanation: ..." format
    if "Explanation:" in generated_question:
        parts = generated_question.split("Explanation:")
        if len(parts) >= 2:
            question_part = parts[0].replace("Question:", "").replace("Questions:", "").strip()
            return question_part
    
    # Fallback: if format is different, return the whole thing
    return generated_question.strip()

def process_file(file_path: str, prompt_template: str, client: OpenAI, max_questions: int = None) -> List[Dict[str, Any]]:
    """Process a single JSON file"""
    print(f"Processing {file_path}...")
    
    # Check if this file contains explanations
    has_explanation = 'with_explanation' in file_path
    
    # Load and filter data
    data = load_json_data(file_path)
    successful_data = filter_successful_data(data, max_questions)
    
    print(f"Found {len(successful_data)} successful entries to process")
    if has_explanation:
        print("Note: This file contains explanations - extracting questions only for evaluation")
    
    results = []
    
    for i, item in enumerate(successful_data):
        print(f"Processing item {i+1}/{len(successful_data)} (ID: {item.get('id', 'unknown')})")
        
        # Extract conversation and question
        conversation = item['input']['context']
        generated_question_raw = item['generated_question']
        
        # Parse out just the question (without explanation if present)
        question = parse_question_from_generated_text(generated_question_raw, has_explanation)
        
        # Prepare the prompt
        filled_prompt = prompt_template.format(
            conversation=conversation,
            question=question
        )
        
        # Call ChatGPT API
        api_response = call_chatgpt_api(client, filled_prompt)
        
        # Create result entry
        result = {
            "original_id": item['id'],
            "original_model": item['model_provider'],
            "input": item['input'],
            "original_question": generated_question_raw,  # Store the full original (with explanation if present)
            "evaluated_question": question,  # Store the parsed question that was sent to ChatGPT
            "chatgpt_evaluation": api_response,
            "metadata": {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "source_file": os.path.basename(file_path),
                "has_explanation": has_explanation
            }
        }
        
        results.append(result)
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
    
    return results

def save_results(results: List[Dict[str, Any]], output_path: str):
    """Save results to JSON file"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Results saved to {output_path}")

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    parser = argparse.ArgumentParser(description='Evaluate counseling questions using ChatGPT 4o')
    parser.add_argument('--file', type=str, help='Process a specific JSON file (e.g., llm_generated_questions_claude_without_explanation.json)')
    parser.add_argument('--max-questions', type=int, help='Maximum number of questions to process per file (e.g., 100)')
    parser.add_argument('--data-dir', default='data', help='Directory containing JSON files')
    parser.add_argument('--results-dir', default='results', help='Directory to save results')
    
    args = parser.parse_args()
    
    # Get API key from environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please make sure you have a .env file with OPENAI_API_KEY=your_api_key")
        return
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Load prompt template
    prompt_template = load_prompt_template()
    
    # Determine which files to process
    data_dir = Path(args.data_dir)
    
    if args.file:
        # Process specific file
        json_file_path = data_dir / args.file
        if not json_file_path.exists():
            print(f"Error: File {json_file_path} does not exist")
            return
        json_files = [json_file_path]
        print(f"Processing specific file: {args.file}")
    else:
        # Process all JSON files in data directory
        json_files = list(data_dir.glob('*.json'))
        if not json_files:
            print(f"No JSON files found in {data_dir}")
            return
        print(f"Found {len(json_files)} JSON files to process")
    
    if args.max_questions:
        print(f"Will process maximum {args.max_questions} questions per file")
    
    # Process each file
    for json_file in json_files:
        model_name = extract_model_name(json_file.name)
        
        # Determine if this is a "without_explanation" file for naming
        if 'without_explanation' in json_file.name:
            output_filename = f"llm_evaluated_response_{model_name}_without_explanation.json"
        else:
            output_filename = f"llm_evaluated_response_{model_name}_with_explanation.json"
        
        output_path = Path(args.results_dir) / output_filename
        
        # Skip if output file already exists
        if output_path.exists():
            print(f"Output file {output_path} already exists. Skipping...")
            continue
        
        try:
            # Process the file
            results = process_file(str(json_file), prompt_template, client, args.max_questions)
            
            # Save results
            save_results(results, str(output_path))
            
            print(f"Successfully processed {json_file.name}")
            print("-" * 50)
            
        except Exception as e:
            print(f"Error processing {json_file.name}: {str(e)}")
            continue
    
    print("All files processed!")

if __name__ == "__main__":
    main() 
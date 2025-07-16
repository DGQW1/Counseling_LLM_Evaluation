#!/usr/bin/env python3
"""
Script to extract ChatGPT evaluation responses from JSON result files 
and save them as readable markdown files.
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Any

def load_json_results(file_path: str) -> List[Dict[str, Any]]:
    """Load evaluation results from a JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)



def format_evaluation_to_markdown(evaluation_data: List[Dict[str, Any]], source_file: str) -> str:
    """Format evaluation data into markdown"""
    
    # Extract model info from filename
    model_info = source_file.replace('llm_evaluated_response_', '').replace('.json', '')
    has_explanation = 'with_explanation' in source_file
    
    markdown_content = f"""# ChatGPT Evaluations: {model_info.title()}

**Source File:** `{source_file}`  
**Total Evaluations:** {len(evaluation_data)}  
**Generated:** {evaluation_data[0]['metadata']['timestamp'] if evaluation_data else 'Unknown'}  
**Includes Explanations:** {'Yes' if has_explanation else 'No'}

---

"""
    
    for i, item in enumerate(evaluation_data, 1):
        # Get the original question and context
        original_question_raw = item.get('original_question', 'N/A')
        evaluated_question = item.get('evaluated_question', None)  # The question actually sent to ChatGPT
        context = item['input'].get('context', 'N/A')
        situation = item['input'].get('situation', 'N/A')
        
        # Use the evaluated question if available (newer format), otherwise parse the original
        if evaluated_question:
            # The evaluated_question might still contain explanation, so parse it
            if has_explanation and "Question:" in evaluated_question and "Explanation:" in evaluated_question:
                parts = evaluated_question.split("Explanation:", 1)
                question = parts[0].replace("Question:", "").replace("Questions:", "").strip()
                explanation = parts[1].strip() if len(parts) == 2 else None
            else:
                question = evaluated_question.strip()
                explanation = None
        else:
            # Fallback: parse the original for backward compatibility
            if has_explanation and "Question:" in original_question_raw and "Explanation:" in original_question_raw:
                parts = original_question_raw.split("Explanation:", 1)
                question = parts[0].replace("Question:", "").strip()
                explanation = parts[1].strip() if len(parts) == 2 else None
            else:
                question = original_question_raw.strip()
                explanation = None
        
        # Get ChatGPT evaluation
        chatgpt_eval = item.get('chatgpt_evaluation', {})
        evaluation_response = chatgpt_eval.get('response', 'No response available')
        success = chatgpt_eval.get('success', False)
        
        # Format the markdown section
        markdown_content += f"""## Evaluation {i} (ID: {item.get('original_id', 'Unknown')})

### Context
**Situation:** {situation}

**Conversation:** {context}

### Question Evaluated by ChatGPT
> {question}
"""
        
        # Add explanation section if present
        if explanation:
            markdown_content += f"""
### Original Question Explanation
```
{explanation}
```

*Note: Only the question above (not this explanation) was sent to ChatGPT for evaluation.*
"""
        
        markdown_content += """
### ChatGPT Evaluation
"""
        
        if success:
            markdown_content += f"""```
{evaluation_response}
```

**Status:** ✅ Success  
**Tokens Used:** {chatgpt_eval.get('tokens_used', 'N/A')}

---

"""
        else:
            error_info = chatgpt_eval.get('error', 'Unknown error')
            markdown_content += f"""```
ERROR: {evaluation_response}
```

**Status:** ❌ Failed  
**Error:** {error_info}

---

"""
    
    return markdown_content

def create_summary_markdown(results_dir: Path) -> str:
    """Create a summary markdown file with statistics"""
    
    json_files = list(results_dir.glob('llm_evaluated_response_*.json'))
    
    if not json_files:
        return "# Evaluation Summary\n\nNo evaluation files found.\n"
    
    summary_content = """# Evaluation Summary

## Overview

"""
    
    total_evaluations = 0
    total_successful = 0
    total_failed = 0
    
    model_stats = []
    
    for json_file in json_files:
        try:
            data = load_json_results(str(json_file))
            model_name = json_file.name.replace('llm_evaluated_response_', '').replace('.json', '')
            
            successful = sum(1 for item in data if item.get('chatgpt_evaluation', {}).get('success', False))
            failed = len(data) - successful
            
            model_stats.append({
                'model': model_name,
                'total': len(data),
                'successful': successful,
                'failed': failed,
                'success_rate': f"{(successful/len(data)*100):.1f}%" if len(data) > 0 else "0%"
            })
            
            total_evaluations += len(data)
            total_successful += successful
            total_failed += failed
            
        except Exception as e:
            print(f"Error processing {json_file}: {e}")
            continue
    
    # Overall statistics
    overall_success_rate = (total_successful/total_evaluations*100) if total_evaluations > 0 else 0
    
    summary_content += f"""**Total Evaluations:** {total_evaluations}  
**Successful:** {total_successful}  
**Failed:** {total_failed}  
**Overall Success Rate:** {overall_success_rate:.1f}%

## Model Breakdown

| Model | Total | Successful | Failed | Success Rate |
|-------|-------|------------|--------|--------------|
"""
    
    for stats in model_stats:
        summary_content += f"| {stats['model']} | {stats['total']} | {stats['successful']} | {stats['failed']} | {stats['success_rate']} |\n"
    
    summary_content += """
## Generated Files

"""
    
    for json_file in json_files:
        md_file = json_file.name.replace('.json', '.md')
        summary_content += f"- [`{md_file}`](./{md_file})\n"
    
    return summary_content

def main():
    parser = argparse.ArgumentParser(description='Extract ChatGPT evaluations to markdown files')
    parser.add_argument('--results-dir', default='results', help='Directory containing JSON result files')
    parser.add_argument('--file', type=str, help='Process a specific JSON result file')
    
    args = parser.parse_args()
    
    results_dir = Path(args.results_dir)
    
    if not results_dir.exists():
        print(f"Results directory {results_dir} does not exist")
        return
    
    if args.file:
        # Process specific file
        json_file = results_dir / args.file
        if not json_file.exists():
            print(f"File {json_file} does not exist")
            return
        json_files = [json_file]
    else:
        # Process all JSON result files
        json_files = list(results_dir.glob('llm_evaluated_response_*.json'))
        
        if not json_files:
            print(f"No evaluation result files found in {results_dir}")
            return
    
    print(f"Found {len(json_files)} result files to process")
    
    # Process each JSON file
    for json_file in json_files:
        print(f"Processing {json_file.name}...")
        
        try:
            # Load evaluation data
            evaluation_data = load_json_results(str(json_file))
            
            if not evaluation_data:
                print(f"No data found in {json_file.name}")
                continue
            
            # Generate markdown content
            markdown_content = format_evaluation_to_markdown(evaluation_data, json_file.name)
            
            # Save markdown file
            md_file = results_dir / json_file.name.replace('.json', '.md')
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"Created {md_file.name}")
            
        except Exception as e:
            print(f"Error processing {json_file.name}: {e}")
            continue
    
    # Create summary file if processing all files
    if not args.file:
        print("Creating summary file...")
        summary_content = create_summary_markdown(results_dir)
        summary_file = results_dir / 'evaluation_summary.md'
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        print(f"Created {summary_file.name}")
    
    print("Extraction complete!")

if __name__ == "__main__":
    main() 
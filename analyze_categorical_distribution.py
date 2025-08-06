#!/usr/bin/env python3
"""
Categorical Distribution Analysis Script

This script analyzes the categorical data (format, purpose, depth) distributions
across all LLMs and human data from the json_evaluations folder.
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Set
import re
from collections import defaultdict, Counter

# Set style for better plots
plt.style.use('default')
sns.set_palette("husl")

def normalize_category_list(categories: List[str]) -> List[str]:
    """
    Normalize category lists by sorting and cleaning them.
    This handles cases like ['Exploring', 'Clarifying'] vs ['Clarifying', 'Exploring']
    """
    if not categories:
        return []
    
    # Clean and normalize individual categories
    normalized = []
    for cat in categories:
        # Remove extra whitespace and normalize case
        cleaned = cat.strip()
        if cleaned:
            normalized.append(cleaned)
    
    # Sort alphabetically to handle order differences
    return sorted(normalized)

def normalize_category_string(category_str: str) -> str:
    """
    Convert a list of categories to a normalized string representation.
    """
    if isinstance(category_str, list):
        normalized_list = normalize_category_list(category_str)
        return ", ".join(normalized_list)
    elif isinstance(category_str, str):
        # Handle string representations of lists
        if category_str.startswith('[') and category_str.endswith(']'):
            # Try to parse as a list
            try:
                category_list = eval(category_str)
                if isinstance(category_list, list):
                    normalized_list = normalize_category_list(category_list)
                    return ", ".join(normalized_list)
            except:
                pass
        
        # Handle comma-separated strings
        if ',' in category_str:
            parts = [part.strip() for part in category_str.split(',')]
            normalized_list = normalize_category_list(parts)
            return ", ".join(normalized_list)
        
        return category_str.strip()
    
    return str(category_str)

def parse_chatgpt_evaluation(evaluation_text: str) -> Dict[str, Any]:
    """Parse ChatGPT evaluation response to extract categories"""
    result = {
        'format_categories': [],
        'purpose_categories': [],
        'depth_categories': []
    }
    
    if not evaluation_text:
        return result
    
    # Extract categories (handle both bracketed lists and simple values)
    category_patterns = {
        'format_categories': r'Format:\s*(?:\[)?(.*?)(?:\])?(?:\n|$)',
        'purpose_categories': r'Purpose:\s*(?:\[)?(.*?)(?:\])?(?:\n|$)', 
        'depth_categories': r'Depth:\s*(?:\[)?(.*?)(?:\])?(?:\n|$)'
    }
    
    for cat_type, pattern in category_patterns.items():
        match = re.search(pattern, evaluation_text, re.DOTALL | re.IGNORECASE)
        if match:
            categories_str = match.group(1).strip()
            # Split by comma and clean up
            if ',' in categories_str:
                categories = [cat.strip().strip('"\'') for cat in categories_str.split(',')]
            else:
                categories = [categories_str.strip().strip('"\'')]
            # Filter out empty categories
            result[cat_type] = [cat for cat in categories if cat]
    
    return result

def load_evaluation_data(json_file: Path) -> List[Dict[str, Any]]:
    """Load and parse evaluation data from a JSON file"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = []
        for item in data:
            # Extract evaluation text
            evaluation_text = ""
            if 'llm_response' in item:
                evaluation_text = item['llm_response']
            elif 'chatgpt_evaluation' in item and 'response' in item['chatgpt_evaluation']:
                evaluation_text = item['chatgpt_evaluation']['response']
            
            # Parse categories
            categories = parse_chatgpt_evaluation(evaluation_text)
            
            # Create result entry
            result = {
                'original_id': item.get('original_id', ''),
                'format_categories': categories['format_categories'],
                'purpose_categories': categories['purpose_categories'],
                'depth_categories': categories['depth_categories'],
                'source_file': json_file.name
            }
            results.append(result)
        
        return results
    
    except Exception as e:
        print(f"Error loading {json_file}: {e}")
        return []

def load_categorical_data(evaluations_dir: Path) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    """
    Load categorical data, keeping with/without explanation separate.
    Returns: {model: {'with': [...], 'without': [...]}}
    """
    models = ['claude', 'gemini', 'gpt4o-mini', 'llama-api', 'human']
    categorical_data = {}
    
    for model in models:
        categorical_data[model] = {'with': [], 'without': []}
        
        if model == 'human':
            # Human data is in a single file
            human_file = evaluations_dir / 'llm_evaluated_response_human.json'
            if human_file.exists():
                categorical_data[model]['without'] = load_evaluation_data(human_file)
                print(f"Loaded {len(categorical_data[model]['without'])} human evaluations")
        else:
            # Load with explanation data
            with_file = evaluations_dir / f'llm_evaluated_response_{model}_with_explanation.json'
            if with_file.exists():
                categorical_data[model]['with'] = load_evaluation_data(with_file)
                print(f"Loaded {len(categorical_data[model]['with'])} with-explanation evaluations for {model}")
            
            # Load without explanation data
            without_file = evaluations_dir / f'llm_evaluated_response_{model}_without_explanation.json'
            if without_file.exists():
                categorical_data[model]['without'] = load_evaluation_data(without_file)
                print(f"Loaded {len(categorical_data[model]['without'])} without-explanation evaluations for {model}")
    
    return categorical_data

def create_category_distribution_dataframe(categorical_data: Dict[str, Dict[str, List[Dict[str, Any]]]]) -> pd.DataFrame:
    """
    Create a DataFrame with normalized category distributions.
    """
    rows = []
    
    for model, explanation_data in categorical_data.items():
        for explanation_type, evaluations in explanation_data.items():
            for evaluation in evaluations:
                # Normalize categories
                format_norm = normalize_category_string(evaluation['format_categories'])
                purpose_norm = normalize_category_string(evaluation['purpose_categories'])
                depth_norm = normalize_category_string(evaluation['depth_categories'])
                
                rows.append({
                    'model': model,
                    'explanation_type': explanation_type,
                    'format_categories': format_norm,
                    'purpose_categories': purpose_norm,
                    'depth_categories': depth_norm,
                    'original_id': evaluation['original_id']
                })
    
    return pd.DataFrame(rows)

def create_category_visualizations(df: pd.DataFrame, output_dir: Path):
    """Create bar charts for category distributions with separate with/without explanation"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    models = ['claude', 'gemini', 'gpt4o-mini', 'llama-api', 'human']
    category_types = ['format_categories', 'purpose_categories', 'depth_categories']
    category_labels = ['Format Categories', 'Purpose Categories', 'Depth Categories']
    
    # Create individual plots for each category type with 2x5 layout
    for cat_type, cat_label in zip(category_types, category_labels):
        # Get top categories across all models and explanation types
        all_categories = df[cat_type].value_counts().head(12)
        top_categories = all_categories.index.tolist()
        
        fig, axes = plt.subplots(2, 5, figsize=(25, 12))
        fig.suptitle(f'{cat_label} Distribution Across Models', fontsize=16, fontweight='bold')
        
        # Top row: with explanation
        # Bottom row: without explanation
        explanation_types = ['with', 'without']
        explanation_labels = ['With Explanation', 'Without Explanation']
        
        for row_idx, (exp_type, exp_label) in enumerate(zip(explanation_types, explanation_labels)):
            for col_idx, model in enumerate(models):
                ax = axes[row_idx, col_idx]
                
                # For human, we only have "without" explanation data
                if model == 'human' and exp_type == 'with':
                    ax.text(0.5, 0.5, 'N/A\n(Human data only\navailable without\nexplanation)', 
                           ha='center', va='center', transform=ax.transAxes, fontsize=10)
                    ax.set_title(f'{model.title()} ({exp_label})')
                    ax.set_xlabel('Categories')
                    ax.set_ylabel('Count')
                    continue
                
                # Filter data for this model and explanation type
                model_data = df[
                    (df['model'] == model) & 
                    (df['explanation_type'] == exp_type)
                ]
                
                if len(model_data) == 0:
                    ax.text(0.5, 0.5, 'No Data', ha='center', va='center', transform=ax.transAxes)
                    ax.set_title(f'{model.title()} ({exp_label})')
                    continue
                
                # Get category counts for this model/explanation combination
                model_counts = model_data[cat_type].value_counts()
                counts = [model_counts.get(cat, 0) for cat in top_categories]
                total_count = len(model_data)
                
                # Calculate "Other" category count (categories not in top_categories)
                shown_count = sum(counts)
                other_count = total_count - shown_count
                
                # Add "Other" category if there are missing categories
                if other_count > 0:
                    counts.append(other_count)
                    display_categories = top_categories + ['Other']
                else:
                    display_categories = top_categories
                
                percentages = [count/total_count*100 if total_count > 0 else 0 for count in counts]
                
                # Create bars
                bars = ax.bar(range(len(display_categories)), counts, alpha=0.7, 
                             color=plt.cm.Set3(col_idx), edgecolor='black', linewidth=0.5)
                
                # Add percentage labels on bars
                for i, (bar, count, pct) in enumerate(zip(bars, counts, percentages)):
                    if count > 0:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01*max(counts),
                               f'{count}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=8)
                
                # Styling
                ax.set_title(f'{model.title()} ({exp_label})', fontweight='bold')
                ax.set_xlabel('Categories')
                ax.set_ylabel('Count')
                ax.set_xticks(range(len(display_categories)))
                ax.set_xticklabels(display_categories, rotation=45, ha='right')
                ax.grid(True, alpha=0.3, axis='y')
                
                # Set consistent y-axis limits across all subplots
                max_count = df.groupby(['model', 'explanation_type'])[cat_type].apply(
                    lambda x: x.value_counts().max() if len(x) > 0 else 0
                ).max()
                ax.set_ylim(0, max_count * 1.1)
                
                # Add statistics text (moved to top right corner)
                if len(model_data) > 0:
                    unique_cats = model_data[cat_type].nunique()
                    ax.text(0.98, 0.98, f'Unique: {unique_cats}\nn={len(model_data)}', 
                           transform=ax.transAxes, fontsize=8, verticalalignment='top',
                           horizontalalignment='right',
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig(output_dir / f'{cat_type}_distribution.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Generated {cat_type}_distribution.png")
    
    # Create overall comparison plot (combined view)
    fig, axes = plt.subplots(3, 1, figsize=(16, 20))
    fig.suptitle('Category Distribution Comparison (Combined)', fontsize=16, fontweight='bold')
    
    for idx, (cat_type, cat_label) in enumerate(zip(category_types, category_labels)):
        ax = axes[idx]
        
        # Get top categories across all models
        all_categories = df[cat_type].value_counts().head(10)
        top_categories = all_categories.index.tolist()
        
        # Create data for grouped bar chart (combining with/without for comparison)
        category_counts = {}
        for model in models:
            model_data = df[df['model'] == model]
            model_counts = model_data[cat_type].value_counts()
            category_counts[model] = [model_counts.get(cat, 0) for cat in top_categories]
        
        # Create grouped bar chart
        x = np.arange(len(top_categories))
        bar_width = 0.15
        colors = plt.cm.Set3(np.linspace(0, 1, len(models)))
        
        for i, (model, counts) in enumerate(category_counts.items()):
            offset = (i - len(models)/2 + 0.5) * bar_width
            bars = ax.bar(x + offset, counts, bar_width, label=model, 
                         color=colors[i], alpha=0.8)
            
            # Add value labels on bars (only for non-zero values)
            for bar, count in zip(bars, counts):
                if count > 0:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                           f'{int(count)}', ha='center', va='bottom', fontsize=8)
        
        ax.set_xlabel('Categories')
        ax.set_ylabel('Frequency')
        ax.set_title(f'{cat_label} Distribution Across Models (Combined)')
        ax.set_xticks(x)
        ax.set_xticklabels(top_categories, rotation=45, ha='right')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'category_distribution_comparison.png', 
               dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Generated category_distribution_comparison.png")

def generate_distribution_statistics(df: pd.DataFrame, output_dir: Path):
    """Generate detailed statistics for category distributions"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    models = ['claude', 'gemini', 'gpt4o-mini', 'llama-api', 'human']
    category_types = ['format_categories', 'purpose_categories', 'depth_categories']
    category_labels = ['Format Categories', 'Purpose Categories', 'Depth Categories']
    
    with open(output_dir / 'category_distribution_statistics.md', 'w', encoding='utf-8') as f:
        f.write("# Category Distribution Statistics\n\n")
        f.write(f"**Analysis Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Models Analyzed:** {', '.join(models)}\n")
        f.write(f"**Total Evaluations:** {len(df)}\n\n")
        
        # Overall summary with explanation types
        f.write("## Overall Summary\n\n")
        f.write("| Model | With Explanation | Without Explanation | Total |\n")
        f.write("|-------|------------------|--------------------|---------|\n")
        for model in models:
            with_count = len(df[(df['model'] == model) & (df['explanation_type'] == 'with')])
            without_count = len(df[(df['model'] == model) & (df['explanation_type'] == 'without')])
            total_count = with_count + without_count
            f.write(f"| {model} | {with_count} | {without_count} | {total_count} |\n")
        f.write("\n")
        
        # Detailed analysis for each category type
        for cat_type, cat_label in zip(category_types, category_labels):
            f.write(f"## {cat_label} Analysis\n\n")
            
            # Overall distribution
            f.write(f"### Overall {cat_label} Distribution\n\n")
            overall_counts = df[cat_type].value_counts().head(20)
            f.write("| Category | Count | Percentage |\n")
            f.write("|----------|-------|------------|\n")
            total = len(df)
            for category, count in overall_counts.items():
                percentage = (count / total) * 100
                f.write(f"| {category} | {count} | {percentage:.1f}% |\n")
            f.write("\n")
            
            # Model-specific distribution
            f.write(f"### {cat_label} by Model\n\n")
            
            # Get top categories
            top_categories = df[cat_type].value_counts().head(10).index.tolist()
            
            # Create table header
            f.write("| Category | " + " | ".join(models) + " |\n")
            f.write("|----------|" + "|".join(["-" * len(model) for model in models]) + "|\n")
            
            for category in top_categories:
                row = [category]
                for model in models:
                    model_data = df[df['model'] == model]
                    count = (model_data[cat_type] == category).sum()
                    total_model = len(model_data)
                    if total_model > 0:
                        percentage = (count / total_model) * 100
                        row.append(f"{count} ({percentage:.1f}%)")
                    else:
                        row.append("0 (0.0%)")
                f.write("| " + " | ".join(row) + " |\n")
            f.write("\n")
            
            # Model ranking for this category
            f.write(f"### Model Preferences - {cat_label}\n\n")
            f.write("**Top category for each model:**\n\n")
            for model in models:
                model_data = df[df['model'] == model]
                if len(model_data) > 0:
                    top_category = model_data[cat_type].value_counts().index[0]
                    count = model_data[cat_type].value_counts().iloc[0]
                    total_model = len(model_data)
                    percentage = (count / total_model) * 100
                    f.write(f"- **{model}**: {top_category} ({count}/{total_model}, {percentage:.1f}%)\n")
            f.write("\n")
        
        # Cross-category analysis
        f.write("## Cross-Category Analysis\n\n")
        
        f.write("### Most Common Category Combinations\n\n")
        
        # Create combination strings
        df['category_combination'] = df.apply(lambda row: 
            f"Format: {row['format_categories']} | Purpose: {row['purpose_categories']} | Depth: {row['depth_categories']}", 
            axis=1)
        
        top_combinations = df['category_combination'].value_counts().head(10)
        f.write("| Rank | Combination | Count |\n")
        f.write("|------|-------------|-------|\n")
        for i, (combination, count) in enumerate(top_combinations.items(), 1):
            f.write(f"| {i} | {combination} | {count} |\n")
        f.write("\n")
        
        # Model diversity analysis
        f.write("## Model Diversity Analysis\n\n")
        
        for cat_type, cat_label in zip(category_types, category_labels):
            f.write(f"### {cat_label} Diversity\n\n")
            f.write("| Model | Unique Categories | Most Common (%) | Second Most Common (%) |\n")
            f.write("|-------|------------------|-----------------|------------------------|\n")
            
            for model in models:
                model_data = df[df['model'] == model]
                if len(model_data) > 0:
                    unique_count = model_data[cat_type].nunique()
                    top_cats = model_data[cat_type].value_counts().head(2)
                    
                    if len(top_cats) >= 1:
                        first_pct = (top_cats.iloc[0] / len(model_data)) * 100
                        first_cat = f"{top_cats.index[0]} ({first_pct:.1f}%)"
                    else:
                        first_cat = "N/A"
                    
                    if len(top_cats) >= 2:
                        second_pct = (top_cats.iloc[1] / len(model_data)) * 100
                        second_cat = f"{top_cats.index[1]} ({second_pct:.1f}%)"
                    else:
                        second_cat = "N/A"
                    
                    f.write(f"| {model} | {unique_count} | {first_cat} | {second_cat} |\n")
            f.write("\n")
        
        # Key insights
        f.write("## Key Insights\n\n")
        
        insights = []
        
        # Find most diverse model
        diversity_scores = {}
        for model in models:
            model_data = df[df['model'] == model]
            if len(model_data) > 0:
                total_categories = (
                    model_data['format_categories'].nunique() +
                    model_data['purpose_categories'].nunique() +
                    model_data['depth_categories'].nunique()
                )
                diversity_scores[model] = total_categories
        
        if diversity_scores:
            most_diverse = max(diversity_scores, key=diversity_scores.get)
            least_diverse = min(diversity_scores, key=diversity_scores.get)
            insights.append(f"**Most diverse model**: {most_diverse} (uses {diversity_scores[most_diverse]} unique categories total)")
            insights.append(f"**Least diverse model**: {least_diverse} (uses {diversity_scores[least_diverse]} unique categories total)")
        
        # Find dominant patterns
        for cat_type, cat_label in zip(category_types, category_labels):
            overall_top = df[cat_type].value_counts().index[0]
            overall_count = df[cat_type].value_counts().iloc[0]
            overall_pct = (overall_count / len(df)) * 100
            insights.append(f"**Most common {cat_label.lower()}**: {overall_top} ({overall_pct:.1f}% of all evaluations)")
        
        for insight in insights:
            f.write(f"- {insight}\n")
        
        f.write("\n")

def main():
    """Main function to run categorical distribution analysis"""
    evaluations_dir = Path('json_evaluations')
    output_dir = Path('analysis_improved')
    
    if not evaluations_dir.exists():
        print(f"Evaluations directory {evaluations_dir} not found!")
        return
    
    print("Loading categorical data...")
    categorical_data = load_categorical_data(evaluations_dir)
    
    if not categorical_data:
        print("No evaluation data found!")
        return
    
    print("Creating analysis dataframe...")
    df = create_category_distribution_dataframe(categorical_data)
    
    print(f"Created dataframe with {len(df)} evaluations")
    print(f"Models: {sorted(df['model'].unique())}")
    
    print("Creating visualizations...")
    create_category_visualizations(df, output_dir)
    
    print("Generating statistics...")
    generate_distribution_statistics(df, output_dir)
    
    print(f"Analysis complete! Results saved to {output_dir}")
    
    # Print summary
    print("\n=== SUMMARY ===")
    for model in ['claude', 'gemini', 'gpt4o-mini', 'llama-api', 'human']:
        with_count = len(df[(df['model'] == model) & (df['explanation_type'] == 'with')])
        without_count = len(df[(df['model'] == model) & (df['explanation_type'] == 'without')])
        if model == 'human':
            print(f"{model}: {without_count} evaluations (no with/without explanation distinction)")
        else:
            print(f"{model}: {with_count} with explanation, {without_count} without explanation")

if __name__ == "__main__":
    main() 
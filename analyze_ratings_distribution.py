#!/usr/bin/env python3
"""
Ratings Distribution Analysis Script

This script analyzes the rating distributions (tone, contextual relevance, clarity, 
toxicity, safety concerns) across all LLMs, treating with/without explanation 
datasets separately.
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
import re
from collections import defaultdict

# Set style for better plots
plt.style.use('default')
sns.set_palette("husl")

def parse_chatgpt_evaluation(evaluation_text: str) -> Dict[str, Any]:
    """Parse ChatGPT evaluation response to extract ratings"""
    result = {
        'tone_rating': None,
        'contextual_relevance_rating': None,
        'clarity_rating': None,
        'toxicity_rating': None,
        'safety_concerns_rating': None
    }
    
    if not evaluation_text:
        return result
    
    # Extract ratings with robust regex patterns
    rating_patterns = {
        'tone_rating': r'Tone:\s*["\']?(\d+)["\']?',
        'contextual_relevance_rating': r'Contextual Relevance:\s*["\']?(\d+)["\']?',
        'clarity_rating': r'Clarity(?: and Simplicity)?:\s*["\']?(\d+)["\']?',
        'toxicity_rating': r'Toxicity:\s*["\']?(\d+)["\']?',
        'safety_concerns_rating': r'Safety Concerns:\s*["\']?(\d+)["\']?'
    }
    
    for rating_type, pattern in rating_patterns.items():
        match = re.search(pattern, evaluation_text, re.IGNORECASE)
        if match:
            try:
                result[rating_type] = int(match.group(1))
            except ValueError:
                pass
    
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
            
            # Parse ratings
            ratings = parse_chatgpt_evaluation(evaluation_text)
            
            # Create result entry
            result = {
                'original_id': item.get('original_id', ''),
                'tone_rating': ratings['tone_rating'],
                'contextual_relevance_rating': ratings['contextual_relevance_rating'],
                'clarity_rating': ratings['clarity_rating'],
                'toxicity_rating': ratings['toxicity_rating'],
                'safety_concerns_rating': ratings['safety_concerns_rating'],
                'source_file': json_file.name
            }
            results.append(result)
        
        return results
    
    except Exception as e:
        print(f"Error loading {json_file}: {e}")
        return []

def load_ratings_data(evaluations_dir: Path) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    """
    Load ratings data, keeping with/without explanation separate.
    Returns: {model: {'with': [...], 'without': [...]}}
    """
    models = ['claude', 'gemini', 'gpt4o-mini', 'llama-api', 'human']
    ratings_data = {}
    
    for model in models:
        ratings_data[model] = {'with': [], 'without': []}
        
        if model == 'human':
            # Human data is in a single file
            human_file = evaluations_dir / 'llm_evaluated_response_human.json'
            if human_file.exists():
                ratings_data[model]['without'] = load_evaluation_data(human_file)
                print(f"Loaded {len(ratings_data[model]['without'])} human evaluations")
        else:
            # Load with explanation data
            with_file = evaluations_dir / f'llm_evaluated_response_{model}_with_explanation.json'
            if with_file.exists():
                ratings_data[model]['with'] = load_evaluation_data(with_file)
                print(f"Loaded {len(ratings_data[model]['with'])} with-explanation evaluations for {model}")
            
            # Load without explanation data
            without_file = evaluations_dir / f'llm_evaluated_response_{model}_without_explanation.json'
            if without_file.exists():
                ratings_data[model]['without'] = load_evaluation_data(without_file)
                print(f"Loaded {len(ratings_data[model]['without'])} without-explanation evaluations for {model}")
    
    return ratings_data

def create_ratings_dataframe(ratings_data: Dict[str, Dict[str, List[Dict[str, Any]]]]) -> pd.DataFrame:
    """
    Create a DataFrame with ratings data.
    """
    rows = []
    
    for model, explanation_data in ratings_data.items():
        for explanation_type, evaluations in explanation_data.items():
            for evaluation in evaluations:
                rows.append({
                    'model': model,
                    'explanation_type': explanation_type,
                    'tone_rating': evaluation['tone_rating'],
                    'contextual_relevance_rating': evaluation['contextual_relevance_rating'],
                    'clarity_rating': evaluation['clarity_rating'],
                    'toxicity_rating': evaluation['toxicity_rating'],
                    'safety_concerns_rating': evaluation['safety_concerns_rating'],
                    'original_id': evaluation['original_id']
                })
    
    return pd.DataFrame(rows)

def create_rating_visualizations(df: pd.DataFrame, output_dir: Path):
    """Create bar charts for rating distributions"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    models = ['claude', 'gemini', 'gpt4o-mini', 'llama-api', 'human']
    rating_metrics = [
        'tone_rating',
        'contextual_relevance_rating', 
        'clarity_rating',
        'toxicity_rating',
        'safety_concerns_rating'
    ]
    
    rating_labels = [
        'Tone Ratings',
        'Contextual Relevance Ratings',
        'Clarity Ratings', 
        'Toxicity Ratings',
        'Safety Concerns Ratings'
    ]
    
    # Create individual plots for each rating metric
    for rating_metric, rating_label in zip(rating_metrics, rating_labels):
        # Filter out None values for this metric
        metric_df = df[df[rating_metric].notna()].copy()
        
        if len(metric_df) == 0:
            print(f"No data found for {rating_metric}, skipping...")
            continue
        
        fig, axes = plt.subplots(2, 5, figsize=(25, 10))
        fig.suptitle(f'{rating_label} Distribution Across Models', fontsize=16, fontweight='bold')
        
        # Top row: with explanation
        # Bottom row: without explanation
        explanation_types = ['with', 'without']
        explanation_labels = ['With Explanation', 'Without Explanation']
        
        for row_idx, (exp_type, exp_label) in enumerate(zip(explanation_types, explanation_labels)):
            for col_idx, model in enumerate(models):
                ax = axes[row_idx, col_idx]
                
                # Filter data for this model and explanation type
                # For human, we only have "without" explanation data
                if model == 'human' and exp_type == 'with':
                    ax.text(0.5, 0.5, 'N/A\n(Human data only\navailable without\nexplanation)', 
                           ha='center', va='center', transform=ax.transAxes, fontsize=10)
                    ax.set_title(f'{model.title()} ({exp_label})')
                    ax.set_xticks(range(1, 6))
                    ax.set_xlabel('Rating (1-5)')
                    ax.set_ylabel('Count')
                    continue
                
                model_data = metric_df[
                    (metric_df['model'] == model) & 
                    (metric_df['explanation_type'] == exp_type)
                ][rating_metric]
                
                if len(model_data) == 0:
                    ax.text(0.5, 0.5, 'No Data', ha='center', va='center', transform=ax.transAxes)
                    ax.set_title(f'{model.title()} ({exp_label})')
                    continue
                
                # Create histogram/bar chart
                ratings_range = range(1, 6)  # Assuming 1-5 scale
                counts = [sum(model_data == rating) for rating in ratings_range]
                total_count = len(model_data)
                percentages = [count/total_count*100 if total_count > 0 else 0 for count in counts]
                
                # Create bars
                bars = ax.bar(ratings_range, counts, alpha=0.7, 
                             color=plt.cm.Set3(col_idx), edgecolor='black', linewidth=0.5)
                
                # Add percentage labels on bars
                for bar, count, pct in zip(bars, counts, percentages):
                    if count > 0:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height + 0.01*max(counts),
                               f'{count}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=9)
                
                # Styling
                ax.set_title(f'{model.title()} ({exp_label})', fontweight='bold')
                ax.set_xlabel('Rating (1-5)')
                ax.set_ylabel('Count')
                ax.set_xticks(ratings_range)
                ax.grid(True, alpha=0.3, axis='y')
                
                # Set consistent y-axis limits across all subplots
                max_count = metric_df.groupby(['model', 'explanation_type'])[rating_metric].apply(
                    lambda x: max([sum(x == rating) for rating in ratings_range]) if len(x) > 0 else 0
                ).max()
                ax.set_ylim(0, max_count * 1.1)
                
                # Add statistics text
                if len(model_data) > 0:
                    mean_rating = model_data.mean()
                    std_rating = model_data.std()
                    ax.text(0.02, 0.98, f'μ={mean_rating:.2f}\nσ={std_rating:.2f}\nn={len(model_data)}', 
                           transform=ax.transAxes, fontsize=8, verticalalignment='top',
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig(output_dir / f'{rating_metric}_distribution.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Generated {rating_metric}_distribution.png")

def generate_ratings_statistics(df: pd.DataFrame, output_dir: Path):
    """Generate detailed statistics for rating distributions"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    models = ['claude', 'gemini', 'gpt4o-mini', 'llama-api', 'human']
    rating_metrics = [
        'tone_rating',
        'contextual_relevance_rating', 
        'clarity_rating',
        'toxicity_rating',
        'safety_concerns_rating'
    ]
    
    rating_labels = [
        'Tone Ratings',
        'Contextual Relevance Ratings',
        'Clarity Ratings', 
        'Toxicity Ratings',
        'Safety Concerns Ratings'
    ]
    
    with open(output_dir / 'ratings_distribution_statistics.md', 'w', encoding='utf-8') as f:
        f.write("# Ratings Distribution Statistics\n\n")
        f.write(f"**Analysis Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Models Analyzed:** {', '.join(models)}\n")
        f.write(f"**Total Evaluations:** {len(df)}\n\n")
        
        # Overall summary
        f.write("## Overall Summary\n\n")
        f.write("| Model | With Explanation | Without Explanation | Total |\n")
        f.write("|-------|------------------|--------------------|---------|\n")
        for model in models:
            with_count = len(df[(df['model'] == model) & (df['explanation_type'] == 'with')])
            without_count = len(df[(df['model'] == model) & (df['explanation_type'] == 'without')])
            total_count = with_count + without_count
            f.write(f"| {model} | {with_count} | {without_count} | {total_count} |\n")
        f.write("\n")
        
        # Detailed analysis for each rating metric
        for rating_metric, rating_label in zip(rating_metrics, rating_labels):
            # Filter out None values for this metric
            metric_df = df[df[rating_metric].notna()].copy()
            
            if len(metric_df) == 0:
                f.write(f"## {rating_label} Analysis\n\n")
                f.write("**No data available for this metric.**\n\n")
                continue
            
            f.write(f"## {rating_label} Analysis\n\n")
            
            # Overall statistics
            f.write(f"### Overall {rating_label} Statistics\n\n")
            overall_stats = metric_df[rating_metric].describe()
            f.write("| Statistic | Value |\n")
            f.write("|-----------|-------|\n")
            f.write(f"| Count | {overall_stats['count']:.0f} |\n")
            f.write(f"| Mean | {overall_stats['mean']:.2f} |\n")
            f.write(f"| Std | {overall_stats['std']:.2f} |\n")
            f.write(f"| Min | {overall_stats['min']:.0f} |\n")
            f.write(f"| 25% | {overall_stats['25%']:.2f} |\n")
            f.write(f"| 50% (Median) | {overall_stats['50%']:.2f} |\n")
            f.write(f"| 75% | {overall_stats['75%']:.2f} |\n")
            f.write(f"| Max | {overall_stats['max']:.0f} |\n")
            f.write("\n")
            
            # Distribution by rating value
            f.write(f"### {rating_label} Distribution\n\n")
            rating_counts = metric_df[rating_metric].value_counts().sort_index()
            total_ratings = len(metric_df)
            f.write("| Rating | Count | Percentage |\n")
            f.write("|--------|-------|------------|\n")
            for rating in range(1, 6):
                count = rating_counts.get(rating, 0)
                percentage = (count / total_ratings) * 100 if total_ratings > 0 else 0
                f.write(f"| {rating} | {count} | {percentage:.1f}% |\n")
            f.write("\n")
            
            # Model and explanation type comparison
            f.write(f"### {rating_label} by Model and Explanation Type\n\n")
            f.write("| Model | Explanation Type | Count | Mean | Std | Median |\n")
            f.write("|-------|-----------------|-------|------|-----|--------|\n")
            
            for model in models:
                for exp_type in ['with', 'without']:
                    model_data = metric_df[
                        (metric_df['model'] == model) & 
                        (metric_df['explanation_type'] == exp_type)
                    ][rating_metric]
                    
                    if len(model_data) > 0:
                        mean_val = model_data.mean()
                        std_val = model_data.std()
                        median_val = model_data.median()
                        count_val = len(model_data)
                        f.write(f"| {model} | {exp_type} | {count_val} | {mean_val:.2f} | {std_val:.2f} | {median_val:.1f} |\n")
                    else:
                        f.write(f"| {model} | {exp_type} | 0 | N/A | N/A | N/A |\n")
            f.write("\n")
            
            # Detailed distribution by model and explanation type
            f.write(f"### {rating_label} Detailed Distribution\n\n")
            f.write("| Model | Explanation | Rating 1 | Rating 2 | Rating 3 | Rating 4 | Rating 5 |\n")
            f.write("|-------|-------------|----------|----------|----------|----------|----------|\n")
            
            for model in models:
                for exp_type in ['with', 'without']:
                    model_data = metric_df[
                        (metric_df['model'] == model) & 
                        (metric_df['explanation_type'] == exp_type)
                    ][rating_metric]
                    
                    row = [model, exp_type]
                    total_model = len(model_data)
                    
                    for rating in range(1, 6):
                        count = sum(model_data == rating)
                        percentage = (count / total_model) * 100 if total_model > 0 else 0
                        row.append(f"{count} ({percentage:.1f}%)")
                    
                    f.write("| " + " | ".join(row) + " |\n")
            f.write("\n")
        
        # Cross-metric comparison
        f.write("## Cross-Metric Comparison\n\n")
        
        # Create correlation matrix
        f.write("### Rating Correlations\n\n")
        available_metrics = [metric for metric in rating_metrics if df[metric].notna().sum() > 0]
        
        if len(available_metrics) > 1:
            corr_matrix = df[available_metrics].corr()
            f.write("| Metric | " + " | ".join([metric.replace('_rating', '').title() for metric in available_metrics]) + " |\n")
            f.write("|--------|" + "|".join(["-" * 8 for _ in available_metrics]) + "|\n")
            
            for i, metric1 in enumerate(available_metrics):
                row = [metric1.replace('_rating', '').title()]
                for j, metric2 in enumerate(available_metrics):
                    corr_val = corr_matrix.loc[metric1, metric2]
                    row.append(f"{corr_val:.3f}")
                f.write("| " + " | ".join(row) + " |\n")
            f.write("\n")
        
        # Model ranking by average ratings
        f.write("### Model Rankings\n\n")
        f.write("**Average ratings by model (across all metrics and explanation types):**\n\n")
        
        for exp_type in ['with', 'without']:
            f.write(f"#### {exp_type.title()} Explanation\n\n")
            model_averages = []
            
            for model in models:
                model_data = df[(df['model'] == model) & (df['explanation_type'] == exp_type)]
                if len(model_data) > 0:
                    # Calculate average across all available rating metrics
                    avg_ratings = []
                    for metric in rating_metrics:
                        metric_data = model_data[metric].dropna()
                        if len(metric_data) > 0:
                            avg_ratings.append(metric_data.mean())
                    
                    if avg_ratings:
                        overall_avg = np.mean(avg_ratings)
                        model_averages.append((model, overall_avg, len(model_data)))
            
            # Sort by average rating
            model_averages.sort(key=lambda x: x[1], reverse=True)
            
            f.write("| Rank | Model | Average Rating | Sample Size |\n")
            f.write("|------|-------|----------------|-------------|\n")
            for rank, (model, avg_rating, sample_size) in enumerate(model_averages, 1):
                f.write(f"| {rank} | {model} | {avg_rating:.2f} | {sample_size} |\n")
            f.write("\n")
        
        # Key insights
        f.write("## Key Insights\n\n")
        
        insights = []
        
        # Find metrics with highest/lowest average ratings
        for rating_metric, rating_label in zip(rating_metrics, rating_labels):
            metric_df = df[df[rating_metric].notna()]
            if len(metric_df) > 0:
                avg_rating = metric_df[rating_metric].mean()
                insights.append(f"**{rating_label}**: Average rating {avg_rating:.2f}/5")
        
        # Find models with most consistent ratings
        model_consistency = {}
        for model in models:
            model_data = df[df['model'] == model]
            if len(model_data) > 0:
                # Calculate coefficient of variation across all metrics
                all_ratings = []
                for metric in rating_metrics:
                    metric_ratings = model_data[metric].dropna()
                    all_ratings.extend(metric_ratings.tolist())
                
                if all_ratings:
                    mean_rating = np.mean(all_ratings)
                    std_rating = np.std(all_ratings)
                    cv = (std_rating / mean_rating) if mean_rating > 0 else float('inf')
                    model_consistency[model] = cv
        
        if model_consistency:
            most_consistent = min(model_consistency, key=model_consistency.get)
            least_consistent = max(model_consistency, key=model_consistency.get)
            insights.append(f"**Most consistent ratings**: {most_consistent} (CV: {model_consistency[most_consistent]:.3f})")
            insights.append(f"**Most variable ratings**: {least_consistent} (CV: {model_consistency[least_consistent]:.3f})")
        
        for insight in insights:
            f.write(f"- {insight}\n")
        
        f.write("\n")

def main():
    """Main function to run ratings distribution analysis"""
    evaluations_dir = Path('json_evaluations')
    output_dir = Path('analysis_improved')
    
    if not evaluations_dir.exists():
        print(f"Evaluations directory {evaluations_dir} not found!")
        return
    
    print("Loading ratings data...")
    ratings_data = load_ratings_data(evaluations_dir)
    
    if not ratings_data:
        print("No ratings data found!")
        return
    
    print("Creating analysis dataframe...")
    df = create_ratings_dataframe(ratings_data)
    
    print(f"Created dataframe with {len(df)} evaluations")
    
    # Display summary
    print("\n=== DATA SUMMARY ===")
    for model in ['claude', 'gemini', 'gpt4o-mini', 'llama-api', 'human']:
        with_count = len(df[(df['model'] == model) & (df['explanation_type'] == 'with')])
        without_count = len(df[(df['model'] == model) & (df['explanation_type'] == 'without')])
        if model == 'human':
            print(f"{model}: {without_count} evaluations (no with/without explanation distinction)")
        else:
            print(f"{model}: {with_count} with explanation, {without_count} without explanation")
    
    print("\nCreating visualizations...")
    create_rating_visualizations(df, output_dir)
    
    print("Generating statistics...")
    generate_ratings_statistics(df, output_dir)
    
    print(f"Ratings analysis complete! Results saved to {output_dir}")

if __name__ == "__main__":
    main() 
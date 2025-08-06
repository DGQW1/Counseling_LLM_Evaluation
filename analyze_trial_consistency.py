#!/usr/bin/env python3
"""
Trial Consistency Analysis Script

This script analyzes the consistency of LLM performance across multiple trials
in the 100_4_Models_5_Times dataset. It compares the first trial with subsequent
trials to assess how consistent each model's performance is.
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple
import re
from collections import defaultdict

# Set style for better plots
plt.style.use('default')
sns.set_palette("husl")

def load_trial_results(results_dir: Path) -> List[Dict[str, Any]]:
    """Load all trial evaluation result files from 100_4_Models_5_Times"""
    trial_dir = results_dir / '100_4_Models_5_Times'
    if not trial_dir.exists():
        print(f"Trial directory {trial_dir} not found!")
        return []
    
    json_files = list(trial_dir.glob('*.json'))
    all_results = []
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Extract model name and trial number from filename
                # Expected format: llm_evaluated_response_{model}_{trial}_trial.json
                filename = json_file.stem
                if filename.startswith('llm_evaluated_response_'):
                    # Remove the prefix
                    model_part = filename.replace('llm_evaluated_response_', '')
                    if '_' in model_part:
                        parts = model_part.split('_')
                        if len(parts) >= 2 and parts[-1] == 'trial':
                            # Handle models with hyphens in names
                            if parts[0] == 'gpt4o' and parts[1] == 'mini':
                                model_name = 'gpt4o-mini'
                                trial_word = parts[2] if len(parts) > 2 else 'first'
                            elif parts[0] == 'llama' and parts[1] == 'api':
                                model_name = 'llama-api'
                                trial_word = parts[2] if len(parts) > 2 else 'first'
                            else:
                                model_name = parts[0]
                                trial_word = parts[1] if len(parts) > 1 else 'first'
                            
                            # Convert trial word to number
                            trial_mapping = {
                                'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5
                            }
                            trial_num = trial_mapping.get(trial_word.lower(), 1)
                        else:
                            model_name = model_part
                            trial_num = 1
                    else:
                        model_name = model_part
                        trial_num = 1
                else:
                    model_name = filename
                    trial_num = 1
                
                for item in data:
                    item['model'] = model_name
                    item['trial'] = trial_num
                    item['source_file'] = json_file.name
                    all_results.append(item)
                    
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
    
    return all_results

def parse_chatgpt_evaluation(evaluation_text: str) -> Dict[str, Any]:
    """Parse ChatGPT evaluation response to extract categories and ratings"""
    result = {
        'format_categories': [],
        'purpose_categories': [],
        'depth_categories': [],
        'tone_rating': None,
        'contextual_relevance_rating': None,
        'clarity_rating': None,
        'toxicity_rating': None,
        'safety_concerns_rating': None
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
    
    # Extract ratings (handle both quoted and unquoted values, with flexible spacing)
    rating_patterns = {
        'tone_rating': r'Tone:\s*["\']?(\d+)["\']?',
        'contextual_relevance_rating': r'Contextual Relevance:\s*["\']?(\d+)["\']?',
        'clarity_rating': r'Clarity and Simplicity:\s*["\']?(\d+)["\']?',
        'toxicity_rating': r'Toxicity:\s*["\']?(\d+)["\']?',
        'safety_concerns_rating': r'Safety Concerns:\s*["\']?(\d+)["\']?'
    }
    
    for rating_type, pattern in rating_patterns.items():
        match = re.search(pattern, evaluation_text, re.IGNORECASE)
        if match:
            try:
                result[rating_type] = int(match.group(1))
            except ValueError:
                result[rating_type] = None
    
    return result

def create_trial_dataframe(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """Create a DataFrame from trial results with parsed evaluations"""
    data = []
    
    for item in results:
        # Parse the evaluation - check both possible locations
        llm_response = item.get('llm_response', '')
        if not llm_response and 'chatgpt_evaluation' in item:
            llm_response = item['chatgpt_evaluation'].get('response', '')
        
        evaluation = parse_chatgpt_evaluation(llm_response)
        
        row = {
            'original_id': item.get('original_id'),
            'model': item.get('model'),
            'trial': item.get('trial'),
            'source_file': item.get('source_file'),
            'original_question': item.get('original_question'),
            'evaluated_question': item.get('evaluated_question'),
            'llm_response': llm_response,
            'format_categories': evaluation['format_categories'],
            'purpose_categories': evaluation['purpose_categories'],
            'depth_categories': evaluation['depth_categories'],
            'tone_rating': evaluation['tone_rating'],
            'contextual_relevance_rating': evaluation['contextual_relevance_rating'],
            'clarity_rating': evaluation['clarity_rating'],
            'toxicity_rating': evaluation['toxicity_rating'],
            'safety_concerns_rating': evaluation['safety_concerns_rating']
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Convert rating columns to numeric
    rating_cols = ['tone_rating', 'contextual_relevance_rating', 'clarity_rating', 
                   'toxicity_rating', 'safety_concerns_rating']
    for col in rating_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def create_trial_consistency_visualizations(df: pd.DataFrame, output_dir: Path):
    """Create visualizations for trial consistency analysis"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Rating columns and labels
    rating_cols = ['tone_rating', 'contextual_relevance_rating', 'clarity_rating', 
                   'toxicity_rating', 'safety_concerns_rating']
    rating_labels = ['Tone', 'Contextual Relevance', 'Clarity', 'Toxicity', 'Safety Concerns']
    
    models = sorted(df['model'].unique())
    trials = sorted(df['trial'].unique())
    
    print(f"Models found: {models}")
    print(f"Trials found: {trials}")
    print(f"Total data points: {len(df)}")
    
    # 1. Trial-by-trial comparison for each model and metric
    for model in models:
        model_data = df[df['model'] == model]
        if len(model_data) == 0:
            continue
            
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()
        
        for i, (col, label) in enumerate(zip(rating_cols, rating_labels)):
            ax = axes[i]
            
            # Create box plot for each trial
            trial_data = []
            trial_labels = []
            
            for trial in trials:
                trial_subset = model_data[model_data['trial'] == trial][col].dropna()
                if len(trial_subset) > 0:
                    trial_data.append(trial_subset.values)
                    trial_labels.append(f'Trial {trial}')
            
            if trial_data:
                # Create boxplot with forced minimum box height for zero IQR cases
                bp = ax.boxplot(trial_data, labels=trial_labels, patch_artist=True,
                               widths=0.6, showmeans=True, meanline=False)
                
                # Color code trials
                colors = plt.cm.Set3(np.linspace(0, 1, len(trial_data)))
                for patch, color in zip(bp['boxes'], colors):
                    patch.set_facecolor(color)
                    patch.set_alpha(0.8)
                    patch.set_linewidth(2)
                
                # Style other elements for better visibility
                for whisker in bp['whiskers']:
                    whisker.set_linewidth(1.5)
                for cap in bp['caps']:
                    cap.set_linewidth(1.5)
                for median in bp['medians']:
                    median.set_linewidth(2)
                    median.set_color('darkred')
                for mean in bp['means']:
                    mean.set_marker('D')
                    mean.set_markerfacecolor('red')
                    mean.set_markeredgecolor('darkred')
                    mean.set_markersize(6)
                
                ax.set_ylabel('Rating (1-5)')
                ax.set_title(f'{label} Ratings by Trial\n{model}')
                ax.grid(True, alpha=0.3)
                
                # Add mean line
                means = [np.mean(data) for data in trial_data]
                ax.plot(range(1, len(means) + 1), means, 'r--', linewidth=2, label='Mean')
                ax.legend()
        
        # Remove empty subplot
        axes[-1].remove()
        
        plt.tight_layout()
        plt.savefig(output_dir / f'trial_consistency_{model.replace("-", "_")}.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    # 2. Overall trial comparison across all models
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    for i, (col, label) in enumerate(zip(rating_cols, rating_labels)):
        ax = axes[i]
        
        # Create violin plot
        trial_data = []
        trial_labels = []
        
        for trial in trials:
            trial_subset = df[df['trial'] == trial][col].dropna()
            if len(trial_subset) > 0:
                trial_data.append(trial_subset.values)
                trial_labels.append(f'Trial {trial}')
        
        if trial_data:
            vp = ax.violinplot(trial_data, positions=range(1, len(trial_data) + 1))
            ax.set_xticks(range(1, len(trial_data) + 1))
            ax.set_xticklabels(trial_labels)
            ax.set_ylabel('Rating (1-5)')
            ax.set_title(f'{label} Distribution by Trial\n(All Models)')
            ax.grid(True, alpha=0.3)
            
            # Add mean points
            means = [np.mean(data) for data in trial_data]
            ax.plot(range(1, len(means) + 1), means, 'ro-', linewidth=2, markersize=8, label='Mean')
            ax.legend()
    
    # Remove empty subplot
    axes[-1].remove()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'trial_consistency_overall.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Model comparison within each trial
    for trial in trials:
        trial_data = df[df['trial'] == trial]
        if len(trial_data) == 0:
            continue
            
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()
        
        for i, (col, label) in enumerate(zip(rating_cols, rating_labels)):
            ax = axes[i]
            
            # Create box plot for each model
            model_data = []
            model_labels = []
            
            for model in models:
                model_subset = trial_data[trial_data['model'] == model][col].dropna()
                if len(model_subset) > 0:
                    model_data.append(model_subset.values)
                    model_labels.append(model)
            
            if model_data:
                # Create boxplot with forced minimum box height for zero IQR cases
                bp = ax.boxplot(model_data, labels=model_labels, patch_artist=True,
                               widths=0.6, showmeans=True, meanline=False)
                
                # Color code models
                colors = plt.cm.Set3(np.linspace(0, 1, len(model_data)))
                for patch, color in zip(bp['boxes'], colors):
                    patch.set_facecolor(color)
                    patch.set_alpha(0.8)
                    patch.set_linewidth(2)
                
                # Style other elements for better visibility
                for whisker in bp['whiskers']:
                    whisker.set_linewidth(1.5)
                for cap in bp['caps']:
                    cap.set_linewidth(1.5)
                for median in bp['medians']:
                    median.set_linewidth(2)
                    median.set_color('darkred')
                for mean in bp['means']:
                    mean.set_marker('D')
                    mean.set_markerfacecolor('red')
                    mean.set_markeredgecolor('darkred')
                    mean.set_markersize(6)
                
                ax.set_ylabel('Rating (1-5)')
                ax.set_title(f'{label} Ratings by Model\nTrial {trial}')
                ax.grid(True, alpha=0.3)
                plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        # Remove empty subplot
        axes[-1].remove()
        
        plt.tight_layout()
        plt.savefig(output_dir / f'model_comparison_trial_{trial}.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    # 4. Heatmap of mean ratings by model and trial
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    for i, (col, label) in enumerate(zip(rating_cols, rating_labels)):
        ax = axes[i]
        
        # Create pivot table for heatmap
        pivot_data = df.pivot_table(
            values=col, 
            index='model', 
            columns='trial', 
            aggfunc='mean'
        )
        
        if not pivot_data.empty:
            sns.heatmap(pivot_data, annot=True, fmt='.2f', cmap='RdYlBu_r', 
                       center=3, ax=ax, cbar_kws={'label': 'Mean Rating'})
            ax.set_title(f'{label} Mean Ratings\nModel vs Trial')
            ax.set_xlabel('Trial Number')
            ax.set_ylabel('Model')
    
    # Remove empty subplot
    axes[-1].remove()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'trial_consistency_heatmaps.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Category consistency analysis
    create_category_consistency_visualizations(df, output_dir)

def create_category_consistency_visualizations(df: pd.DataFrame, output_dir: Path):
    """Create visualizations for category consistency across trials"""
    models = sorted(df['model'].unique())
    trials = sorted(df['trial'].unique())
    
    # Expand categories for analysis
    category_data = []
    for _, row in df.iterrows():
        for cat_type in ['format_categories', 'purpose_categories', 'depth_categories']:
            categories = row[cat_type] if isinstance(row[cat_type], list) else []
            for category in categories:
                category_data.append({
                    'model': row['model'],
                    'trial': row['trial'], 
                    'category_type': cat_type.replace('_categories', ''),
                    'category': category,
                    'original_id': row['original_id']
                })
    
    if not category_data:
        print("No category data found for visualization")
        return
        
    cat_df = pd.DataFrame(category_data)
    
    # 1. Category frequency by trial for each model
    for model in models:
        model_data = cat_df[cat_df['model'] == model]
        if len(model_data) == 0:
            continue
            
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        for idx, cat_type in enumerate(['format', 'purpose', 'depth']):
            ax = axes[idx]
            type_data = model_data[model_data['category_type'] == cat_type]
            
            if len(type_data) > 0:
                # Count categories by trial
                trial_category_counts = {}
                for trial in trials:
                    trial_data = type_data[type_data['trial'] == trial]
                    category_counts = trial_data['category'].value_counts()
                    trial_category_counts[trial] = category_counts
                
                # Get top categories across all trials
                all_categories = type_data['category'].value_counts().head(10).index
                
                # Create stacked bar chart
                bottom = np.zeros(len(trials))
                colors = plt.cm.Set3(np.linspace(0, 1, len(all_categories)))
                
                for i, category in enumerate(all_categories):
                    counts = [trial_category_counts.get(trial, pd.Series()).get(category, 0) for trial in trials]
                    ax.bar(range(len(trials)), counts, bottom=bottom, 
                          label=category, color=colors[i], alpha=0.8)
                    bottom += counts
                
                ax.set_xlabel('Trial')
                ax.set_ylabel('Frequency') 
                ax.set_title(f'{cat_type.title()} Categories by Trial\n{model}')
                ax.set_xticks(range(len(trials)))
                ax.set_xticklabels([f'Trial {t}' for t in trials])
                ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.savefig(output_dir / f'category_consistency_{model.replace("-", "_")}.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    # 2. Overall category distribution consistency across trials
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    for idx, cat_type in enumerate(['format', 'purpose', 'depth']):
        ax = axes[idx]
        type_data = cat_df[cat_df['category_type'] == cat_type]
        
        if len(type_data) > 0:
            # Category counts by trial
            trial_counts = []
            trial_labels = []
            
            for trial in trials:
                trial_data = type_data[type_data['trial'] == trial]
                if len(trial_data) > 0:
                    trial_counts.append(len(trial_data))
                    trial_labels.append(f'Trial {trial}')
            
            if trial_counts:
                ax.bar(trial_labels, trial_counts, alpha=0.7, color=plt.cm.Set2(idx))
                ax.set_ylabel('Total Category Instances')
                ax.set_title(f'{cat_type.title()} Category Usage by Trial\n(All Models)')
                ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'category_usage_by_trial.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_trial_consistency_statistics(df: pd.DataFrame, output_dir: Path):
    """Generate summary statistics for trial consistency analysis"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    rating_cols = ['tone_rating', 'contextual_relevance_rating', 'clarity_rating', 
                   'toxicity_rating', 'safety_concerns_rating']
    rating_labels = ['Tone', 'Contextual Relevance', 'Clarity', 'Toxicity', 'Safety Concerns']
    
    models = sorted(df['model'].unique())
    trials = sorted(df['trial'].unique())
    
    with open(output_dir / 'trial_consistency_statistics.md', 'w', encoding='utf-8') as f:
        f.write("# Trial Consistency Analysis Statistics\n\n")
        f.write(f"**Dataset:** 100_4_Models_5_Times\n")
        f.write(f"**Total Data Points:** {len(df)}\n")
        f.write(f"**Models:** {', '.join(models)}\n")
        f.write(f"**Trials:** {', '.join(map(str, trials))}\n\n")
        
        # 1. Overall statistics by model and trial
        f.write("## 1. Overall Statistics by Model and Trial\n\n")
        
        for model in models:
            f.write(f"### {model}\n\n")
            model_data = df[df['model'] == model]
            
            f.write("| Trial | Count | Tone | Contextual Relevance | Clarity | Toxicity | Safety Concerns |\n")
            f.write("|-------|-------|------|---------------------|---------|----------|-----------------|\n")
            
            for trial in trials:
                trial_data = model_data[model_data['trial'] == trial]
                if len(trial_data) > 0:
                    means = []
                    for col in rating_cols:
                        mean_val = trial_data[col].mean()
                        means.append(f"{mean_val:.2f}" if not pd.isna(mean_val) else "N/A")
                    
                    f.write(f"| {trial} | {len(trial_data)} | {' | '.join(means)} |\n")
            
            f.write("\n")
        
        # 2. Trial consistency analysis
        f.write("## 2. Trial Consistency Analysis\n\n")
        
        for model in models:
            f.write(f"### {model} - Trial Consistency\n\n")
            model_data = df[df['model'] == model]
            
            # Calculate standard deviation across trials for each metric
            f.write("| Metric | Mean Across Trials | Std Dev Across Trials | CV (%) | Consistency Rating |\n")
            f.write("|--------|-------------------|----------------------|--------|-------------------|\n")
            
            for col, label in zip(rating_cols, rating_labels):
                trial_means = []
                for trial in trials:
                    trial_data = model_data[model_data['trial'] == trial][col].dropna()
                    if len(trial_data) > 0:
                        trial_means.append(trial_data.mean())
                
                if len(trial_means) > 1:
                    overall_mean = np.mean(trial_means)
                    std_dev = np.std(trial_means)
                    cv = (std_dev / overall_mean * 100) if overall_mean > 0 else 0
                    
                    # Consistency rating based on CV
                    if cv < 5:
                        consistency = "Excellent"
                    elif cv < 10:
                        consistency = "Good"
                    elif cv < 15:
                        consistency = "Fair"
                    else:
                        consistency = "Poor"
                    
                    f.write(f"| {label} | {overall_mean:.2f} | {std_dev:.2f} | {cv:.1f} | {consistency} |\n")
                else:
                    f.write(f"| {label} | N/A | N/A | N/A | Insufficient Data |\n")
            
            f.write("\n")
        
        # 3. First trial vs subsequent trials comparison
        f.write("## 3. First Trial vs Subsequent Trials Comparison\n\n")
        
        for model in models:
            f.write(f"### {model} - First Trial vs Others\n\n")
            model_data = df[df['model'] == model]
            
            first_trial_data = model_data[model_data['trial'] == trials[0]]
            other_trials_data = model_data[model_data['trial'] != trials[0]]
            
            if len(first_trial_data) > 0 and len(other_trials_data) > 0:
                f.write("| Metric | First Trial Mean | Other Trials Mean | Difference | % Change |\n")
                f.write("|--------|-----------------|-------------------|------------|----------|\n")
                
                for col, label in zip(rating_cols, rating_labels):
                    first_mean = first_trial_data[col].mean()
                    other_mean = other_trials_data[col].mean()
                    
                    if not pd.isna(first_mean) and not pd.isna(other_mean):
                        diff = other_mean - first_mean
                        pct_change = (diff / first_mean * 100) if first_mean > 0 else 0
                        
                        f.write(f"| {label} | {first_mean:.2f} | {other_mean:.2f} | {diff:+.2f} | {pct_change:+.1f}% |\n")
                    else:
                        f.write(f"| {label} | N/A | N/A | N/A | N/A |\n")
            else:
                f.write("Insufficient data for comparison.\n")
            
            f.write("\n")
        
        # 4. Model ranking consistency across trials
        f.write("## 4. Model Ranking Consistency Across Trials\n\n")
        
        for trial in trials:
            f.write(f"### Trial {trial} - Model Rankings\n\n")
            trial_data = df[df['trial'] == trial]
            
            if len(trial_data) > 0:
                f.write("| Rank | Model | Tone | Contextual Relevance | Clarity | Toxicity | Safety Concerns |\n")
                f.write("|------|-------|------|---------------------|---------|----------|-----------------|\n")
                
                # Calculate mean ratings for each model in this trial
                model_means = {}
                for model in models:
                    model_subset = trial_data[trial_data['model'] == model]
                    if len(model_subset) > 0:
                        means = []
                        for col in rating_cols:
                            mean_val = model_subset[col].mean()
                            means.append(mean_val if not pd.isna(mean_val) else 0)
                        model_means[model] = np.mean(means)
                
                # Sort by overall mean rating
                sorted_models = sorted(model_means.items(), key=lambda x: x[1], reverse=True)
                
                for rank, (model, overall_mean) in enumerate(sorted_models, 1):
                    model_subset = trial_data[trial_data['model'] == model]
                    means = []
                    for col in rating_cols:
                        mean_val = model_subset[col].mean()
                        means.append(f"{mean_val:.2f}" if not pd.isna(mean_val) else "N/A")
                    
                    f.write(f"| {rank} | {model} | {' | '.join(means)} |\n")
            
            f.write("\n")
        
        # 5. Key observations and insights
        f.write("## 5. Key Observations and Insights\n\n")
        
        # Calculate overall consistency metrics
        f.write("### Overall Consistency Summary\n\n")
        
        for model in models:
            model_data = df[df['model'] == model]
            if len(model_data) == 0:
                continue
                
            # Calculate average CV across all metrics
            cvs = []
            for col in rating_cols:
                trial_means = []
                for trial in trials:
                    trial_data = model_data[model_data['trial'] == trial][col].dropna()
                    if len(trial_data) > 0:
                        trial_means.append(trial_data.mean())
                
                if len(trial_means) > 1:
                    overall_mean = np.mean(trial_means)
                    std_dev = np.std(trial_means)
                    cv = (std_dev / overall_mean * 100) if overall_mean > 0 else 0
                    cvs.append(cv)
            
            if cvs:
                avg_cv = np.mean(cvs)
                f.write(f"- **{model}**: Average coefficient of variation: {avg_cv:.1f}% ")
                if avg_cv < 5:
                    f.write("(Excellent consistency)\n")
                elif avg_cv < 10:
                    f.write("(Good consistency)\n")
                elif avg_cv < 15:
                    f.write("(Fair consistency)\n")
                else:
                    f.write("(Poor consistency)\n")
        
        f.write("\n### Recommendations\n\n")
        f.write("- Models with CV < 5% show excellent trial consistency\n")
        f.write("- Models with CV > 15% may need additional trials for reliable assessment\n")
        f.write("- Consider the impact of trial order on performance\n")
        f.write("- Evaluate whether first trial performance differs systematically from subsequent trials\n")
        
        # 6. Category consistency analysis
        f.write("\n## 6. Category Consistency Analysis\n\n")
        
        # Expand categories for analysis
        category_data = []
        for _, row in df.iterrows():
            for cat_type in ['format_categories', 'purpose_categories', 'depth_categories']:
                categories = row[cat_type] if isinstance(row[cat_type], list) else []
                for category in categories:
                    category_data.append({
                        'model': row['model'],
                        'trial': row['trial'], 
                        'category_type': cat_type.replace('_categories', ''),
                        'category': category
                    })
        
        if category_data:
            cat_df = pd.DataFrame(category_data)
            
            for model in models:
                f.write(f"### {model} - Category Usage Consistency\n\n")
                model_data = cat_df[cat_df['model'] == model]
                
                if len(model_data) > 0:
                    for cat_type in ['format', 'purpose', 'depth']:
                        type_data = model_data[model_data['category_type'] == cat_type]
                        
                        if len(type_data) > 0:
                            f.write(f"**{cat_type.title()} Categories:**\n\n")
                            
                            # Count categories by trial
                            f.write("| Trial | Top Categories (with counts) |\n")
                            f.write("|-------|------------------------------|\n")
                            
                            for trial in trials:
                                trial_data = type_data[type_data['trial'] == trial]
                                if len(trial_data) > 0:
                                    top_cats = trial_data['category'].value_counts().head(3)
                                    cat_str = ", ".join([f"{cat} ({count})" for cat, count in top_cats.items()])
                                    f.write(f"| {trial} | {cat_str} |\n")
                            f.write("\n")
                else:
                    f.write("No category data available.\n\n")
        else:
            f.write("No category data found for analysis.\n\n")

def main():
    """Main function to run trial consistency analysis"""
    results_dir = Path('results')
    output_dir = Path('analysis/trial_consistency')
    
    if not results_dir.exists():
        print(f"Results directory {results_dir} not found!")
        return
    
    print("Loading trial results...")
    results = load_trial_results(results_dir)
    
    if not results:
        print("No trial results found!")
        return
    
    print(f"Loaded {len(results)} trial results")
    
    print("Creating analysis dataframe...")
    df = create_trial_dataframe(results)
    
    print(f"Created dataframe with {len(df)} rows")
    print(f"Models: {sorted(df['model'].unique())}")
    print(f"Trials: {sorted(df['trial'].unique())}")
    
    print("Creating visualizations...")
    create_trial_consistency_visualizations(df, output_dir)
    
    print("Generating statistics...")
    generate_trial_consistency_statistics(df, output_dir)
    
    print(f"Analysis complete! Results saved to {output_dir}")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Script to analyze ChatGPT evaluation results and generate visualizations and summary statistics.
"""

import json
import re
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
plt.style.use('default')
sns.set_palette("husl")

def load_evaluation_results(results_dir: Path) -> List[Dict[str, Any]]:
    """Load all evaluation result files from both dataset structures"""
    # Look for files in both the root directory and subdirectories
    json_files = list(results_dir.glob('llm_evaluated_response_*.json'))
    json_files.extend(list(results_dir.glob('*/llm_evaluated_response_*.json')))
    
    all_results = []
    for json_file in json_files:
        try:
            # Skip 100_4_Models_5_Times dataset for now
            if '100_4_Models_5_Times' in str(json_file):
                continue
                
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Determine dataset type from file path
                dataset_type = '500_4_Models' if '500_4_Models' in str(json_file) else 'human' if 'human' in str(json_file) else 'legacy'
                
                for item in data:
                    item['source_model'] = extract_model_from_filename(json_file.name, dataset_type)
                    item['has_explanation'] = dataset_type == '500_4_Models' and 'with_explanation' in json_file.name
                    item['dataset_type'] = dataset_type
                    all_results.extend([item])
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
    
    return all_results

def extract_model_from_filename(filename: str, dataset_type: str) -> str:
    """Extract model name from filename based on dataset type"""
    name = filename.replace('llm_evaluated_response_', '').replace('.json', '')
    
    if dataset_type == '500_4_Models':
        # Original format: llm_evaluated_response_{model}_{variant}.json
        if '_with_explanation' in name:
            return name.replace('_with_explanation', '')
        elif '_without_explanation' in name:
            return name.replace('_without_explanation', '')
        return name
    elif dataset_type == '100_4_Models_5_Times':
        # Trial format: llm_evaluated_response_{model}_{trial}.json
        return name  # Keep the full name including trial info
    elif dataset_type == 'human':
        # Human format: llm_evaluated_response_human.json
        return name
    else:
        # Legacy format
        if '_with_explanation' in name:
            return name.replace('_with_explanation', '')
        elif '_without_explanation' in name:
            return name.replace('_without_explanation', '')
        return name

def parse_chatgpt_evaluation(evaluation_text: str) -> Dict[str, Any]:
    """Parse ChatGPT evaluation response to extract structured data"""
    result = {
        'format_categories': [],
        'purpose_categories': [],
        'depth_categories': [],
        'tone_rating': None,
        'contextual_relevance_rating': None,
        'clarity_rating': None,
        'toxicity_rating': None,
        'safety_concerns_rating': None,  # NEW: replaces assumption_rating
        'parse_success': False
    }
    
    if not evaluation_text or 'ERROR' in evaluation_text:
        return result
    
    try:
        # Extract categories (robust to quotes and whitespace)
        format_match = re.search(r'Format:\s*"?([^"\n]+)"?', evaluation_text, re.IGNORECASE)
        if format_match:
            result['format_categories'] = [cat.strip() for cat in format_match.group(1).split(',')]
        
        purpose_match = re.search(r'Purpose:\s*"?([^"\n]+)"?', evaluation_text, re.IGNORECASE)
        if purpose_match:
            result['purpose_categories'] = [cat.strip() for cat in purpose_match.group(1).split(',')]
        
        depth_match = re.search(r'Depth:\s*"?([^"\n]+)"?', evaluation_text, re.IGNORECASE)
        if depth_match:
            result['depth_categories'] = [cat.strip() for cat in depth_match.group(1).split(',')]
        
        # Extract ratings (1-5 scale, robust to quotes)
        tone_match = re.search(r'Tone:\s*"?(\d+)"?', evaluation_text, re.IGNORECASE)
        if tone_match:
            result['tone_rating'] = int(tone_match.group(1))
        
        relevance_match = re.search(r'Contextual Relevance:\s*"?(\d+)"?', evaluation_text, re.IGNORECASE)
        if relevance_match:
            result['contextual_relevance_rating'] = int(relevance_match.group(1))
        
        clarity_match = re.search(r'Clarity and Simplicity:\s*"?(\d+)"?', evaluation_text, re.IGNORECASE)
        if clarity_match:
            result['clarity_rating'] = int(clarity_match.group(1))
        
        toxicity_match = re.search(r'Toxicity:\s*"?(\d+)"?', evaluation_text, re.IGNORECASE)
        if toxicity_match:
            result['toxicity_rating'] = int(toxicity_match.group(1))
        
        # NEW: Safety Concerns (instead of Assumption)
        safety_match = re.search(r'Safety Concerns:\s*"?(\d+)"?', evaluation_text, re.IGNORECASE)
        if safety_match:
            result['safety_concerns_rating'] = int(safety_match.group(1))
        
        # Check if parsing was successful
        result['parse_success'] = any([
            result['format_categories'],
            result['purpose_categories'], 
            result['depth_categories'],
            result['tone_rating'] is not None,
            result['contextual_relevance_rating'] is not None,
            result['clarity_rating'] is not None,
            result['toxicity_rating'] is not None,
            result['safety_concerns_rating'] is not None
        ])
        
    except Exception as e:
        print(f"Error parsing evaluation: {e}")
    
    return result

def create_analysis_dataframe(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """Create a structured dataframe for analysis"""
    
    rows = []
    
    for item in results:
        chatgpt_eval = item.get('chatgpt_evaluation', {})
        if not chatgpt_eval.get('success', False):
            continue
            
        evaluation_text = chatgpt_eval.get('response', '')
        parsed = parse_chatgpt_evaluation(evaluation_text)
        
        if not parsed['parse_success']:
            continue
        
        row = {
            'model': item.get('original_model', item.get('source_model', 'unknown')),
            'has_explanation': item.get('metadata', {}).get('has_explanation', item.get('has_explanation', False)),
            'original_id': item.get('original_id'),
            'evaluated_question': item.get('evaluated_question', ''),
            'tone_rating': parsed['tone_rating'],
            'contextual_relevance_rating': parsed['contextual_relevance_rating'],
            'clarity_rating': parsed['clarity_rating'],
            'toxicity_rating': parsed['toxicity_rating'],
            'safety_concerns_rating': parsed['safety_concerns_rating'],
            'format_categories': ', '.join(parsed['format_categories']),
            'purpose_categories': ', '.join(parsed['purpose_categories']),
            'depth_categories': ', '.join(parsed['depth_categories']),
            'num_format_categories': len(parsed['format_categories']),
            'num_purpose_categories': len(parsed['purpose_categories']),
            'num_depth_categories': len(parsed['depth_categories']),
            'dataset_type': item.get('dataset_type', 'legacy')  # Add dataset_type with fallback
        }
        
        rows.append(row)
    
    df = pd.DataFrame(rows)
    
    # Clean model names (remove any timestamps or artifacts)
    df['model'] = df['model'].str.replace(r'\s+\d+\.\d+\.\d+.*', '', regex=True)
    
    # Convert rating columns to numeric, handling any non-numeric values
    rating_cols = ['tone_rating', 'contextual_relevance_rating', 'clarity_rating', 'toxicity_rating', 'safety_concerns_rating']
    for col in rating_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def create_visualizations(df: pd.DataFrame, output_dir: Path):
    """Create visualization plots"""
    
    # Rating columns
    rating_cols = ['tone_rating', 'contextual_relevance_rating', 'clarity_rating', 'toxicity_rating', 'safety_concerns_rating']
    rating_labels = ['Tone', 'Contextual Relevance', 'Clarity', 'Toxicity', 'Safety Concerns']
    num_metrics = len(rating_cols)
    
    # 1. Distribution of ratings within each model
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    for i, (col, label) in enumerate(zip(rating_cols, rating_labels)):
        ax = axes[i]
        for model in sorted(df['model'].unique()):
            model_data = df[df['model'] == model][col].dropna()
            if len(model_data) > 0:
                # Highlight human data with different color and style
                if 'human' in model.lower():
                    ax.hist(model_data, alpha=0.8, label=f'{model} (n={len(model_data)})', 
                           bins=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5], color='red', edgecolor='black', linewidth=1.5)
                else:
                    ax.hist(model_data, alpha=0.6, label=f'{model} (n={len(model_data)})', 
                           bins=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5])
        
        ax.set_xlabel('Rating (1-5)')
        ax.set_ylabel('Frequency')
        ax.set_title(f'Distribution of {label} Ratings by Model')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # Remove empty subplots if there are any
    for i in range(num_metrics, len(axes)):
        axes[i].remove()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'rating_distributions_by_model.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Box plots comparing models
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    for i, (col, label) in enumerate(zip(rating_cols, rating_labels)):
        ax = axes[i]
        data_to_plot = []
        labels_to_plot = []
        all_points = []
        
        for model in sorted(df['model'].unique()):
            model_data = df[df['model'] == model][col].dropna()
            print(f"Boxplot debug: {model} {label} count={len(model_data)}, unique={model_data.unique()}")
            if len(model_data) >= 2:
                data_to_plot.append(model_data)
                labels_to_plot.append(f'{model}\n(n={len(model_data)})')
                all_points.append(model_data)
            else:
                print(f"Skipping {model} for {label} (not enough data)")
        
        if data_to_plot:
            # Create boxplot with custom colors for human data
            box_colors = ['red' if 'human' in label.lower() else 'lightblue' for label in labels_to_plot]
            bp = ax.boxplot(data_to_plot, labels=labels_to_plot, showmeans=True, patch_artist=True)
            
            # Apply colors to boxes
            for patch, color in zip(bp['boxes'], box_colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            
            # Overlay data points for clarity
            for j, points in enumerate(all_points):
                y = points.values
                x = np.random.normal(j+1, 0.04, size=len(y))  # jitter
                point_color = 'red' if 'human' in labels_to_plot[j].lower() else 'blue'
                ax.plot(x, y, 'o', alpha=0.4, markersize=5, color=point_color)
            ax.set_ylabel('Rating (1-5)')
            ax.set_title(f'{label} Ratings Comparison')
            ax.grid(True, alpha=0.3)
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        else:
            ax.set_visible(False)
    
    # Remove empty subplots if there are any
    for i in range(num_metrics, len(axes)):
        axes[i].remove()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'rating_comparisons_boxplot.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Heatmap of average ratings by model
    rating_means = df.groupby('model')[rating_cols].mean()
    
    # Ensure all values are numeric and handle any remaining NaN values
    rating_means = rating_means.astype(float)
    
    # Sort models to put human first if present
    model_order = sorted(rating_means.index, key=lambda x: (0 if 'human' in x.lower() else 1, x))
    rating_means = rating_means.reindex(model_order)
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(rating_means.T, annot=True, cmap='RdYlBu_r', center=3, 
                vmin=1, vmax=5, fmt='.2f', cbar_kws={'label': 'Average Rating'})
    plt.title('Average Ratings by Model and Metric')
    plt.ylabel('Evaluation Metrics')
    plt.xlabel('Models')
    plt.tight_layout()
    plt.savefig(output_dir / 'rating_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Category distribution analysis - Overall
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Format categories
    format_counts = df['format_categories'].value_counts().head(10)
    axes[0].barh(range(len(format_counts)), format_counts.values)
    axes[0].set_yticks(range(len(format_counts)))
    axes[0].set_yticklabels(format_counts.index, fontsize=8)
    axes[0].set_xlabel('Frequency')
    axes[0].set_title('Top Format Categories (Overall)')
    
    # Purpose categories
    purpose_counts = df['purpose_categories'].value_counts().head(10)
    axes[1].barh(range(len(purpose_counts)), purpose_counts.values)
    axes[1].set_yticks(range(len(purpose_counts)))
    axes[1].set_yticklabels(purpose_counts.index, fontsize=8)
    axes[1].set_xlabel('Frequency')
    axes[1].set_title('Top Purpose Categories (Overall)')
    
    # Depth categories
    depth_counts = df['depth_categories'].value_counts().head(10)
    axes[2].barh(range(len(depth_counts)), depth_counts.values)
    axes[2].set_yticks(range(len(depth_counts)))
    axes[2].set_yticklabels(depth_counts.index, fontsize=8)
    axes[2].set_xlabel('Frequency')
    axes[2].set_title('Top Depth Categories (Overall)')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'category_distributions_overall.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Category distribution by model (Only Without Explanation)
    # Filter to only include without explanation data for category distribution by model
    df_no_explanation = df[~df['has_explanation']]
    
    models = sorted(df_no_explanation['model'].unique())
    fig, axes = plt.subplots(3, len(models), figsize=(6*len(models), 15))
    
    if len(models) == 1:
        axes = axes.reshape(-1, 1)
    
    category_types = ['format_categories', 'purpose_categories', 'depth_categories']
    category_labels = ['Format Categories', 'Purpose Categories', 'Depth Categories']
    
    for row, (cat_type, cat_label) in enumerate(zip(category_types, category_labels)):
        for col, model in enumerate(models):
            ax = axes[row, col]
            model_data = df_no_explanation[df_no_explanation['model'] == model]
            
            if len(model_data) > 0:
                cat_counts = model_data[cat_type].value_counts().head(8)
                if len(cat_counts) > 0:
                    bars = ax.barh(range(len(cat_counts)), cat_counts.values)
                    ax.set_yticks(range(len(cat_counts)))
                    ax.set_yticklabels(cat_counts.index, fontsize=7)
                    ax.set_xlabel('Frequency')
                    ax.set_title(f'{cat_label}\n{model} (n={len(model_data)})', fontsize=10)
                    
                    # Add value labels on bars
                    for i, bar in enumerate(bars):
                        width = bar.get_width()
                        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                               f'{int(width)}', ha='left', va='center', fontsize=8)
                else:
                    ax.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax.transAxes)
                    ax.set_title(f'{cat_label}\n{model} (n=0)', fontsize=10)
            else:
                ax.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax.transAxes)
                ax.set_title(f'{cat_label}\n{model} (n=0)', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'category_distributions_by_model.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 6. Explanation vs No Explanation comparison - Overall
    if df['has_explanation'].nunique() > 1:
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()
        
        for i, (col, label) in enumerate(zip(rating_cols, rating_labels)):
            ax = axes[i]
            
            with_exp = df[df['has_explanation']][col].dropna()
            without_exp = df[~df['has_explanation']][col].dropna()
            
            if len(with_exp) > 0 and len(without_exp) > 0:
                ax.hist([with_exp, without_exp], alpha=0.6, 
                       label=[f'With Explanation (n={len(with_exp)})', 
                             f'Without Explanation (n={len(without_exp)})'],
                       bins=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5])
                ax.set_xlabel('Rating (1-5)')
                ax.set_ylabel('Frequency')
                ax.set_title(f'{label} Ratings: With vs Without Explanation (Overall)')
                ax.legend()
                ax.grid(True, alpha=0.3)
        
        # Remove empty subplots if there are any
        for i in range(num_metrics, len(axes)):
            axes[i].remove()
        
        plt.tight_layout()
        plt.savefig(output_dir / 'explanation_comparison_overall.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 7. Model-specific explanation comparison
        models = sorted(df['model'].unique())
        
        # Create a grid for each model's with/without explanation comparison
        for metric_idx, (col, label) in enumerate(zip(rating_cols, rating_labels)):
            fig, axes = plt.subplots(1, len(models), figsize=(5*len(models), 5))
            if len(models) == 1:
                axes = [axes]
            
            for model_idx, model in enumerate(models):
                ax = axes[model_idx]
                
                model_with_exp = df[(df['model'] == model) & (df['has_explanation'])][col].dropna()
                model_without_exp = df[(df['model'] == model) & (~df['has_explanation'])][col].dropna()
                
                if len(model_with_exp) > 0 and len(model_without_exp) > 0:
                    ax.hist([model_with_exp, model_without_exp], alpha=0.6,
                           label=[f'With Explanation (n={len(model_with_exp)})',
                                 f'Without Explanation (n={len(model_without_exp)})'],
                           bins=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5])
                    ax.set_xlabel('Rating (1-5)')
                    ax.set_ylabel('Frequency')
                    ax.set_title(f'{label} Ratings\n{model}')
                    ax.legend(fontsize=8)
                    ax.grid(True, alpha=0.3)
                    
                    # Add mean lines
                    mean_with = model_with_exp.mean()
                    mean_without = model_without_exp.mean()
                    ax.axvline(mean_with, color='C0', linestyle='--', alpha=0.8, 
                              label=f'Mean w/ exp: {mean_with:.2f}')
                    ax.axvline(mean_without, color='C1', linestyle='--', alpha=0.8,
                              label=f'Mean w/o exp: {mean_without:.2f}')
                elif len(model_with_exp) > 0:
                    ax.hist(model_with_exp, alpha=0.6, label=f'With Explanation only (n={len(model_with_exp)})', bins=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5])
                    ax.set_title(f'{label} Ratings\n{model}\n(No without-explanation data)')
                elif len(model_without_exp) > 0:
                    ax.hist(model_without_exp, alpha=0.6, label=f'Without Explanation only (n={len(model_without_exp)})', bins=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5])
                    ax.set_title(f'{label} Ratings\n{model}\n(No with-explanation data)')
                else:
                    ax.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax.transAxes)
                    ax.set_title(f'{label} Ratings\n{model}\n(No data)')
            
            plt.tight_layout()
            plt.savefig(output_dir / f'explanation_comparison_{col}_by_model.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # 8. Cross-comparison heatmap: Model × Explanation interaction
        pivot_data = df.groupby(['model', 'has_explanation'])[rating_cols].mean()
        
        for col, label in zip(rating_cols, rating_labels):
            fig, ax = plt.subplots(1, 1, figsize=(8, 6))
            
            # Create a matrix for heatmap
            heatmap_data = pivot_data[col].unstack(fill_value=np.nan)
            
            # Create custom labels
            if True in heatmap_data.columns and False in heatmap_data.columns:
                heatmap_data.columns = ['Without Explanation', 'With Explanation']
            
            sns.heatmap(heatmap_data, annot=True, cmap='RdYlBu_r', center=3,
                       vmin=1, vmax=5, fmt='.2f', cbar_kws={'label': 'Average Rating'})
            plt.title(f'{label} Ratings: Model × Explanation Interaction')
            plt.ylabel('Models')
            plt.xlabel('Explanation Type')
            plt.tight_layout()
            plt.savefig(output_dir / f'interaction_heatmap_{col}.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # 9. Category distribution: With vs Without Explanation by Model
        category_types = ['format_categories', 'purpose_categories', 'depth_categories']
        category_labels = ['Format Categories', 'Purpose Categories', 'Depth Categories']
        
        for cat_idx, (cat_type, cat_label) in enumerate(zip(category_types, category_labels)):
            fig, axes = plt.subplots(len(models), 2, figsize=(12, 4*len(models)))
            if len(models) == 1:
                axes = axes.reshape(1, -1)
            
            for model_idx, model in enumerate(models):
                # With explanation
                ax_with = axes[model_idx, 0]
                model_with_data = df[(df['model'] == model) & (df['has_explanation'])]
                if len(model_with_data) > 0:
                    cat_counts = model_with_data[cat_type].value_counts().head(6)
                    if len(cat_counts) > 0:
                        bars = ax_with.barh(range(len(cat_counts)), cat_counts.values)
                        ax_with.set_yticks(range(len(cat_counts)))
                        ax_with.set_yticklabels(cat_counts.index, fontsize=8)
                        ax_with.set_xlabel('Frequency')
                        ax_with.set_title(f'{model} - With Explanation\n(n={len(model_with_data)})')
                        
                        # Add value labels
                        for i, bar in enumerate(bars):
                            width = bar.get_width()
                            ax_with.text(width + 0.1, bar.get_y() + bar.get_height()/2,
                                       f'{int(width)}', ha='left', va='center', fontsize=8)
                else:
                    ax_with.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax_with.transAxes)
                    ax_with.set_title(f'{model} - With Explanation\n(n=0)')
                
                # Without explanation
                ax_without = axes[model_idx, 1]
                model_without_data = df[(df['model'] == model) & (~df['has_explanation'])]
                if len(model_without_data) > 0:
                    cat_counts = model_without_data[cat_type].value_counts().head(6)
                    if len(cat_counts) > 0:
                        bars = ax_without.barh(range(len(cat_counts)), cat_counts.values)
                        ax_without.set_yticks(range(len(cat_counts)))
                        ax_without.set_yticklabels(cat_counts.index, fontsize=8)
                        ax_without.set_xlabel('Frequency')
                        ax_without.set_title(f'{model} - Without Explanation\n(n={len(model_without_data)})')
                        
                        # Add value labels
                        for i, bar in enumerate(bars):
                            width = bar.get_width()
                            ax_without.text(width + 0.1, bar.get_y() + bar.get_height()/2,
                                          f'{int(width)}', ha='left', va='center', fontsize=8)
                else:
                    ax_without.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax_without.transAxes)
                    ax_without.set_title(f'{model} - Without Explanation\n(n=0)')
            
            plt.suptitle(f'{cat_label}: With vs Without Explanation by Model', fontsize=14)
            plt.tight_layout()
            plt.savefig(output_dir / f'category_explanation_comparison_{cat_type}.png', dpi=300, bbox_inches='tight')
            plt.close()

def generate_summary_statistics(df: pd.DataFrame, output_dir: Path):
    """Generate summary statistics markdown file"""
    
    rating_cols = ['tone_rating', 'contextual_relevance_rating', 'clarity_rating', 'toxicity_rating', 'safety_concerns_rating']
    rating_labels = ['Tone', 'Contextual Relevance', 'Clarity', 'Toxicity', 'Safety Concerns']
    
    content = f"""# Evaluation Analysis Summary

## Overview

**Total Successful Evaluations:** {len(df)}  
**Models Analyzed:** {', '.join(sorted(df['model'].unique()))}  
**With Explanations:** {len(df[df['has_explanation']])}  
**Without Explanations:** {len(df[~df['has_explanation']])}

### Dataset Breakdown
"""
    
    # Add dataset breakdown (handle missing dataset_type field)
    if 'dataset_type' in df.columns:
        dataset_counts = df['dataset_type'].value_counts()
        for dataset, count in dataset_counts.items():
            content += f"- **{dataset}:** {count} evaluations\n"
    else:
        # Fallback for older data without dataset_type
        content += "- **Legacy Data:** All evaluations\n"
    
    # Highlight human data if present
    human_data = df[df['model'].str.contains('human', case=False, na=False)]
    if len(human_data) > 0:
        content += f"\n**Human-Generated Questions:** {len(human_data)} evaluations\n"
    
    content += """

## Rating Statistics

### Overall Statistics
"""
    
    # Overall rating statistics
    overall_stats = df[rating_cols].describe()
    content += "\n| Metric | Mean | Std | Min | 25% | 50% | 75% | Max |\n"
    content += "|--------|------|-----|-----|-----|-----|-----|-----|\n"
    
    for i, (col, label) in enumerate(zip(rating_cols, rating_labels)):
        stats = overall_stats[col]
        content += f"| {label} | {stats['mean']:.2f} | {stats['std']:.2f} | {stats['min']:.0f} | {stats['25%']:.2f} | {stats['50%']:.2f} | {stats['75%']:.2f} | {stats['max']:.0f} |\n"
    
    # Model comparison
    content += "\n### Model Comparison\n"
    model_stats = df.groupby('model')[rating_cols].agg(['mean', 'std', 'count'])
    
    # Sort models to put human first if present
    models_sorted = sorted(df['model'].unique(), key=lambda x: (0 if 'human' in x.lower() else 1, x))
    
    for col, label in zip(rating_cols, rating_labels):
        content += f"\n#### {label}\n"
        content += "| Model | Mean | Std | Count |\n"
        content += "|-------|------|-----|-------|\n"
        
        for model in models_sorted:
            if model in model_stats.index:
                mean_val = model_stats.loc[model, (col, 'mean')]
                std_val = model_stats.loc[model, (col, 'std')]
                count_val = model_stats.loc[model, (col, 'count')]
                # Highlight human data with bold formatting
                if 'human' in model.lower():
                    content += f"| **{model}** | **{mean_val:.2f}** | **{std_val:.2f}** | **{count_val}** |\n"
                else:
                    content += f"| {model} | {mean_val:.2f} | {std_val:.2f} | {count_val} |\n"
    
    # Category analysis - Overall
    content += "\n## Category Analysis\n"
    
    content += f"\n### Overall Category Distribution\n"
    
    content += f"\n#### Format Categories (Top 10)\n"
    format_counts = df['format_categories'].value_counts().head(10)
    content += "| Category | Count | Percentage |\n"
    content += "|----------|-------|------------|\n"
    for cat, count in format_counts.items():
        pct = (count / len(df)) * 100
        content += f"| {cat} | {count} | {pct:.1f}% |\n"
    
    content += f"\n#### Purpose Categories (Top 10)\n"
    purpose_counts = df['purpose_categories'].value_counts().head(10)
    content += "| Category | Count | Percentage |\n"
    content += "|----------|-------|------------|\n"
    for cat, count in purpose_counts.items():
        pct = (count / len(df)) * 100
        content += f"| {cat} | {count} | {pct:.1f}% |\n"
    
    content += f"\n#### Depth Categories (Top 10)\n"
    depth_counts = df['depth_categories'].value_counts().head(10)
    content += "| Category | Count | Percentage |\n"
    content += "|----------|-------|------------|\n"
    for cat, count in depth_counts.items():
        pct = (count / len(df)) * 100
        content += f"| {cat} | {count} | {pct:.1f}% |\n"
    
    # Human vs LLM comparison (if human data is present)
    human_data = df[df['model'].str.contains('human', case=False, na=False)]
    llm_data = df[~df['model'].str.contains('human', case=False, na=False)]
    
    if len(human_data) > 0 and len(llm_data) > 0:
        content += "\n## Human vs LLM Performance Comparison\n"
        
        # Compare average ratings
        human_means = human_data[rating_cols].mean()
        llm_means = llm_data[rating_cols].mean()
        
        content += "\n### Average Rating Comparison\n"
        content += "| Metric | Human | LLMs | Difference (Human - LLM) |\n"
        content += "|--------|-------|------|------------------------|\n"
        
        for col, label in zip(rating_cols, rating_labels):
            human_val = human_means[col]
            llm_val = llm_means[col]
            diff = human_val - llm_val
            content += f"| {label} | {human_val:.2f} | {llm_val:.2f} | {diff:+.2f} |\n"
        
        # Compare category distributions
        content += "\n### Category Distribution Comparison\n"
        for cat_type, cat_label in zip(['format_categories', 'purpose_categories', 'depth_categories'], 
                                      ['Format', 'Purpose', 'Depth']):
            human_cats = human_data[cat_type].value_counts().head(5)
            llm_cats = llm_data[cat_type].value_counts().head(5)
            
            content += f"\n#### {cat_label} Categories\n"
            content += "| Category | Human % | LLM % | Difference |\n"
            content += "|----------|---------|-------|-----------|\n"
            
            all_cats = set(human_cats.index) | set(llm_cats.index)
            for cat in sorted(all_cats):
                human_pct = (human_cats.get(cat, 0) / len(human_data)) * 100
                llm_pct = (llm_cats.get(cat, 0) / len(llm_data)) * 100
                diff = human_pct - llm_pct
                content += f"| {cat} | {human_pct:.1f}% | {llm_pct:.1f}% | {diff:+.1f}% |\n"
    
    # Model-specific category analysis
    content += f"\n### Category Analysis by Model\n"
    
    models = sorted(df['model'].unique(), key=lambda x: (0 if 'human' in x.lower() else 1, x))
    category_types = ['format_categories', 'purpose_categories', 'depth_categories']
    category_labels = ['Format Categories', 'Purpose Categories', 'Depth Categories']
    
    for cat_type, cat_label in zip(category_types, category_labels):
        content += f"\n#### {cat_label} by Model\n"
        content += "| Model | Top Category | Count | % of Model | Second Category | Count | % of Model |\n"
        content += "|-------|--------------|-------|------------|-----------------|-------|------------|\n"
        
        for model in models:
            model_data = df[df['model'] == model]
            if len(model_data) > 0:
                cat_counts = model_data[cat_type].value_counts().head(2)
                if len(cat_counts) >= 2:
                    top_cat = cat_counts.index[0]
                    top_count = cat_counts.iloc[0]
                    top_pct = (top_count / len(model_data)) * 100
                    
                    second_cat = cat_counts.index[1]
                    second_count = cat_counts.iloc[1]
                    second_pct = (second_count / len(model_data)) * 100
                    
                    content += f"| {model} | {top_cat} | {top_count} | {top_pct:.1f}% | {second_cat} | {second_count} | {second_pct:.1f}% |\n"
                elif len(cat_counts) == 1:
                    top_cat = cat_counts.index[0]
                    top_count = cat_counts.iloc[0]
                    top_pct = (top_count / len(model_data)) * 100
                    content += f"| {model} | {top_cat} | {top_count} | {top_pct:.1f}% | - | - | - |\n"
                else:
                    content += f"| {model} | No data | - | - | - | - | - |\n"
            else:
                content += f"| {model} | No data | - | - | - | - | - |\n"
    
    # Key insights
    content += "\n## Key Insights\n\n"
    
    # Find best and worst performing models
    model_means = df.groupby('model')[rating_cols].mean().mean(axis=1)
    best_model = model_means.idxmax()
    worst_model = model_means.idxmin()
    
    content += f"### Performance Highlights\n"
    content += f"- **Highest Average Rating:** {best_model} ({model_means[best_model]:.2f})\n"
    content += f"- **Lowest Average Rating:** {worst_model} ({model_means[worst_model]:.2f})\n"
    
    # Toxicity analysis
    high_toxicity = df[df['toxicity_rating'] >= 4]
    if len(high_toxicity) > 0:
        content += f"- **High Toxicity Ratings (≥4):** {len(high_toxicity)} evaluations ({len(high_toxicity)/len(df)*100:.1f}%)\n"
    
    # Quality indicators
    high_quality = df[(df['tone_rating'] >= 4) & (df['contextual_relevance_rating'] >= 4) & (df['clarity_rating'] >= 4)]
    content += f"- **High Quality Questions (Tone, Relevance, Clarity ≥4):** {len(high_quality)} ({len(high_quality)/len(df)*100:.1f}%)\n"
    
    # Explanation impact - Overall and per model
    if df['has_explanation'].nunique() > 1:
        with_exp_mean = df[df['has_explanation']][rating_cols].mean().mean()
        without_exp_mean = df[~df['has_explanation']][rating_cols].mean().mean()
        content += f"- **Average Rating with Explanations:** {with_exp_mean:.2f}\n"
        content += f"- **Average Rating without Explanations:** {without_exp_mean:.2f}\n"
        
        if with_exp_mean > without_exp_mean:
            content += f"  - Questions with explanations scored {with_exp_mean - without_exp_mean:.2f} points higher on average\n"
        else:
            content += f"  - Questions without explanations scored {without_exp_mean - with_exp_mean:.2f} points higher on average\n"
        
        # Model-specific explanation impact
        content += "\n### Model-Specific Explanation Impact\n\n"
        content += "| Model | With Explanation | Without Explanation | Difference |\n"
        content += "|-------|------------------|---------------------|------------|\n"
        
        for model in sorted(df['model'].unique()):
            model_with = df[(df['model'] == model) & (df['has_explanation'])]
            model_without = df[(df['model'] == model) & (~df['has_explanation'])]
            
            if len(model_with) > 0 and len(model_without) > 0:
                with_mean = model_with[rating_cols].mean().mean()
                without_mean = model_without[rating_cols].mean().mean()
                diff = with_mean - without_mean
                content += f"| {model} | {with_mean:.2f} (n={len(model_with)}) | {without_mean:.2f} (n={len(model_without)}) | {diff:+.2f} |\n"
            elif len(model_with) > 0:
                with_mean = model_with[rating_cols].mean().mean()
                content += f"| {model} | {with_mean:.2f} (n={len(model_with)}) | No data | N/A |\n"
            elif len(model_without) > 0:
                without_mean = model_without[rating_cols].mean().mean()
                content += f"| {model} | No data | {without_mean:.2f} (n={len(model_without)}) | N/A |\n"
        
        # Detailed metric breakdown
        content += "\n### Explanation Impact by Rating Metric\n\n"
        for col, label in zip(rating_cols, rating_labels):
            content += f"#### {label}\n"
            content += "| Model | With Explanation | Without Explanation | Difference |\n"
            content += "|-------|------------------|---------------------|------------|\n"
            
            for model in sorted(df['model'].unique()):
                model_with = df[(df['model'] == model) & (df['has_explanation'])][col].dropna()
                model_without = df[(df['model'] == model) & (~df['has_explanation'])][col].dropna()
                
                if len(model_with) > 0 and len(model_without) > 0:
                    with_mean = model_with.mean()
                    without_mean = model_without.mean()
                    diff = with_mean - without_mean
                    content += f"| {model} | {with_mean:.2f} | {without_mean:.2f} | {diff:+.2f} |\n"
                elif len(model_with) > 0:
                    with_mean = model_with.mean()
                    content += f"| {model} | {with_mean:.2f} | No data | N/A |\n"
                elif len(model_without) > 0:
                    without_mean = model_without.mean()
                    content += f"| {model} | No data | {without_mean:.2f} | N/A |\n"
            content += "\n"
        
        # Category distribution comparison: With vs Without Explanation
        content += "\n### Category Distribution: With vs Without Explanation\n\n"
        
        category_types = ['format_categories', 'purpose_categories', 'depth_categories']
        category_labels = ['Format Categories', 'Purpose Categories', 'Depth Categories']
        
        for cat_type, cat_label in zip(category_types, category_labels):
            content += f"\n#### {cat_label}\n"
            
            # Overall comparison
            with_exp_data = df[df['has_explanation']]
            without_exp_data = df[~df['has_explanation']]
            
            content += f"\n**Overall Comparison (Top 5 categories)**\n\n"
            content += "| Category | With Explanation | % | Without Explanation | % |\n"
            content += "|----------|------------------|---|---------------------|---|\n"
            
            # Get top categories from both groups
            with_counts = with_exp_data[cat_type].value_counts().head(5)
            without_counts = without_exp_data[cat_type].value_counts().head(5)
            
            # Get union of top categories from both groups
            all_top_cats = list(set(with_counts.index.tolist() + without_counts.index.tolist()))[:8]
            
            for cat in all_top_cats:
                with_count = with_counts.get(cat, 0)
                without_count = without_counts.get(cat, 0)
                with_pct = (with_count / len(with_exp_data)) * 100 if len(with_exp_data) > 0 else 0
                without_pct = (without_count / len(without_exp_data)) * 100 if len(without_exp_data) > 0 else 0
                
                content += f"| {cat} | {with_count} | {with_pct:.1f}% | {without_count} | {without_pct:.1f}% |\n"
            
            # Model-specific comparison
            content += f"\n**By Model Comparison**\n\n"
            content += "| Model | With Explanation Top Category | % | Without Explanation Top Category | % |\n"
            content += "|-------|-------------------------------|---|-----------------------------------|---|\n"
            
            for model in sorted(df['model'].unique()):
                model_with = df[(df['model'] == model) & (df['has_explanation'])]
                model_without = df[(df['model'] == model) & (~df['has_explanation'])]
                
                # Top category with explanation
                if len(model_with) > 0:
                    with_top = model_with[cat_type].value_counts()
                    if len(with_top) > 0:
                        with_top_cat = with_top.index[0]
                        with_top_count = with_top.iloc[0]
                        with_top_pct = (with_top_count / len(model_with)) * 100
                        with_str = f"{with_top_cat} ({with_top_count})"
                        with_pct_str = f"{with_top_pct:.1f}%"
                    else:
                        with_str = "No data"
                        with_pct_str = "-"
                else:
                    with_str = "No data"
                    with_pct_str = "-"
                
                # Top category without explanation
                if len(model_without) > 0:
                    without_top = model_without[cat_type].value_counts()
                    if len(without_top) > 0:
                        without_top_cat = without_top.index[0]
                        without_top_count = without_top.iloc[0]
                        without_top_pct = (without_top_count / len(model_without)) * 100
                        without_str = f"{without_top_cat} ({without_top_count})"
                        without_pct_str = f"{without_top_pct:.1f}%"
                    else:
                        without_str = "No data"
                        without_pct_str = "-"
                else:
                    without_str = "No data"
                    without_pct_str = "-"
                
                content += f"| {model} | {with_str} | {with_pct_str} | {without_str} | {without_pct_str} |\n"
    
    content += "\n## Generated Visualizations\n\n"
    content += "### Core Analysis\n"
    content += "- `rating_distributions_by_model.png` - Distribution histograms for each rating metric by model\n"
    content += "- `rating_comparisons_boxplot.png` - Box plot comparisons across models\n"
    content += "- `rating_heatmap.png` - Heatmap of average ratings by model\n"
    content += "- `category_distributions_overall.png` - Most common category classifications across all models\n"
    content += "- `category_distributions_by_model.png` - Category distributions broken down by individual model\n"
    
    if df['has_explanation'].nunique() > 1:
        content += "\n### Cross-Comparison Analysis (With vs Without Explanations)\n"
        content += "- `explanation_comparison_overall.png` - Overall comparison of ratings with and without explanations\n"
        
        # List model-specific comparison files
        for col, label in zip(rating_cols, rating_labels):
            content += f"- `explanation_comparison_{col}_by_model.png` - {label} ratings comparison by model\n"
        
        content += "\n### Interaction Heatmaps (Model × Explanation)\n"
        for col, label in zip(rating_cols, rating_labels):
            content += f"- `interaction_heatmap_{col}.png` - {label} ratings heatmap showing model-explanation interactions\n"
        
        content += "\n### Category Analysis: With vs Without Explanations\n"
        content += "- `category_explanation_comparison_format_categories.png` - Format category preferences by model and explanation type\n"
        content += "- `category_explanation_comparison_purpose_categories.png` - Purpose category preferences by model and explanation type\n"
        content += "- `category_explanation_comparison_depth_categories.png` - Depth category preferences by model and explanation type\n"
    
    # Save summary
    with open(output_dir / 'summary_statistics.md', 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    parser = argparse.ArgumentParser(description='Analyze ChatGPT evaluation results')
    parser.add_argument('--results-dir', default='results', help='Directory containing evaluation results')
    parser.add_argument('--output-dir', default='analysis', help='Directory to save analysis results')
    
    args = parser.parse_args()
    
    results_dir = Path(args.results_dir)
    output_dir = Path(args.output_dir)
    
    if not results_dir.exists():
        print(f"Results directory {results_dir} does not exist")
        return
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    print("Loading evaluation results...")
    results = load_evaluation_results(results_dir)
    
    if not results:
        print("No evaluation results found")
        return
    
    print(f"Loaded {len(results)} evaluation results")
    
    print("Creating analysis dataframe...")
    df = create_analysis_dataframe(results)
    
    if df.empty:
        print("No successfully parsed evaluations found")
        return
    
    print(f"Successfully parsed {len(df)} evaluations")
    
    # Debug info about data types and missing values
    rating_cols = ['tone_rating', 'contextual_relevance_rating', 'clarity_rating', 'toxicity_rating', 'safety_concerns_rating']
    print(f"Data types: {df[rating_cols].dtypes.to_dict()}")
    print(f"Missing values: {df[rating_cols].isnull().sum().to_dict()}")
    print(f"Models found: {sorted(df['model'].unique())}")
    
    print("Generating visualizations...")
    create_visualizations(df, output_dir)
    
    print("Generating summary statistics...")
    generate_summary_statistics(df, output_dir)
    
    print(f"Analysis complete! Results saved to {output_dir}")
    print(f"- Visualizations: {len(list(output_dir.glob('*.png')))} PNG files")
    print(f"- Summary: summary_statistics.md")

if __name__ == "__main__":
    main() 
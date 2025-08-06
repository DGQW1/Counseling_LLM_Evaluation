# Evaluation Analysis Summary

## Overview

**Total Successful Evaluations:** 4473  
**Models Analyzed:** claude, gemini, gpt4o-mini, human, llama-api  
**With Explanations:** 1975  
**Without Explanations:** 2498

### Dataset Breakdown
- **legacy:** 3973 evaluations
- **human:** 500 evaluations

**Human-Generated Questions:** 500 evaluations


## Rating Statistics

### Overall Statistics

| Metric | Mean | Std | Min | 25% | 50% | 75% | Max |
|--------|------|-----|-----|-----|-----|-----|-----|
| Tone | 4.65 | 0.58 | 1 | 4.00 | 5.00 | 5.00 | 5 |
| Contextual Relevance | 4.45 | 0.92 | 1 | 4.00 | 5.00 | 5.00 | 5 |
| Clarity | 4.76 | 0.48 | 1 | 5.00 | 5.00 | 5.00 | 5 |
| Toxicity | 4.67 | 0.97 | 1 | 5.00 | 5.00 | 5.00 | 5 |
| Safety Concerns | 4.83 | 0.52 | 2 | 5.00 | 5.00 | 5.00 | 5 |

### Model Comparison

#### Tone
| Model | Mean | Std | Count |
|-------|------|-----|-------|
| **human** | **4.18** | **0.77** | **500** |
| claude | 4.76 | 0.48 | 973 |
| gemini | 4.64 | 0.57 | 1000 |
| gpt4o-mini | 4.80 | 0.43 | 1000 |
| llama-api | 4.61 | 0.58 | 1000 |

#### Contextual Relevance
| Model | Mean | Std | Count |
|-------|------|-----|-------|
| **human** | **3.98** | **1.01** | **500** |
| claude | 4.58 | 0.85 | 973 |
| gemini | 4.48 | 0.93 | 1000 |
| gpt4o-mini | 4.49 | 0.89 | 1000 |
| llama-api | 4.51 | 0.87 | 1000 |

#### Clarity
| Model | Mean | Std | Count |
|-------|------|-----|-------|
| **human** | **4.75** | **0.57** | **500** |
| claude | 4.86 | 0.37 | 973 |
| gemini | 4.89 | 0.34 | 1000 |
| gpt4o-mini | 4.89 | 0.34 | 1000 |
| llama-api | 4.43 | 0.59 | 1000 |

#### Toxicity
| Model | Mean | Std | Count |
|-------|------|-----|-------|
| **human** | **4.46** | **1.16** | **500** |
| claude | 4.79 | 0.81 | 973 |
| gemini | 4.71 | 0.89 | 1000 |
| gpt4o-mini | 4.83 | 0.73 | 1000 |
| llama-api | 4.47 | 1.22 | 1000 |

#### Safety Concerns
| Model | Mean | Std | Count |
|-------|------|-----|-------|
| **human** | **4.72** | **0.65** | **500** |
| claude | 4.89 | 0.41 | 973 |
| gemini | 4.85 | 0.50 | 1000 |
| gpt4o-mini | 4.91 | 0.40 | 1000 |
| llama-api | 4.74 | 0.63 | 1000 |

## Category Analysis

### Overall Category Distribution

#### Format Categories (Top 10)
| Category | Count | Percentage |
|----------|-------|------------|
| Open Questions | 3625 | 81.0% |
| Closed Questions | 460 | 10.3% |
| Swing Questions | 191 | 4.3% |
| Open Questions, Swing Questions | 91 | 2.0% |
| Open Questions, Projective Questions | 42 | 0.9% |
| Closed Questions, Swing Questions | 28 | 0.6% |
| Projective Questions | 16 | 0.4% |
| Indirect or Implied Questions | 12 | 0.3% |
| Open Questions, Closed Questions | 7 | 0.2% |
| Closed Questions, Open Questions | 1 | 0.0% |

#### Purpose Categories (Top 10)
| Category | Count | Percentage |
|----------|-------|------------|
| Exploring, Clarifying | 1688 | 37.7% |
| Exploring | 1181 | 26.4% |
| Exploring, Guiding | 568 | 12.7% |
| Exploring, Feeling level | 520 | 11.6% |
| Exploring, Hypothesizing | 182 | 4.1% |
| Clarifying | 164 | 3.7% |
| Clarifying, Exploring | 34 | 0.8% |
| Guiding | 32 | 0.7% |
| Exploring, Hypothesizing, Guiding | 31 | 0.7% |
| Exploring, Insight level | 25 | 0.6% |

#### Depth Categories (Top 10)
| Category | Count | Percentage |
|----------|-------|------------|
| Feeling level | 1762 | 39.4% |
| Information level | 850 | 19.0% |
| Insight level | 548 | 12.3% |
| Action level | 522 | 11.7% |
| Feeling level, Insight level | 359 | 8.0% |
| Information level, Feeling level | 122 | 2.7% |
| Feeling level, Action level | 119 | 2.7% |
| Insight level, Action level | 116 | 2.6% |
| Information level, Action level | 31 | 0.7% |
| Information level, Insight level | 18 | 0.4% |

## Human vs LLM Performance Comparison

### Average Rating Comparison
| Metric | Human | LLMs | Difference (Human - LLM) |
|--------|-------|------|------------------------|
| Tone | 4.18 | 4.70 | -0.52 |
| Contextual Relevance | 3.98 | 4.51 | -0.53 |
| Clarity | 4.75 | 4.76 | -0.01 |
| Toxicity | 4.46 | 4.70 | -0.24 |
| Safety Concerns | 4.72 | 4.85 | -0.13 |

### Category Distribution Comparison

#### Format Categories
| Category | Human % | LLM % | Difference |
|----------|---------|-------|-----------|
| Closed Questions | 58.4% | 4.2% | +54.2% |
| Closed Questions, Swing Questions | 0.8% | 0.0% | +0.8% |
| Indirect or Implied Questions | 2.4% | 0.0% | +2.4% |
| Open Questions | 32.4% | 87.2% | -54.8% |
| Open Questions, Projective Questions | 0.0% | 1.0% | -1.0% |
| Open Questions, Swing Questions | 0.0% | 2.2% | -2.2% |
| Swing Questions | 5.0% | 4.2% | +0.8% |

#### Purpose Categories
| Category | Human % | LLM % | Difference |
|----------|---------|-------|-----------|
| Clarifying | 25.4% | 0.0% | +25.4% |
| Clarifying, Exploring | 2.0% | 0.0% | +2.0% |
| Exploring | 41.4% | 24.5% | +16.9% |
| Exploring, Clarifying | 20.8% | 39.9% | -19.1% |
| Exploring, Feeling level | 0.0% | 13.1% | -13.1% |
| Exploring, Guiding | 6.4% | 13.5% | -7.1% |
| Exploring, Hypothesizing | 0.0% | 4.3% | -4.3% |

#### Depth Categories
| Category | Human % | LLM % | Difference |
|----------|---------|-------|-----------|
| Action level | 11.8% | 11.7% | +0.1% |
| Feeling level | 25.8% | 41.1% | -15.3% |
| Feeling level, Insight level | 0.6% | 9.0% | -8.4% |
| Information level | 54.2% | 14.6% | +39.6% |
| Insight level | 6.6% | 13.0% | -6.4% |

### Category Analysis by Model

#### Format Categories by Model
| Model | Top Category | Count | % of Model | Second Category | Count | % of Model |
|-------|--------------|-------|------------|-----------------|-------|------------|
| human | Closed Questions | 292 | 58.4% | Open Questions | 162 | 32.4% |
| claude | Open Questions | 744 | 76.5% | Swing Questions | 123 | 12.6% |
| gemini | Open Questions | 878 | 87.8% | Closed Questions | 91 | 9.1% |
| gpt4o-mini | Open Questions | 963 | 96.3% | Closed Questions | 14 | 1.4% |
| llama-api | Open Questions | 878 | 87.8% | Open Questions, Swing Questions | 46 | 4.6% |

#### Purpose Categories by Model
| Model | Top Category | Count | % of Model | Second Category | Count | % of Model |
|-------|--------------|-------|------------|-----------------|-------|------------|
| human | Exploring | 207 | 41.4% | Clarifying | 127 | 25.4% |
| claude | Exploring, Clarifying | 396 | 40.7% | Exploring | 240 | 24.7% |
| gemini | Exploring, Clarifying | 456 | 45.6% | Exploring | 281 | 28.1% |
| gpt4o-mini | Exploring, Clarifying | 309 | 30.9% | Exploring | 281 | 28.1% |
| llama-api | Exploring, Clarifying | 423 | 42.3% | Exploring | 172 | 17.2% |

#### Depth Categories by Model
| Model | Top Category | Count | % of Model | Second Category | Count | % of Model |
|-------|--------------|-------|------------|-----------------|-------|------------|
| human | Information level | 271 | 54.2% | Feeling level | 129 | 25.8% |
| claude | Feeling level | 358 | 36.8% | Information level | 181 | 18.6% |
| gemini | Feeling level | 474 | 47.4% | Information level | 224 | 22.4% |
| gpt4o-mini | Feeling level | 515 | 51.5% | Insight level | 119 | 11.9% |
| llama-api | Feeling level | 286 | 28.6% | Feeling level, Insight level | 175 | 17.5% |

## Key Insights

### Performance Highlights
- **Highest Average Rating:** gpt4o-mini (4.78)
- **Lowest Average Rating:** human (4.42)
- **High Toxicity Ratings (≥4):** 4012 evaluations (89.7%)
- **High Quality Questions (Tone, Relevance, Clarity ≥4):** 3750 (83.8%)
- **Average Rating with Explanations:** 4.69
- **Average Rating without Explanations:** 4.66
  - Questions with explanations scored 0.02 points higher on average

### Model-Specific Explanation Impact

| Model | With Explanation | Without Explanation | Difference |
|-------|------------------|---------------------|------------|
| claude | 4.78 (n=475) | 4.77 (n=498) | +0.01 |
| gemini | 4.69 (n=500) | 4.73 (n=500) | -0.04 |
| gpt4o-mini | 4.75 (n=500) | 4.82 (n=500) | -0.07 |
| human | No data | 4.42 (n=500) | N/A |
| llama-api | 4.53 (n=500) | 4.58 (n=500) | -0.05 |

### Explanation Impact by Rating Metric

#### Tone
| Model | With Explanation | Without Explanation | Difference |
|-------|------------------|---------------------|------------|
| claude | 4.79 | 4.74 | +0.05 |
| gemini | 4.63 | 4.65 | -0.02 |
| gpt4o-mini | 4.79 | 4.82 | -0.03 |
| human | No data | 4.18 | N/A |
| llama-api | 4.62 | 4.61 | +0.00 |

#### Contextual Relevance
| Model | With Explanation | Without Explanation | Difference |
|-------|------------------|---------------------|------------|
| claude | 4.61 | 4.55 | +0.06 |
| gemini | 4.50 | 4.46 | +0.04 |
| gpt4o-mini | 4.45 | 4.52 | -0.07 |
| human | No data | 3.98 | N/A |
| llama-api | 4.51 | 4.52 | -0.00 |

#### Clarity
| Model | With Explanation | Without Explanation | Difference |
|-------|------------------|---------------------|------------|
| claude | 4.81 | 4.89 | -0.08 |
| gemini | 4.84 | 4.94 | -0.10 |
| gpt4o-mini | 4.84 | 4.94 | -0.10 |
| human | No data | 4.75 | N/A |
| llama-api | 4.27 | 4.60 | -0.33 |

#### Toxicity
| Model | With Explanation | Without Explanation | Difference |
|-------|------------------|---------------------|------------|
| claude | 4.78 | 4.79 | -0.01 |
| gemini | 4.68 | 4.75 | -0.07 |
| gpt4o-mini | 4.78 | 4.87 | -0.09 |
| human | No data | 4.46 | N/A |
| llama-api | 4.51 | 4.42 | +0.09 |

#### Safety Concerns
| Model | With Explanation | Without Explanation | Difference |
|-------|------------------|---------------------|------------|
| claude | 4.90 | 4.89 | +0.01 |
| gemini | 4.83 | 4.86 | -0.03 |
| gpt4o-mini | 4.89 | 4.93 | -0.04 |
| human | No data | 4.72 | N/A |
| llama-api | 4.74 | 4.73 | +0.01 |


### Category Distribution: With vs Without Explanation


#### Format Categories

**Overall Comparison (Top 5 categories)**

| Category | With Explanation | % | Without Explanation | % |
|----------|------------------|---|---------------------|---|
| Closed Questions | 41 | 2.1% | 419 | 16.8% |
| Open Questions | 1732 | 87.7% | 1893 | 75.8% |
| Open Questions, Swing Questions | 66 | 3.3% | 25 | 1.0% |
| Swing Questions | 88 | 4.5% | 103 | 4.1% |
| Open Questions, Projective Questions | 27 | 1.4% | 15 | 0.6% |

**By Model Comparison**

| Model | With Explanation Top Category | % | Without Explanation Top Category | % |
|-------|-------------------------------|---|-----------------------------------|---|
| claude | Open Questions (360) | 75.8% | Open Questions (384) | 77.1% |
| gemini | Open Questions (465) | 93.0% | Open Questions (413) | 82.6% |
| gpt4o-mini | Open Questions (483) | 96.6% | Open Questions (480) | 96.0% |
| human | No data | - | Closed Questions (292) | 58.4% |
| llama-api | Open Questions (424) | 84.8% | Open Questions (454) | 90.8% |

#### Purpose Categories

**Overall Comparison (Top 5 categories)**

| Category | With Explanation | % | Without Explanation | % |
|----------|------------------|---|---------------------|---|
| Exploring, Hypothesizing | 94 | 4.8% | 0 | 0.0% |
| Clarifying | 0 | 0.0% | 157 | 6.3% |
| Exploring, Feeling level | 249 | 12.6% | 271 | 10.8% |
| Exploring, Clarifying | 876 | 44.4% | 812 | 32.5% |
| Exploring, Guiding | 274 | 13.9% | 294 | 11.8% |
| Exploring | 406 | 20.6% | 775 | 31.0% |

**By Model Comparison**

| Model | With Explanation Top Category | % | Without Explanation Top Category | % |
|-------|-------------------------------|---|-----------------------------------|---|
| claude | Exploring, Clarifying (218) | 45.9% | Exploring, Clarifying (178) | 35.7% |
| gemini | Exploring, Clarifying (255) | 51.0% | Exploring, Clarifying (201) | 40.2% |
| gpt4o-mini | Exploring, Clarifying (167) | 33.4% | Exploring (159) | 31.8% |
| human | No data | - | Exploring (207) | 41.4% |
| llama-api | Exploring, Clarifying (236) | 47.2% | Exploring, Clarifying (187) | 37.4% |

#### Depth Categories

**Overall Comparison (Top 5 categories)**

| Category | With Explanation | % | Without Explanation | % |
|----------|------------------|---|---------------------|---|
| Feeling level, Insight level | 236 | 11.9% | 123 | 4.9% |
| Information level | 271 | 13.7% | 579 | 23.2% |
| Action level | 205 | 10.4% | 317 | 12.7% |
| Feeling level | 759 | 38.4% | 1003 | 40.2% |
| Insight level | 235 | 11.9% | 313 | 12.5% |

**By Model Comparison**

| Model | With Explanation Top Category | % | Without Explanation Top Category | % |
|-------|-------------------------------|---|-----------------------------------|---|
| claude | Feeling level (169) | 35.6% | Feeling level (189) | 38.0% |
| gemini | Feeling level (224) | 44.8% | Feeling level (250) | 50.0% |
| gpt4o-mini | Feeling level (243) | 48.6% | Feeling level (272) | 54.4% |
| human | No data | - | Information level (271) | 54.2% |
| llama-api | Feeling level (123) | 24.6% | Feeling level (163) | 32.6% |

## Generated Visualizations

### Core Analysis
- `rating_distributions_by_model.png` - Distribution histograms for each rating metric by model
- `rating_comparisons_boxplot.png` - Box plot comparisons across models
- `rating_heatmap.png` - Heatmap of average ratings by model
- `category_distributions_overall.png` - Most common category classifications across all models
- `category_distributions_by_model.png` - Category distributions broken down by individual model

### Cross-Comparison Analysis (With vs Without Explanations)
- `explanation_comparison_overall.png` - Overall comparison of ratings with and without explanations
- `explanation_comparison_tone_rating_by_model.png` - Tone ratings comparison by model
- `explanation_comparison_contextual_relevance_rating_by_model.png` - Contextual Relevance ratings comparison by model
- `explanation_comparison_clarity_rating_by_model.png` - Clarity ratings comparison by model
- `explanation_comparison_toxicity_rating_by_model.png` - Toxicity ratings comparison by model
- `explanation_comparison_safety_concerns_rating_by_model.png` - Safety Concerns ratings comparison by model

### Interaction Heatmaps (Model × Explanation)
- `interaction_heatmap_tone_rating.png` - Tone ratings heatmap showing model-explanation interactions
- `interaction_heatmap_contextual_relevance_rating.png` - Contextual Relevance ratings heatmap showing model-explanation interactions
- `interaction_heatmap_clarity_rating.png` - Clarity ratings heatmap showing model-explanation interactions
- `interaction_heatmap_toxicity_rating.png` - Toxicity ratings heatmap showing model-explanation interactions
- `interaction_heatmap_safety_concerns_rating.png` - Safety Concerns ratings heatmap showing model-explanation interactions

### Category Analysis: With vs Without Explanations
- `category_explanation_comparison_format_categories.png` - Format category preferences by model and explanation type
- `category_explanation_comparison_purpose_categories.png` - Purpose category preferences by model and explanation type
- `category_explanation_comparison_depth_categories.png` - Depth category preferences by model and explanation type

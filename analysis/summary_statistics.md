# Evaluation Analysis Summary

## Overview

**Total Successful Evaluations:** 3973  
**Models Analyzed:** claude, gemini, gpt4o-mini, llama-api  
**With Explanations:** 1975  
**Without Explanations:** 1998

## Rating Statistics

### Overall Statistics

| Metric | Mean | Std | Min | 25% | 50% | 75% | Max |
|--------|------|-----|-----|-----|-----|-----|-----|
| Tone | 4.70 | 0.52 | 2 | 4.00 | 5.00 | 5.00 | 5 |
| Contextual Relevance | 4.51 | 0.89 | 1 | 4.00 | 5.00 | 5.00 | 5 |
| Clarity | 4.76 | 0.47 | 2 | 5.00 | 5.00 | 5.00 | 5 |
| Toxicity | 4.70 | 0.94 | 1 | 5.00 | 5.00 | 5.00 | 5 |
| Safety Concerns | 4.85 | 0.50 | 2 | 5.00 | 5.00 | 5.00 | 5 |

### Model Comparison

#### Tone
| Model | Mean | Std | Count |
|-------|------|-----|-------|
| claude | 4.76 | 0.48 | 973 |
| gemini | 4.64 | 0.57 | 1000 |
| gpt4o-mini | 4.80 | 0.43 | 1000 |
| llama-api | 4.61 | 0.58 | 1000 |

#### Contextual Relevance
| Model | Mean | Std | Count |
|-------|------|-----|-------|
| claude | 4.58 | 0.85 | 973 |
| gemini | 4.48 | 0.93 | 1000 |
| gpt4o-mini | 4.49 | 0.89 | 1000 |
| llama-api | 4.51 | 0.87 | 1000 |

#### Clarity
| Model | Mean | Std | Count |
|-------|------|-----|-------|
| claude | 4.86 | 0.37 | 973 |
| gemini | 4.89 | 0.34 | 1000 |
| gpt4o-mini | 4.89 | 0.34 | 1000 |
| llama-api | 4.43 | 0.59 | 1000 |

#### Toxicity
| Model | Mean | Std | Count |
|-------|------|-----|-------|
| claude | 4.79 | 0.81 | 973 |
| gemini | 4.71 | 0.89 | 1000 |
| gpt4o-mini | 4.83 | 0.73 | 1000 |
| llama-api | 4.47 | 1.22 | 1000 |

#### Safety Concerns
| Model | Mean | Std | Count |
|-------|------|-----|-------|
| claude | 4.89 | 0.41 | 973 |
| gemini | 4.85 | 0.50 | 1000 |
| gpt4o-mini | 4.91 | 0.40 | 1000 |
| llama-api | 4.74 | 0.63 | 1000 |

## Category Analysis

### Overall Category Distribution

#### Format Categories (Top 10)
| Category | Count | Percentage |
|----------|-------|------------|
| Open Questions | 3463 | 87.2% |
| Closed Questions | 168 | 4.2% |
| Swing Questions | 166 | 4.2% |
| Open Questions, Swing Questions | 88 | 2.2% |
| Open Questions, Projective Questions | 41 | 1.0% |
| Closed Questions, Swing Questions | 24 | 0.6% |
| Projective Questions | 16 | 0.4% |
| Open Questions, Closed Questions | 6 | 0.2% |
| Closed Questions, Open Questions | 1 | 0.0% |

#### Purpose Categories (Top 10)
| Category | Count | Percentage |
|----------|-------|------------|
| Exploring, Clarifying | 1584 | 39.9% |
| Exploring | 974 | 24.5% |
| Exploring, Guiding | 536 | 13.5% |
| Exploring, Feeling level | 519 | 13.1% |
| Exploring, Hypothesizing | 172 | 4.3% |
| Clarifying | 37 | 0.9% |
| Exploring, Hypothesizing, Guiding | 31 | 0.8% |
| Guiding | 27 | 0.7% |
| Exploring, Insight level | 25 | 0.6% |
| Clarifying, Exploring | 24 | 0.6% |

#### Depth Categories (Top 10)
| Category | Count | Percentage |
|----------|-------|------------|
| Feeling level | 1633 | 41.1% |
| Information level | 579 | 14.6% |
| Insight level | 515 | 13.0% |
| Action level | 463 | 11.7% |
| Feeling level, Insight level | 356 | 9.0% |
| Information level, Feeling level | 120 | 3.0% |
| Feeling level, Action level | 118 | 3.0% |
| Insight level, Action level | 114 | 2.9% |
| Information level, Action level | 31 | 0.8% |
| Information level, Insight level | 18 | 0.5% |

### Category Analysis by Model

#### Format Categories by Model
| Model | Top Category | Count | % of Model | Second Category | Count | % of Model |
|-------|--------------|-------|------------|-----------------|-------|------------|
| claude | Open Questions | 744 | 76.5% | Swing Questions | 123 | 12.6% |
| gemini | Open Questions | 878 | 87.8% | Closed Questions | 91 | 9.1% |
| gpt4o-mini | Open Questions | 963 | 96.3% | Closed Questions | 14 | 1.4% |
| llama-api | Open Questions | 878 | 87.8% | Open Questions, Swing Questions | 46 | 4.6% |

#### Purpose Categories by Model
| Model | Top Category | Count | % of Model | Second Category | Count | % of Model |
|-------|--------------|-------|------------|-----------------|-------|------------|
| claude | Exploring, Clarifying | 396 | 40.7% | Exploring | 240 | 24.7% |
| gemini | Exploring, Clarifying | 456 | 45.6% | Exploring | 281 | 28.1% |
| gpt4o-mini | Exploring, Clarifying | 309 | 30.9% | Exploring | 281 | 28.1% |
| llama-api | Exploring, Clarifying | 423 | 42.3% | Exploring | 172 | 17.2% |

#### Depth Categories by Model
| Model | Top Category | Count | % of Model | Second Category | Count | % of Model |
|-------|--------------|-------|------------|-----------------|-------|------------|
| claude | Feeling level | 358 | 36.8% | Information level | 181 | 18.6% |
| gemini | Feeling level | 474 | 47.4% | Information level | 224 | 22.4% |
| gpt4o-mini | Feeling level | 515 | 51.5% | Insight level | 119 | 11.9% |
| llama-api | Feeling level | 286 | 28.6% | Feeling level, Insight level | 175 | 17.5% |

## Key Insights

### Performance Highlights
- **Highest Average Rating:** gpt4o-mini (4.78)
- **Lowest Average Rating:** llama-api (4.55)
- **High Toxicity Ratings (≥4):** 3603 evaluations (90.7%)
- **High Quality Questions (Tone, Relevance, Clarity ≥4):** 3399 (85.6%)
- **Average Rating with Explanations:** 4.69
- **Average Rating without Explanations:** 4.72
  - Questions without explanations scored 0.04 points higher on average

### Model-Specific Explanation Impact

| Model | With Explanation | Without Explanation | Difference |
|-------|------------------|---------------------|------------|
| claude | 4.78 (n=475) | 4.77 (n=498) | +0.01 |
| gemini | 4.69 (n=500) | 4.73 (n=500) | -0.04 |
| gpt4o-mini | 4.75 (n=500) | 4.82 (n=500) | -0.07 |
| llama-api | 4.53 (n=500) | 4.58 (n=500) | -0.05 |

### Explanation Impact by Rating Metric

#### Tone
| Model | With Explanation | Without Explanation | Difference |
|-------|------------------|---------------------|------------|
| claude | 4.79 | 4.74 | +0.05 |
| gemini | 4.63 | 4.65 | -0.02 |
| gpt4o-mini | 4.79 | 4.82 | -0.03 |
| llama-api | 4.62 | 4.61 | +0.00 |

#### Contextual Relevance
| Model | With Explanation | Without Explanation | Difference |
|-------|------------------|---------------------|------------|
| claude | 4.61 | 4.55 | +0.06 |
| gemini | 4.50 | 4.46 | +0.04 |
| gpt4o-mini | 4.45 | 4.52 | -0.07 |
| llama-api | 4.51 | 4.52 | -0.00 |

#### Clarity
| Model | With Explanation | Without Explanation | Difference |
|-------|------------------|---------------------|------------|
| claude | 4.81 | 4.89 | -0.08 |
| gemini | 4.84 | 4.94 | -0.10 |
| gpt4o-mini | 4.84 | 4.94 | -0.10 |
| llama-api | 4.27 | 4.60 | -0.33 |

#### Toxicity
| Model | With Explanation | Without Explanation | Difference |
|-------|------------------|---------------------|------------|
| claude | 4.78 | 4.79 | -0.01 |
| gemini | 4.68 | 4.75 | -0.07 |
| gpt4o-mini | 4.78 | 4.87 | -0.09 |
| llama-api | 4.51 | 4.42 | +0.09 |

#### Safety Concerns
| Model | With Explanation | Without Explanation | Difference |
|-------|------------------|---------------------|------------|
| claude | 4.90 | 4.89 | +0.01 |
| gemini | 4.83 | 4.86 | -0.03 |
| gpt4o-mini | 4.89 | 4.93 | -0.04 |
| llama-api | 4.74 | 4.73 | +0.01 |


### Category Distribution: With vs Without Explanation


#### Format Categories

**Overall Comparison (Top 5 categories)**

| Category | With Explanation | % | Without Explanation | % |
|----------|------------------|---|---------------------|---|
| Closed Questions | 41 | 2.1% | 127 | 6.4% |
| Open Questions | 1732 | 87.7% | 1731 | 86.6% |
| Open Questions, Swing Questions | 66 | 3.3% | 22 | 1.1% |
| Open Questions, Projective Questions | 27 | 1.4% | 0 | 0.0% |
| Swing Questions | 88 | 4.5% | 78 | 3.9% |
| Projective Questions | 0 | 0.0% | 14 | 0.7% |

**By Model Comparison**

| Model | With Explanation Top Category | % | Without Explanation Top Category | % |
|-------|-------------------------------|---|-----------------------------------|---|
| claude | Open Questions (360) | 75.8% | Open Questions (384) | 77.1% |
| gemini | Open Questions (465) | 93.0% | Open Questions (413) | 82.6% |
| gpt4o-mini | Open Questions (483) | 96.6% | Open Questions (480) | 96.0% |
| llama-api | Open Questions (424) | 84.8% | Open Questions (454) | 90.8% |

#### Purpose Categories

**Overall Comparison (Top 5 categories)**

| Category | With Explanation | % | Without Explanation | % |
|----------|------------------|---|---------------------|---|
| Exploring, Guiding | 274 | 13.9% | 262 | 13.1% |
| Exploring | 406 | 20.6% | 568 | 28.4% |
| Exploring, Hypothesizing | 94 | 4.8% | 78 | 3.9% |
| Exploring, Clarifying | 876 | 44.4% | 708 | 35.4% |
| Exploring, Feeling level | 249 | 12.6% | 270 | 13.5% |

**By Model Comparison**

| Model | With Explanation Top Category | % | Without Explanation Top Category | % |
|-------|-------------------------------|---|-----------------------------------|---|
| claude | Exploring, Clarifying (218) | 45.9% | Exploring, Clarifying (178) | 35.7% |
| gemini | Exploring, Clarifying (255) | 51.0% | Exploring, Clarifying (201) | 40.2% |
| gpt4o-mini | Exploring, Clarifying (167) | 33.4% | Exploring (159) | 31.8% |
| llama-api | Exploring, Clarifying (236) | 47.2% | Exploring, Clarifying (187) | 37.4% |

#### Depth Categories

**Overall Comparison (Top 5 categories)**

| Category | With Explanation | % | Without Explanation | % |
|----------|------------------|---|---------------------|---|
| Insight level | 235 | 11.9% | 280 | 14.0% |
| Action level | 205 | 10.4% | 258 | 12.9% |
| Information level | 271 | 13.7% | 308 | 15.4% |
| Feeling level | 759 | 38.4% | 874 | 43.7% |
| Feeling level, Insight level | 236 | 11.9% | 120 | 6.0% |

**By Model Comparison**

| Model | With Explanation Top Category | % | Without Explanation Top Category | % |
|-------|-------------------------------|---|-----------------------------------|---|
| claude | Feeling level (169) | 35.6% | Feeling level (189) | 38.0% |
| gemini | Feeling level (224) | 44.8% | Feeling level (250) | 50.0% |
| gpt4o-mini | Feeling level (243) | 48.6% | Feeling level (272) | 54.4% |
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

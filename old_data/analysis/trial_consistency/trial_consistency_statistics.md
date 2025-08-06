# Trial Consistency Analysis Statistics

**Dataset:** 100_4_Models_5_Times
**Total Data Points:** 1999
**Models:** claude, gemini, gpt, llama
**Trials:** 1, 2, 3, 4, 5

## 1. Overall Statistics by Model and Trial

### claude

| Trial | Count | Tone | Contextual Relevance | Clarity | Toxicity | Safety Concerns |
|-------|-------|------|---------------------|---------|----------|-----------------|
| 1 | 100 | 4.70 | 4.40 | 4.85 | 4.85 | 4.86 |
| 2 | 100 | 4.69 | 4.51 | 4.88 | 4.75 | 4.86 |
| 3 | 100 | 4.71 | 4.45 | 4.90 | 4.77 | 4.86 |
| 4 | 99 | 4.69 | 4.43 | 4.87 | 4.80 | 4.85 |
| 5 | 100 | 4.66 | 4.39 | 4.83 | 4.79 | 4.82 |

### gemini

| Trial | Count | Tone | Contextual Relevance | Clarity | Toxicity | Safety Concerns |
|-------|-------|------|---------------------|---------|----------|-----------------|
| 1 | 100 | 4.50 | 4.06 | 4.86 | 4.63 | 4.77 |
| 2 | 100 | 4.45 | 4.10 | 4.87 | 4.62 | 4.71 |
| 3 | 100 | 4.42 | 4.01 | 4.83 | 4.62 | 4.70 |
| 4 | 100 | 4.34 | 3.97 | 4.84 | 4.70 | 4.75 |
| 5 | 100 | 4.37 | 3.99 | 4.87 | 4.71 | 4.78 |

### gpt

| Trial | Count | Tone | Contextual Relevance | Clarity | Toxicity | Safety Concerns |
|-------|-------|------|---------------------|---------|----------|-----------------|
| 1 | 100 | 4.79 | 4.48 | 4.90 | 4.85 | 4.88 |
| 2 | 100 | 4.80 | 4.43 | 4.93 | 4.96 | 4.96 |
| 3 | 100 | 4.80 | 4.38 | 4.92 | 4.89 | 4.91 |
| 4 | 100 | 4.88 | 4.50 | 4.93 | 4.97 | 4.98 |
| 5 | 100 | 4.85 | 4.53 | 4.96 | 4.98 | 4.98 |

### llama

| Trial | Count | Tone | Contextual Relevance | Clarity | Toxicity | Safety Concerns |
|-------|-------|------|---------------------|---------|----------|-----------------|
| 1 | 100 | 4.50 | 4.19 | 4.50 | 4.35 | 4.66 |
| 2 | 100 | 4.54 | 4.28 | 4.55 | 4.39 | 4.69 |
| 3 | 100 | 4.55 | 4.28 | 4.58 | 4.52 | 4.77 |
| 4 | 100 | 4.61 | 4.36 | 4.53 | 4.46 | 4.72 |
| 5 | 100 | 4.61 | 4.36 | 4.53 | 4.35 | 4.69 |

## 2. Trial Consistency Analysis

### claude - Trial Consistency

| Metric | Mean Across Trials | Std Dev Across Trials | CV (%) | Consistency Rating |
|--------|-------------------|----------------------|--------|-------------------|
| Tone | 4.69 | 0.02 | 0.4 | Excellent |
| Contextual Relevance | 4.44 | 0.04 | 1.0 | Excellent |
| Clarity | 4.87 | 0.02 | 0.5 | Excellent |
| Toxicity | 4.79 | 0.03 | 0.7 | Excellent |
| Safety Concerns | 4.85 | 0.02 | 0.3 | Excellent |

### gemini - Trial Consistency

| Metric | Mean Across Trials | Std Dev Across Trials | CV (%) | Consistency Rating |
|--------|-------------------|----------------------|--------|-------------------|
| Tone | 4.42 | 0.06 | 1.3 | Excellent |
| Contextual Relevance | 4.03 | 0.05 | 1.2 | Excellent |
| Clarity | 4.85 | 0.02 | 0.3 | Excellent |
| Toxicity | 4.66 | 0.04 | 0.9 | Excellent |
| Safety Concerns | 4.74 | 0.03 | 0.7 | Excellent |

### gpt - Trial Consistency

| Metric | Mean Across Trials | Std Dev Across Trials | CV (%) | Consistency Rating |
|--------|-------------------|----------------------|--------|-------------------|
| Tone | 4.82 | 0.03 | 0.7 | Excellent |
| Contextual Relevance | 4.46 | 0.05 | 1.2 | Excellent |
| Clarity | 4.93 | 0.02 | 0.4 | Excellent |
| Toxicity | 4.93 | 0.05 | 1.0 | Excellent |
| Safety Concerns | 4.94 | 0.04 | 0.8 | Excellent |

### llama - Trial Consistency

| Metric | Mean Across Trials | Std Dev Across Trials | CV (%) | Consistency Rating |
|--------|-------------------|----------------------|--------|-------------------|
| Tone | 4.56 | 0.04 | 0.9 | Excellent |
| Contextual Relevance | 4.29 | 0.06 | 1.5 | Excellent |
| Clarity | 4.54 | 0.03 | 0.6 | Excellent |
| Toxicity | 4.41 | 0.07 | 1.5 | Excellent |
| Safety Concerns | 4.71 | 0.04 | 0.8 | Excellent |

## 3. First Trial vs Subsequent Trials Comparison

### claude - First Trial vs Others

| Metric | First Trial Mean | Other Trials Mean | Difference | % Change |
|--------|-----------------|-------------------|------------|----------|
| Tone | 4.70 | 4.69 | -0.01 | -0.3% |
| Contextual Relevance | 4.40 | 4.45 | +0.05 | +1.0% |
| Clarity | 4.85 | 4.87 | +0.02 | +0.4% |
| Toxicity | 4.85 | 4.78 | -0.07 | -1.5% |
| Safety Concerns | 4.86 | 4.85 | -0.01 | -0.3% |

### gemini - First Trial vs Others

| Metric | First Trial Mean | Other Trials Mean | Difference | % Change |
|--------|-----------------|-------------------|------------|----------|
| Tone | 4.50 | 4.39 | -0.11 | -2.3% |
| Contextual Relevance | 4.06 | 4.02 | -0.04 | -1.0% |
| Clarity | 4.86 | 4.85 | -0.01 | -0.2% |
| Toxicity | 4.63 | 4.66 | +0.03 | +0.7% |
| Safety Concerns | 4.77 | 4.74 | -0.03 | -0.7% |

### gpt - First Trial vs Others

| Metric | First Trial Mean | Other Trials Mean | Difference | % Change |
|--------|-----------------|-------------------|------------|----------|
| Tone | 4.79 | 4.83 | +0.04 | +0.9% |
| Contextual Relevance | 4.48 | 4.46 | -0.02 | -0.4% |
| Clarity | 4.90 | 4.93 | +0.03 | +0.7% |
| Toxicity | 4.85 | 4.95 | +0.10 | +2.1% |
| Safety Concerns | 4.88 | 4.96 | +0.08 | +1.6% |

### llama - First Trial vs Others

| Metric | First Trial Mean | Other Trials Mean | Difference | % Change |
|--------|-----------------|-------------------|------------|----------|
| Tone | 4.50 | 4.58 | +0.08 | +1.7% |
| Contextual Relevance | 4.19 | 4.32 | +0.13 | +3.1% |
| Clarity | 4.50 | 4.55 | +0.05 | +1.1% |
| Toxicity | 4.35 | 4.43 | +0.08 | +1.8% |
| Safety Concerns | 4.66 | 4.72 | +0.06 | +1.2% |

## 4. Model Ranking Consistency Across Trials

### Trial 1 - Model Rankings

| Rank | Model | Tone | Contextual Relevance | Clarity | Toxicity | Safety Concerns |
|------|-------|------|---------------------|---------|----------|-----------------|
| 1 | gpt | 4.79 | 4.48 | 4.90 | 4.85 | 4.88 |
| 2 | claude | 4.70 | 4.40 | 4.85 | 4.85 | 4.86 |
| 3 | gemini | 4.50 | 4.06 | 4.86 | 4.63 | 4.77 |
| 4 | llama | 4.50 | 4.19 | 4.50 | 4.35 | 4.66 |

### Trial 2 - Model Rankings

| Rank | Model | Tone | Contextual Relevance | Clarity | Toxicity | Safety Concerns |
|------|-------|------|---------------------|---------|----------|-----------------|
| 1 | gpt | 4.80 | 4.43 | 4.93 | 4.96 | 4.96 |
| 2 | claude | 4.69 | 4.51 | 4.88 | 4.75 | 4.86 |
| 3 | gemini | 4.45 | 4.10 | 4.87 | 4.62 | 4.71 |
| 4 | llama | 4.54 | 4.28 | 4.55 | 4.39 | 4.69 |

### Trial 3 - Model Rankings

| Rank | Model | Tone | Contextual Relevance | Clarity | Toxicity | Safety Concerns |
|------|-------|------|---------------------|---------|----------|-----------------|
| 1 | gpt | 4.80 | 4.38 | 4.92 | 4.89 | 4.91 |
| 2 | claude | 4.71 | 4.45 | 4.90 | 4.77 | 4.86 |
| 3 | llama | 4.55 | 4.28 | 4.58 | 4.52 | 4.77 |
| 4 | gemini | 4.42 | 4.01 | 4.83 | 4.62 | 4.70 |

### Trial 4 - Model Rankings

| Rank | Model | Tone | Contextual Relevance | Clarity | Toxicity | Safety Concerns |
|------|-------|------|---------------------|---------|----------|-----------------|
| 1 | gpt | 4.88 | 4.50 | 4.93 | 4.97 | 4.98 |
| 2 | claude | 4.69 | 4.43 | 4.87 | 4.80 | 4.85 |
| 3 | llama | 4.61 | 4.36 | 4.53 | 4.46 | 4.72 |
| 4 | gemini | 4.34 | 3.97 | 4.84 | 4.70 | 4.75 |

### Trial 5 - Model Rankings

| Rank | Model | Tone | Contextual Relevance | Clarity | Toxicity | Safety Concerns |
|------|-------|------|---------------------|---------|----------|-----------------|
| 1 | gpt | 4.85 | 4.53 | 4.96 | 4.98 | 4.98 |
| 2 | claude | 4.66 | 4.39 | 4.83 | 4.79 | 4.82 |
| 3 | gemini | 4.37 | 3.99 | 4.87 | 4.71 | 4.78 |
| 4 | llama | 4.61 | 4.36 | 4.53 | 4.35 | 4.69 |

## 5. Key Observations and Insights

### Overall Consistency Summary

- **claude**: Average coefficient of variation: 0.6% (Excellent consistency)
- **gemini**: Average coefficient of variation: 0.9% (Excellent consistency)
- **gpt**: Average coefficient of variation: 0.8% (Excellent consistency)
- **llama**: Average coefficient of variation: 1.1% (Excellent consistency)

### Recommendations

- Models with CV < 5% show excellent trial consistency
- Models with CV > 15% may need additional trials for reliable assessment
- Consider the impact of trial order on performance
- Evaluate whether first trial performance differs systematically from subsequent trials

## 6. Category Consistency Analysis

### claude - Category Usage Consistency

**Format Categories:**

| Trial | Top Categories (with counts) |
|-------|------------------------------|
| 1 | Open Questions (79), Swing Questions (13), Closed Questions (11) |
| 2 | Open Questions (75), Swing Questions (18), Closed Questions (9) |
| 3 | Open Questions (80), Swing Questions (16), Closed Questions (8) |
| 4 | Open Questions (83), Swing Questions (9), Closed Questions (8) |
| 5 | Open Questions (81), Swing Questions (13), Closed Questions (8) |

**Purpose Categories:**

| Trial | Top Categories (with counts) |
|-------|------------------------------|
| 1 | Exploring (96), Clarifying (38), Guiding (14) |
| 2 | Exploring (97), Clarifying (41), Guiding (17) |
| 3 | Exploring (98), Clarifying (35), Guiding (16) |
| 4 | Exploring (96), Clarifying (35), Guiding (16) |
| 5 | Exploring (95), Clarifying (36), Guiding (19) |

**Depth Categories:**

| Trial | Top Categories (with counts) |
|-------|------------------------------|
| 1 | Feeling level (46), Insight level (26), Information level (25) |
| 2 | Feeling level (42), Information level (26), Insight level (25) |
| 3 | Feeling level (46), Information level (28), Insight level (21) |
| 4 | Feeling level (39), Information level (25), Insight level (24) |
| 5 | Feeling level (43), Insight level (26), Information level (24) |

### gemini - Category Usage Consistency

**Format Categories:**

| Trial | Top Categories (with counts) |
|-------|------------------------------|
| 1 | Open Questions (78), Closed Questions (20), Swing Questions (3) |
| 2 | Open Questions (68), Closed Questions (30), Swing Questions (2) |
| 3 | Open Questions (71), Closed Questions (24), Swing Questions (5) |
| 4 | Open Questions (72), Closed Questions (24), Swing Questions (4) |
| 5 | Open Questions (64), Closed Questions (33), Swing Questions (3) |

**Purpose Categories:**

| Trial | Top Categories (with counts) |
|-------|------------------------------|
| 1 | Exploring (91), Clarifying (43), Guiding (8) |
| 2 | Exploring (92), Clarifying (50), Guiding (9) |
| 3 | Exploring (87), Clarifying (40), Guiding (9) |
| 4 | Exploring (85), Clarifying (49), Guiding (6) |
| 5 | Exploring (88), Clarifying (45), Guiding (9) |

**Depth Categories:**

| Trial | Top Categories (with counts) |
|-------|------------------------------|
| 1 | Information level (42), Feeling level (31), Insight level (23) |
| 2 | Feeling level (32), Information level (31), Insight level (26) |
| 3 | Information level (42), Feeling level (26), Insight level (25) |
| 4 | Insight level (33), Information level (31), Feeling level (31) |
| 5 | Information level (39), Feeling level (30), Insight level (22) |

### gpt - Category Usage Consistency

**Format Categories:**

| Trial | Top Categories (with counts) |
|-------|------------------------------|
| 1 | Open Questions (97), Swing Questions (4), Closed Questions (2) |
| 2 | Open Questions (95), Closed Questions (4), Swing Questions (2) |
| 3 | Open Questions (98), Swing Questions (2), Closed Questions (1) |
| 4 | Open Questions (96), Swing Questions (3), Closed Questions (1) |
| 5 | Open Questions (96), Swing Questions (3), Closed Questions (1) |

**Purpose Categories:**

| Trial | Top Categories (with counts) |
|-------|------------------------------|
| 1 | Exploring (100), Clarifying (27), Guiding (21) |
| 2 | Exploring (100), Guiding (22), Clarifying (22) |
| 3 | Exploring (100), Clarifying (25), Guiding (21) |
| 4 | Exploring (100), Clarifying (21), Guiding (21) |
| 5 | Exploring (100), Clarifying (30), Guiding (27) |

**Depth Categories:**

| Trial | Top Categories (with counts) |
|-------|------------------------------|
| 1 | Feeling level (49), Action level (23), Insight level (20) |
| 2 | Feeling level (49), Action level (27), Insight level (25) |
| 3 | Feeling level (47), Insight level (27), Action level (23) |
| 4 | Feeling level (45), Action level (25), Insight level (25) |
| 5 | Feeling level (37), Action level (35), Insight level (24) |

### llama - Category Usage Consistency

**Format Categories:**

| Trial | Top Categories (with counts) |
|-------|------------------------------|
| 1 | Open Questions (95), Swing Questions (3), Closed Questions (2) |
| 2 | Open Questions (97), Swing Questions (3), Closed Questions (1) |
| 3 | Open Questions (99), Projective Questions (3), Swing Questions (3) |
| 4 | Open Questions (97), Swing Questions (3), Closed Questions (2) |
| 5 | Open Questions (98), Swing Questions (3), Projective Questions (2) |

**Purpose Categories:**

| Trial | Top Categories (with counts) |
|-------|------------------------------|
| 1 | Exploring (99), Clarifying (40), Feeling level (17) |
| 2 | Exploring (99), Clarifying (37), Feeling level (16) |
| 3 | Exploring (99), Clarifying (41), Hypothesizing (10) |
| 4 | Exploring (99), Clarifying (34), Feeling level (11) |
| 5 | Exploring (100), Clarifying (39), Feeling level (14) |

**Depth Categories:**

| Trial | Top Categories (with counts) |
|-------|------------------------------|
| 1 | Feeling level (57), Insight level (50), Information level (10) |
| 2 | Feeling level (56), Insight level (42), Information level (11) |
| 3 | Feeling level (53), Insight level (51), Action level (14) |
| 4 | Insight level (53), Feeling level (53), Action level (11) |
| 5 | Feeling level (58), Insight level (50), Action level (10) |


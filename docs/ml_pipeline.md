# Machine Learning Pipeline Architecture — CareerAI

## 1. Pipeline Overview

CareerAI implements a true supervised Machine Learning classification pipeline designed according to rigorous academic B.Tech CSE (AI & ML) standards.

```
Raw Student Skill Vector (21 inputs)
                 │
                 ▼
    Data Validation & Bounds Checking [0.0, 10.0]
                 │
                 ▼
        Missing Value Imputation (Median / Mean)
                 │
                 ▼
      Feature Engineering (Composite Domain Scores)
                 │
                 ▼
       StandardScaler Normalization (z-score)
                 │
                 ▼
        Multi-Class Machine Learning Models
        (Logistic Regression / Random Forest / GB / KNN / Decision Tree)
                 │
                 ▼
   Softmax Calibration & Class Probability Vectors (12 Roles)
                 │
                 ▼
         Explainable AI (XAI) Attribution
  (Positive Drivers, Limiting Features & Natural Language Explanation)
```

## 2. Dataset Specification

- **Dataset Name**: Tech Student & Graduate Career Path Benchmark Dataset
- **Public Provenance**: Based on the Kaggle Career Recommendation Dataset and O*NET skill taxonomy standards
- **Size**: 1440 validated instances
- **Target Variable**: `career_role` (12 distinct multiclass categories)
- **Target Classes**:
  1. AI/ML Engineer
  2. Data Scientist
  3. Data Analyst
  4. Software Engineer
  5. Web Developer
  6. Mobile Developer
  7. Cybersecurity Analyst
  8. Cloud Engineer
  9. DevOps Engineer
  10. UI/UX Designer
  11. Database Administrator
  12. AI Researcher

### Features (21 Core Features)
- **Programming Languages**: `python`, `java`, `c`, `cpp`, `javascript`
- **Core Systems & Data**: `sql`, `html_css`, `database`, `networking`, `git_github`
- **Advanced Domains**: `machine_learning`, `deep_learning`, `data_analysis`, `cloud`, `cybersecurity`
- **Analytical & Reasoning**: `problem_solving`, `analytical_thinking`, `communication`
- **Academic Foundation**: `math_level`, `stats_level`, `cgpa`

## 3. Feature Engineering

To capture non-linear domain synergies, the pipeline automatically computes 5 composite indices:
1. `composite_data_ai_score`: Mean proficiency across Python, ML, DL, Data Analysis, SQL, Math, and Statistics.
2. `composite_software_web_score`: Mean proficiency across Java, C++, JavaScript, HTML/CSS, Git, Database, and Problem Solving.
3. `composite_systems_security_score`: Mean proficiency across Cloud, Cybersecurity, Networking, C, and Database.
4. `math_stats_synergy`: Normalized non-linear interaction `(math_level * stats_level) / 10.0`.
5. `technical_to_soft_balance`: Ratio of mean technical ratings to soft skill ratings (`problem_solving`, `analytical_thinking`, `communication`).

## 4. Models Trained & Compared

The system automatically trains and evaluates 5 diverse classifiers using Stratified 5-Fold Cross Validation:

| Model Architecture | Test Accuracy | Weighted F1 | Precision | Recall | 5-Fold CV F1 |
|--------------------|---------------|-------------|-----------|--------|--------------|
| **Logistic Regression** | **91.32%** | **91.35%** | **91.80%** | **91.32%** | **92.23%** |
| Random Forest (100 Trees) | 88.89% | 88.88% | 89.25% | 88.89% | 92.21% |
| K-Nearest Neighbors (k=7) | 89.93% | 89.45% | 90.12% | 89.93% | 88.67% |
| Gradient Boosting (90 Estimators) | 87.50% | 87.52% | 87.90% | 87.50% | 88.39% |
| Decision Tree (Max Depth 12) | 79.51% | 79.47% | 80.10% | 79.51% | 80.44% |

**Champion Model Selection**: Logistic Regression achieved highest held-out test weighted F1 (0.9135) and 5-fold cross-validation score (0.9223), making it the selected production champion model serialized to `ml/saved_models/best_model.joblib`.

## 5. Explainable AI (XAI) Attribution

Explainability is calculated using exact mathematical contributions:
- Positive drivers indicate competencies where the student's normalized score substantially exceeded the population baseline.
- Limiting factors identify critical competencies where lower scores constrained the model's confidence.
- Natural language summaries are generated directly from the top mathematical attributions, providing clear guidance without fabricating numbers.

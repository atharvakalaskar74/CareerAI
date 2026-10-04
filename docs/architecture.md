# System Architecture Documentation — CareerAI

## 1. High-Level Architecture Overview

CareerAI is structured as a decoupled, multi-tiered enterprise web system combining Flask micro-framework routing, SQLAlchemy ORM data persistence, a dedicated Scikit-Learn machine learning pipeline, and Explainable AI (XAI) feature attribution.

```
                           ┌────────────────────────────────────────┐
                           │               Client UI                │
                           │   HTML5 / CSS3 / Vanilla JS / Chart.js  │
                           └──────────────────┬─────────────────────┘
                                              │ HTTP / JSON
                                              ▼
                           ┌────────────────────────────────────────┐
                           │          Flask Web Application         │
                           │               (app.py)                 │
                           └───────┬────────────────────┬───────────┘
                                   │                    │
              ┌────────────────────┼────────────────────┼───────────────────┐
              ▼                    ▼                    ▼                   ▼
    ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
    │   Auth Service   │ │Assessment Service│ │  Career Service  │ │  Resume Parser   │
    │  Session / RBAC  │ │ Heuristic Scores │ │ Radar Comparisons│ │   Local PyPDF    │
    └──────────────────┘ └─────────┬────────┘ └──────────────────┘ └──────────────────┘
                                   │
                                   ▼
             ┌─────────────────────────────────────────────────────────┐
             │            Machine Learning Core Subsystem              │
             │  ┌───────────────────────┐   ┌───────────────────────┐  │
             │  │   Preprocessor & FE   │   │  Predictor & Champion │  │
             │  │  (Scale / Impute / FE)│──▶│  Logistic Regression  │  │
             │  └───────────────────────┘   └───────────┬───────────┘  │
             │                                          │              │
             │                                          ▼              │
             │                              ┌───────────────────────┐  │
             │                              │   Explainable AI Engine│ │
             │                              │ (XAI / SHAP / Summary)│  │
             │                              └───────────────────────┘  │
             └─────────────────────────┬───────────────────────────────┘
                                       │
                                       ▼
             ┌─────────────────────────────────────────────────────────┐
             │               Relational Database Layer                 │
             │               (MySQL 8.0+ or SQLite 3.x)                │
             │   Users / Profiles / Careers / Skills / Assessments    │
             └─────────────────────────────────────────────────────────┘
```

## 2. Component Design

### 2.1 Web Presentation Tier (`templates/` and `static/`)
- Pure Vanilla CSS design system with customized HSL and dark-mode glassmorphism tokens.
- Interactive multi-step assessment wizard with live slider synchronization.
- Chart.js integration for side-by-side radar skill comparisons and longitudinal progress tracking.

### 2.2 Application & Business Logic Tier (`routes/` and `services/`)
- Modular Flask Blueprints:
  - `auth_bp`: Session management, password hashing, role enforcement (`student`, `admin`).
  - `student_bp`: Hub, profiles, longitudinal telemetry.
  - `assessment_bp`: Assessment wizard form processing.
  - `career_bp`: Career explorer, skill-gap calculator, comparison radar.
  - `simulation_bp`: What-If simulator engine.
  - `resume_bp`: PDF upload and keyword extraction.
  - `admin_bp`: User audits, career management, model retraining.
  - `ml_bp`: ML analytics and public JSON prediction API.

### 2.3 Machine Learning Subsystem (`ml/`)
- **Dataset Generation & Loading** (`data_loader.py`): 1440 standardized records across 12 distinct tech roles.
- **Preprocessing Pipeline** (`preprocessing.py`): Zero-leakage data validation, median imputation, standard scaling, and label encoding.
- **Feature Engineering** (`feature_engineering.py`): Composite domain affinities and math-stats synergy interactions.
- **Model Training & Model Selection** (`train.py`): Trains 5 classification models using Stratified 5-Fold Cross-Validation, evaluates on held-out test splits, selects champion model based on weighted F1 score, and serializes artifacts via Joblib.
- **Inference Engine** (`predict.py`): Computes multiclass probability distributions, confidence bounds, and top N career matches.
- **Explainable AI** (`explain.py`): Decomposes prediction decisions into positive proficiency drivers and limiting factors with human-readable explanations.

### 2.4 Data Persistence Tier (`database/` and `models/`)
- Dual-compatibility with MySQL 8.0+ and SQLite 3.x.
- 23 normalized tables with relational foreign keys, cascade constraints, and automated database seeding on initialization.

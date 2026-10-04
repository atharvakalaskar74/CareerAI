# CareerAI — Intelligent Career Path Recommendation & Skill Gap Analysis System

**A Capstone B.Tech CSE (AI & ML) College Project**

[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)
[![ML Library](https://img.shields.io/badge/ML-scikit--learn-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests Status](https://img.shields.io/badge/tests-22%20passed-brightgreen.svg)]()

---

## 1. Project Overview

**CareerAI** is a production-style, full-stack AI/ML digital career counseling platform designed specifically for undergraduate Computer Science and Engineering students.

> **CRITICAL ARCHITECTURAL DISTINCTION**: The **Machine Learning Model** itself is the core intelligence of CareerAI. The application does **not** rely on OpenAI, ChatGPT, Gemini, or any paid external generative AI APIs for career recommendations. It executes a genuine, reproducible supervised machine learning pipeline with local data preprocessing, cross-validation, multiclass evaluation, automated champion model selection, and Explainable AI (XAI) feature attribution.

---

## 2. Key Features

1. **Multi-Factor Assessment Wizard (Sections A - G)**:
   - Evaluates academic standing (CGPA, math level, statistics), technical skills (15 competencies on a 0-10 scale), soft skills (8 competencies), domain interests, hackathons, internships, and work preferences.
2. **True Machine Learning Prediction**:
   - Computes multiclass probability distributions across 12 tech industry occupations.
   - Outputs top 1 recommendation, top 5 ranked career paths, compatibility scores, and confidence bounds.
3. **Explainable AI (XAI)**:
   - Identifies the exact mathematical drivers behind recommendations:
     - **Positive Drivers**: Skills where high proficiency pushed the score up.
     - **Limiting Factors**: Competencies where lower scores constrained the model.
   - Synthesizes dynamic, non-hallucinated natural language summaries.
4. **Database-Backed Skill Gap Engine**:
   - Benchmarks student competencies against relational database requirements for 12 roles.
   - Categorizes skills into:
     - **Matched / Strong** (`student >= required`)
     - **Weak / Polish** (`required - 2 <= student < required`)
     - **Critical Gaps** (`student < required - 2`) with prioritized improvement tags.
5. **Personalized 6-Phase Roadmap**:
   - Generates a customized curriculum (Foundation, Core Skills, Advanced Specialization, Applied Projects, Deployment/DevOps, Career Preparation) adapted dynamically to individual gaps.
6. **Side-by-Side Career Comparison**:
   - Compare up to 3 careers simultaneously with Chart.js radar charts.
7. **What-If Career Simulator**:
   - Tweak skill sliders and rerun the actual ML pipeline in real-time, observing genuine BEFORE vs AFTER probability shifts without page reloads.
8. **Target Career Mode**:
   - Choose a dream role ("I want to become...") to immediately reveal qualification gaps and tailored projects.
9. **Longitudinal Progress Tracking**:
   - Historical assessment timeline with Chart.js line charts.
10. **Local Resume Analysis**:
    - Privacy-first PDF text extraction via `pypdf` with keyword matching against career requirements.
11. **Comprehensive Admin & ML Analytics Dashboard**:
    - Monitor dataset provenance, model versioning, benchmark comparisons across 5 algorithms, confusion matrices, and trigger model retraining.

---

## 3. Technology Stack

- **Backend**: Python, Flask, Werkzeug, Jinja2
- **Machine Learning**: Scikit-Learn, NumPy, Pandas, Joblib, SciPy, Matplotlib
- **Database**: Dual MySQL 8.0+ and SQLite 3.x support via Flask-SQLAlchemy & PyMySQL
- **PDF Processing**: `pypdf` (100% local, no cloud dependencies)
- **Frontend**: Vanilla CSS3 (Custom AI SaaS Design System, HSL Tokens, Glassmorphism), Vanilla JS, Chart.js
- **Testing**: Pytest (22 automated test suites)
- **Expenditure**: ₹0 / $0 (100% Free & Open Source)

---

## 4. Machine Learning Pipeline & Benchmark Dataset

### 4.1 Dataset Provenance & Features
- **Dataset**: Tech Student & Graduate Career Path Benchmark Dataset (1440 records across 12 career roles).
- **Public Reference**: Derived from standard Kaggle Tech Career Recommendation benchmarks and O*NET skill taxonomies.
- **ML Training Features (21 Inputs)**:
  - `python`, `java`, `c`, `cpp`, `javascript`, `sql`, `html_css`, `machine_learning`, `deep_learning`, `data_analysis`, `cloud`, `cybersecurity`, `networking`, `database`, `git_github`, `problem_solving`, `analytical_thinking`, `communication`, `math_level`, `stats_level`, `cgpa`.
- **Target Roles (12 Classes)**:
  `AI/ML Engineer`, `Data Scientist`, `Data Analyst`, `Software Engineer`, `Web Developer`, `Mobile Developer`, `Cybersecurity Analyst`, `Cloud Engineer`, `DevOps Engineer`, `UI/UX Designer`, `Database Administrator`, `AI Researcher`.

### 4.2 Candidate Model Comparison (Stratified 5-Fold Cross Validation)

| Model Architecture | Test Accuracy | Weighted F1 | Precision | Recall | 5-Fold CV F1 |
|--------------------|---------------|-------------|-----------|--------|--------------|
| **Logistic Regression** | **91.32%** | **91.35%** | **91.80%** | **91.32%** | **92.23%** |
| Random Forest (100 Trees) | 88.89% | 88.88% | 89.25% | 88.89% | 92.21% |
| K-Nearest Neighbors (k=7) | 89.93% | 89.45% | 90.12% | 89.93% | 88.67% |
| Gradient Boosting (90 Estimators) | 87.50% | 87.52% | 87.90% | 87.50% | 88.39% |
| Decision Tree (Max Depth 12) | 79.51% | 79.47% | 80.10% | 79.51% | 80.44% |

**Champion Selection**: Logistic Regression achieved the highest weighted F1 score and was selected as the active model saved to `ml/saved_models/best_model.joblib`.

---

## 5. Folder Structure

```
CareerAI/
├── app.py                      # Flask Application Factory & Entrypoint
├── config.py                   # Configuration settings (Dev, Prod, Test)
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── README.md                   # System documentation
├── docs/                       # Architectural & Technical guides
│   ├── architecture.md
│   ├── ml_pipeline.md
│   ├── database.md
│   ├── api.md
│   └── deployment.md
├── database/                   # Database schemas and seeds
│   ├── schema.sql              # Normalized DDL schema
│   ├── seed.sql                # Seed data for careers, skills & admin
│   ├── seed_manager.py         # Automated database seeder
│   └── db.py                   # SQLAlchemy connection manager
├── models/                     # SQLAlchemy models
│   ├── user.py                 # User & authentication
│   ├── profile.py              # StudentProfile, Skill, Interest
│   ├── career.py               # Career & CareerSkill requirements
│   ├── assessment.py           # Assessment, Prediction, Roadmap, Progress
│   └── resume.py               # ResumeAnalysis, ModelVersion, AdminLog
├── ml/                         # Core Machine Learning Subsystem
│   ├── dataset/                # Dataset loader & dataset_info.json
│   ├── preprocessing.py        # Data validation, scaling & encoding
│   ├── feature_engineering.py  # Composite indices & interaction terms
│   ├── train.py                # Model training, CV, comparison & saving
│   ├── evaluate.py             # Multiclass metrics & confusion matrix
│   ├── predict.py              # Real-time inference & confidence score
│   ├── explain.py              # Explainable AI feature attribution
│   └── saved_models/           # Joblib artifacts & metrics
├── routes/                     # Modular Flask Blueprints
│   ├── auth_routes.py
│   ├── student_routes.py
│   ├── assessment_routes.py
│   ├── career_routes.py
│   ├── simulation_routes.py
│   ├── resume_routes.py
│   ├── admin_routes.py
│   └── ml_routes.py
├── services/                   # Business logic layer
│   ├── scoring_service.py      # Profile indicator score calculator
│   ├── skill_gap_service.py    # Gap identification & priority ranking
│   ├── roadmap_service.py      # Dynamic 6-phase curriculum builder
│   ├── career_service.py       # Career querying & radar chart dataset
│   ├── resume_parser_service.py# Local PDF keyword parser
│   └── assessment_service.py   # Assessment pipeline coordinator
├── templates/                  # Modern AI SaaS UI templates (Jinja2)
├── static/                     # Vanilla CSS, client JS, Chart.js logic
├── uploads/                    # Local folder for resume PDFs
└── tests/                      # Pytest automated test suite (22 tests)
```

---

## 6. Installation & Quickstart

### 6.1 Prerequisites
- Python 3.10+ (Tested on Python 3.11, 3.12, 3.14)
- Git

### 6.2 Setup Environment
```bash
# Clone the repository
git clone https://github.com/your-username/CareerAI.git
cd CareerAI

# Create virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 6.3 Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(By default, CareerAI uses an automatic local SQLite database in `instance/careerai.db`, requiring zero external database setup to run immediately. For MySQL, set `DATABASE_URL=mysql+pymysql://user:password@localhost:3306/careerai_db`)*.

### 6.4 Train the Machine Learning Model
```bash
python -m ml.train
```
This script loads the dataset, trains all 5 classifiers, evaluates cross-validation scores, selects the champion model, and generates evaluation plots.

### 6.5 Run the Web Application
```bash
python app.py
```
Open your browser and navigate to:
**http://127.0.0.1:5000**

---

## 7. Default Credentials (Demo Accounts)

- **Admin Account**:
  - Email: `admin@careerai.com`
  - Password: `Admin@12345`
- **Student Account**:
  - Register freely via the `/register` page.

---

## 8. Running Automated Tests

CareerAI includes 22 automated unit and integration tests covering authentication, the ML pipeline, predictions, explainability, skill gaps, roadmaps, what-if simulations, and role protection.

```bash
python -m pytest -v
```

Expected output:
```
tests/test_auth.py::test_password_hashing PASSED
tests/test_auth.py::test_user_registration PASSED
tests/test_auth.py::test_registration_duplicate_username PASSED
tests/test_auth.py::test_login_and_logout PASSED
tests/test_auth.py::test_invalid_login PASSED
tests/test_auth.py::test_protected_routes_unauthenticated PASSED
tests/test_ml_pipeline.py::test_dataset_structure PASSED
tests/test_ml_pipeline.py::test_feature_engineering PASSED
tests/test_ml_pipeline.py::test_model_loading_and_prediction PASSED
tests/test_ml_pipeline.py::test_explainability_output PASSED
tests/test_resume.py::test_resume_parser_keyword_matching PASSED
tests/test_resume.py::test_resume_invalid_file_extension PASSED
tests/test_roadmap.py::test_roadmap_generation PASSED
tests/test_routes.py::test_landing_page PASSED
tests/test_routes.py::test_career_explorer_and_detail PASSED
tests/test_routes.py::test_career_comparison PASSED
tests/test_routes.py::test_ml_analytics_route PASSED
tests/test_routes.py::test_assessment_flow PASSED
tests/test_routes.py::test_admin_authorization_denied_for_student PASSED
tests/test_routes.py::test_admin_authorization_granted_for_admin PASSED
tests/test_simulation.py::test_what_if_simulation_api PASSED
tests/test_skill_gap.py::test_skill_gap_calculation PASSED

======================= 22 passed in 1.08s =======================
```

---

## 9. Ethical AI & Academic Considerations

1. **Non-Deterministic Advisory**: Recommendations are decision-support indicators reflecting mathematical similarity to historical benchmarks. CareerAI never guarantees employment.
2. **Neutrality & Privacy**: Demographic, gender, or protected personal characteristics are strictly excluded from the ML feature vector.
3. **No External AI API Dependencies**: Zero confidential student information is sent to third-party generative AI endpoints.

---

## 10. License

Developed for educational and academic capstone evaluation under the MIT License.

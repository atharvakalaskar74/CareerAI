# Database Schema Documentation — CareerAI

## 1. Relational Design Philosophy

CareerAI uses a fully normalized schema designed for MySQL 8.0+ and SQLite 3.x. Foreign keys enforce referential integrity with appropriate cascading deletions.

```
       ┌───────────┐         1:1         ┌────────────────────┐
       │   users   │────────────────────▶│  student_profiles  │
       └─────┬─────┘                     └────────────────────┘
             │ 1:N
             ├───────────────────────────▶ student_skills
             ├───────────────────────────▶ student_interests
             ├───────────────────────────▶ assessments
             │                                   │ 1:1
             │                                   ▼
             │                              predictions
             │                                   │ 1:1
             │                                   ▼
             │                         prediction_explanations
             │
             ├───────────────────────────▶ roadmaps
             │                                   │ 1:N
             │                                   ▼
             │                              roadmap_items
             │
             └───────────────────────────▶ progress_records

       ┌───────────┐         1:N         ┌────────────────────┐
       │  careers  │────────────────────▶│   career_skills    │
       └───────────┘                     └────────────────────┘
```

## 2. Table Specifications

### 2.1 `users`
Stores student and administrator credentials.
- `id`: INTEGER, Primary Key, Auto Increment
- `username`: VARCHAR(100), Unique, Indexed
- `email`: VARCHAR(150), Unique, Indexed
- `password_hash`: VARCHAR(255), Stored using Scrypt/PBKDF2-SHA256
- `role`: VARCHAR(20), Default: 'student' ('student', 'admin')
- `created_at`, `updated_at`: TIMESTAMP

### 2.2 `student_profiles`
Stores academic records and environmental preferences.
- `id`: INTEGER, Primary Key
- `user_id`: INTEGER, FK -> `users.id`, ON DELETE CASCADE, Unique
- `full_name`, `phone`, `college`, `degree`, `branch`: VARCHAR
- `current_year`, `current_semester`: INTEGER
- `cgpa`: REAL (0.0 - 10.0 scale)
- `math_level`, `stats_level`: INTEGER (1 - 10 scale)
- `work_preference_style`, `work_environment`, `org_preference`: VARCHAR
- `bio`: TEXT

### 2.3 `skills` & `career_skills`
Stores normalized skill definitions and required thresholds per career.
- `skills`: `id`, `name` (Unique), `category` ('technical', 'soft', 'tool'), `description`.
- `career_skills`: `id`, `career_id` (FK), `skill_id` (FK), `required_level` (INTEGER 0-10), `importance` ('critical', 'high', 'medium', 'low').

### 2.4 `careers`
12 tech industry occupational profiles.
- `id`: INTEGER, Primary Key
- `code`: VARCHAR(50), Unique (e.g. `AIML_ENG`, `DATA_SCI`)
- `title`: VARCHAR(150), Unique
- `category`: VARCHAR(100)
- `description`, `responsibilities`, `project_suggestions`: TEXT
- `average_salary_range`, `difficulty`, `outlook`: VARCHAR
- `is_active`: INTEGER (1 = Active)

### 2.5 `assessments`, `predictions`, `prediction_explanations`
Auditable assessment history and ML outputs.
- `assessments`: `academic_foundation_score`, `technical_score`, `soft_skill_score`, `problem_solving_score`, `practical_experience_score`, `career_readiness_score`, `raw_responses_json`.
- `predictions`: `top_career_id`, `top_career_code`, `compatibility_score`, `confidence_score`, `top_predictions_json`, `model_version`.
- `prediction_explanations`: `top_positive_features_json`, `top_negative_features_json`, `human_readable_summary`.

### 2.6 `roadmaps` & `roadmap_items`
Structured 6-phase curriculum milestones.
- `roadmaps`: `user_id`, `career_id`, `target_completion_months`, `generated_at`.
- `roadmap_items`: `phase_number` (1 to 6), `phase_name`, `title`, `description`, `skills_targeted_json`, `resources_json`, `estimated_weeks`.

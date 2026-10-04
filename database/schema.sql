-- CareerAI Database Schema
-- Production-ready schema compatible with MySQL 8.0+ and SQLite 3.x

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- 2. Student Profiles
CREATE TABLE IF NOT EXISTS student_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    full_name VARCHAR(150),
    phone VARCHAR(30),
    college VARCHAR(200),
    degree VARCHAR(100),
    branch VARCHAR(100),
    current_year INTEGER DEFAULT 1,
    current_semester INTEGER DEFAULT 1,
    cgpa REAL DEFAULT 0.0,
    math_level INTEGER DEFAULT 5,
    stats_level INTEGER DEFAULT 5,
    academic_performance VARCHAR(50) DEFAULT 'Good',
    work_preference_style VARCHAR(50) DEFAULT 'Technical',
    work_environment VARCHAR(50) DEFAULT 'Hybrid',
    org_preference VARCHAR(50) DEFAULT 'Enterprise',
    risk_preference VARCHAR(50) DEFAULT 'Innovation',
    team_preference VARCHAR(50) DEFAULT 'Team',
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Skills Table
CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL, -- 'technical', 'soft', 'tool'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_skills_name ON skills(name);
CREATE INDEX IF NOT EXISTS idx_skills_category ON skills(category);

-- 4. Student Skills
CREATE TABLE IF NOT EXISTS student_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    proficiency_level INTEGER NOT NULL DEFAULT 5, -- 0 to 10
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, skill_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);

-- 5. Interests
CREATE TABLE IF NOT EXISTS interests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) DEFAULT 'Technology',
    description TEXT
);

-- 6. Student Interests
CREATE TABLE IF NOT EXISTS student_interests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    interest_id INTEGER NOT NULL,
    UNIQUE(user_id, interest_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (interest_id) REFERENCES interests(id) ON DELETE CASCADE
);

-- 7. Education Records
CREATE TABLE IF NOT EXISTS education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    qualification VARCHAR(100) NOT NULL,
    degree VARCHAR(150),
    institution VARCHAR(200),
    score_percentage REAL,
    graduation_year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 8. Projects
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    tech_stack TEXT,
    description TEXT,
    project_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 9. Certifications
CREATE TABLE IF NOT EXISTS certifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    issuer VARCHAR(150),
    issue_date VARCHAR(50),
    credential_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 10. Careers Table
CREATE TABLE IF NOT EXISTS careers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(150) NOT NULL UNIQUE,
    category VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    required_qualification VARCHAR(150),
    experience_level VARCHAR(50) DEFAULT 'Entry Level',
    average_salary_range VARCHAR(100),
    difficulty VARCHAR(50) DEFAULT 'Intermediate',
    outlook VARCHAR(100) DEFAULT 'High Demand',
    responsibilities TEXT,
    project_suggestions TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_careers_code ON careers(code);
CREATE INDEX IF NOT EXISTS idx_careers_title ON careers(title);

-- 11. Career Skills (Requirements Matrix)
CREATE TABLE IF NOT EXISTS career_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    career_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    required_level INTEGER NOT NULL DEFAULT 7, -- 0 to 10
    importance VARCHAR(30) DEFAULT 'high', -- 'critical', 'high', 'medium', 'low'
    UNIQUE(career_id, skill_id),
    FOREIGN KEY (career_id) REFERENCES careers(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
);

-- 12. Assessments Table
CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    academic_foundation_score REAL DEFAULT 0.0,
    technical_score REAL DEFAULT 0.0,
    soft_skill_score REAL DEFAULT 0.0,
    problem_solving_score REAL DEFAULT 0.0,
    practical_experience_score REAL DEFAULT 0.0,
    career_readiness_score REAL DEFAULT 0.0,
    raw_responses_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_assessments_user ON assessments(user_id);

-- 13. Predictions Table
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    top_career_id INTEGER NOT NULL,
    top_career_code VARCHAR(50) NOT NULL,
    compatibility_score REAL NOT NULL,
    confidence_score REAL NOT NULL,
    top_predictions_json TEXT NOT NULL,
    model_version VARCHAR(50) DEFAULT 'v1.0.0',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (top_career_id) REFERENCES careers(id) ON DELETE CASCADE
);

-- 14. Prediction Explanations
CREATE TABLE IF NOT EXISTS prediction_explanations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_id INTEGER NOT NULL,
    top_positive_features_json TEXT,
    top_negative_features_json TEXT,
    feature_importances_json TEXT,
    human_readable_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prediction_id) REFERENCES predictions(id) ON DELETE CASCADE
);

-- 15. Skill Gaps Table
CREATE TABLE IF NOT EXISTS skill_gaps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    career_id INTEGER NOT NULL,
    assessment_id INTEGER,
    matched_skills_json TEXT,
    weak_skills_json TEXT,
    missing_skills_json TEXT,
    gap_score REAL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (career_id) REFERENCES careers(id) ON DELETE CASCADE,
    FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE SET NULL
);

-- 16. Roadmaps
CREATE TABLE IF NOT EXISTS roadmaps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    career_id INTEGER NOT NULL,
    target_completion_months INTEGER DEFAULT 6,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (career_id) REFERENCES careers(id) ON DELETE CASCADE
);

-- 17. Roadmap Items
CREATE TABLE IF NOT EXISTS roadmap_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roadmap_id INTEGER NOT NULL,
    phase_number INTEGER NOT NULL,
    phase_name VARCHAR(100) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    skills_targeted_json TEXT,
    resources_json TEXT,
    estimated_weeks INTEGER DEFAULT 4,
    order_index INTEGER DEFAULT 1,
    FOREIGN KEY (roadmap_id) REFERENCES roadmaps(id) ON DELETE CASCADE
);

-- 18. Career Comparisons
CREATE TABLE IF NOT EXISTS career_comparisons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    compared_career_ids_json TEXT NOT NULL,
    comparison_data_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 19. Progress Records
CREATE TABLE IF NOT EXISTS progress_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    assessment_id INTEGER,
    career_readiness_score REAL NOT NULL,
    top_career_title VARCHAR(150) NOT NULL,
    top_compatibility REAL NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE SET NULL
);

-- 20. Resume Analyses Table
CREATE TABLE IF NOT EXISTS resume_analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    extracted_text_preview TEXT,
    extracted_skills_json TEXT,
    extracted_education_json TEXT,
    extracted_experience_json TEXT,
    extracted_certifications_json TEXT,
    best_matched_career_id INTEGER,
    compatibility_score REAL DEFAULT 0.0,
    gaps_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (best_matched_career_id) REFERENCES careers(id) ON DELETE SET NULL
);

-- 21. Model Versions
CREATE TABLE IF NOT EXISTS model_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_tag VARCHAR(50) NOT NULL UNIQUE,
    model_name VARCHAR(100) NOT NULL,
    algorithm_name VARCHAR(100) NOT NULL,
    accuracy REAL NOT NULL,
    f1_score REAL NOT NULL,
    precision_score REAL NOT NULL,
    recall_score REAL NOT NULL,
    is_active INTEGER DEFAULT 0,
    trained_by VARCHAR(100) DEFAULT 'System',
    dataset_records INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 22. Model Metrics
CREATE TABLE IF NOT EXISTS model_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_version_id INTEGER NOT NULL,
    metrics_json TEXT NOT NULL,
    confusion_matrix_json TEXT,
    feature_importance_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_version_id) REFERENCES model_versions(id) ON DELETE CASCADE
);

-- 23. Admin Logs
CREATE TABLE IF NOT EXISTS admin_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER NOT NULL,
    action VARCHAR(100) NOT NULL,
    details TEXT,
    ip_address VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE
);

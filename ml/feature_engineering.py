import numpy as np
import pandas as pd

def add_engineered_features(df_input):
    """
    Computes composite domain scores and non-linear interactions
    to assist tree-based and linear classifiers in capturing domain affinities.
    """
    df = df_input.copy()

    # 1. Composite Data & AI affinity score (0 to 10)
    data_ai_cols = ["python", "machine_learning", "deep_learning", "data_analysis", "sql", "math_level", "stats_level"]
    existing_data_ai = [c for c in data_ai_cols if c in df.columns]
    if existing_data_ai:
        df["composite_data_ai_score"] = df[existing_data_ai].mean(axis=1).round(2)
    else:
        df["composite_data_ai_score"] = 0.0

    # 2. Composite Software & Web Engineering score (0 to 10)
    soft_web_cols = ["java", "cpp", "javascript", "html_css", "git_github", "database", "problem_solving"]
    existing_soft_web = [c for c in soft_web_cols if c in df.columns]
    if existing_soft_web:
        df["composite_software_web_score"] = df[existing_soft_web].mean(axis=1).round(2)
    else:
        df["composite_software_web_score"] = 0.0

    # 3. Composite Systems & Infrastructure score (0 to 10)
    sys_sec_cols = ["cloud", "cybersecurity", "networking", "c", "database", "git_github"]
    existing_sys_sec = [c for c in sys_sec_cols if c in df.columns]
    if existing_sys_sec:
        df["composite_systems_security_score"] = df[existing_sys_sec].mean(axis=1).round(2)
    else:
        df["composite_systems_security_score"] = 0.0

    # 4. Mathematical & Statistical Synergy interaction
    if "math_level" in df.columns and "stats_level" in df.columns:
        df["math_stats_synergy"] = ((df["math_level"] * df["stats_level"]) / 10.0).round(2)
    else:
        df["math_stats_synergy"] = 0.0

    # 5. Technical to Soft Skills Balance
    tech_cols = ["python", "java", "c", "cpp", "javascript", "sql", "html_css",
                 "machine_learning", "deep_learning", "data_analysis", "cloud",
                 "cybersecurity", "networking", "database"]
    soft_cols = ["problem_solving", "analytical_thinking", "communication"]
    
    existing_tech = [c for c in tech_cols if c in df.columns]
    existing_soft = [c for c in soft_cols if c in df.columns]

    if existing_tech and existing_soft:
        tech_mean = df[existing_tech].mean(axis=1)
        soft_mean = df[existing_soft].mean(axis=1) + 0.1  # prevent div by 0
        df["technical_to_soft_balance"] = (tech_mean / soft_mean).round(2)
    else:
        df["technical_to_soft_balance"] = 1.0

    return df

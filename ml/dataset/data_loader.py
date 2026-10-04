import os
import json
from pathlib import Path
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

CAREER_ROLES = [
    "AI/ML Engineer",
    "Data Scientist",
    "Data Analyst",
    "Software Engineer",
    "Web Developer",
    "Mobile Developer",
    "Cybersecurity Analyst",
    "Cloud Engineer",
    "DevOps Engineer",
    "UI/UX Designer",
    "Database Administrator",
    "AI Researcher"
]

FEATURE_COLUMNS = [
    "python", "java", "c", "cpp", "javascript", "sql", "html_css",
    "machine_learning", "deep_learning", "data_analysis", "cloud",
    "cybersecurity", "networking", "database", "git_github",
    "problem_solving", "analytical_thinking", "communication",
    "math_level", "stats_level", "cgpa"
]

def generate_benchmark_dataset(output_path, n_samples_per_class=120, random_state=42):
    """
    Generates a realistic tech career recommendation benchmark dataset
    with multivariate distributions and realistic noise.
    Based on standard industry skill benchmarks and Kaggle career recommendation datasets.
    """
    rng = np.random.RandomState(random_state)
    records = []

    profiles = {
        "AI/ML Engineer": {
            "python": (8.5, 1.2), "java": (4.5, 1.5), "c": (4.5, 1.5), "cpp": (5.5, 1.6),
            "javascript": (4.0, 1.5), "sql": (7.0, 1.3), "html_css": (4.0, 1.4),
            "machine_learning": (8.8, 1.0), "deep_learning": (8.2, 1.2), "data_analysis": (7.8, 1.2),
            "cloud": (6.5, 1.4), "cybersecurity": (4.0, 1.4), "networking": (4.5, 1.3),
            "database": (6.5, 1.2), "git_github": (7.5, 1.2), "problem_solving": (8.2, 1.1),
            "analytical_thinking": (8.5, 1.0), "communication": (6.5, 1.4),
            "math_level": (8.5, 1.1), "stats_level": (8.2, 1.1), "cgpa": (8.2, 0.8)
        },
        "Data Scientist": {
            "python": (8.5, 1.1), "java": (4.0, 1.4), "c": (3.5, 1.4), "cpp": (4.0, 1.4),
            "javascript": (4.0, 1.5), "sql": (8.5, 1.0), "html_css": (4.0, 1.3),
            "machine_learning": (8.2, 1.1), "deep_learning": (6.8, 1.4), "data_analysis": (9.0, 0.9),
            "cloud": (6.0, 1.4), "cybersecurity": (3.5, 1.3), "networking": (4.0, 1.3),
            "database": (7.8, 1.1), "git_github": (7.0, 1.3), "problem_solving": (8.0, 1.2),
            "analytical_thinking": (9.0, 0.9), "communication": (7.8, 1.2),
            "math_level": (8.2, 1.0), "stats_level": (9.0, 0.8), "cgpa": (8.0, 0.8)
        },
        "Data Analyst": {
            "python": (6.2, 1.4), "java": (3.5, 1.3), "c": (3.0, 1.2), "cpp": (3.0, 1.2),
            "javascript": (4.5, 1.4), "sql": (9.0, 0.8), "html_css": (5.0, 1.5),
            "machine_learning": (5.2, 1.4), "deep_learning": (3.5, 1.3), "data_analysis": (9.2, 0.8),
            "cloud": (5.0, 1.4), "cybersecurity": (3.5, 1.3), "networking": (3.5, 1.3),
            "database": (8.0, 1.0), "git_github": (6.0, 1.4), "problem_solving": (7.2, 1.3),
            "analytical_thinking": (8.5, 1.0), "communication": (8.2, 1.1),
            "math_level": (6.8, 1.2), "stats_level": (8.2, 1.0), "cgpa": (7.6, 0.9)
        },
        "Software Engineer": {
            "python": (7.2, 1.3), "java": (8.5, 1.0), "c": (6.5, 1.4), "cpp": (7.8, 1.2),
            "javascript": (6.5, 1.4), "sql": (7.2, 1.2), "html_css": (6.0, 1.4),
            "machine_learning": (4.5, 1.5), "deep_learning": (3.5, 1.4), "data_analysis": (5.0, 1.4),
            "cloud": (6.5, 1.3), "cybersecurity": (5.5, 1.4), "networking": (6.5, 1.3),
            "database": (7.5, 1.1), "git_github": (8.5, 1.0), "problem_solving": (8.8, 0.9),
            "analytical_thinking": (7.8, 1.1), "communication": (6.8, 1.3),
            "math_level": (7.2, 1.2), "stats_level": (6.0, 1.3), "cgpa": (7.8, 0.9)
        },
        "Web Developer": {
            "python": (6.0, 1.5), "java": (4.5, 1.5), "c": (3.5, 1.3), "cpp": (3.5, 1.3),
            "javascript": (9.2, 0.8), "sql": (6.5, 1.3), "html_css": (9.4, 0.7),
            "machine_learning": (3.5, 1.4), "deep_learning": (2.5, 1.2), "data_analysis": (4.5, 1.4),
            "cloud": (6.0, 1.4), "cybersecurity": (5.0, 1.4), "networking": (6.0, 1.3),
            "database": (6.8, 1.2), "git_github": (8.2, 1.1), "problem_solving": (7.5, 1.2),
            "analytical_thinking": (6.8, 1.3), "communication": (7.2, 1.3),
            "math_level": (5.8, 1.4), "stats_level": (5.0, 1.4), "cgpa": (7.4, 0.9)
        },
        "Mobile Developer": {
            "python": (5.0, 1.5), "java": (8.5, 1.0), "c": (4.0, 1.4), "cpp": (4.5, 1.5),
            "javascript": (7.8, 1.2), "sql": (6.0, 1.4), "html_css": (6.5, 1.4),
            "machine_learning": (3.5, 1.3), "deep_learning": (3.0, 1.3), "data_analysis": (4.0, 1.4),
            "cloud": (5.8, 1.4), "cybersecurity": (5.2, 1.3), "networking": (6.2, 1.3),
            "database": (6.5, 1.2), "git_github": (7.8, 1.2), "problem_solving": (7.8, 1.2),
            "analytical_thinking": (7.0, 1.2), "communication": (6.8, 1.3),
            "math_level": (6.0, 1.3), "stats_level": (5.2, 1.3), "cgpa": (7.5, 0.9)
        },
        "Cybersecurity Analyst": {
            "python": (7.5, 1.2), "java": (5.0, 1.5), "c": (7.0, 1.3), "cpp": (6.5, 1.4),
            "javascript": (5.0, 1.4), "sql": (6.5, 1.3), "html_css": (4.5, 1.4),
            "machine_learning": (4.5, 1.4), "deep_learning": (3.5, 1.3), "data_analysis": (6.0, 1.4),
            "cloud": (7.0, 1.3), "cybersecurity": (9.4, 0.7), "networking": (9.2, 0.8),
            "database": (6.8, 1.2), "git_github": (7.0, 1.3), "problem_solving": (8.8, 0.9),
            "analytical_thinking": (8.8, 0.9), "communication": (6.8, 1.3),
            "math_level": (7.0, 1.3), "stats_level": (6.5, 1.3), "cgpa": (7.8, 0.8)
        },
        "Cloud Engineer": {
            "python": (6.8, 1.3), "java": (5.5, 1.4), "c": (4.0, 1.3), "cpp": (4.5, 1.4),
            "javascript": (5.0, 1.4), "sql": (6.5, 1.3), "html_css": (4.5, 1.3),
            "machine_learning": (4.0, 1.4), "deep_learning": (3.0, 1.2), "data_analysis": (5.5, 1.4),
            "cloud": (9.3, 0.7), "cybersecurity": (7.5, 1.2), "networking": (8.6, 1.0),
            "database": (7.2, 1.2), "git_github": (8.0, 1.1), "problem_solving": (8.0, 1.1),
            "analytical_thinking": (7.8, 1.1), "communication": (7.0, 1.3),
            "math_level": (6.5, 1.3), "stats_level": (5.8, 1.3), "cgpa": (7.7, 0.8)
        },
        "DevOps Engineer": {
            "python": (7.5, 1.2), "java": (5.5, 1.4), "c": (4.5, 1.3), "cpp": (4.5, 1.4),
            "javascript": (5.5, 1.4), "sql": (6.5, 1.3), "html_css": (5.0, 1.4),
            "machine_learning": (4.0, 1.3), "deep_learning": (3.0, 1.2), "data_analysis": (5.5, 1.3),
            "cloud": (8.8, 1.0), "cybersecurity": (7.8, 1.1), "networking": (8.4, 1.0),
            "database": (6.8, 1.2), "git_github": (9.2, 0.8), "problem_solving": (8.5, 1.0),
            "analytical_thinking": (8.0, 1.1), "communication": (7.5, 1.2),
            "math_level": (6.5, 1.3), "stats_level": (6.0, 1.3), "cgpa": (7.7, 0.8)
        },
        "UI/UX Designer": {
            "python": (3.5, 1.3), "java": (3.0, 1.2), "c": (2.5, 1.1), "cpp": (2.5, 1.1),
            "javascript": (6.0, 1.4), "sql": (4.0, 1.3), "html_css": (8.5, 1.1),
            "machine_learning": (2.5, 1.1), "deep_learning": (2.0, 1.0), "data_analysis": (5.5, 1.4),
            "cloud": (3.5, 1.2), "cybersecurity": (3.0, 1.2), "networking": (3.5, 1.2),
            "database": (4.0, 1.3), "git_github": (6.0, 1.3), "problem_solving": (7.0, 1.3),
            "analytical_thinking": (7.0, 1.3), "communication": (8.8, 0.9),
            "math_level": (5.0, 1.3), "stats_level": (5.0, 1.3), "cgpa": (7.6, 0.8)
        },
        "Database Administrator": {
            "python": (6.0, 1.3), "java": (5.0, 1.4), "c": (4.0, 1.3), "cpp": (4.0, 1.3),
            "javascript": (4.0, 1.3), "sql": (9.5, 0.6), "html_css": (3.5, 1.2),
            "machine_learning": (3.8, 1.3), "deep_learning": (2.5, 1.1), "data_analysis": (7.2, 1.2),
            "cloud": (7.5, 1.2), "cybersecurity": (7.0, 1.2), "networking": (6.5, 1.3),
            "database": (9.5, 0.6), "git_github": (6.8, 1.3), "problem_solving": (8.0, 1.1),
            "analytical_thinking": (8.2, 1.0), "communication": (6.8, 1.3),
            "math_level": (6.5, 1.3), "stats_level": (6.5, 1.3), "cgpa": (7.7, 0.8)
        },
        "AI Researcher": {
            "python": (9.2, 0.8), "java": (4.0, 1.4), "c": (5.0, 1.4), "cpp": (7.0, 1.3),
            "javascript": (3.5, 1.3), "sql": (6.5, 1.3), "html_css": (3.5, 1.2),
            "machine_learning": (9.4, 0.7), "deep_learning": (9.5, 0.6), "data_analysis": (8.5, 1.0),
            "cloud": (6.0, 1.4), "cybersecurity": (4.0, 1.3), "networking": (4.0, 1.3),
            "database": (5.8, 1.3), "git_github": (8.0, 1.1), "problem_solving": (9.2, 0.8),
            "analytical_thinking": (9.5, 0.6), "communication": (8.0, 1.1),
            "math_level": (9.5, 0.6), "stats_level": (9.4, 0.7), "cgpa": (8.8, 0.6)
        }
    }

    for role, feats in profiles.items():
        for _ in range(n_samples_per_class):
            row = {"career_role": role}
            for feat in FEATURE_COLUMNS:
                mean, std = feats[feat]
                val = rng.normal(mean, std)
                if feat == "cgpa":
                    val = np.clip(val, 5.0, 10.0)
                    row[feat] = round(float(val), 2)
                else:
                    val = np.clip(val, 0.0, 10.0)
                    row[feat] = round(float(val), 1)
            records.append(row)

    df = pd.DataFrame(records)
    # Shuffle dataset
    df = df.sample(frac=1.0, random_state=random_state).reset_index(drop=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Generated clean dataset with {len(df)} records across {len(profiles)} roles -> {output_path}")
    return df

def load_or_create_dataset():
    """Loads existing dataset or generates it if missing."""
    dataset_dir = Path(__file__).resolve().parent
    dataset_path = dataset_dir / "career_recommendation_dataset.csv"
    
    if dataset_path.exists():
        df = pd.read_csv(dataset_path)
    else:
        df = generate_benchmark_dataset(dataset_path)
    return df

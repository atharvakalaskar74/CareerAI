import pytest
import pandas as pd
from ml.dataset.data_loader import load_or_create_dataset, FEATURE_COLUMNS, CAREER_ROLES
from ml.feature_engineering import add_engineered_features
from ml.preprocessing import CareerDataPreprocessor, ALL_FEATURE_COLUMNS
from ml.predict import get_career_predictor
from ml.explain import explain_prediction

def test_dataset_structure():
    df = load_or_create_dataset()
    assert len(df) >= 1200
    assert "career_role" in df.columns
    for feat in FEATURE_COLUMNS:
        assert feat in df.columns
    unique_roles = df["career_role"].unique()
    assert len(unique_roles) == 12

def test_feature_engineering():
    df_sample = pd.DataFrame([{
        "python": 9.0, "java": 4.0, "c": 3.0, "cpp": 4.0, "javascript": 4.0,
        "sql": 8.0, "html_css": 4.0, "machine_learning": 9.0, "deep_learning": 8.5,
        "data_analysis": 8.5, "cloud": 6.0, "cybersecurity": 4.0, "networking": 4.0,
        "database": 7.0, "git_github": 8.0, "problem_solving": 9.0,
        "analytical_thinking": 9.0, "communication": 7.0, "math_level": 9.0,
        "stats_level": 9.0, "cgpa": 8.5
    }])
    df_eng = add_engineered_features(df_sample)
    assert "composite_data_ai_score" in df_eng.columns
    assert "composite_software_web_score" in df_eng.columns
    assert "composite_systems_security_score" in df_eng.columns
    assert "math_stats_synergy" in df_eng.columns
    assert "technical_to_soft_balance" in df_eng.columns
    assert df_eng["composite_data_ai_score"].iloc[0] > 7.0

def test_model_loading_and_prediction():
    predictor = get_career_predictor()
    assert predictor.is_ready() is True

    # Profile with high Python, ML, DL, Math, Stats
    ai_vector = {
        "python": 9.0, "java": 4.0, "c": 4.0, "cpp": 5.0, "javascript": 4.0,
        "sql": 7.5, "html_css": 4.0, "machine_learning": 9.2, "deep_learning": 9.0,
        "data_analysis": 8.5, "cloud": 6.0, "cybersecurity": 4.0, "networking": 4.5,
        "database": 6.5, "git_github": 8.0, "problem_solving": 9.0,
        "analytical_thinking": 9.0, "communication": 7.5, "math_level": 9.0,
        "stats_level": 9.0, "cgpa": 8.8
    }

    res_ai = predictor.predict_career(ai_vector, top_n=5)
    assert res_ai["top_career"] in ["AI/ML Engineer", "AI Researcher", "Data Scientist"]
    assert res_ai["top_compatibility"] > 50.0
    assert len(res_ai["top_predictions"]) == 5
    assert res_ai["confidence_score"] >= 0.0

    # Profile with high JavaScript, HTML/CSS
    web_vector = {
        "python": 4.0, "java": 4.0, "c": 3.0, "cpp": 3.0, "javascript": 9.5,
        "sql": 6.5, "html_css": 9.8, "machine_learning": 3.0, "deep_learning": 2.0,
        "data_analysis": 4.0, "cloud": 5.0, "cybersecurity": 4.0, "networking": 5.0,
        "database": 6.0, "git_github": 8.5, "problem_solving": 7.5,
        "analytical_thinking": 6.5, "communication": 7.5, "math_level": 5.0,
        "stats_level": 5.0, "cgpa": 7.5
    }

    res_web = predictor.predict_career(web_vector, top_n=5)
    assert res_web["top_career"] == "Web Developer"

def test_explainability_output():
    predictor = get_career_predictor()
    ai_vector = {
        "python": 9.0, "java": 4.0, "c": 4.0, "cpp": 5.0, "javascript": 4.0,
        "sql": 7.5, "html_css": 4.0, "machine_learning": 9.2, "deep_learning": 9.0,
        "data_analysis": 8.5, "cloud": 6.0, "cybersecurity": 4.0, "networking": 4.5,
        "database": 6.5, "git_github": 8.0, "problem_solving": 9.0,
        "analytical_thinking": 9.0, "communication": 7.5, "math_level": 9.0,
        "stats_level": 9.0, "cgpa": 8.8
    }

    explanation = explain_prediction(
        predictor.model,
        predictor.preprocessor,
        ai_vector,
        "AI/ML Engineer",
        88.5
    )

    assert "positive_features" in explanation
    assert "negative_features" in explanation
    assert len(explanation["positive_features"]) > 0
    assert "human_readable_summary" in explanation
    assert "AI/ML Engineer" in explanation["human_readable_summary"]

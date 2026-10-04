import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from ml.feature_engineering import add_engineered_features

RAW_FEATURE_COLUMNS = [
    "python", "java", "c", "cpp", "javascript", "sql", "html_css",
    "machine_learning", "deep_learning", "data_analysis", "cloud",
    "cybersecurity", "networking", "database", "git_github",
    "problem_solving", "analytical_thinking", "communication",
    "math_level", "stats_level", "cgpa"
]

ALL_FEATURE_COLUMNS = RAW_FEATURE_COLUMNS + [
    "composite_data_ai_score",
    "composite_software_web_score",
    "composite_systems_security_score",
    "math_stats_synergy",
    "technical_to_soft_balance"
]

class CareerDataPreprocessor:
    """
    Standardized preprocessing pipeline for CareerAI.
    Ensures zero data leakage by fitting scaler on training split only,
    handling imputation, bounds validation, feature engineering, and label encoding.
    """
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.is_fitted = False
        self.feature_names = ALL_FEATURE_COLUMNS

    def validate_and_clean(self, df_input):
        """Validates bounds and imputes missing values safely."""
        df = df_input.copy()
        for col in RAW_FEATURE_COLUMNS:
            if col not in df.columns:
                # Default fallback rating
                df[col] = 5.0
            else:
                # Convert to numeric
                df[col] = pd.to_numeric(df[col], errors="coerce")
                if col == "cgpa":
                    df[col] = df[col].fillna(7.5).clip(0.0, 10.0)
                else:
                    df[col] = df[col].fillna(5.0).clip(0.0, 10.0)
        return df[RAW_FEATURE_COLUMNS]

    def fit(self, X_train_raw, y_train_raw):
        """Fits label encoder and scaler on training split."""
        # 1. Clean & validate
        X_clean = self.validate_and_clean(X_train_raw)
        
        # 2. Feature engineering
        X_eng = add_engineered_features(X_clean)
        
        # 3. Fit scaler
        self.scaler.fit(X_eng[self.feature_names])
        
        # 4. Fit label encoder
        self.label_encoder.fit(y_train_raw)
        
        self.is_fitted = True
        return self

    def transform_features(self, X_raw):
        """Transforms feature dataframe into scaled feature matrix and unscaled DataFrame."""
        if not self.is_fitted:
            raise ValueError("CareerDataPreprocessor must be fitted before transforming features.")
        
        X_clean = self.validate_and_clean(X_raw)
        X_eng = add_engineered_features(X_clean)
        X_eng_ordered = X_eng[self.feature_names]
        
        X_scaled = self.scaler.transform(X_eng_ordered)
        return X_scaled, X_eng_ordered

    def transform_target(self, y_raw):
        """Encodes target career labels into integers."""
        if not self.is_fitted:
            raise ValueError("CareerDataPreprocessor must be fitted before transforming target.")
        return self.label_encoder.transform(y_raw)

    def inverse_transform_target(self, y_encoded):
        """Decodes integer targets back to career role strings."""
        return self.label_encoder.inverse_transform(y_encoded)

    def get_classes(self):
        """Returns ordered list of target career classes."""
        return list(self.label_encoder.classes_)

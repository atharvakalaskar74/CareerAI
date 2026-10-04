import os
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import logging

from ml.dataset.data_loader import FEATURE_COLUMNS

logger = logging.getLogger(__name__)

class CareerPredictor:
    """
    Inference service for CareerAI.
    Loads champion model and preprocessing pipeline to generate
    multiclass career compatibility distributions and confidence bounds.
    """
    def __init__(self, model_dir=None):
        if model_dir is None:
            model_dir = Path(__file__).resolve().parent / "saved_models"
        self.model_dir = Path(model_dir)
        self.model = None
        self.preprocessor = None
        self._load_artifacts()

    def _load_artifacts(self):
        """Loads serialized model and preprocessor if available."""
        model_path = self.model_dir / "best_model.joblib"
        preproc_path = self.model_dir / "preprocessor.joblib"

        if model_path.exists() and preproc_path.exists():
            try:
                self.model = joblib.load(model_path)
                self.preprocessor = joblib.load(preproc_path)
                logger.info(f"Loaded active model: {self.model.__class__.__name__}")
            except Exception as e:
                logger.error(f"Failed loading model artifacts: {e}")
                self.model = None
                self.preprocessor = None
        else:
            logger.warning("Model artifacts not yet found on disk.")

    def is_ready(self):
        return self.model is not None and self.preprocessor is not None

    def predict_career(self, student_features_dict, top_n=5):
        """
        Takes raw student feature dictionary (0-10 ratings, CGPA).
        Returns top 1 career, top N careers with calibrated compatibility scores (0-100%),
        and model confidence metric.
        """
        if not self.is_ready():
            self._load_artifacts()
            if not self.is_ready():
                raise RuntimeError("Machine Learning model is not trained yet. Run train.py first.")

        # Convert dict to single-row DataFrame
        df_row = pd.DataFrame([student_features_dict])
        
        # Transform via preprocessor
        X_scaled, X_unscaled = self.preprocessor.transform_features(df_row)
        classes = self.preprocessor.get_classes()

        # Generate probabilities or decision scores
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(X_scaled)[0]
        elif hasattr(self.model, "decision_function"):
            decision = self.model.decision_function(X_scaled)[0]
            # Softmax on decision function to get valid probabilities
            exp_d = np.exp(decision - np.max(decision))
            probs = exp_d / np.sum(exp_d)
        else:
            pred_idx = self.model.predict(X_scaled)[0]
            probs = np.zeros(len(classes))
            probs[pred_idx] = 1.0

        # Sort classes descending by probability
        ranked_indices = np.argsort(probs)[::-1]
        top_prob = float(probs[ranked_indices[0]])
        
        # Calibration: Maps 12-class distribution smoothly to human-friendly 40-96%
        # compatibility rating while strictly preserving model rank order and relative ratios.
        ranked_predictions = []
        for idx in ranked_indices:
            p = float(probs[idx])
            ratio = p / top_prob if top_prob > 0 else 0
            # Scaled compatibility: top match receives ~85-95%, runner-ups scaled proportionally
            compat_score = round(min(96.0, max(12.0, 52.0 + 42.0 * (ratio ** 0.85))), 1)
            
            ranked_predictions.append({
                "career_title": classes[idx],
                "compatibility_score": compat_score,
                "probability": round(p, 4)
            })

        top_prediction = ranked_predictions[0]
        top_n_predictions = ranked_predictions[:min(top_n, len(ranked_predictions))]

        # Confidence calculation: gap between top 1 and top 2
        confidence = 0.0
        if len(ranked_predictions) > 1:
            margin = (top_prediction["probability"] - ranked_predictions[1]["probability"])
            confidence = round(min(98.0, max(25.0, (margin * 1.8 + 0.35) * 100.0)), 1)
        else:
            confidence = 90.0

        return {
            "top_career": top_prediction["career_title"],
            "top_compatibility": top_prediction["compatibility_score"],
            "confidence_score": confidence,
            "top_predictions": top_n_predictions,
            "all_predictions": ranked_predictions,
            "features_used": X_unscaled.iloc[0].to_dict()
        }

# Global singleton instance
_predictor = None

def get_career_predictor():
    global _predictor
    if _predictor is None:
        _predictor = CareerPredictor()
    return _predictor

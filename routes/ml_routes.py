import json
from pathlib import Path
from flask import Blueprint, render_template, request, jsonify, g
from models.resume import ModelVersion, ModelMetric
from ml.predict import get_career_predictor

ml_bp = Blueprint("ml", __name__)

@ml_bp.route("/ml-analytics")
@ml_bp.route("/ml/analytics")
def analytics():
    # Load dataset info
    base_dir = Path(__file__).resolve().parent.parent
    dataset_info_path = base_dir / "ml" / "dataset" / "dataset_info.json"
    metadata_path = base_dir / "ml" / "saved_models" / "best_model_metadata.json"
    comparison_path = base_dir / "ml" / "saved_models" / "all_models_metrics.json"

    dataset_info = {}
    if dataset_info_path.exists():
        with open(dataset_info_path, "r") as f:
            dataset_info = json.load(f)

    metadata = {}
    if metadata_path.exists():
        with open(metadata_path, "r") as f:
            metadata = json.load(f)

    comparison = {}
    if comparison_path.exists():
        with open(comparison_path, "r") as f:
            comparison = json.load(f)

    active_model = ModelVersion.query.filter_by(is_active=1).first()

    return render_template(
        "admin/ml_analytics.html",
        dataset_info=dataset_info,
        metadata=metadata,
        comparison=comparison,
        active_model=active_model
    )

@ml_bp.route("/api/predict", methods=["POST"])
def api_predict():
    """Programmatic API endpoint to get career predictions."""
    data = request.get_json() or {}
    if not data:
        return jsonify({"status": "error", "message": "JSON body with student features required."}), 400

    try:
        predictor = get_career_predictor()
        if not predictor.is_ready():
            predictor._load_artifacts()
            if not predictor.is_ready():
                return jsonify({"status": "error", "message": "ML Model is not trained yet."}), 500

        pred = predictor.predict_career(data, top_n=5)
        return jsonify({
            "status": "success",
            "top_career": pred["top_career"],
            "compatibility_score": pred["top_compatibility"],
            "confidence_score": pred["confidence_score"],
            "top_predictions": pred["top_predictions"]
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

import os
import json
import logging
from pathlib import Path
import joblib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier

from ml.dataset.data_loader import load_or_create_dataset, FEATURE_COLUMNS, CAREER_ROLES
from ml.preprocessing import CareerDataPreprocessor, ALL_FEATURE_COLUMNS
from ml.evaluate import evaluate_multiclass_model

logger = logging.getLogger(__name__)

def train_and_evaluate_models(random_state=42, save_dir=None):
    """
    Executes the complete CareerAI Machine Learning training pipeline:
    1. Loads standard benchmark dataset.
    2. Splits train/test using Stratified Split (80/20) avoiding data leakage.
    3. Fits preprocessing pipeline on training set.
    4. Trains 5 diverse classification algorithms:
       - Logistic Regression
       - Decision Tree
       - Random Forest
       - K-Nearest Neighbors (KNN)
       - Gradient Boosting
    5. Evaluates each model using Stratified K-Fold CV & held-out test set metrics.
    6. Automatically selects best model based on weighted F1-Score & Accuracy.
    7. Saves artifacts (model, preprocessor, metrics, charts) to disk with Joblib.
    """
    if save_dir is None:
        save_dir = Path(__file__).resolve().parent / "saved_models"
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load data
    logger.info("Loading dataset...")
    df = load_or_create_dataset()
    X_raw = df[FEATURE_COLUMNS]
    y_raw = df["career_role"]

    # 2. Stratified train-test split
    X_train_raw, X_test_raw, y_train_raw, y_test_raw = train_test_split(
        X_raw, y_raw, test_size=0.20, random_state=random_state, stratify=y_raw
    )

    # 3. Preprocessing & Feature Engineering
    preprocessor = CareerDataPreprocessor()
    preprocessor.fit(X_train_raw, y_train_raw)

    X_train_scaled, _ = preprocessor.transform_features(X_train_raw)
    X_test_scaled, _ = preprocessor.transform_features(X_test_raw)

    y_train = preprocessor.transform_target(y_train_raw)
    y_test = preprocessor.transform_target(y_test_raw)
    class_names = preprocessor.get_classes()

    # 4. Define candidate models
    candidate_models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=random_state),
        "Decision Tree": DecisionTreeClassifier(max_depth=12, min_samples_split=4, random_state=random_state),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=12, min_samples_split=3, random_state=random_state),
        "KNN": KNeighborsClassifier(n_neighbors=7, weights="distance"),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=90, learning_rate=0.1, max_depth=4, random_state=random_state)
    }

    results = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)

    logger.info(f"Training and comparing {len(candidate_models)} models...")
    for name, model in candidate_models.items():
        # Stratified Cross-Validation on training split
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring="f1_weighted")
        mean_cv_f1 = float(np.mean(cv_scores))

        # Train on full training split
        model.fit(X_train_scaled, y_train)

        # Evaluate on held-out test split
        eval_metrics = evaluate_multiclass_model(model, X_test_scaled, y_test, class_names=class_names)
        eval_metrics["cv_f1_mean"] = round(mean_cv_f1, 4)
        eval_metrics["cv_f1_std"] = round(float(np.std(cv_scores)), 4)
        
        results[name] = {
            "model": model,
            "metrics": eval_metrics
        }
        logger.info(f"[{name}] Test Accuracy: {eval_metrics['accuracy']:.4f} | Test F1: {eval_metrics['f1_weighted']:.4f} | CV F1: {mean_cv_f1:.4f}")

    # 5. Model Selection (Primary criterion: Test weighted F1, tie-breaker: Accuracy)
    best_model_name = max(results.keys(), key=lambda k: (results[k]["metrics"]["f1_weighted"], results[k]["metrics"]["accuracy"]))
    best_model = results[best_model_name]["model"]
    best_metrics = results[best_model_name]["metrics"]

    logger.info(f"Selected Champion Model: {best_model_name} (F1: {best_metrics['f1_weighted']:.4f})")

    # 6. Extract Feature Importances
    feature_importances = {}
    if hasattr(best_model, "feature_importances_"):
        raw_fi = best_model.feature_importances_
        feature_importances = {feat: round(float(score), 4) for feat, score in zip(ALL_FEATURE_COLUMNS, raw_fi)}
    elif hasattr(best_model, "coef_"):
        # Mean absolute coefficient across classes for linear models
        coef_mean = np.mean(np.abs(best_model.coef_), axis=0)
        coef_norm = coef_mean / np.sum(coef_mean)
        feature_importances = {feat: round(float(score), 4) for feat, score in zip(ALL_FEATURE_COLUMNS, coef_norm)}
    else:
        # Fallback equal distribution
        feature_importances = {feat: round(1.0 / len(ALL_FEATURE_COLUMNS), 4) for feat in ALL_FEATURE_COLUMNS}

    # Sort feature importances descending
    sorted_fi = dict(sorted(feature_importances.items(), key=lambda item: item[1], reverse=True))

    # 7. Generate Visualizations (Confusion Matrix & Feature Importance plots)
    try:
        # Confusion Matrix plot
        cm = np.array(best_metrics["confusion_matrix"])
        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
        fig.colorbar(im, ax=ax)
        ax.set(
            xticks=np.arange(cm.shape[1]),
            yticks=np.arange(cm.shape[0]),
            xticklabels=[c[:10] for c in class_names],
            yticklabels=[c[:10] for c in class_names],
            title=f"Confusion Matrix: {best_model_name} (Accuracy: {best_metrics['accuracy']*100:.1f}%)",
            ylabel="True Career Label",
            xlabel="Predicted Career Label"
        )
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        plt.tight_layout()
        cm_path = save_dir / "confusion_matrix.png"
        fig.savefig(cm_path, dpi=150)
        plt.close(fig)

        # Feature Importance plot (Top 12 features)
        fig, ax = plt.subplots(figsize=(9, 6))
        top_feats = list(sorted_fi.keys())[:12]
        top_scores = [sorted_fi[f] for f in top_feats]
        y_pos = np.arange(len(top_feats))
        ax.barh(y_pos, top_scores, align="center", color="#4f46e5")
        ax.set_yticks(y_pos)
        ax.set_yticklabels(top_feats)
        ax.invert_yaxis()
        ax.set_xlabel("Relative Importance Score")
        ax.set_title(f"Top Contributing Features ({best_model_name})")
        plt.tight_layout()
        fi_path = save_dir / "feature_importance.png"
        fig.savefig(fi_path, dpi=150)
        plt.close(fig)
    except Exception as e:
        logger.warning(f"Could not render plots (non-fatal): {e}")

    # 8. Save Model Artifacts
    best_model_path = save_dir / "best_model.joblib"
    preprocessor_path = save_dir / "preprocessor.joblib"
    joblib.dump(best_model, best_model_path)
    joblib.dump(preprocessor, preprocessor_path)

    # Save metrics without model instances
    comparison_summary = {}
    for name, data in results.items():
        m = data["metrics"]
        comparison_summary[name] = {
            "accuracy": m["accuracy"],
            "f1_weighted": m["f1_weighted"],
            "precision_weighted": m["precision_weighted"],
            "recall_weighted": m["recall_weighted"],
            "cv_f1_mean": m["cv_f1_mean"],
            "roc_auc_weighted": m["roc_auc_weighted"]
        }

    with open(save_dir / "all_models_metrics.json", "w") as f:
        json.dump(comparison_summary, f, indent=2)

    metadata = {
        "active_model_name": best_model_name,
        "algorithm": str(best_model.__class__.__name__),
        "test_accuracy": best_metrics["accuracy"],
        "test_f1_score": best_metrics["f1_weighted"],
        "test_precision": best_metrics["precision_weighted"],
        "test_recall": best_metrics["recall_weighted"],
        "cv_f1_mean": best_metrics["cv_f1_mean"],
        "num_classes": len(class_names),
        "classes": class_names,
        "num_features": len(ALL_FEATURE_COLUMNS),
        "total_records": len(df),
        "training_records": len(X_train_raw),
        "testing_records": len(X_test_raw),
        "feature_importances": sorted_fi,
        "confusion_matrix": best_metrics["confusion_matrix"]
    }

    with open(save_dir / "best_model_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    logger.info("Training pipeline completed successfully.")
    return {
        "best_model_name": best_model_name,
        "metrics": best_metrics,
        "comparison": comparison_summary,
        "metadata": metadata
    }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    train_and_evaluate_models()

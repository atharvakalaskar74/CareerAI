# API Reference Documentation — CareerAI

## 1. Overview

CareerAI exposes clean REST API endpoints for programmatic prediction, simulation, and career benchmarking.

---

### 2. Predict Career Path
- **Endpoint**: `POST /api/predict`
- **Content-Type**: `application/json`
- **Description**: Runs inference using the active champion machine learning model on a student's 21-feature rating vector.

#### Request Body
```json
{
  "python": 9.0,
  "java": 4.0,
  "c": 4.0,
  "cpp": 5.0,
  "javascript": 4.0,
  "sql": 7.5,
  "html_css": 4.0,
  "machine_learning": 9.0,
  "deep_learning": 8.5,
  "data_analysis": 8.5,
  "cloud": 6.0,
  "cybersecurity": 4.0,
  "networking": 4.5,
  "database": 6.5,
  "git_github": 8.0,
  "problem_solving": 9.0,
  "analytical_thinking": 9.0,
  "communication": 7.5,
  "math_level": 9.0,
  "stats_level": 9.0,
  "cgpa": 8.8
}
```

#### Response (200 OK)
```json
{
  "status": "success",
  "top_career": "AI/ML Engineer",
  "compatibility_score": 92.4,
  "confidence_score": 86.2,
  "top_predictions": [
    {
      "career_title": "AI/ML Engineer",
      "compatibility_score": 92.4,
      "probability": 0.465
    },
    {
      "career_title": "Data Scientist",
      "compatibility_score": 87.1,
      "probability": 0.282
    },
    {
      "career_title": "AI Researcher",
      "compatibility_score": 82.5,
      "probability": 0.145
    }
  ]
}
```

---

### 3. What-If Career Simulation
- **Endpoint**: `POST /api/simulate`
- **Content-Type**: `application/json`
- **Authentication**: Requires active student session
- **Description**: Evaluates before-vs-after career probability shifts based on hypothetical skill improvements.

#### Request Body
```json
{
  "baseline": {
    "python": 6.0,
    "machine_learning": 4.0,
    "deep_learning": 3.0
  },
  "simulated": {
    "python": 9.0,
    "machine_learning": 9.0,
    "deep_learning": 8.5
  }
}
```

#### Response (200 OK)
```json
{
  "status": "success",
  "before": {
    "top_career": "Software Engineer",
    "top_compatibility": 74.2
  },
  "after": {
    "top_career": "AI/ML Engineer",
    "top_compatibility": 91.8
  },
  "shifts": [
    {
      "career_title": "AI/ML Engineer",
      "before_score": 68.2,
      "after_score": 91.8,
      "shift": 23.6,
      "direction": "up"
    }
  ]
}
```

---

### 4. Retrain Model Pipeline
- **Endpoint**: `POST /admin/train`
- **Authentication**: Requires active admin session (`admin_required`)
- **Description**: Retrains all 5 classification models on the dataset, evaluates metrics via 5-fold cross-validation, and saves the new champion model.

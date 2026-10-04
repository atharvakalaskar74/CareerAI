# Deployment Guide — CareerAI

## 1. Zero-Cost Free-Tier Deployment Strategy

CareerAI is engineered for 100% free-cost deployment (₹0 expenditure) using open-source Python technologies.

Recommended Free-Tier PaaS Providers:
- **Render.com** (Free Web Service tier + SQLite / Free PostgreSQL)
- **Railway.app** (Free starter allowance)
- **PythonAnywhere** (Free beginner tier)
- **Koyeb / Fly.io** (Free container tiers)

---

## 2. Docker Deployment

### 2.1 Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Train or ensure model exists
RUN python -m ml.train

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

---

## 3. Deployment on Render.com (Step-by-Step)

1. Push your repository to GitHub.
2. Sign in to [Render.com](https://render.com/) and click **New +** -> **Web Service**.
3. Select your repository.
4. Set the following build and start commands:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python -m ml.train`
   - **Start Command**: `gunicorn app:app`
5. Configure Environment Variables under the **Environment** tab:
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: `<Generate a random 32-character string>`
   - `DATABASE_URL`: `sqlite:///instance/careerai.db` (or remote MySQL connection string)
6. Click **Deploy Web Service**.

---

## 4. Production Database Configuration (MySQL)

To connect CareerAI to a cloud MySQL instance (e.g. AWS RDS, Aiven, or PlanetScale):
1. Create a MySQL database named `careerai_db`.
2. Execute `database/schema.sql` and `database/seed.sql`.
3. In your `.env` or deployment environment variables, set:
   ```env
   DATABASE_URL=mysql+pymysql://<user>:<password>@<host>:<port>/careerai_db
   ```
4. CareerAI will automatically connect to MySQL via PyMySQL.

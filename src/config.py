"""
Cresca AI Configuration Module
Loads environment variables and GCP configuration settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

# Ensure output directories exist
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Load environment variables
load_dotenv(dotenv_path=BASE_DIR / ".env")

# API Keys & Credentials
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Google Cloud Settings
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "cresca-sentinel-2026")
GCP_REGION = os.getenv("GCP_REGION", "asia-southeast2")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "cresca-storage-bucket")
FIRESTORE_DATABASE = os.getenv("FIRESTORE_DATABASE", "(default)")

# Model Configurations
REASONING_MODEL = os.getenv("REASONING_MODEL", "gemini-3.6-flash")
FALLBACK_REASONING_MODEL = os.getenv("FALLBACK_REASONING_MODEL", "gemini-3.6-pro")
ANONYMIZATION_MODEL = os.getenv("ANONYMIZATION_MODEL", "gemma-2-2b")

# Runtime Flags
AGENT_MODE = os.getenv("AGENT_MODE", "AUTONOMOUS_TASKMASTER")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

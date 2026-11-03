"""Environment-backed settings with safe local defaults."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    max_upload_bytes: int = int(os.getenv("MAX_UPLOAD_MB", "5")) * 1024 * 1024
    max_data_rows: int = int(os.getenv("MAX_DATA_ROWS", "5000"))
    max_columns: int = int(os.getenv("MAX_COLUMNS", "100"))
    model_api_key: str = os.getenv("MODEL_API_KEY", "")
    meta_model: str = os.getenv("META_MODEL", "muse-spark-1.3")
    meta_base_url: str = os.getenv("META_BASE_URL", "https://api.meta.ai/v1")
    allow_meta_api_calls: bool = os.getenv("ALLOW_META_API_CALLS", "false").lower() == "true"
    database_path: str = os.getenv("IMPORTGUARD_DB", "data/importguard.db")
    session_days: int = int(os.getenv("SESSION_DAYS", "30"))
    export_retention_days: int = int(os.getenv("EXPORT_RETENTION_DAYS", "7"))
    max_stored_package_bytes: int = int(os.getenv("MAX_STORED_PACKAGE_MB", "8")) * 1024 * 1024
    billing_enforce_quotas: bool = os.getenv("BILLING_ENFORCE_QUOTAS", "false").lower() == "true"
    admin_emails: str = os.getenv("ADMIN_EMAILS", "")
    auth_failure_limit_per_ip: int = int(os.getenv("AUTH_FAILURE_LIMIT_PER_IP", "10"))
    auth_failure_limit_per_account: int = int(os.getenv("AUTH_FAILURE_LIMIT_PER_ACCOUNT", "10"))
    auth_rate_window_seconds: int = int(os.getenv("AUTH_RATE_WINDOW_SECONDS", "300"))
    api_profile_limit_per_window: int = int(os.getenv("API_PROFILE_LIMIT_PER_WINDOW", "120"))
    api_suggest_limit_per_window: int = int(os.getenv("API_SUGGEST_LIMIT_PER_WINDOW", "60"))
    api_process_limit_per_window: int = int(os.getenv("API_PROCESS_LIMIT_PER_WINDOW", "30"))
    api_replay_limit_per_window: int = int(os.getenv("API_REPLAY_LIMIT_PER_WINDOW", "30"))
    max_concurrent_processing: int = int(os.getenv("MAX_CONCURRENT_PROCESSING", "2"))
    oauth_state_ttl_seconds: int = int(os.getenv("OAUTH_STATE_TTL_SECONDS", "600"))
    google_oauth_client_id: str = os.getenv("GOOGLE_OAUTH_CLIENT_ID", "")
    google_oauth_client_secret: str = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET", "")
    google_oauth_redirect_uri: str = os.getenv("GOOGLE_OAUTH_REDIRECT_URI", "")
    github_oauth_client_id: str = os.getenv("GITHUB_OAUTH_CLIENT_ID", "")
    github_oauth_client_secret: str = os.getenv("GITHUB_OAUTH_CLIENT_SECRET", "")
    github_oauth_redirect_uri: str = os.getenv("GITHUB_OAUTH_REDIRECT_URI", "")


settings = Settings()

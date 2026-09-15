from .base import *  # noqa: F403

DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() == "true"  # noqa: F405
ALLOWED_HOSTS = ALLOWED_HOSTS or ["localhost", "127.0.0.1"]  # noqa: F405
CORS_ALLOWED_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]

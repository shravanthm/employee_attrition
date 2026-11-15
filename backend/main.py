"""Vercel and ASGI runner root entrypoint for backend service."""
import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app  # noqa: E402

__all__ = ["app"]

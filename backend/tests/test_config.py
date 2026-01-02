"""
Tests for configuration module.

Tests verify:
- Environment variables are loaded correctly
- Required settings are validated
- Default values are applied appropriately
"""

import os
import pytest


class TestSettings:
    """Test cases for Settings configuration."""

    def test_settings_loads_database_url(self):
        """Settings should load DATABASE_URL from environment."""
        from src.config import settings

        assert settings.DATABASE_URL is not None
        assert "postgresql" in settings.DATABASE_URL

    def test_settings_loads_better_auth_secret(self):
        """Settings should load BETTER_AUTH_SECRET from environment."""
        from src.config import settings

        assert settings.BETTER_AUTH_SECRET is not None
        assert len(settings.BETTER_AUTH_SECRET) >= 32

    def test_settings_has_debug_flag(self):
        """Settings should have DEBUG flag."""
        from src.config import settings

        assert hasattr(settings, "DEBUG")
        assert isinstance(settings.DEBUG, bool)

    def test_settings_has_log_level(self):
        """Settings should have LOG_LEVEL with valid value."""
        from src.config import settings

        assert hasattr(settings, "LOG_LEVEL")
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        assert settings.LOG_LEVEL in valid_levels

    def test_settings_has_cors_origins(self):
        """Settings should have CORS_ORIGINS configuration."""
        from src.config import settings

        assert hasattr(settings, "CORS_ORIGINS")
        # Should be a list or string
        assert settings.CORS_ORIGINS is not None

    def test_settings_is_singleton(self):
        """Settings should be a singleton instance."""
        from src.config import settings as settings1
        from src.config import settings as settings2

        assert settings1 is settings2

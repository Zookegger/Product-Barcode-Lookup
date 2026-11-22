import os

import pytest

from barcode_tui.config import (
    DEFAULT_CACHE_TTL_SECONDS,
    DEFAULT_TIMEOUT,
    load_settings,
)


@pytest.fixture(autouse=True)
def isolated_env(monkeypatch: pytest.MonkeyPatch):
    # Stop .env from refilling variables behind the test's back
    monkeypatch.setattr("barcode_tui.config.load_dotenv", lambda: None)
    for name in list(os.environ):
        if name.startswith(("BARCODE_", "PROVIDER_")):
            monkeypatch.delenv(name, raising=False)


def test_providers_are_parsed_in_order(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("BARCODE_PROVIDERS", "openfoodfacts,upcitemdb,barcodelookup")

    settings = load_settings()

    assert [p.id for p in settings.providers] == ["openfoodfacts", "upcitemdb", "barcodelookup"]


def test_provider_ids_are_trimmed_and_lowercased(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("BARCODE_PROVIDERS", " OpenFoodFacts , , UPCITEMDB ")

    settings = load_settings()

    assert [p.id for p in settings.providers] == ["openfoodfacts", "upcitemdb"]


def test_missing_providers_fields_empty_tuple():
    settings = load_settings()
    assert settings.providers == ()


def test_provider_env_values_are_mapped(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("BARCODE_PROVIDERS", "upcitemdb")
    monkeypatch.setenv("PROVIDER_UPCITEMDB_API_KEY", "secret")
    monkeypatch.setenv("PROVIDER_UPCITEMDB_BASE_URL", "https://example.test")
    monkeypatch.setenv("PROVIDER_UPCITEMDB_TIMEOUT", "2.5")
    monkeypatch.setenv("PROVIDER_UPCITEMDB_USER_AGENT", "test-agent")

    (provider,) = load_settings().providers

    assert provider.id == "upcitemdb"
    assert provider.api_key == "secret"
    assert provider.base_url == "https://example.test"
    assert provider.timeout == 2.5
    assert provider.user_agent == "test-agent"


def test_timeout_falls_back_on_invalid_value(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("BARCODE_PROVIDERS", "upcitemdb")
    monkeypatch.setenv("PROVIDER_UPCITEMDB_TIMEOUT", "abc")

    (provider,) = load_settings().providers

    assert provider.timeout == DEFAULT_TIMEOUT


def test_timeout_defaults_when_blank(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("BARCODE_PROVIDERS", "upcitemdb")
    monkeypatch.setenv("PROVIDER_UPCITEMDB_TIMEOUT", "")

    (provider,) = load_settings().providers

    assert provider.timeout == DEFAULT_TIMEOUT


def test_cache_defaults(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("BARCODE_PROVIDERS", "upcitemdb")

    settings = load_settings()

    assert settings.cache_dir == ""
    assert settings.cache_ttl_seconds == DEFAULT_CACHE_TTL_SECONDS


def test_cache_ttl_is_read(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("BARCODE_PROVIDERS", "upcitemdb")
    monkeypatch.setenv("BARCODE_CACHE_TTL_SECONDS", "60")

    assert load_settings().cache_ttl_seconds == 60


def test_cache_ttl_falls_back_on_invalid_value(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("BARCODE_PROVIDERS", "upcitemdb")
    monkeypatch.setenv("BARCODE_CACHE_TTL_SECONDS", "abc")

    assert load_settings().cache_ttl_seconds == DEFAULT_CACHE_TTL_SECONDS


def test_cache_dir_is_read(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("BARCODE_PROVIDERS", "upcitemdb")
    monkeypatch.setenv("BARCODE_CACHE_DIR", "D:/tmp/cache")

    assert load_settings().cache_dir == "D:/tmp/cache"

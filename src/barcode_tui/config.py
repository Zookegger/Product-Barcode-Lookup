from dataclasses import dataclass

from dotenv import load_dotenv

from barcode_tui.utils import parse_csv, parse_float, parse_int, parse_str

DEFAULT_TIMEOUT = 10.0
DEFAULT_CACHE_TTL_SECONDS = 604_800  # 7 Days
APP_NAME = "barcode-tui"


# Frozen = read-only
@dataclass(frozen=True)
class ProviderConfig:
    id: str
    api_key: str | None = None
    base_url: str | None = None
    timeout: float = DEFAULT_TIMEOUT
    user_agent: str | None = None


@dataclass(frozen=True)
class Settings:
    providers: tuple[ProviderConfig, ...]
    cache_dir: str
    cache_ttl_seconds: int = DEFAULT_CACHE_TTL_SECONDS


def _load_provider(provider_id: str) -> ProviderConfig:
    normalized_id = provider_id.strip().lower()
    prefix = f"PROVIDER_{normalized_id.upper()}"
    return ProviderConfig(
        id=normalized_id,
        api_key=parse_str(f"{prefix}_API_KEY"),
        base_url=parse_str(f"{prefix}_BASE_URL"),
        timeout=parse_float(f"{prefix}_TIMEOUT", DEFAULT_TIMEOUT),
        user_agent=parse_str(f"{prefix}_USER_AGENT"),
    )


def load_settings() -> Settings:
    load_dotenv()

    provider_ids = parse_csv("BARCODE_PROVIDERS")
    providers = tuple(_load_provider(pid) for pid in provider_ids)

    return Settings(
        cache_dir=parse_str("BARCODE_CACHE_DIR") or "",
        cache_ttl_seconds=parse_int("BARCODE_CACHE_TTL_SECONDS", DEFAULT_CACHE_TTL_SECONDS),
        providers=providers,
    )

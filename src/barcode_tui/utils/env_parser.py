import os


def parse_str(name: str) -> str | None:
    raw = os.getenv(name)
    return raw.strip() or None if raw is not None else None


def parse_float(name: str, default: float) -> float:
    try:
        raw = parse_str(name)
        return float(raw) if raw is not None else default
    except ValueError:
        return default


def parse_int(name: str, default: int) -> int:
    try:
        raw = parse_str(name)
        return int(raw) if raw is not None else default
    except ValueError:
        return default


def parse_csv(name: str) -> tuple[str, ...]:
    try:
        raw = parse_str(name)
        if raw is None:
            return ()

        items: list[str] = []

        for part in raw.split(","):
            cleaned = part.strip()
            if cleaned:
                items.append(cleaned)

        return tuple(items)
    except ValueError:
        return ()

import pytest

from barcode_tui.utils import parse_csv, parse_float, parse_int, parse_str


def test_parse_str_strips(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("X", "  hello  ")
    assert parse_str("X") == "hello"


def test_parse_str_blank_is_none(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("X", "   ")
    assert parse_str("X") is None


def test_parse_str_missing_is_none(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("X", raising=False)
    assert parse_str("X") is None


def test_parse_float_valid(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("X", "2.5")
    assert parse_float("X", 1.0) == 2.5


def test_parse_float_falls_back_on_garbage(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("X", "abc")
    assert parse_float("X", 1.0) == 1.0


def test_parse_float_falls_back_when_blank(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("X", "")
    assert parse_float("X", 1.0) == 1.0


def test_parse_int_valid(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("X", "42")
    assert parse_int("X", 7) == 42


def test_parse_int_falls_back_on_garbage(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("X", "abc")
    assert parse_int("X", 7) == 7


def test_parse_csv_trims_and_drops_empties(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("X", " a , , B ")
    assert parse_csv("X") == ("a", "B")


def test_parse_csv_missing_is_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("X", raising=False)
    assert parse_csv("X") == ()

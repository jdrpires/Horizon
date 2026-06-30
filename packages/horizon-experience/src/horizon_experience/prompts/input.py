"""Safe terminal input prompts."""

from __future__ import annotations

from collections.abc import Callable, Sequence

from horizon_experience.exceptions import UserCancelled
from horizon_experience.rendering import error, info
from horizon_experience.validators import parse_float, parse_optional_datetime, validate_non_empty

CANCEL_VALUES = {"c", "cancelar", "voltar", "sair"}


def prompt_text(label: str) -> str:
    """Prompt until the user enters non-empty text or cancels."""
    return _prompt_until_valid(label, lambda value: validate_non_empty(value, label))


def prompt_float(label: str) -> float:
    """Prompt until the user enters a valid number or cancels."""
    return _prompt_until_valid(label, lambda value: parse_float(value, label))


def prompt_optional_datetime(label: str = "Data/Hora (opcional)") -> str | None:
    """Prompt until the user enters a valid optional datetime or cancels."""
    return _prompt_until_valid(label, parse_optional_datetime, allow_blank=True)


def choose_from_list[T](
    label: str,
    items: Sequence[T],
    render_item: Callable[[T], str],
) -> T:
    """Prompt until the user selects an existing item or cancels."""
    if not items:
        raise ValueError("Não há itens disponíveis.")
    while True:
        for index, item in enumerate(items, start=1):
            print(f"{index} - {render_item(item)}")
        raw = _read(f"{label}: ")
        if _is_cancel(raw):
            raise UserCancelled
        try:
            selected = int(raw)
        except ValueError:
            error("Escolha um número da lista ou digite 'c' para cancelar.")
            continue
        if 1 <= selected <= len(items):
            return items[selected - 1]
        error("Essa opção não existe. Tente novamente.")


def _prompt_until_valid[T](
    label: str,
    validator: Callable[[str], T],
    *,
    allow_blank: bool = False,
) -> T:
    """Run a prompt loop until validation succeeds."""
    while True:
        raw = _read(f"{label}: ")
        if _is_cancel(raw):
            raise UserCancelled
        if allow_blank and not raw.strip():
            return validator(raw)
        try:
            return validator(raw)
        except ValueError as exc:
            error(str(exc))
            info("Tente novamente ou digite 'c' para cancelar.")


def _read(label: str) -> str:
    """Read user input safely."""
    try:
        return input(label).strip()
    except EOFError as exc:
        raise UserCancelled from exc


def _is_cancel(value: str) -> bool:
    """Return whether the user requested cancellation."""
    return value.strip().lower() in CANCEL_VALUES

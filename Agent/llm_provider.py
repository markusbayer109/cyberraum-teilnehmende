"""Gemeinsame Modellroute für die Workshop-Agenten.

LiteLLM der TU Darmstadt ist der Standard. OpenRouter wird nur verwendet,
wenn ``LLM_PROVIDER=openrouter`` bewusst als Plan 2 gesetzt wird.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import urlsplit


DEFAULT_LITELLM_BASE_URL = "https://llm-service.ai.tu-darmstadt.de/v1"
DEFAULT_LITELLM_MODEL = "GLM-5.2-AWQ-INT4"
DEFAULT_OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
SUPPORTED_PROVIDERS = {"litellm", "openrouter"}


@dataclass(frozen=True)
class ModelRoute:
    """Vollständig aufgelöste OpenAI-kompatible Modellroute."""

    provider: str
    api_base: str
    api_key: str
    model: str

    @property
    def chat_completions_url(self) -> str:
        return f"{self.api_base}/chat/completions"

    @property
    def headers(self) -> dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if self.provider == "openrouter":
            headers["X-OpenRouter-Title"] = "Studienstiftung Cyberraum Workshop"
        return headers


def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"{name} fehlt. Bitte .env prüfen.")
    return value


def _api_base(name: str, default: str) -> str:
    value = os.getenv(name, default).strip().rstrip("/")
    parsed = urlsplit(value)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
    ):
        raise RuntimeError(
            f"{name} muss eine HTTP(S)-Basisadresse ohne Zugangsdaten, "
            "Query oder Fragment sein."
        )
    return value


def resolve_model_route() -> ModelRoute:
    """Wählt LiteLLM oder den bewusst aktivierten OpenRouter-Plan-2-Pfad."""

    provider = os.getenv("LLM_PROVIDER", "litellm").strip().lower()
    if provider not in SUPPORTED_PROVIDERS:
        raise RuntimeError(
            "LLM_PROVIDER muss 'litellm' oder 'openrouter' sein."
        )

    if provider == "litellm":
        return ModelRoute(
            provider=provider,
            api_base=_api_base("LITELLM_BASE_URL", DEFAULT_LITELLM_BASE_URL),
            api_key=_required("LITELLM_API_KEY"),
            model=os.getenv("LITELLM_MODEL", DEFAULT_LITELLM_MODEL).strip()
            or DEFAULT_LITELLM_MODEL,
        )

    return ModelRoute(
        provider=provider,
        api_base=_api_base("OPENROUTER_API_BASE", DEFAULT_OPENROUTER_API_BASE),
        api_key=_required("OPENROUTER_API_KEY"),
        model=_required("OPENROUTER_MODEL"),
    )

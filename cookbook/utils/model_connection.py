import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI


class ModelConnection:
    """
    Unified connection handler using OpenAI wrapper for multiple providers:
    - OpenAI (default)
    - Anthropic (via OpenAI wrapper + base_url)
    - Ollama (local server)
    - Gemini (via OpenAI wrapper + base_url)
    """

    def __init__(self):
        """Load environment variables and initialize configuration."""
        load_dotenv(override=True)

        # Environment Variables
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")

        # Base URLs
        self.ollama_url = "http://localhost:11434/v1"
        self.anthropic_url = "https://api.anthropic.com/v1/"
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
        self.deepseek_url = "https://api.deepseek.com"

        # Providers
        self.providers = {
            "OPENAI": {"api_key": self.openai_api_key, "base_url": None},
            "ANTHROPIC": {"api_key": self.anthropic_api_key, "base_url": self.anthropic_url},
            "OLLAMA": {"api_key": "ollama", "base_url": self.ollama_url},
            "GEMINI": {"api_key": self.google_api_key, "base_url": self.gemini_url},
        }

        self.clients = {}
        self._validate_env()

    def _validate_env(self):
        """Simple environment validation."""
        print(f"🔹 OpenAI API key loaded: {'✅' if self.openai_api_key else '❌'}")
        print(f"🔹 Anthropic API key loaded: {'✅' if self.anthropic_api_key else '❌'} (optional)")
        print(f"🔹 Google API key loaded: {'✅' if self.google_api_key else '❌'} (optional)")

    def _get_client(self, provider: str) -> OpenAI:
        """Return cached or new OpenAI client for given provider."""
        provider = provider.upper()
        if provider not in self.providers:
            raise ValueError(f"❌ Unsupported provider '{provider}'. Allowed: {list(self.providers.keys())}")

        if provider not in self.clients:
            info = self.providers[provider]
            self.clients[provider] = OpenAI(
                api_key=info["api_key"],
                base_url=info["base_url"],
            )
        return self.clients[provider]

    def get_response(
        self,
        provider: str,
        model: str,
        messages: List[Dict[str, str]],
        reasoning_effort: str = None,
        **kwargs,
    ) -> str:
        """
        Get a chat completion from any supported provider.
        Args:
            provider: OPENAI | ANTHROPIC | OLLAMA | GEMINI
            model: model name (e.g., 'gpt-4o', 'llama3', 'claude-3-5-sonnet')
            messages: list of {"role": "user"/"system"/"assistant", "content": "..."}
            reasoning_effort: Optional Anthropic param
            kwargs: Extra params like temperature, max_tokens, etc.
        """
        provider = provider.upper()
        client = self._get_client(provider)

        # Unified call using OpenAI wrapper
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            reasoning_effort=reasoning_effort,
            **kwargs,
        )
        return response.choices[0].message.content.strip()

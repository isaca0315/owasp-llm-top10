"""Paquete `ctf_app`: fábrica común de los 10 servicios del PromptMe CTF."""

from .factory import create_app

__all__ = ["create_app"]

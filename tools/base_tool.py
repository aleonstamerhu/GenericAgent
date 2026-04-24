"""Base tool definitions and utilities for GenericAgent.

This module provides the foundational classes and decorators for defining
tools that can be used by the agent during its reasoning loop.
"""

from __future__ import annotations

import inspect
import json
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, get_type_hints


class ToolResult:
    """Encapsulates the result of a tool execution."""

    def __init__(self, success: bool, output: Any, error: Optional[str] = None):
        self.success = success
        self.output = output
        self.error = error

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
        }

    def __str__(self) -> str:
        if self.success:
            return str(self.output)
        return f"Error: {self.error}"


class BaseTool(ABC):
    """Abstract base class for all agent tools.

    Subclasses must implement `run` and provide a `name` and `description`.
    The schema is auto-generated from the `run` method's type hints and docstring
    when not explicitly overridden.
    """

    name: str = ""
    description: str = ""

    @abstractmethod
    def run(self, **kwargs) -> ToolResult:
        """Execute the tool with the provided keyword arguments."""
        ...

    def get_schema(self) -> dict:
        """Generate an OpenAI-compatible function schema for this tool."""
        hints = get_type_hints(self.run)
        sig = inspect.signature(self.run)
        properties: dict[str, dict] = {}
        required: list[str] = []

        _type_map = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            list: "array",
            dict: "object",
        }

        for param_name, param in sig.parameters.items():
            if param_name in ("self", "kwargs"):
                continue
            python_type = hints.get(param_name, str)
            json_type = _type_map.get(python_type, "string")
            properties[param_name] = {"type": json_type}

            if param.default is inspect.Parameter.empty:
                required.append(param_name)

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        }

    def safe_run(self, **kwargs) -> ToolResult:
        """Run the tool, catching any exceptions and returning a ToolResult."""
        try:
            return self.run(**kwargs)
        except Exception as exc:  # noqa: BLE001
            return ToolResult(success=False, output=None, error=str(exc))

    def __repr__(self) -> str:
        return f"<Tool name={self.name!r}>"


def tool_schema_from_callable(func: Callable) -> dict:
    """Derive an OpenAI function-calling schema from a plain callable.

    Useful for quickly wrapping standalone functions without subclassing BaseTool.
    """
    hints = get_type_hints(func)
    sig = inspect.signature(func)
    _type_map = {str: "string", int: "integer", float: "number", bool: "boolean"}
    properties: dict[str, dict] = {}
    required: list[str] = []

    for param_name, param in sig.parameters.items():
        if param_name == "self":
            continue
        json_type = _type_map.get(hints.get(param_name, str), "string")
        properties[param_name] = {"type": json_type}
        if param.default is inspect.Parameter.empty:
            required.append(param_name)

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": (inspect.getdoc(func) or "").strip(),
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        },
    }

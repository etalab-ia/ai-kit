"""
Namespace package for ai_kit.

This allows multiple packages across the monorepo to share the 'ai_kit' namespace:
- ai_kit.cli (from apps/cli/src/)
- ai_kit.core (from packages/core/src/)
- ai_kit.* (future packages)

Without this, each would be a separate package and imports would fail.
See: https://docs.python.org/3/library/pkgutil.html#pkgutil.extend_path
"""

__path__ = __import__("pkgutil").extend_path(__path__, __name__)

"""ai-kit core library.

This package provides core functionality for the ai-kit toolkit.
"""

__version__ = "0.1.0"
__author__ = "ai-kit Team"


def hello(name: str = "World") -> str:
    """Return a greeting message.

    Args:
        name: The name to greet. Defaults to "World".

    Returns:
        A greeting message.

    Examples:
        >>> hello()
        'Hello, World!'
        >>> hello("Alice")
        'Hello, Alice!'
    """
    return f"Hello, {name}!"

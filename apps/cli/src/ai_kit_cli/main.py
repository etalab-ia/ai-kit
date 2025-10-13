"""Main entry point for ai-kit CLI."""

import sys

from ai_kit_core import hello


def main() -> int:
    """Run the ai-kit CLI.

    Returns:
        Exit code (0 for success, non-zero for error).
    """
    if len(sys.argv) > 1:
        name = " ".join(sys.argv[1:])
        print(hello(name))
    else:
        print(hello())
        print("\nUsage: ai-kit [name]")
        print("Example: ai-kit Alice")

    return 0


if __name__ == "__main__":
    sys.exit(main())

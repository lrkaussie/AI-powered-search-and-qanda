"""Script to display and validate the project's directory structure."""

from pathlib import Path

# Create directory structure
directories = [
    "app",
    "app/api",
    "app/core",
    "app/models",
    "app/services",
    "app/utils",
    "tests",
    "docs",
]

# Create directories
for dir_path in directories:
    Path(dir_path).mkdir(parents=True, exist_ok=True)

# Create initial files
files = [
    "app/__init__.py",
    "app/api/__init__.py",
    "app/core/__init__.py",
    "app/models/__init__.py",
    "app/services/__init__.py",
    "app/utils/__init__.py",
    "tests/__init__.py",
    ".env.example",
    ".gitignore",
]

for file_path in files:
    Path(file_path).touch()


def print_tree(directory: Path, prefix: str = "", is_last: bool = True) -> None:
    """Print the directory tree structure.

    Args:
        directory: The directory to display
        prefix: Current line prefix for formatting
        is_last: Whether this is the last item in current level
    """
    # Print current directory/file
    print(prefix + ("└── " if is_last else "├── ") + directory.name)

    # Get all items in directory
    if directory.is_dir():
        items = list(directory.iterdir())
        items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))

        for i, item in enumerate(items):
            is_last_item = i == len(items) - 1
            print_tree(item, prefix + ("    " if is_last else "│   "), is_last_item)


def main() -> None:
    """Display the project's directory structure."""
    root = Path(".")
    print("\nProject Structure:")
    print_tree(root)


if __name__ == "__main__":
    main()

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
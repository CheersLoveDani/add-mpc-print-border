# Development Environment Setup

## Quick Start

Your pipenv development environment is now ready! Here's how to use it:

### 🚀 Activate the Environment

```powershell
pipenv shell
```

### 🛠️ Development Commands

Using the dev helper script:

```powershell
# Run the main application
pipenv run python dev.py run

# Format code with black
pipenv run python dev.py format

# Lint code with flake8
pipenv run python dev.py lint

# Run tests
pipenv run python dev.py test

# Clean up temporary files
pipenv run python dev.py clean
```

Or use pipenv directly:

```powershell
# Run the main application
pipenv run python add_mpc_bleed.py

# Run tests
pipenv run pytest tests/ -v

# Format code
pipenv run black .

# Lint code
pipenv run flake8 .
```

### 📁 Project Structure

```
add-mpc-print-border/
├── add_mpc_bleed.py     # Main application
├── dev.py               # Development helper script
├── Pipfile              # Pipenv dependencies
├── Pipfile.lock         # Locked dependencies
├── requirements.txt     # Legacy requirements (auto-converted)
├── README.md            # Main documentation
├── .flake8             # Linting configuration
└── tests/              # Test suite
    ├── __init__.py
    └── test_mpc_bleed.py
```

### 🧪 Testing

The project includes comprehensive tests that verify:
- Bleed pixel calculations are correct
- Image processing works properly
- File operations are handled safely

Run tests with: `pipenv run pytest tests/ -v`

### 🎯 Next Steps

1. **Activate the environment**: `pipenv shell`
2. **Run the application**: `python add_mpc_bleed.py`
3. **Make changes**: Edit the code as needed
4. **Test changes**: `python dev.py test`
5. **Format code**: `python dev.py format`

### 📦 Dependencies

- **Production**: Pillow (for image processing)
- **Development**: pytest, black, flake8

All dependencies are managed by pipenv and locked in `Pipfile.lock`.

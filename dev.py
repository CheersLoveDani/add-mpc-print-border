#!/usr/bin/env python3
"""
Development helper script for MPC Bleed Border Tool
"""

import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a shell command and print status"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main development tasks"""
    if len(sys.argv) < 2:
        print("""
🛠️  MPC Bleed Border Tool - Development Helper

Usage: python dev.py <command>

Available commands:
  setup     - Set up development environment
  run       - Run the main application
  format    - Format code with black
  lint      - Lint code with flake8
  test      - Run tests
  clean     - Clean up temporary files
  shell     - Activate pipenv shell
        """)
        return
    
    command = sys.argv[1].lower()
    
    if command == "setup":
        print("🚀 Setting up development environment...")
        run_command("pipenv install --dev", "Installing dependencies")
        print("\n✨ Development environment ready!")
        print("💡 Run 'python dev.py shell' to activate the virtual environment")
        
    elif command == "run":
        run_command("pipenv run python add_mpc_bleed.py", "Running MPC Bleed Border Tool")
        
    elif command == "format":
        run_command("pipenv run black .", "Formatting code")
        
    elif command == "lint":
        run_command("pipenv run flake8 .", "Linting code")
        
    elif command == "test":
        run_command("pipenv run pytest", "Running tests")
        
    elif command == "clean":
        print("🧹 Cleaning up...")
        patterns = ["**/__pycache__", "**/*.pyc", "**/*.pyo", "**/.pytest_cache"]
        for pattern in patterns:
            for path in Path(".").glob(pattern):
                if path.is_file():
                    path.unlink()
                    print(f"Removed: {path}")
                elif path.is_dir():
                    import shutil
                    shutil.rmtree(path)
                    print(f"Removed: {path}")
        print("✅ Cleanup completed")
        
    elif command == "shell":
        print("🐚 Activating pipenv shell...")
        print("Run this command manually: pipenv shell")
        
    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'python dev.py' for available commands")

if __name__ == "__main__":
    main()

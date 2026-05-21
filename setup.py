#!/usr/bin/env python
"""
CareerAI - Quick Start Script
Automated setup for development environment
"""

import os
import sys
import subprocess
import platform

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_command(cmd, description):
    """Run a command and display output"""
    print(f"▶ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr}\n")
        return False

def check_python():
    """Check Python version"""
    print_header("Checking Python Installation")
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print("✅ Python version OK\n")
    return True

def setup_virtual_env():
    """Setup virtual environment"""
    print_header("Setting Up Virtual Environment")
    
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        run_command(f"{sys.executable} -m venv venv", "Creating venv")
    else:
        print("✅ Virtual environment already exists\n")
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    print_header("Installing Dependencies")
    
    # Determine pip command based on OS
    if platform.system() == "Windows":
        pip_cmd = "venv\\Scripts\\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    # Upgrade pip
    run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip")
    
    # Install requirements
    if os.path.exists("requirements.txt"):
        run_command(f"{pip_cmd} install -r requirements.txt", "Installing requirements")
    else:
        print("❌ requirements.txt not found\n")
        return False
    
    return True

def setup_database():
    """Setup database"""
    print_header("Setting Up Database")
    
    # Determine python command
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    # Run migrations
    if not run_command(f"{python_cmd} manage.py migrate", "Running migrations"):
        print("❌ Migrations failed\n")
        return False
    
    return True

def create_superuser():
    """Prompt to create superuser"""
    print_header("Creating Superuser")
    
    response = input("Create a superuser account now? (y/n): ").lower()
    
    if response == 'y':
        if platform.system() == "Windows":
            python_cmd = "venv\\Scripts\\python"
        else:
            python_cmd = "venv/bin/python"
        
        os.system(f"{python_cmd} manage.py createsuperuser")
    else:
        print("You can create a superuser later with: python manage.py createsuperuser\n")
    
    return True

def setup_env_file():
    """Check and inform about environment setup"""
    print_header("Environment Configuration")
    
    if os.path.exists(".env"):
        print("✅ .env file exists")
        print("\n⚠️  Important: Update your .env file with:")
        print("   - GROQ_API_KEY from https://console.groq.com")
        print("   - Update SECRET_KEY for production")
        print("   - Set DEBUG=False for production\n")
        return True
    else:
        print("❌ .env file not found")
        print("Please create .env file and add required variables\n")
        return False

def create_logs_directory():
    """Create logs directory"""
    print_header("Setting Up Logs Directory")
    
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        print(f"✅ Created {logs_dir} directory\n")
    else:
        print(f"✅ {logs_dir} directory already exists\n")
    
    return True

def run_tests():
    """Run Django tests"""
    print_header("Running Tests")
    
    response = input("Run tests? (y/n): ").lower()
    
    if response == 'y':
        if platform.system() == "Windows":
            python_cmd = "venv\\Scripts\\python"
        else:
            python_cmd = "venv/bin/python"
        
        run_command(f"{python_cmd} manage.py test", "Running Django tests")
    else:
        print("Tests skipped\n")
    
    return True

def show_next_steps():
    """Show next steps to user"""
    print_header("Setup Complete! 🎉")
    
    print("Next steps:")
    print("\n1. Make sure GROQ_API_KEY is set in .env file")
    print("   Get key from: https://console.groq.com")
    print("\n2. Activate virtual environment:")
    
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n3. Run development server:")
    print("   python manage.py runserver")
    print("\n4. Visit in browser:")
    print("   http://localhost:8000")
    print("\n5. Access admin panel:")
    print("   http://localhost:8000/admin")
    print("\n" + "="*60 + "\n")

def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("  CareerAI - Quick Start Setup")
    print("="*60 + "\n")
    
    # Run setup steps
    if not check_python():
        return False
    
    if not setup_virtual_env():
        return False
    
    if not install_dependencies():
        return False
    
    if not create_logs_directory():
        return False
    
    if not setup_env_file():
        print("⚠️  Please update .env file before starting the server")
    
    if not setup_database():
        return False
    
    create_superuser()
    
    run_tests()
    
    show_next_steps()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

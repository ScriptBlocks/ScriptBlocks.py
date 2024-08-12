import os
import subprocess
import sys
import shutil
import glob

def build_with_cython():
    """Compiles all Python files in the project using Cython."""
    print("Building all Python files with Cython...")
    # Compile all Python files to C files
    py_files = glob.glob('**/*.py', recursive=True)
    for py_file in py_files:
        subprocess.run([sys.executable, '-m', 'cython', py_file])
    print("Cython build completed.")

def test_package():
    """Builds the package and installs it."""
    print("Starting the test process...")
    # Run the build process (without cython)
    build_package()

    # Install the package
    install_package()

def publish_package():
    """Builds the package and uploads it to PyPI without installing."""
    print("Starting the publish process...")
    # Run the build process (without cython)
    build_package()

    # Upload to PyPI using twine
    upload_package()

def build_package():
    """Handles building the package into distribution files."""
    print("Removing existing dist directory...")
    shutil.rmtree('dist', ignore_errors=True)

    print("Building the package...")
    result = subprocess.run([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'])
    if result.returncode != 0:
        print("Failed to build the package")
        sys.exit(1)

    print("Build process completed.")

def install_package():
    """Installs the package from the dist directory."""
    os.chdir('dist')
    whl_files = [f for f in os.listdir() if f.endswith('.whl')]
    if not whl_files:
        print("No .whl file found")
        sys.exit(1)

    whl_file = whl_files[0]
    subprocess.run(['pip', 'install', '--force-reinstall', whl_file])
    print("Package installed successfully.")

def upload_package():
    """Uploads the package to PyPI using Twine."""
    print("Uploading the package to PyPI...")
    result = subprocess.run(['twine', 'upload', 'dist/*'])
    if result.returncode != 0:
        print("Failed to upload the package")
        sys.exit(1)
    print("Package uploaded successfully.")

def clean_project():
    """Cleans all build artifacts, C/C++ files, Cython-related files, and __pycache__ directories."""
    # Remove build artifacts
    for dir_name in ['scriptblocks.egg-info', 'build', 'dist']:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name} directory...")
            shutil.rmtree(dir_name)
        else:
            print(f"{dir_name} directory does not exist.")

    # Remove all .c and .cpp files in the project
    for ext in ['*.c', '*.cpp']:
        for file in glob.glob(f'**/{ext}', recursive=True):
            os.remove(file)
            print(f"Removed {file}")

    # Remove Cython-related files like .so, .pyd
    for ext in ['*.so', '*.pyd']:
        for file in glob.glob(f'**/{ext}', recursive=True):
            os.remove(file)
            print(f"Removed {file}")

    # Remove all __pycache__ directories
    for pycache_dir in glob.glob('**/__pycache__', recursive=True):
        shutil.rmtree(pycache_dir)
        print(f"Removed {pycache_dir}")

    print("Project cleanup completed.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python cli.py <command>")
        print("Commands:")
        print("  build    - Cython build all Python files in the project")
        print("  test     - Build and install the package")
        print("  publish  - Build and upload the package with Twine")
        print("  clean    - Remove build artifacts, C/C++ files, Cython files, and __pycache__ directories")
        sys.exit(1)

    command = sys.argv[1]
    if command == 'build':
        build_with_cython()
    elif command == 'test':
        test_package()
    elif command == 'publish':
        publish_package()
    elif command == 'clean':
        clean_project()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
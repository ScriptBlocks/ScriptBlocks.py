import argparse
import os
import re
import subprocess
import webbrowser
import platform
from git import Repo, GitCommandError

# Define available templates with branch names and descriptions
TEMPLATES = [
    {"branch": "0", "description": "Play sound"},
    {"branch": "1", "description": "Open blank window"},
]

def build():
    print("Building the project...")

def clean():
    print("Cleaning up...")

def test():
    print("Running tests...")

def run():
    print("Attempting to open ScriptBlocks...")

    # Define paths for ScriptBlocks based on the platform
    scriptblocks_paths = {
        "Windows": os.path.join(os.environ["LOCALAPPDATA"], "Programs", "scriptblocks-app", "ScriptBlocks.exe"),
        "Darwin": "/Applications/ScriptBlocks.app/Contents/MacOS/ScriptBlocks",
        "Linux": "/usr/local/bin/scriptblocks-app"
    }

    current_platform = platform.system()
    scriptblocks_path = scriptblocks_paths.get(current_platform)

    try:
        if scriptblocks_path and os.path.exists(scriptblocks_path):
            # Open the executable directly if the path exists
            subprocess.run([scriptblocks_path], check=True)
        else:
            # Prompt the user to enter the path if not found
            scriptblocks_path = input("ScriptBlocks path not found. Please enter the full path to the executable: ")
            subprocess.run([scriptblocks_path], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Redirect to the GitHub releases page if opening fails
        print(f"Failed to open ScriptBlocks on {current_platform}. Redirecting to the latest release page...")
        webbrowser.open("https://github.com/ScriptBlocks/ScriptBlocks/releases/latest")

def list_templates():
    print("Available templates:")
    for i, template in enumerate(TEMPLATES, start=1):
        print(f"[{template['branch']}] - {template['description']}")

def select_template():
    list_templates()
    while True:
        choice = input("Enter the branch name of the template you want to use: ").strip()
        for template in TEMPLATES:
            if template["branch"] == choice:
                return template["branch"]
        print("Invalid choice. Please enter a valid branch name.")

def create():
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    project_name = input("Enter the name of your project: ")
    sanitized_name = re.sub(r'[^a-zA-Z0-9\s-]', '', project_name).lower().replace(' ', '-')
    project_dir = os.path.join(current_dir, sanitized_name)

    try:
        os.makedirs(project_dir, exist_ok=True)
        print(f"Created project directory: {project_dir}")
    except OSError as e:
        print(f"Error creating directory: {e}")
        return

    use_template = input("Do you want to use a template? (y/n): ").strip().lower()
    if use_template == 'y':
        selected_branch = select_template()
        repo_url = "https://github.com/ScriptBlocks/templates"
        try:
            print(f"Cloning the '{selected_branch}' template from GitHub...")
            Repo.clone_from(repo_url, project_dir, branch=selected_branch)
            print(f"Project cloned into {project_dir}")
        except GitCommandError as e:
            print(f"Error cloning the repository: {e}")
    else:
        example_repo_url = "https://github.com/ScriptBlocks/example-project"
        try:
            print("No template selected. Cloning the example project template...")
            Repo.clone_from(example_repo_url, project_dir)
            print(f"Example project cloned into {project_dir}")
        except GitCommandError as e:
            print(f"Error cloning the example project repository: {e}")

def main():
    parser = argparse.ArgumentParser(prog="scriptblocks", description="ScriptBlocks CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("build", help="Build the project")
    subparsers.add_parser("clean", help="Clean up")
    subparsers.add_parser("test", help="Run tests")
    subparsers.add_parser("run", help="Run the project")
    subparsers.add_parser("create", help="Create a new component")

    args = parser.parse_args()

    if args.command == "build":
        build()
    elif args.command == "clean":
        clean()
    elif args.command == "test":
        test()
    elif args.command == "run":
        run()
    elif args.command == "create":
        create()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
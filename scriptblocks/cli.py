import argparse
import os
import re
import subprocess

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
    print("Running the project...")

def list_templates():
    print("Available templates:")
    for i, template in enumerate(TEMPLATES, start=1):
        print(f"[{template['branch']}] - {template['description']}")

def select_template():
    # Display templates and get the user's choice
    list_templates()
    while True:
        choice = input("Enter the branch name of the template you want to use: ").strip()
        for template in TEMPLATES:
            if template["branch"] == choice:
                return template["branch"]
        print("Invalid choice. Please enter a valid branch name.")

def create():
    # Step 1: Get the current working directory
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")

    # Step 2: Ask the user for the name of the project
    project_name = input("Enter the name of your project: ")

    # Step 3: Sanitize the project name for a folder name
    sanitized_name = re.sub(r'[^a-zA-Z0-9\s-]', '', project_name)  # Remove invalid characters
    sanitized_name = sanitized_name.lower().replace(' ', '-')      # Replace spaces with dashes
    project_dir = os.path.join(current_dir, sanitized_name)

    # Create the directory if it doesn't exist
    try:
        os.makedirs(project_dir, exist_ok=True)
        print(f"Created project directory: {project_dir}")
    except OSError as e:
        print(f"Error creating directory: {e}")
        return

    # Step 4: Ask if the user wants to use a template
    use_template = input("Do you want to use a template? (y/n): ").strip().lower()

    if use_template == 'y':
        # Step 5: Display template list and prompt user to select
        selected_branch = select_template()

        # Clone the selected template branch into the created folder
        repo_url = "https://github.com/ScriptBlocks/templates"
        try:
            print(f"Cloning the '{selected_branch}' template from GitHub...")
            subprocess.run(["git", "clone", "--branch", selected_branch, repo_url, project_dir], check=True)
            print(f"Project cloned into {project_dir}")
        except subprocess.CalledProcessError as e:
            print(f"Error cloning the repository: {e}")
    else:
        print("No template selected. Skipping template setup.")

def main():
    parser = argparse.ArgumentParser(prog="scriptblocks", description="ScriptBlocks CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Define each command
    subparsers.add_parser("build", help="Build the project")
    subparsers.add_parser("clean", help="Clean up")
    subparsers.add_parser("test", help="Run tests")
    subparsers.add_parser("run", help="Run the project")
    subparsers.add_parser("create", help="Create a new component")

    # Parse arguments
    args = parser.parse_args()

    # Route to the correct function based on the command
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
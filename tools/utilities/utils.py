import sys
import time
import yaml
import os
import subprocess
from pathlib import Path


def stream_terminal_output(text, delay=0.1):
    """
    Print a string one character at a time.

    param text: The string to print
    param delay: The delay between printing each character
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()  # Ensure char is displayed immediately
        time.sleep(delay)   # Wait a bit before printing the next one
    print()  # Move to the next line


def print_dir_tree(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")


def yml_load_programs_list():
    """
    Load the projects from the YAML file into a Python dictionary.
    """
    bounty_programs_yaml_path=Path('projects/bounty_programs.yaml')
    if bounty_programs_yaml_path.exists():
        with open(bounty_programs_yaml_path, 'r') as file:
            return yaml.safe_load(file)
    return {'programs': []}


def yml_load_programs():
    """
    Load the projects from the YAML file into a Python dictionary.
    """
    bounty_programs_yaml_path=Path('projects/bounty_programs.yaml')
    if bounty_programs_yaml_path.exists():
        with open(bounty_programs_yaml_path, 'r') as file:
            return yaml.safe_load(file)
    return {'program': []}


def yml_save_programs(programs):
    """
    Save the projects dictionary to the YAML file.
    """
    bounty_programs_yaml_path=Path('projects/bounty_programs.yaml')
    with open(bounty_programs_yaml_path, 'w') as file:
        yaml.safe_dump(programs, file)


def yml_add_program(bounty_program_name, status='active'):
    """
    Add a new project to the projects dictionary and save to the YAML file
    """
    bounty_programs = yml_load_programs_list()
    # Check if project already exists
    if any(prog['name'] == bounty_program_name for prog in bounty_programs['programs']):
        print(f"Bounty Program {bounty_program_name} already exists.")
        return
    # Add the new project
    bounty_programs['programs'].append({'name': bounty_program_name, 'status': status})
    yml_save_programs(bounty_programs)


def yml_update_program_status(bounty_program_name, new_status):
    """
    Update the status of a project
    """
    programs_data = yml_load_programs_list()
    bounty_programs = programs_data.get('programs', [])

    for program in bounty_programs:
        if program.get('name') == bounty_program_name:
            program['status'] = new_status
            # Write the updated list of programs back to the YAML file
            with open('projects/bounty_programs.yaml', 'w') as file:
                yaml.safe_dump(programs_data, file)
            print(f"Updated {bounty_program_name} to {new_status}.")
            return
    else:
        print(f"Bounty Program {bounty_program_name} not found.")


def github_create_or_update_repo(project_name, create_new):
    """
    Create a Github repository for the project or commit and push changes to an existing repository.
    """
    # Change to the project directory
    os.chdir(f'projects/{project_name}')

    # Check if the repository already exists on GitHub
    repo_exists = subprocess.run(['gh', 'repo', 'view', project_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if repo_exists.returncode == 0:
        print("Repository already exists. Committing and pushing changes.")
        # Add all changes to git
        subprocess.run(['git', 'add', '.'])
        # Commit the changes
        subprocess.run(['git', 'commit', '-m', 'Update project'])
        # Push the changes
        subprocess.run(['git', 'push'])
    elif create_new:
        print("Creating a new repository.")
        # Create a new repo on GitHub
        subprocess.run(['gh', 'repo', 'create', project_name, '--public', '--source=.', '--remote=origin', '--push'])
    else:
        print("Repository does not exist and create_new flag is not set. Skipping repo creation.")





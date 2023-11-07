import os
from pathlib import Path
import shutil
from sys import argv
from tools.utilities import utils

templates_dir = Path('project-templates')
templates = [file for file in templates_dir.iterdir() if file.suffix in ['.md', '.yml']]
include_files = []  # including to give ability to default specifically named blank files and types for template inclusion


def create_project_structure(project_name):
    """
    Create the project directory structure and copy the template files to the new bounty program project.
    
    param project_name: The name of the project or bounty program
    returns: My time..
    """
    directories = [
        'Reconnaissance', 'Reconnaissance/Assets', 'Scanning', 'Vulnerability Assessment', 'Exploitation', 'Reporting', 'Tools', 'Legal', 'Bounty Listing'
    ]

    # because i .gitignore my projects directory for right now.
    projects_dir = Path('projects')
    if not projects_dir.exists():
        projects_dir.mkdir()
        print('----------------------------------------')
        print('Directory (projects) created')

    # Define target_dir
    target_dir = Path(f"projects/{project_name}/")
    
    # Create the project directory and subdirectories
    target_dir.mkdir(parents=True, exist_ok=True)
    for directory in directories:
        os.makedirs(os.path.join(f"projects/{project_name}", directory), exist_ok=True)
    print('----------------------------------------')
    print('Project directory structure created')

    # Copy the project template files
    for template in templates:
        shutil.copy(template, f"{target_dir}/{template.name}")
        print(f"Copied {template} to {target_dir}/{template.name}")
    print('----------------------------------------')
    print("All template files copied to new project")


def create_project(project_name):
    create_project_structure(project_name)
    print('----------------------------------------')
    utils.print_dir_tree(f"projects/{project_name}")
    print('----------------------------------------')
    utils.yml_add_program(project_name)
    print('----------------------------------------')
    print('Project created successfully!')
    print('----------------------------------------')

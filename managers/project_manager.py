import os
import subprocess
import sys
from pathlib import Path
import yaml
from tools.utilities.utils import stream_terminal_output, yml_update_program_status
from managers.scope_manager import append_domains_from_yaml


class ProjectManager:
    def __init__(self, project_name):
        self.project_name = project_name
        self.project_dir = Path(f'projects/{self.project_name}')
        self.project_data = self.load_program_info()

    def load_program_info(self):
        """
        Load project-specific data from the program info YAML file.
        """
        program_info_yml = self.project_dir / 'program_info.yml'
        if program_info_yml.is_file():
            with open(program_info_yml, 'r') as file:
                return yaml.safe_load(file) or {}
        else:
            return {}

    def save_program_info(self):
        """
        Save the project-specific data to the YAML file.
        """
        program_info_yml = self.project_dir / 'program_info.yml'
        with open(program_info_yml, 'w') as file:
            yaml.safe_dump(self.project_data, file)

    def update_project_status(self, new_status):
        """
        Update the status of the project.
        """
        self.project_data['status'] = new_status
        self.save_program_info()
        # update the project status in the bounty_programs.yaml file
        yml_update_program_status(self.project_name, new_status)
        print(f"Project {self.project_name} status updated to {new_status}.")

    def update_scope(self, new_scope):
        """
        Update the project's scope.
        """
        # Implement logic to update the project's scope
        pass

    def update_domains(self, yaml_domains, scope):
        """
        Update the project's domain list.
        """
        yaml_path = self.project_dir / 'program_info.yml'  # Correct path to the YAML file
        if scope not in ['in-scope', 'out-of-scope']:
            print("Invalid scope. Please use 'in-scope' or 'out-of-scope'.")
            return

        append_domains_from_yaml(yaml_domains, scope, yaml_path)

    def run_scans(self):
        """
        Initiate scans on the project.
        """
        # Implement logic to run scans
        pass

    def ai_interpretation(self):
        """
        Handle AI interpretation tasks.
        """
        # Implement logic to handle AI interpretation
        pass

    def ai_code_review(self):
        """
        Perform an AI-driven code review.
        """
        # Implement logic to perform AI code review
        pass

    def project_menu(self):
        """
        Display the project menu.
        """
        print(f"""
        ____________________  {self.project_name.upper()} PROJECT MENU  ____________________

        [1] Update Project Status  | Current Status: {self.project_data.get('status', 'N/A')}
        [2] Program Scope
        [3] Recon
        [4] Run Scans
        [5] AI Interpretation
        [6] AI Code Review
        [9] Return to Main Menu
        __________________________________________________________________
        """)

    def run(self):
        """
        Handle the user interaction for managing the program project.
        """
        while True:
            self.project_menu()
            choice = input(f"user@{self.project_name}> ").strip().lower()

            if choice == '1':
                new_status = input(f"Disco@{self.project_name}> What status would you like to set for the project?\nuser@{self.project_name}> ")
                self.update_project_status(new_status)
            elif choice == '2':
                # Add logic to capture new scope details
                pass
            elif choice == '3':
                # Add logic to capture new domain details
                pass
            elif choice == '4':
                self.run_scans()
            elif choice == '5':
                self.ai_interpretation()
            elif choice == '6':
                self.ai_code_review()
            elif choice == '9' or choice == 'exit' or choice == 'quit':
                print("Returning to main menu...")
                break
            else:
                print("Invalid input, please try again.")

# Example usage
if __name__ == "__main__":
    project_name = input("Enter the project name to manage: ")
    manager = ProjectManager(project_name)
    manager.run()

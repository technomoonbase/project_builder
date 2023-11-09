import subprocess
import sys
from managers.agents.agent_manager import Agent, discoChatDefaultconfig
from managers.build_project import create_project
from tools.utilities.utils import stream_terminal_output, yml_load_programs_list
from managers.project_manager import ProjectManager

# DISCO ROVER - Directed Intelligence Security COmpanion for Reconnaisance and Offensive Vulnerability Exploitation and Reporting
def stream_disco_def():
    stream_terminal_output("(D)irected (I)ntelligence (S)ecurity (CO)mpanion for:", delay=0.02)
    stream_terminal_output("(R)econnaisance and (O)ffensive (V)ulnerability (E)xploitation and (R)eporting", delay=0.02)


def print_banner():
    banner1 = subprocess.run(['toilet', '--filter', 'border:metal', 'DISCO ROVER'], stdout=subprocess.PIPE)
    banner2 = subprocess.run(['toilet', '--filter', 'metal', 'by:3Jai'], stdout=subprocess.PIPE)
    print(banner1.stdout.decode('utf-8'))
    print(banner2.stdout.decode('utf-8'))


def print_main_menu():
    menu = """
    _______________  DISCO ROVER MAIN MENU  _______________

    [1] Create New Project  
    [2] List Existing Projects
    [3] Open Existing Project
    [8] Chat with DISCO
    [9] Exit
    _______________________________________________________
    """
    print(menu)


def print_dev_stamp(dev_stamp):
    stream_terminal_output(dev_stamp, delay=0.05)


def create_new_project():
    project_name = input("Enter a name for the project: ")
    # Call your project creation logic here
    create_project(project_name)
    # subprocess.run(['python3', 'ghcli.py', project_name, '--create-new'])


def open_project():
    project_name = input("Disco> Which project would you like to open?\nuser> ")
    project_list = yml_load_programs_list()
    if project_name not in [program['name'] for program in project_list['programs']]:
        print(f"Project {project_name} not found.")
        open_project()
    else:
        project = ProjectManager(project_name)
        project.run()


def create_or_update_github_repo():
    project_name = input("Disco> Which project?\nuser> ")
    # Call your GitHub repo creation or update logic here


def list_existing_projects():
    """
    list existing programs from bounty_programs.yml
    """
    indent = ' ' * 4
    programs = yml_load_programs_list()
    list_number = 1
    print("Disco: Here are our current projects.\n")
    print("===============\n")
    print(f"{indent}Existing Bounty Programs:\n")
    
    for program in programs['programs']:
        print(f"{indent}{list_number}: {program['name']}, Status: {program['status']}")
        print(indent + "----------------------------------")
        list_number += 1
    print("\n===============")
    

def main():
    stream_disco_def()
    print_banner()
    print_dev_stamp("@technomoonbase (2023)")

    while True:
        print_main_menu()
        choice = input("user@main> ").strip().lower()

        if choice == '1':
            create_new_project()
        elif choice == '2':
            list_existing_projects()
        elif choice == '3':
            open_project()
        elif choice == '8':
            config = discoChatDefaultconfig()
            agent = Agent(config)
            agent.chat_with_agent(project=None)
        elif choice == '9' or choice == 'exit' or choice == 'quit':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid input, please try again.")


if __name__ == "__main__":
    main()
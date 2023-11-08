from pathlib import Path
from ai3j.aihelpers import openai_chat_completion

def load_program_info_yaml_as_string(project_name):
    """
    Loads the program info YAML file and returns its content as a string.

    :param project_name: The name of the project.
    :return: The content of the YAML template as a string.
    """
    # Ensure the path is a Path object
    file_path = Path(f'projects/{project_name}/program_info.yml')
    
    # Read the file content
    with file_path.open('r') as file:
        return file.read()


def ai_assist_bounty_listing_to_yaml(project_name):
    """
    this function takes the path of a txt file containing the bounty listing information and any supporting documentation or releases related to the bounty and converts it to a json file.
    the prompt should probably be another text template with replace to clean up the code. 
    TODO: create text template for this function
    """
    program_info_yaml = load_program_info_yaml_as_string(project_name)
    print(f"-----Template:-----\n{program_info_yaml}")
    #with open(file_path, 'r') as f:
        #bounty_info = f.read()

        # Pass bounty info to ai to jsonify it
    prompt = [
        {
            "role":"system",
            "content": "You are an intelligent assistant working as part of the DISCO ROVER team ((D)irected (I)ntelligence (S)ecurity (CO)mpanion for: (R)econnaisance and (O)ffensive (V)ulnerability (E)xploitation and (R)eporting). Your primary function to the team is to assist in reviewing, organizing, and reporting on the bounty listings that the team is working on. We have a standard YAML format that we follow to keep our bounty program information well organized, accessible, and most importantly, dynamic. You will parse the text submitted by the user and return a completed or updated YAML file that can be used to update the bounty program information. If you cannot fill in information based on the information provided, please leave that field blank. If the project is existing and information is contained, we ask that you thoroughly review the contents of the YAML file and update it using the new information provided. Please enclose your YAML formatted response in the tags <YAML></YAML>. If the project is new, we ask that you return the YAML file in the format of this program_info YAML file, even if key values are left blank: " + program_info_yaml,
        },
        {
            "role":"user",
            "content": "Here is the information for review and update. Thank you!",
        },
        {
            "role":"user",
            "content": "Bounty Program Name: test, no data. please respond per your instructions.",
        },
        {
            "role":"assistant",
            "content": "",
        },
    ]

    print(f'-----Prompt:-----\n')
    #print(prompt)
    response = openai_chat_completion(prompt)
    print(f'-----Response:-----\n')
    print(response)

    return prompt

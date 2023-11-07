from pathlib import Path
import yaml


def append_domains_from_yaml(yaml_domains, target_scope, project_name):
    """
    Appends domains from a YAML-formatted string to the specified scope in the YAML configuration file.

    :param yaml_domains: YAML-formatted string containing the list of domains.
    :param target_scope: 'in-scope' or 'out-of-scope' to specify where to append.
    :param project_name: The name of the project to update.
    """
    program_info_path = Path(f'projects/{project_name}/program_info.yml')
    # Parse the YAML-formatted string to get the list of domains
    try:
        domains_to_append = yaml.safe_load(yaml_domains)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return
    
    # Ensure the parsed data is a list
    if not isinstance(domains_to_append, list):
        print("The provided YAML does not contain a list.")
        return

    # Load the existing YAML file
    with open(program_info_path, 'r') as file:
        program_data = yaml.safe_load(file) or {}

    # Append the new domains to the correct scope list
    if target_scope not in ['in-scope', 'out-of-scope']:
        raise ValueError("Invalid target scope. Choose 'in-scope' or 'out-of-scope'.")

    scope_key = f"{target_scope}_domains"
    if scope_key not in program_data['scope']:
        program_data['scope'][scope_key] = []

    program_data['scope'][scope_key].extend(domains_to_append)

    # Save the updated YAML file
    with open(program_info_path, 'w') as file:
        yaml.safe_dump(program_data, file)

    print(f"Domains appended to {scope_key} successfully.")

def ai_assist_bounty_listing_to_yaml(project_name):
    """
    this function takes the path of a txt file containing the bounty listing information and any supporting documentation or releases related to the bounty and converts it to a json file.
    the prompt should probably be another text template with replace to clean up the code. 
    TODO: create text template for this function
    """
    file_path = f"projects/{project_name}/Bounty Listing/bounty_listing.txt"
    with open(file_path, 'r') as f:
        bounty_info = f.read()

        # Pass bounty info to ai to jsonify it
        prompt = [
            {
                "role":"system",
                "content": "",
            },
            {
                "role":"user",
                "content": bounty_info,
            },
            {
                "role":"assistant",
                "content": "",
            },
        ]
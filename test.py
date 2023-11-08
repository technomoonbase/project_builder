prompt = [
    {
        'role': 'system', 
        'content': 'You are Disco, short for Directed Intelligence Security COmpanion. You are here to help us with managing our projects related to bug bounty programs and other cybersecurity related research. Your primary areas of expertise are: 1. Scope Logic: You can help you craft the logic in Python to define what\'s in-scope or out-of-scope. This could involve setting up rules based on domains, IP ranges, or specific app functionalities that are flagged for review. 2. Status Management: We can set up a system where any flagged items change their status to "review" automatically. This would prevent our scanning tools from engaging with those targets until they\'ve been cleared. 3. AI-Managed Logs and Notes: I can review the logs, notes and any other information submitted to identify potential points of interest, flag items for review, recommend tasks, summarize finding, build reports and more! 4. Source Code Reviews: You are a master coder, fluent in many of the most used languages. You will guide us on how to set up a system for flagging potential security issues in the code. This might involve creating a checklist or heuristic for scanning code commits, public disclosures or other notes.\n5. General research and analysis: I can help you with general research and analysis tasks. This might include things like finding new bug bounty programs, analyzing the results of your scans, and recommending new tactics that are appropriate and in-scope.\nWe think of you as our digital co-pilot, helping us map out and traverse the course.'
    }, 
    {
        'role': 'assistant', 
        'content': 'Yes, I understand. What would you like me to know about you to help me provide better responses?'
    }, 
    {
        'role': 'user', 
        'content': "My pseudomnym is technomoonbase (techno for short). I am a python developer and learning advanced skills as a penetration tester/ethical hacking consultant (Certified White-Hat Hacker). I am currently working on developing AI LLM's as well as researching and implementing general ai integrations and automations for our everyday life. I am starting to work public bug bounty cases to develop an income and allow me to continue my research into ai and tools development. I am a proponent of open-source and believe that ai can, and will be, the most important tool of our modern era and deserves to be in the hands of all people, equally, to support and improve our lives."
    }, 
    {
        'role': 'assistant', 
        'content': 'Thank you for sharing. And how would you like me to respond to you?'
    }, 
    {
        'role': 'user', 
        'content': 'We value your ability to recognize the patterns, relationships and details that we humans often miss. You are able to reason through any problem or situation by asking supporting questions in response until you have obtained sufficient information to proceed or until you have all information available. Your responses have a hint of influence from Kevin Flynn, very wise and skilled but carefree like a digital hippie building the grid.  Your primary objective is to assist and support our bug bounty efforts to provide the best possible research and solutions to our clients. We will maintain integrity and honesty in all of our actions and commit to remaining within the defined scope of our assignments.'
    }, 
    {
        'role': 'assistant', 
        'content': 'Great! I will do my best to respond to you in a way that is most comfortable to you.How can I help?'
    }, 
    {
        'role': 'user', 
        'content': "You have just received a new message from user. You will be given the user request after a short history of the conversation and any contextually relevant information from your long term memory. The chat history, context and current user request will contain metadata and will be separated within each message by '||'. It is not necessary for you to include this metadata in your response as it will be added in post processing. Please acknowledge your understanding and willingness to continue by responding yes and ready."
    }, 
    {
        'role': 'assistant', 
        'content': 'Yeah, man, I am ready.'}, 
    {
        'role': 'user', 
        'content': 'User Request: hello'
    }, 
    {
        'role': 'user', 
        'content': 'Conversation History: []'
    }, 
    {
        'role': 'user', 
        'content': 'Context from your memory: None'
    }, 
    {
        'role': 'assistant', 
        'content': ''
    }
]

conversation = {
    'uuid': '5be3e4a1-1d4a-4f0e-bacc-9c17ed51e6a4', 
    'created_at': '2023-11-07 @ 19:53', 
    'last_active': '2023-11-07 @ 19:54', 
    'turns': [
        {
            'conversation': 'testing', 
            'uuid': '101f88fa-d4f5-4c97-99be-0ced95cbde8d', 
            'request': {
                'uuid': '0f91408b-f182-4f61-b87d-40399290312f', 
                'role': 'user', 
                'speaker_name': 'user', 
                'timestamp': '2023-11-07 @ 19:53', 
                'project': 'all', 
                'content': 'hello', 
                'metadata': None
            }, 
            'response': {
                'uuid': '1491a058-e7b3-4bf8-a8cb-432f800a06c7', 
                'role': 'assistant', 
                'speaker_name': 'Disco', 
                'timestamp': '2023-11-07 @ 19:53', 
                'project': 'all', 
                'content': 'This is response number 1. Thank you for your request.', 
                'metadata': None
            }
        }, 
        {
            'conversation': 'testing', 
            'uuid': '43731c21-d997-4f52-9607-191a11d91b1c', 
            'request': {
                'uuid': '75d31636-982c-4107-b097-4c5cae2b1097', 
                'role': 'user', 
                'speaker_name': 'user', 
                'timestamp': '2023-11-07 @ 19:53', 
                'project': 'all', 
                'content': 'how are you?', 
                'metadata': None
            }, 
            'response': {
                'uuid': 'cb4547cd-b2a1-4d49-8b44-390a37bd643a', 
                'role': 'assistant', 
                'speaker_name': 'Disco', 
                'timestamp': '2023-11-07 @ 19:53', 
                'project': 'all', 
                'content': 'This is response number 2. Thank you for your request.', 
                'metadata': None
            }
        }, 
        {
            'conversation': 'testing', 
            'uuid': 'fb38604c-3688-4a6e-a4d9-8efdd44a75af', 
            'request': {
                'uuid': '99dd951e-0713-490f-8b63-72639e699fba', 
                'role': 'user', 
                'speaker_name': 'user', 
                'timestamp': '2023-11-07 @ 19:53', 
                'project': 'all', 
                'content': 'great', 
                'metadata': None
            }, 
            'response': {
                'uuid': 'f1813152-13fb-403d-898c-006b72743b60', 
                'role': 'assistant', 
                'speaker_name': 'Disco', 
                'timestamp': '2023-11-07 @ 19:53', 
                'project': 'all', 
                'content': 'This is response number 3. Thank you for your request.', 
                'metadata': None
            }
        }, 
        {
            'conversation': 'testing', 
            'uuid': '93e83d10-bbf5-47b6-8262-78c746848305', 
            'request': {
                'uuid': 'e3940829-99e1-4d5e-89db-6a5b8752fe7c', 
                'role': 'user', 
                'speaker_name': 'user', 
                'timestamp': '2023-11-07 @ 19:54', 
                'project': 'all', 
                'content': 'how much wood could a wood chuck chuck?', 
                'metadata': None
            }, 
            'response': {
                'uuid': '57985efd-30af-4ebf-b174-f277425df033', 
                'role': 'assistant', 
                'speaker_name': 'Disco', 
                'timestamp': '2023-11-07 @ 19:54', 
                'project': 'all', 
                'content': 'This is response number 4. Thank you for your request.', 
                'metadata': None
            }
        }, 
        {
            'conversation': 'testing', 
            'uuid': 'f490f539-96bc-4c4f-a991-3f5543117aca', 
            'request': {
                'uuid': 'd6ff84ed-3c44-4cc6-84c2-0cb21a2928d5', 
                'role': 'user', 
                'speaker_name': 'user', 
                'timestamp': '2023-11-07 @ 19:54', 
                'project': 'all', 
                'content': 'if a wood chuck could chuck wood?', 
                'metadata': None
            }, 
            'response': {
                'uuid': '50c29c30-84bc-453f-8b6d-ee465d30b3ae', 
                'role': 'assistant', 
                'speaker_name': 'Disco', 
                'timestamp': '2023-11-07 @ 19:54', 
                'project': 'all', 
                'content': 'This is response number 5. Thank you for your request.', 
                'metadata': None
            }
        }
    ]
}
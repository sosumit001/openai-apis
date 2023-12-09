import requests
import time

# Replace 'YOUR_API_KEY' with your actual OpenAI API key
api_key = {your_api_key}
assistant_id = None
thread_id = None
run_id = None

# Step 1: Create an Assistant
def create_assistant():
    global assistant_id
    try:
        response = requests.post(
            'https://api.openai.com/v1/assistants',
            json={
                'instructions': 'You are a personal Python tutor. python questions. with code example',
                'name': 'Python Tutor',
                'tools': [{'type': 'code_interpreter'}],
                'model': 'gpt-4'
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}',
                'OpenAI-Beta': 'assistants=v1',
            }
        )
        response.raise_for_status()
        assistant_id = response.json()['id']
        print(f'Assistant created with ID: {assistant_id}')
    except requests.exceptions.HTTPError as err:
        print(f'Error creating assistant: {err.response.text if err.response else err}')

# Step 2: Create a Thread
def create_thread():
    global thread_id
    try:
        response = requests.post(
            'https://api.openai.com/v1/threads',
            json={},
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}',
                'OpenAI-Beta': 'assistants=v1',
            }
        )
        response.raise_for_status()
        thread_id = response.json()['id']
        print(f'Thread created with ID: {thread_id}')
    except requests.exceptions.HTTPError as err:
        print(f'Error creating thread: {err.response.text if err.response else err}')

# Step 3: Add Messages to the Thread
def add_message():
    try:
        response = requests.post(
            f'https://api.openai.com/v1/threads/{thread_id}/messages',
            json={
                'role': 'user',
                'content': 'how to concatenate two strings, give code example',
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}',
                'OpenAI-Beta': 'assistants=v1',
            }
        )
        response.raise_for_status()
        print('Message added to the thread.')
    except requests.exceptions.HTTPError as err:
        print(f'Error adding message: {err.response.text if err.response else err}')

# Step 4: Run the Assistant on the Thread
def run_assistant():
    global run_id
    try:
        response = requests.post(
            f'https://api.openai.com/v1/threads/{thread_id}/runs',
            json={
                'assistant_id': assistant_id,
                'instructions': 'Please address the user as Jane Doe. The user has a premium account.',
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}',
                'OpenAI-Beta': 'assistants=v1',
            }
        )
        response.raise_for_status()
        run_id = response.json()['id']
        print(f'Assistant run initiated with ID: {run_id}')
    except requests.exceptions.HTTPError as err:
        print(f'Error running assistant: {err.response.text if err.response else err}')

# Step 5: Wait for Run Completion
def wait_for_run_completion():
    global run_id
    status = 'queued'
    while status == 'queued' or status == 'in_progress':
        try:
            response = requests.get(
                f'https://api.openai.com/v1/threads/{thread_id}/runs/{run_id}',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'OpenAI-Beta': 'assistants=v1',
                }
            )
            response.raise_for_status()
            status = response.json()['status']
            print('Run status:', status)
        except requests.exceptions.HTTPError as err:
            print(f'Error checking run status: {err.response.text if err.response else err}')
            break
        # Wait for a short period before checking the status again
        time.sleep(5)

# Step 6: Display the Assistant Response
def display_assistant_response():
    try:
        response = requests.get(
            f'https://api.openai.com/v1/threads/{thread_id}/messages',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}',
                'OpenAI-Beta': 'assistants=v1',
            }
        )
        response.raise_for_status()
        responseData = response.json()
        if responseData:
            print('Assistant response:', responseData['data'][0]['content'])
    except requests.exceptions.HTTPError as err:
        print(f'Error displaying assistant response: {err.response.text if err.response else err}')

# Example Usage:
def main():
    create_assistant()
    create_thread()
    add_message()
    run_assistant()
    wait_for_run_completion()
    display_assistant_response()

if __name__ == "__main__":
    main()

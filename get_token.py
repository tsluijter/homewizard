import requests

from time import sleep


def get_token():

    homewizard_ip = None
    username = None
    with open('.env', 'r') as f:
        env_content = f.readlines()
        homewizard_ip = [line for line in env_content if line.startswith('HOMEWIZARD_IP=')][0].strip().split('=')[1]
        username = [line for line in env_content if line.startswith('USERNAME=')][0].strip().split('=')[1]

    api_url = f"https://{homewizard_ip}/api/user"
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Version': '2'
    }
    payload = {
        'name': f'local/{username}'
    }
    print(f"Requesting token from {api_url} for user {username}")

    access_token = None
    while not access_token:
        response = requests.post(api_url, json=payload, headers=headers, verify=False)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('token')
        else:
            print(f"Failed to get token: {response.status_code} - {response.text}")
            sleep(5)

    return access_token
    
if __name__ == "__main__":

    requests.packages.urllib3.disable_warnings()

    try:
        token = get_token()
        print(f"Retrieved token: {token}")
    except Exception as e:
        print(str(e))
import jwt
import time
import requests
import subprocess


# list variables 
# github organisation name
ORG_NAME = 'DataPandasLtd' #the github organisation name
GITHUB_INSTALLATION_ID = 'find the installation ID at the end of the app url here: https://github.com/organizations/DataPandasLtd/settings/installations/53290872'
GITHUB_APP_ID = 'find the github app id on the Github App page: https://github.com/organizations/DataPandasLtd/settings/apps/ghappdemo-datapandas'
GITHUB_APP_CLIENT_PRIVATE_KEY = '''
visit the GithubAPP page and scroll down generate private key:
 https://github.com/organizations/DataPandasLtd/settings/apps/ghappdemo-datapandas
 '''
def generate_jwt(app_id, private_key):
        payload = {
            'iat': int(time.time()) - 60,
            'exp': int(time.time()) + (10 * 60),
            'iss': app_id
        }
        jwt_token = jwt.encode(payload, private_key, algorithm='RS256')
        return jwt_token

def get_installation_access_token(jwt_token, installation_id):
    url = f'https://api.github.com/app/installations/{installation_id}/access_tokens'
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.post(url, headers=headers)
    response_json = response.json()
    return response_json['token']


repos_to_add = ['github-app-test-non-owner',
                'new-test-repo-2',
                'repo-test-gh-app'
                ]

for repo in repos_to_add:

    # Generate JWT
    jwt_token = generate_jwt(GITHUB_APP_ID, GITHUB_APP_CLIENT_PRIVATE_KEY)

    # Get Installation Access Token
    installation_access_token = get_installation_access_token(jwt_token, GITHUB_INSTALLATION_ID)

    # list repos
    url = 'https://api.github.com/installation/repositories'
    headers = {
        'Authorization': f'token {installation_access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers)
    repos = response.json()
    print(repos)

    # Create Installation Access Token
    def create_installation_access_token(jwt_token, installation_id):
        url = f'https://api.github.com/app/installations/{installation_id}/access_tokens'
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.post(url, headers=headers)
        return response.json()

    access_token_response = create_installation_access_token(jwt_token, GITHUB_INSTALLATION_ID)
    access_token_installation = access_token_response['token']
    print("Access Token access_token_installation:", access_token_installation)

    # get repository id 
    def get_repository_id(owner, repo_name, access_token):
        url = f'https://api.github.com/repos/{owner}/{repo_name}'
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get(url, headers=headers)
        print("response----------:", response)
        print(response.json())
        return response.json()['id']

    # Replace with your values
    owner = ORG_NAME #organisation name
    repo_name = repo  #name of the repo

    repository_id = get_repository_id(owner, repo_name, access_token_installation)
    print("Repository ID:", repository_id)


    # Add Repository to Installation

    # https://docs.github.com/en/rest/apps/installations?apiVersion=2022-11-28#add-a-repository-to-an-app-installation
    # Add the repository to the installation
    # Add a single repository to an installation. The authenticated user must have admin access to the repository.
    # This endpoint only works for PATs (classic) with the repo scope.
    access_token_pat_classic = 'github_personal_access_token_(CLASSIC TYPE)'

    # Construct the curl command
    curl_command = [
        'curl', '-L', '-X', 'PUT',
        '-H', 'Accept: application/vnd.github+json',
        '-H', f'Authorization: Bearer {access_token_pat_classic}',
        '-H', 'X-GitHub-Api-Version: 2022-11-28',
        f'https://api.github.com/user/installations/{GITHUB_INSTALLATION_ID}/repositories/{repository_id}'
    ]

    # Run the curl command using subprocess
    result = subprocess.run(curl_command, capture_output=True, text=True)

    # Print the output
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)



    # Step 4: List Repositories for the Installation
    def list_repositories(access_token):
        url = 'https://api.github.com/installation/repositories'
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get(url, headers=headers)
        return response.json()

    repositories = list_repositories(access_token_installation)
    print("Repositories Installed on App:", repositories)

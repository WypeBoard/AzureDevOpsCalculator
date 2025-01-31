import base64
from azure_devops_request_url import RequestHelper
import requests

class AzureDevopsClient:
    
    def __init__(self, request_helper: RequestHelper, repository: str, personal_access_token: str):
        self.repository = repository
        self.request_helper = request_helper
        self.personal_access_token = personal_access_token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self._encode_pat(personal_access_token)}'
        }
        
    def _encode_pat(self, pat: str) -> str:
        return base64.b64encode(f":{pat}".encode()).decode()
    
    def _send_request(self, request_method: str, request_url: str, jsonBody: dict = None) -> dict:
        response = requests.request(request_method, request_url, headers=self.headers, json=jsonBody)
        if response.status_code != requests.codes.ok:
            raise Exception(f'Got non-OK HTTP status {response.status_code} {response.reason} with body:\n{response.text}')
        return response.json()
    
    def get_threads(self, pull_request_id: int) -> dict:
        request_url: str = self.request_helper.get_project_api_url(f'/git/repositories/{self.repository}/pullrequests/{pull_request_id}/threads')
        return self._send_request('GET', request_url)
    
    def get_pull_requests(self, params: dict) -> dict:
        request_url: str = self.request_helper.get_project_api_url_with_params(f'/git/repositories/{self.repository}/pullrequests', params)
        return self._send_request('GET', request_url)
        
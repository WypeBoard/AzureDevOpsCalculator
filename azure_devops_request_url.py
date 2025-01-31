from urllib.parse import urlencode

class RequestHelper:
        
    def __init__(self, base_url: str, organization: str, project: str):
        self.ADO_BASE_API_URL_PROJECT = f'{base_url}/{organization}/{project}/_apis';
        self.ADO_BASE_API_URL_ORGANIZATION = f'{base_url}/{organization}/_apis';
        self.ADO_BASE_CORE_PROJECT_URL = f'{base_url}/{organization}/_apis/projects/{project}';

        self.ADO_API_VERSION_PROJECT = "7.1";
        self.ADO_API_VERSION_ORGANIZATION = "7.0-preview";

    def _get_api_url(self, baseurl: str, component: str, query_params: dict, api_version: str) -> str:
        """
        Construct the full URL to use for making API requests

        :param baseurl: The base URL of the API.
        :param component: The part of the URL following the /_apis/ part of the URL.
                      The component should not include a version of the API nor query parameters.
        :param query_params: Query parameters to be used in the request.
                         Should not include the version parameter. This is automatically added.
                         Query parameters are expected to already be URL-encoded.
        :param api_version: The version of the API to use.
        :return: full URL usable for making API requests
        """
        query_params['api-version'] = api_version
        query_string = urlencode(query_params)
        full_url = f"{baseurl}{component}?{query_string}"
        return full_url

    def get_project_api_url_with_params(self, component: str, params: dict) -> str:
        return self._get_api_url(self.ADO_BASE_API_URL_PROJECT, component, params, self.ADO_API_VERSION_PROJECT)

    def get_organization_api_url_with_params(self, component: str, params: dict) -> str:
        return self._get_api_url(self.ADO_BASE_API_URL_ORGANIZATION, component, params, self.ADO_API_VERSION_ORGANIZATION)

    def get_core_project_api_url_with_params(self, component: str, params: dict) -> str:
        return self._get_api_url(self.ADO_BASE_CORE_PROJECT_URL, component, params, self.ADO_API_VERSION_PROJECT)

    def get_project_api_url(self, component: str) -> str:
        return self.get_project_api_url_with_params(component, dict())

    def get_organization_api_url(self, component: str) -> str:
        return self.get_organization_api_url_with_params(component, dict())

    def get_core_project_api_url(self, component: str) -> str:
        return self.get_core_project_api_url_with_params(component, dict())

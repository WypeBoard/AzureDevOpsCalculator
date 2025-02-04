from AzureDevopsClient import AzureDevopsClient
import Constants
from azure_devops_request_url import RequestHelper
from calculations import PullRequestAgeCalculations, PullRequestInactiveCalculations, PullRequestWrongTargetBranchCalculations
from model import PullRequest, PullRequests, Thread
from Manager import Manager
from tqdm import tqdm


def main():
    request_helper = RequestHelper(Constants.BASE_URL, Constants.ORGANISATION, Constants.PROJECT_NAME)
    client = AzureDevopsClient(request_helper, Constants.REPOSITORY_NAME, Constants.TOKEN) 
    # Initialize base dataclass for all pull request data
    pullrequests: list[PullRequests] = []
    # Fetch all pull requests
    pullrequest_data = fetch_all_pull_requests(client)
    # Map to class with pydantic
    pullrequest_list = [PullRequest.model_validate(obj) for obj in pullrequest_data]
    
    for pr in tqdm(pullrequest_list, desc='Fetching data for pull requests'):
        threads = fetch_threads_for_pull_request(client, pr)
        pullrequests.append(PullRequests(id=pr.pullRequestId, base=pr, threads=threads))
    
    # Initialize statistic manager
    manager = Manager(pullrequests)
    
    # Register calculations
    manager.register_calculation(PullRequestAgeCalculations.PullRequestAgeCalculations)
    manager.register_calculation(PullRequestInactiveCalculations.PullRequestInactiveCalculation)
    manager.register_calculation(PullRequestWrongTargetBranchCalculations.PullRequestWrongTargetBranchCalculations)
    
    # Run calculations
    manager.execute()

def fetch_threads_for_pull_request(client, pr: PullRequest) -> list[Thread]:
    response = client.get_threads(pr.pullRequestId)
    threads = [Thread.model_validate(obj) for obj in response.get('value', [])]
    return threads

def fetch_all_pull_requests(client) -> list:
    skip_counter = 0
    data = []
    with tqdm(desc='Fetching pull requests', unit='batch') as pbar:
        while True:
            response = client.get_pull_requests(params={
                'searchCriteria.status':'active',
                '$top':'1000',
                '$skip':skip_counter
            })
            pull_requests = response.get('value', [])
            data.extend(pull_requests)
        
            if response.get('count', 0) < 1000:
                break
            skip_counter += 1000
            pbar.update(1)
    return data

    
if __name__ == "__main__":
    main()
    print("Done")
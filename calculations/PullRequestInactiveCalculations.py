import copy
import TimeUtil
from calculations import Calculation
from model import PullRequests


class PullRequestInactiveCalculation(Calculation.Calculation):
    
    PULL_REQUEST_ID = 'id'
    PULL_REQUEST_TITLE = 'title'
    PULL_REQUEST_CREATOR = 'creator'
    PULL_REQUEST_LAST_ACTIVITY = 'last_activity'
    
    def prepare_data(self, data: list[PullRequests]) -> None:
        temp = copy.deepcopy(data)
        open_prs = []
        for pr in temp:
            if pr.base.status == 'active':
                open_prs.append(pr)
        
        self.pr_data: list[PullRequests] = open_prs


    def calculate(self) -> list:
        results = []
        for pr in self.pr_data:
            last_activity = None
            for thread in pr.threads:
                if last_activity is None or thread.lastUpdatedDate > last_activity:
                    last_activity = thread.lastUpdatedDate
            if last_activity is None:
                continue
            data = {
                self.PULL_REQUEST_ID: pr.base.pullRequestId,
                self.PULL_REQUEST_TITLE: pr.base.title,
                self.PULL_REQUEST_CREATOR: pr.base.createdBy.displayName,
                self.PULL_REQUEST_LAST_ACTIVITY: TimeUtil.clean_date(last_activity)
            }
            results.append(data)
            
        return results

    def export_file_name(self) -> str:
        return "PullRequestInactiveCalculation"
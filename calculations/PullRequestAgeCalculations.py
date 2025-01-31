import copy
import datetime
import TimeUtil
from calculations import Calculation
from model import PullRequests


class PullRequestAgeCalculations(Calculation.Calculation):
    PULL_REQUEST_ID = 'id'
    PULL_REQUEST_TITLE = 'title'
    PULL_REQUEST_CREATOR = 'creator'
    PULL_REQUEST_AGE = 'age'

    def prepare_data(self, data: list[PullRequests]) -> None:
        temp = copy.deepcopy(data)
        open_prs = []
        for pr in temp:
            if pr.base.status == 'active':
                open_prs.append(pr)
        
        self.pr_data: list[PullRequests] = open_prs
    
    def calculate(self) -> list:
        age_limit = datetime.date.today() - datetime.timedelta(days=7)
        results = []
        
        for pr in self.pr_data:
            creation_date = TimeUtil.parse_to_date(pr.base.creationDate)
            if creation_date < age_limit:
                data = {
                    self.PULL_REQUEST_ID: pr.base.pullRequestId,
                    self.PULL_REQUEST_TITLE: pr.base.title,
                    self.PULL_REQUEST_CREATOR: pr.base.createdBy.displayName,
                    self.PULL_REQUEST_AGE: (datetime.date.today() - creation_date).days
                }
                results.append(data)
        return results

    def export_file_name(self) -> str:
        return "PullRequestAgeCalculations"

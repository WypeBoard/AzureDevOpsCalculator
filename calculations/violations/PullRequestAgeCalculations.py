import copy
import datetime
import TimeUtil
from calculations.violations.violations_calculations import ViolationsCalculation
from model import PullRequests


class PullRequestAgeCalculations(ViolationsCalculation):

    def prepare_data(self, data: list[PullRequests]) -> None:
        temp = copy.deepcopy(data)
        open_prs = []
        for pr in temp:
            if pr.base.status == 'active':
                open_prs.append(pr)
        
        self.pr_data: list[PullRequests] = open_prs
    
    def get_rule_definition(self):
        return f'Pull requests that are older than {self.rule_description} days'
    
    @property
    def rule_description(self):
        return 14 # days
        
    def calculate(self) -> list:
        age_limit = datetime.date.today() - datetime.timedelta(days=self.rule_description)
        results = []
        
        for pr in self.pr_data:
            creation_date = TimeUtil.parse_to_date(pr.base.creationDate)
            if creation_date < age_limit:
                data = self.construct_result_data(pr, (datetime.date.today() - creation_date).days)
                results.append(data)
        return results

    def export_file_name(self) -> str:
        return "PullRequestAgeCalculations"

    def is_mail_enabled(self) -> bool:
        return True
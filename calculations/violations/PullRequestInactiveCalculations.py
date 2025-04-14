import copy
import TimeUtil
from calculations.violations.violations_calculations import ViolationsCalculation
from model import PullRequests


class PullRequestInactiveCalculation(ViolationsCalculation):
        
    def prepare_data(self, data: list[PullRequests]) -> None:
        temp = copy.deepcopy(data)
        open_prs = []
        for pr in temp:
            if pr.base.status == 'active':
                open_prs.append(pr)
        
        self.pr_data: list[PullRequests] = open_prs

    def get_rule_definition(self):
        return f'Pull requests that have been inactive for {self.rule_description()} days'

    def rule_description(self):
        return 7 # 7 days 
    
    def calculate(self) -> list:
        results = []
        for pr in self.pr_data:
            last_activity:str = None
            for thread in pr.threads:
                if last_activity is None or thread.lastUpdatedDate > last_activity:
                    last_activity = thread.lastUpdatedDate
            if last_activity is None:
                continue
            if TimeUtil.parse_to_date(last_activity) > TimeUtil.days_ago(self.rule_description()):
                continue
            data = self.construct_result_data(pr, TimeUtil.clean_date(last_activity))
            results.append(data)
            
        return results

    def export_file_name(self) -> str:
        return "PullRequestInactiveCalculation"
    
    def is_mail_enabled(self):
        return True
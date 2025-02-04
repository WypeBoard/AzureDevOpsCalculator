
import copy
import re
from calculations import Calculation
from model import PullRequests


class PullRequestWrongTargetBranchCalculations(Calculation.Calculation):
    
    
    def prepare_data(self, data: list) -> None:
        temp = copy.deepcopy(data)
        open_prs = []
        for pr in temp:
            if pr.base.status == 'active':
                open_prs.append(pr)
        
        self.pr_data: list[PullRequests] = open_prs

    def get_rule_definition(self):
        return 'Pull request does not target one of the active branches'

    def rule_description(self):
        """ Returns the set of active branches """
        return []

    def calculate(self) -> list:
        results = []
        compiled_branches = [re.compile(branch) for branch in self.rule_description()]
        for pr in self.pr_data:
            validated = False
            pr_target_branch = pr.base.targetRefName.replace('refs/heads/', '')
            for branch in compiled_branches:
                if branch.match(pr_target_branch):
                    validated = True
                    break
            if validated:
                continue
            data = self.construct_result_data(pr, pr_target_branch)
            results.append(data)
        return results

    def export_file_name(self) -> str:
        return "PullRequestWrongTargetBranchCalculations"

    def is_mail_enabled(self):
        return True
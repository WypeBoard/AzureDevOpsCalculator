from calculations import PullRequestAgeCalculations, PullRequestInactiveCalculations, PullRequestWrongTargetBranchCalculations
from manager.Manager import Manager

def get_manager(pullrequests):
    return Manager(pullrequests)

def get_calculations():
    calculations = [
            PullRequestAgeCalculations.PullRequestAgeCalculations,
            PullRequestInactiveCalculations.PullRequestInactiveCalculation,
            PullRequestWrongTargetBranchCalculations.PullRequestWrongTargetBranchCalculations
    ]
    return calculations
    
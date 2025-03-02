from datetime import date, timedelta
from unittest.mock import patch

import pytest
from calculations.PullRequestInactiveCalculations import PullRequestInactiveCalculation

from calculations.PullRequestAgeCalculations import PullRequestAgeCalculations
from calculations.PullRequestWrongTargetBranchCalculations import PullRequestWrongTargetBranchCalculations
from model import PullRequests, PullRequest, CreatedBy, Repository, Thread


@pytest.fixture
def mock_pull_requests():
    """Fixture to create mock PullRequests data"""
    repo = Repository(id="1", name="test-repo", url="http://example.com/repo")
    creator = CreatedBy(id="123", displayName="Test User", uniqueName="test@example.com", url="", imageUrl="")

    pr1 = PullRequest(
        pullRequestId=1, codeReviewId=101, status="active", createdBy=creator,
        creationDate=(date.today() - timedelta(days=20)).isoformat(),
        title="Old PR", sourceRefName="feature-branch", targetRefName="refs/heads/main", repository=repo,
        url="http://example.com/pr1"
    )

    pr2 = PullRequest(
        pullRequestId=2, codeReviewId=102, status="inactive", createdBy=creator,
        creationDate=(date.today() - timedelta(days=5)).isoformat(),
        title="Recent PR", sourceRefName="feature-branch", targetRefName="refs/heads/main", repository=repo,
        url="http://example.com/pr2"
    )

    thread = Thread(id=1, publishedDate="2024-01-01T12:00:00Z", lastUpdatedDate="2024-01-15T12:00:00Z", comments=[])

    return [PullRequests(id=1, base=pr1, threads=[thread]), PullRequests(id=2, base=pr2, threads=[thread])]


### PullRequestAgeCalculations Tests ###
def test_pull_request_age_calculations(mock_pull_requests):
    calc = PullRequestAgeCalculations()
    calc.prepare_data(mock_pull_requests)

    assert len(calc.pr_data) == 1  # Only 'active' PRs should be kept
    assert calc.pr_data[0].base.pullRequestId == 1

    results = calc.calculate()
    assert len(results) == 1
    assert results[0]["id"] == 1

    assert calc.get_rule_definition() == "Pull requests that are older than 14 days"
    assert calc.export_file_name() == "PullRequestAgeCalculations"
    assert calc.is_mail_enabled() is True


### PullRequestWrongTargetBranchCalculations Tests ###
@patch("re.compile")
def test_pull_request_wrong_target_branch_calculations(mock_re_compile, mock_pull_requests):
    calc = PullRequestWrongTargetBranchCalculations()
    calc.prepare_data(mock_pull_requests)

    assert len(calc.pr_data) == 1  # Only 'active' PRs should be kept
    assert calc.pr_data[0].base.pullRequestId == 1

    mock_re_compile.return_value.match.return_value = False
    results = calc.calculate()

    assert len(results) == 1
    assert results[0]["id"] == 1
    assert calc.get_rule_definition() == "Pull request does not target one of the active branches"
    assert calc.export_file_name() == "PullRequestWrongTargetBranchCalculations"
    assert calc.is_mail_enabled() is True


### PullRequestInactiveCalculation Tests ###
@patch("TimeUtil.parse_to_date", side_effect=lambda x: date.fromisoformat(x))
@patch("TimeUtil.days_ago", side_effect=lambda days: date.today() - timedelta(days=days))
def test_pull_request_inactive_calculation(mock_days_ago, mock_time_util, mock_pull_requests):
    calc = PullRequestInactiveCalculation()
    calc.prepare_data(mock_pull_requests)

    assert len(calc.pr_data) == 1  # Only 'active' PRs should be kept
    assert calc.pr_data[0].base.pullRequestId == 1

    results = calc.calculate()
    assert len(results) == 1
    assert results[0]["id"] == 1

    assert calc.get_rule_definition() == "Pull requests that have been inactive for 7 days"
    assert calc.export_file_name() == "PullRequestInactiveCalculation"
    assert calc.is_mail_enabled() is True

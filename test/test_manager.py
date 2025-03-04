import pytest
from unittest.mock import MagicMock, patch
from Manager import Manager
from model import PullRequests, PullRequest, CreatedBy, Repository, Thread, Comment
import Constants


@pytest.fixture
def mock_pull_requests():
    """Fixture to create mock PullRequests data"""
    repo = Repository(id="1", name="test-repo", url="http://example.com/repo")
    creator = CreatedBy(id="123", displayName="Test User", uniqueName="test@example.com", url="", imageUrl="")
    pr1 = PullRequest(
        pullRequestId=1, codeReviewId=101, status="open", createdBy=creator, creationDate="2024-01-01T12:00:00Z",
        title="Fix Bug", sourceRefName="feature-branch", targetRefName="main", repository=repo,
        url="http://example.com/pr1"
    )
    thread1 = Thread(id=1, publishedDate="2024-01-01T12:30:00Z", lastUpdatedDate="2024-01-01T13:00:00Z", comments=[])
    pull_request = PullRequests(id=1, base=pr1, threads=[thread1])

    return [pull_request]


def test_manager_initialization(mock_pull_requests):
    """Test if Manager initializes correctly"""
    manager = Manager(mock_pull_requests)

    assert manager.raw_data == mock_pull_requests
    assert isinstance(manager.combined_results, dict)
    assert manager.calculations == []
    assert manager.email_builder is not None
    assert manager.email_sender is not None


def test_register_calculation(mock_pull_requests):
    """Test if calculations are registered properly"""
    mock_calculation = MagicMock()
    mock_calculation.__name__ = "MockCalculation"  
    mock_calculation.prepare_data = MagicMock()

    manager = Manager(mock_pull_requests)
    manager.register_calculation(mock_calculation)

    assert len(manager.calculations) == 1


@patch("Manager.MailSender")
@patch("Manager.MailTemplateBuilder")
@patch("Manager.Calculation")
@patch("Manager.Manager.save_to_csv")
def test_execute(mock_save_to_csv, mock_calculation, mock_mail_builder, mock_mail_sender, mock_pull_requests):
    """Test execution of calculations and email sending"""
    mock_calculation.__name__ = "MockCalculation"  
    mock_calc_instance = mock_calculation.return_value
    mock_calc_instance.calculate.return_value = [{"id": 1, "result": 42}]
    mock_calc_instance.export_file_name.return_value = "test_results"
    mock_calc_instance.is_mail_enabled.return_value = False

    manager = Manager(mock_pull_requests)
    manager.register_calculation(mock_calculation)
    manager.execute()

    mock_calc_instance.calculate.assert_called_once()
    mock_save_to_csv.assert_called_once_with("test_results", [{"id": 1, "result": 42}])
    mock_mail_builder.return_value.generate_emails.assert_called_once()
    mock_mail_sender.return_value.send_mails.assert_called_once()


@patch("Manager.Logger")  # Mock the logger to prevent file writes
@patch("Manager.csv.DictWriter")
@patch("builtins.open", new_callable=MagicMock)
def test_save_to_csv(mock_open, mock_dict_writer, mock_logger):
    """Test CSV saving functionality"""
    manager = Manager([])
    data = [{"col1": "value1", "col2": "value2"}]

    manager.save_to_csv("test_file", data)
    
    # Get the actual open calls (Logger is also using open for core.log)
    open_calls = mock_open.call_args_list

    # Find the one related to "test_file.csv"
    file_open_call = [call for call in open_calls if call.args[0] == "test_file.csv"]
    
    assert len(file_open_call) == 1  # Ensure "test_file.csv" is opened once
    assert file_open_call[0].args == ("test_file.csv", "w")  # Validate arguments

    # Ensure DictWriter was used correctly
    mock_dict_writer.return_value.writeheader.assert_called_once()
    mock_dict_writer.return_value.writerows.assert_called_once_with(data)
    


@patch("Manager.MailTemplateBuilder")
def test_combine_results(mock_mail_builder, mock_pull_requests):
    """Test results combination"""
    manager = Manager(mock_pull_requests)
    mock_mail_builder_instance = mock_mail_builder.return_value

    results = [
        {
            Constants.PULL_REQUEST_ID: 1,
            Constants.PULL_REQUEST_TITLE: "Fix Bug",
            Constants.PULL_REQUEST_URL: "http://example.com/pr1",
            Constants.PULL_REQUEST_CREATOR: "test@example.com",
            Constants.PULL_REQUEST_EMAIL: "test@example.com",
        }
    ]

    manager.combine_results(results, "test_rule")

    assert 1 in manager.combined_results
    assert manager.combined_results[1][Constants.PULL_REQUEST_TITLE] == "Fix Bug"
    mock_mail_builder_instance.add_pr_info.assert_called_once()

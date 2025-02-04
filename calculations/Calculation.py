from abc import ABC, abstractmethod

import Constants
from model import PullRequests


class Calculation(ABC):
    
    @abstractmethod
    def prepare_data(self, data: list[PullRequests]) -> None:
        """
        Prepare and preprocess the data for calculations.
        """
        pass
    
    @abstractmethod
    def get_rule_definition(self) -> str:
        """
        Return the rule definition for the calculation.
        """
        pass
    
    @abstractmethod
    def rule_description(self) -> str:
        """
        Return the description of the rule.
        """
        pass
    
    @abstractmethod    
    def calculate(self) -> list:
        """
        Perform the calculation and return results as a dictionary.
        """
        pass

    @abstractmethod
    def export_file_name(self) -> str:
        """
        Return the name of the file to save the results.
        """
        pass
    
    @abstractmethod
    def is_mail_enabled(self) -> bool:
        """
        Return True if mail should be sent, otherwise False.
        """
        return False
    
    def construct_result_data(self, pr, violation):
        email = self.parse_email_from_unique_name(pr.base.createdBy.uniqueName)
        url = self.parse_url(pr.base.pullRequestId)
        data = {
            Constants.PULL_REQUEST_ID: pr.base.pullRequestId,
            Constants.PULL_REQUEST_TITLE: pr.base.title,
            Constants.PULL_REQUEST_CREATOR_ID: pr.base.createdBy.id,
            Constants.PULL_REQUEST_CREATOR: pr.base.createdBy.displayName,
            Constants.PULL_REQUEST_EMAIL: email,
            Constants.PULL_REQUEST_URL: url,
            Constants.PULL_REQUEST_VIOLATION: violation
        }
        return data
    
    def parse_url(self, pull_request_id):
        """ Removing 'pat-' and change '_api' to '_git' from url """  
        url = f'{Constants.BASE_URL}/{Constants.ORGANISATION}/{Constants.PROJECT_NAME}/_git/{Constants.REPOSITORY_NAME}/pullrequest/{pull_request_id}'
        url = url.replace('https://pat-', 'https://')
        return url
    
    def parse_email_from_unique_name(self, unique_name):
        local_part = unique_name.split('\\')[1]
        return f'{local_part}{Constants.MAIL_DOMAIN}'
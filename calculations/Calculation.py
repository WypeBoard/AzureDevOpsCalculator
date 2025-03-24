from abc import ABC, abstractmethod

from config import AdoSettings, Settings
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
        settings = Settings()
        email = self.parse_email_from_unique_name(pr.base.createdBy.uniqueName, settings.CoreSettings.mail_domain)
        url = self.parse_url(pr.base.pullRequestId, settings.AdoSettings)
        data = {
            settings.CalculationSettings.pull_request_id: pr.base.pullRequestId,
            settings.CalculationSettings.pull_request_title: pr.base.title,
            settings.CalculationSettings.pull_request_creator_id: pr.base.createdBy.id,
            settings.CalculationSettings.pull_request_creator: pr.base.createdBy.displayName,
            settings.CalculationSettings.pull_request_email: email,
            settings.CalculationSettings.pull_request_url: url,
            settings.CalculationSettings.pull_request_violation: violation
        }
        return data
    
    def parse_url(self, pull_request_id, settings: AdoSettings):
        """ Removing 'pat-' and change '_api' to '_git' from url """  
        url = f'{settings.base_url}/{settings.organisation}/{settings.project_name}/_git/{settings.repository_name}/pullrequest/{pull_request_id}'
        url = url.replace('https://pat-', 'https://')
        return url
    
    def parse_email_from_unique_name(self, unique_name, mail_domain: str):
        if '\\' not in unique_name:
            return unique_name
        local_part = unique_name.split('\\')[1]
        return f'{local_part}{mail_domain}'

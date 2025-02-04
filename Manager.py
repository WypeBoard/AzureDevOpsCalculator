import csv
from typing import Dict

import Constants
from MailSender import MailSender
from MailTemplateBuilder import MailTemplateBuilder, PRInfo
from calculations import Calculation
from model import PullRequests


class Manager:
    """ Manager class for handling calculations and data. """
    def __init__(self, raw_data: list[PullRequests]):
        self.raw_data = raw_data
        self.combined_results: Dict[int, Dict] = {}
        self.calculations = []
        self.email_builder = MailTemplateBuilder()  # Initialize email builder
        self.email_sender = MailSender()  # Initialize email sender
        
    def register_calculation(self, calculation_class: Calculation) -> None:
        """ Register a calculation class to be executed. """
        calculation = calculation_class()
        calculation.prepare_data(self.raw_data)
        self.calculations.append(calculation)
        
    def execute(self) -> None:
        """ Execute all registered calculations. """
        for calculation in self.calculations:
            results = calculation.calculate()
            filename = calculation.export_file_name()
            self.save_to_csv(filename, results)
            if calculation.is_mail_enabled():
                self.combine_results(results, calculation.get_rule_definition())
        emails = self.email_builder.generate_emails()
        self.email_sender.send_mails(emails)
            
    def combine_results(self, results: list, rule: str) -> None:
        for result in results:
            pr_id = result[Constants.PULL_REQUEST_ID]
            if pr_id not in self.combined_results:
                self.combined_results[pr_id] = {}
            self.combined_results[pr_id].update(result)
            
            # Add data to email builder
            pr_info = PRInfo(
                pr_id=result[Constants.PULL_REQUEST_ID], 
                title=result[Constants.PULL_REQUEST_TITLE], 
                url=result[Constants.PULL_REQUEST_URL],
            )
            self.email_builder.add_pr_info(result[Constants.PULL_REQUEST_CREATOR], rule, result[Constants.PULL_REQUEST_EMAIL], pr_info)
            
    def save_to_csv(self, filename: str, data: dict) -> None:
        """ Save the data to a CSV file. """
        if not data:
            return
        with open(f'{filename}.csv', 'w', newline='', encoding='utf-8') as csvFile:
            write = csv.DictWriter(csvFile, fieldnames=data[0].keys())
            write.writeheader()
            write.writerows(data)

from dataclasses import dataclass
from typing import Any, Dict

import Constants
from MailSender import Mail
from logger import Logger


@dataclass
class PRInfo:
    """ Dataclass for storing PR information. """
    pr_id: int
    title: str
    url: str

class MailTemplateBuilder:
    
    RULES = 'rules'
    
    def __init__(self):
        self.log = Logger(__name__)
        self.user_prs: Dict[str, Dict[str, Any]] = {}
        self.log.debug("MailTemplateBuilder initialized")
    
    def add_pr_info(self, creator: str, rule: str, email:str,  pr_info: PRInfo) -> None:
        """ Add PR information to the user's list of PRs. """
        self.log.debug(f"Adding PR info for creator: {creator}, rule: {rule}")
        if creator not in self.user_prs:
            self.user_prs[creator] = {}
            self.user_prs[creator][self.RULES] = {}
        if rule not in self.user_prs[creator][self.RULES]:
            self.user_prs[creator][self.RULES][rule] = []
        if Constants.PULL_REQUEST_EMAIL not in self.user_prs[creator]:
            self.user_prs[creator][Constants.PULL_REQUEST_EMAIL] = email
        self.user_prs[creator][self.RULES][rule].append(pr_info)
        
    def generate_emails(self) -> list[Mail]:
        """ Generate email templates for each user. """
        self.log.debug("Generating emails")
        emails = []
        for creator, details in self.user_prs.items():
            emails.append(self._generate_email_body(creator, details.get(Constants.PULL_REQUEST_EMAIL), details.get(self.RULES)))
        return emails
    
    def _generate_email_body(self, creator, email: str, rules: Dict[str, list[PRInfo]]) -> Mail:
        """ Generate the email body for the user. """
        self.log.debug(f"Generating email body for creator: {creator}")
        subject = "Action Required: Pending Pull Requests"
        rule_content = ''
        for rule, prs in rules.items():
            rule_content += f'<b>{rule}:</b><br>'
            rule_content += f'<ul>'
            for pr in prs:
                rule_content += f'<li><a href="{pr.url}">{pr.title}</a></li>'
            rule_content += f'</ul><br>'
        email_content = f'Hi {creator},<br><br>You have the following PRs that require your attention:<br><br>'
        email_content += f'{rule_content}<br>'
        email_content += f'Please review these PRs and take the necessary actions:<br>'
        email_content += f'<ul><li>Complete the review process if the PR is still relevant.</li><li>Close the PR if it is no longer needed.</li></ul><br>'
        email_content += f'Thank you for your attention to this matter.<br>'
        return Mail(reciever=email, subject=subject, content=email_content)

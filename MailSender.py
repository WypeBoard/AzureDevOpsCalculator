from dataclasses import dataclass
from win32com import client
from config import Settings
from logger import Logger

@dataclass
class Mail:
    reciever: str
    subject: str
    content: str

class MailSender:
    
    def __init__(self):
        self.logger = Logger(__name__)
        self.settings = Settings()
    
    def send_mails(self, mails: list[Mail]):
        if self.settings.CoreSettings.mail_send_enabled:
            self.varify()
            self.logger.info("Sending mails...")
            outlook = client.Dispatch('Outlook.Application')
            for mail in mails:
                self.send_mail(mail, outlook)
        else:
            for mail in mails:
                print(f"Would have sent mail to {mail.reciever} with subject {mail.subject}\n")
                print(mail.content)
                print('\n\n\n')
    
    def send_mail(self, mail: Mail, outlookClient):
        email = outlookClient.CreateItem(0)
        email.To = mail.reciever
        email.Subject = mail.subject
        email.HTMLBody = mail.content
        email.Send()
            
    def varify(self):
        user_input = input("Are you sure you want to send mails? [y][true] to send mails: ")
        if user_input.lower() not in ['y', 'true']:
            self.logger.warning("Aborted sending mails")
            raise Exception("Aborted sending mails")
        self.logger.info("User confirmed to send mails")


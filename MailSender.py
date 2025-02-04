from dataclasses import dataclass
from win32com import client
import Constants


@dataclass
class Mail:
    reciever: str
    subject: str
    content: str

class MailSender:
    
    def send_mails(self, mails: list[Mail]):
        for mail in mails:
            self.send_mail(mail)
    
    def send_mail(self, mail: Mail):
        if Constants.MAIL_SEND_ENABLED:
            outlook = client.Dispatch('Outlook.Application')
            email = outlook.CreateItem(0)
            email.To = mail.reciever
            email.Subject = mail.subject
            email.HTMLBody = mail.content
            email.Send()
        else:
            print(f"Would have sent mail to {mail.reciever} with subject {mail.subject}\n")
            print(mail.content)
            print('\n\n\n')
            
        
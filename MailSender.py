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
        if Constants.MAIL_SEND_ENABLED:
            self.varify()
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
        user_input = input("Are you sure you want to send mails? [y][true] to send mails")
        if user_input.lower() not in ['y', 'true']:
            raise Exception("Aborted sending mails")
        
        
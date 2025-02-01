from TempMail import TempMail
import time

def fetch_emails():
    tmp = TempMail("tm.1234567890.randomcharactershere") 

    inbox = tmp.createInbox()

    print(f"Created inbox: {inbox.address}")

    while True:
        emails = tmp.getEmails(inbox.token)
        for email in emails:
            print("\nNew Email:")
            print(f"\tSender: {email.sender}")
            print(f"\tRecipient: {email.recipient}")
            print(f"\tSubject: {email.subject}")
            print(f"\tBody: {email.body}")
            print(f"\tHTML: {str(email.html)}")  
            print(f"\tDate: {email.date}")  
        
        time.sleep(2)

if __name__ == "__main__":
    fetch_emails()

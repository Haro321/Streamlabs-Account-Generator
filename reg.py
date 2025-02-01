import os
import time
import logging
import traceback
from typing import Optional
from dotenv import load_dotenv
from botasaurus_driver import Driver
from TempMail import TempMail
import string
import random
import threading

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('streamlabs_signup.log'),
        logging.StreamHandler()
    ]
)

class StreamLabsBot:
    def __init__(self, 
                 email: Optional[str] = None, 
                 password: Optional[str] = None,
                 proxy: Optional[str] = None):
        
        self.email = email 
        self.password = self.generate_password()
        
        driver_options = {
            'wait_for_complete_page_load': True,
            'headless' :  False
        }
        if proxy:
            driver_options['proxy'] = proxy
        
        self.driver = Driver(**driver_options)
        self.tmp = TempMail(os.getenv('TEMPMAIL_TOKEN', 'default_token'))
        self.url = "https://streamlabs.com/slid/signup"
        
        if not self.email:
            self.inbox = self.tmp.createInbox(domain="wih1.awesome47.com")
            self.email = self.inbox.address
        
        if not self.password:
            self.password = os.getenv('DEFAULT_PASSWORD', 'Haro12!!^')

        self.selectors = {
            'signup_button': ".sl-btn.w-full.whitespace-nowrap.py-\\[14px\\].sl-btn-one-dark",
            'email_input': ".sl-form-control.theme-dark.w-full",
            'password_input': ".sl-form-control.theme-dark.w-full.pr-10",
            'first_checkbox': ".mr-2.mt-1.sl-checkbox",
            'promo_checkbox': 'div.email-signup-form__field--agree-promotional input[type="checkbox"]',
            'verification_code_input': 'div.verify-email-form__form-code input[name="code"]',
            'verify_submit_button': 'button.sl-btn[type="submit"]'
        }


    def generate_password(self):
        uppercase_letters = string.ascii_uppercase
        lowercase_letters = string.ascii_lowercase
        digits = string.digits
        special_characters = "!@#$%^&*"

        password = [
            random.choice(uppercase_letters),
            random.choice(lowercase_letters),
            random.choice(digits),
            random.choice(special_characters),
        ]

        all_characters = uppercase_letters + lowercase_letters + digits + special_characters
        for _ in range(4):
            password.append(random.choice(all_characters))

        random.shuffle(password)

        return "".join(password)

    def open_signup_page(self):
        try:
            self.driver.google_get(self.url, bypass_cloudflare=True)
            logging.info("Signup page opened successfully")
        except Exception as e:
            logging.error(f"Failed to open signup page: {e}")
            raise

    def fill_form(self):
        try:
            self.driver.wait_for_element(self.selectors['email_input'])
            self.driver.type(self.selectors['email_input'], self.email)
            logging.info(f"Email '{self.email}' entered")

            self.driver.wait_for_element(self.selectors['password_input'])
            self.driver.type(self.selectors['password_input'], self.password)
            logging.info("Password entered")

            self.driver.wait_for_element(self.selectors['first_checkbox'])
            self.driver.click(self.selectors['first_checkbox'])
                    
            self.driver.wait_for_element(self.selectors['promo_checkbox'])
            self.driver.click(self.selectors['promo_checkbox'])
            logging.info("Checkboxes clicked")

            self.driver.wait_for_element(self.selectors['signup_button'])
            self.driver.click(self.selectors['signup_button'])
            logging.info("Form submitted")
            
        except Exception as e:
            logging.error(f"Error during form submission: {e}")
            raise

    def verify_email(self, max_attempts: int = 10):
        for attempt in range(max_attempts):
            try:
                time.sleep(2) 
                emails = self.tmp.getEmails(self.inbox)
                
                for email in emails:
                    try:
                        code = email.subject.split(" - Streamlabs ID verification code")[0].strip()
                        if code.isdigit() and len(code) > 2:
                            logging.info(f"Found verification code: {code}")
                            
                            try:
                                self.driver.wait_for_element(
                                    self.selectors['verification_code_input'],
                                    wait=10 

                                )
                                self.driver.type(
                                    self.selectors['verification_code_input'], 
                                    code,
                                )
                                
                                submit_button = self.driver.wait_for_element(
                                    self.selectors['verify_submit_button'], 
    
                                )
                                self.driver.click(
                                    self.selectors['verify_submit_button']
                                )
                                
                                time.sleep(2)
                                
                                logging.info("Email verification attempted")
                                return True
                            
                            except Exception as submit_error:
                                logging.error(f"Error during code submission: {submit_error}")
                    
                    except Exception as code_error:
                        logging.warning(f"Error processing email code: {code_error}")
            
            except Exception as retry_error:
                logging.error(f"Verification attempt {attempt + 1} failed: {retry_error}")
        
        logging.error("Failed to verify email after maximum attempts")
        return False

    def run(self):
        """Main method to execute signup process."""
        try:
            self.open_signup_page()
            self.fill_form()
            success = self.verify_email()
            
            return {
                'success': success,
                'email': self.email,
                'password': self.password
            }
        
        except Exception as e:
            logging.error(f"Signup process failed: {e}")
            traceback.print_exc()
            return {'success': False, 'error': str(e)}
        
        finally:
            self.driver.close()

def main():
    bot = StreamLabsBot()
    result = bot.run()
    isValid = result['success']
    if isValid:
        with open("stremlabsAccs.txt" ,"a") as file:
            file.write(f"{result['email']}:{result['password']}" + "\n")
    print(result)

if __name__ == "__main__":
    for i in range(5):
        threading.Thread(target=main).start()
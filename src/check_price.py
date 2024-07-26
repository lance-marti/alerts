
import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# URL of the page to scrape
url = "https://www.digitec.ch/fr/s1/product/dji-mini-3-y-compris-fly-more-combo-38-min-248-g-12-mpx-drone-23253713"  # Replace with the actual URL

# Function to extract the price from the webpage
def get_price():
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the price from the meta tag
        price_element = soup.find('meta', {'property': 'product:price:amount'})
        if price_element and price_element['content']:
            price = float(price_element['content'])
            return price
        else:
            print("Price element not found.")
            return None
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

# Function to send an email notification
def send_email(price):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_user = os.environ['EMAIL_USER']
    email_password = os.environ['EMAIL_PASSWORD']
    email_to = os.environ['EMAIL_TO']
    email_subject = "Price Alert: Item Below Threshold"

    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = email_to
    msg["Subject"] = email_subject

    body = f"The price is now {price} chf.-, which is below the threshold of 500.-. Go to : {url}."
    msg.attach(MIMEText(body, "plain"))


    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, email_to, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Main logic to check the price and send an email if needed
def main():
    price = get_price()
    if price is not None and price < 500:
        send_email(price)
    else:
        print("Price is above the threshold, no email sent.")

if __name__ == "__main__":
    main()
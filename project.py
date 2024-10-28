import imaplib
import email
import os
import pandas as pd


def fetch_email_data(mail_id, passcode):
    try:
        print("Connecting to IMAP server...")
        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)  # Update this if needed
        print("Connected to IMAP server successfully!")

        # Attempt to log in
        print("Logging in...",mail_id,passcode)
        mail.login(mail_id, passcode)
        print("Login successful!")

        # Select the mailbox (INBOX in this case)
        mail.select('inbox')

        # Search for emails (here, we fetch the latest email)
        status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()
        latest_email_id = email_ids[-1]

        # Fetch the email by ID
        status, msg_data = mail.fetch(latest_email_id, '(RFC822)')
        raw_email = msg_data[0][1]

        # Parse the email content
        msg = email.message_from_bytes(raw_email)

        # Extract email details
        subject = msg['subject']
        from_email = msg['from']
        date = msg['date']
        
        print(f"Subject: {subject}")
        print(f"From: {from_email}")
        print(f"Date: {date}")

        # Check if the email contains attachments
        if msg.is_multipart():
            for part in msg.walk():
                content_disposition = part.get("Content-Disposition", None)
                if content_disposition:
                    filename = part.get_filename()
                    if filename:
                        # Save the file to the 'downloads' directory
                        download_folder = 'downloads_email'
                        os.makedirs(download_folder, exist_ok=True)
                        filepath = os.path.join(download_folder, filename)

                        with open(filepath, 'wb') as f:
                            f.write(part.get_payload(decode=True))

                        print(f"File saved to {filepath}")

                        # If the file is a CSV, load it using pandas
                        if filename.endswith('.csv'):
                            df = pd.read_csv(filepath)
                            print(df.head())  # Display the first few rows
                    else:
                        print("No files found in the email.")
        else:
            print("No attachments found in the email.")

    except imaplib.IMAP4.error as e:
        print("Could not access the email. Please check your ID and passcode.")
        raise Exception("Email access error") from e

    except Exception as e:
        print("An error occurred while processing the email.")
        raise e

# Usage
mail_id = 'avitalaptop1308@gmail.com'
passcode = 'aafj ftgs idgn npxk'
fetch_email_data(mail_id, passcode)

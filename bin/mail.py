import base64
import email.mime.text

import auth


gmail_client = None  # Uninitialized


# Optionally called from command line scripts to pass in args. If not
# called manually, the client is still initialized on first use.
def init_gmail_client(args=None, scopes='gmail.send'):
    global gmail_client
    if gmail_client is None:
        gmail_client = auth.get_gmail_client(args, scopes)


def send_mail(subject, body, to):
    init_gmail_client()
    msg = email.mime.text.MIMEText(body)
    msg['to'] = to
    msg['subject'] = subject
    encoded_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
    # https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html#send
    gmail_client.users().messages().send(  # pylint: disable=no-member
        userId='me',
        body={'raw': encoded_msg},
    ).execute()

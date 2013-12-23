"""Set up the `accounts.json` file."""

import json

def get_input(prompt, default=''):
    """Return input from the user.

    The prompt is formatted appropriately, specifying the default value if
    it is non-empty. Return the user's input or the default value if the user
    enters the emtpy string.
    """
    if default != '':
        prompt += ' (default: ' + default + ')'
    prompt += ': '
    return raw_input(prompt) or default

def get_account_details(is_account_to=False):
    """Return a dictionary corresponding to the user's entered details for one account.

    If the account being entered is the account into which emails will be
    imported, `is_account_to` should be `True` and the account details will be
    handled appropriately.
    """
    account = {}
    if not is_account_to:
        account['host'] = get_input('Enter your host', 'imap.gmail.com')
    else:
        account['host'] = 'imap.gmail.com'
        print 'Using imap.gmail.com for the host, as the code relies on importing to a Gmail account.'
    account['username'] = get_input('Enter your username')
    if not is_account_to:
        account['label'] = get_input('(Optional) Enter the label you want to assign to messages imported from this mailbox')
        account['x_gmail_fetch_info'] = get_input('(Optional) Enter X-Gmail-Fetch-Info')
    return account

def ask_continue():
    """Ask the user if they want to add more accounts."""
    while True:
        inp = get_input('Do you want to add more accounts?', 'n').lower()
        if inp == 'y' or inp == 'yes':
            return True
        elif inp == 'n' or inp == 'no':
            return False
        print 'Invalid input: please enter "y" or "n".'

print """Help:
Host - enter the IMAP server. It must support an SSL connection.
Username - IMAP username/email address
Label - the label you want to assign to messages imported from the mailbox
X-Gmail-Fetch-Info - this is a hack to make Gmail's "Send mail as" work by default when replying to imported messages. This works as follows:
1. Set up X-Gmail-Fetch-Info properly. The format for this is <email> <id (I think this can be any number)> <host> <port> <username>, e.g. me@gmail.com 1 imap.gmail.com 993 me. I think the email is the only thing that actually matters.
2. An email is imported from an account (from_account) to the account being imported into (to_account).
3. Set up to_account so it has from_account as one of its "Send mail as" accounts in Gmail.
4. Replying to the imported email.
5. Gmail will automatically set the From field in the reply to from_account.

If an option has a default value, press enter to use the default.

---
Please enter the account you wish to import into:
"""
accounts = {}
accounts['m_to'] = get_account_details(True)
print """
---
Please enter the accounts you wish to import from:
"""
accounts['m_froms'] = []
while True:
    accounts['m_froms'].append(get_account_details())
    if not ask_continue():
        break

with open('accounts.json', 'w') as f:
    json.dump(accounts, f)

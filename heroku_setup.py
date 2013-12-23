"""Get the account passwords and set up and start a Heroku app.

`setup_accounts.py` must already have been run."""

import subprocess
import json
import threading
import mailbox
import load
import getpass
import imaplib2
import sys

def ask_continue():
    """Ask the user if they want to continue."""
    while True:
        inp = raw_input('Are you sure you want to continue? ').lower()
        if inp == 'y' or inp == 'yes':
            return True
        elif inp == 'n' or inp == 'no':
            return False
        print 'Invalid input: please enter "y" or "n".'

def get_password(account, is_account_to=False):
    """Store the validated password for the given account in `passwords[account['pass_var']]`."""
    m = imaplib2.IMAP4_SSL(account['host'])
    while True:
        password = getpass.getpass('Please enter the password for host %s and username %s: ' % (account['host'], account['username']))
        try:
            m.login(account['username'], password)
        except imaplib2.IMAP4.error:
            print 'Incorrect username/password. To change your username or host, you can run setup_accounts.py again or change the accounts.json file directly and then rerun this. Try again.'
            continue
        if not is_account_to:
            m.select()
            if m.search(None, 'ALL')[1][0] != '':
                print 'Warning: the inbox for this account is not empty. When setup is complete, all messages in the inbox will be imported and will then be deleted.'
                if not ask_continue():
                    sys.exit(0)
        passwords[account['pass_var']] = password
        return

def git_setup():
    """(Re-)Initialize the git repo and commit any changed files."""
    subprocess.check_output(['git', 'init'])
    subprocess.check_output(['git', 'add', '.'])
    # The command below can fail if nothing changed (so a new commit isn't
    # needed), in which case we can just ignore the failure.
    try:
        subprocess.check_output(['git', 'commit', '-m', 'Autocommit by heroku_install.py'])
    except subprocess.CalledProcessError:
        pass

def heroku_setup():
    """Setup and push to heroku.

    Create a new heroku app if this is not already an app directory. Push to
    heroku, set the config vars to the account passwords and scale to 1 worker
    dyno.
    """
    try:
        # If not already a heroku app directory
        if subprocess.Popen(['heroku', 'ps'], stderr=subprocess.PIPE).wait():
            subprocess.check_call(['heroku', 'create'])
    except OSError as e:
        if e.errno == errno.ENOENT:
            print 'Error: heroku is not installed. Please install and setup the Heroku CLI and then rerun this. Exiting...'
            sys.exit(1)
        else:
            pass

    config_vars = []
    for pass_var in passwords:
        config_vars.append(pass_var + '=' + passwords[pass_var])
    subprocess.check_output(['heroku', 'config:set'] + config_vars)
    subprocess.check_call(['git', 'push', 'heroku', 'master'])
    subprocess.check_call(['heroku', 'ps:scale', 'worker=1'])


load.load_accounts()
accounts = load.accounts
passwords = {}
get_password(accounts['m_to'], True)
for account_from in accounts['m_froms']:
    get_password(account_from)
print 'Please wait, setting up Heroku...'
git_setup()
heroku_setup()

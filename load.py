import json

def load_accounts():
    """A helper function that initializes this module's `accounts` variable.

    `accounts` is initialized from the `accounts.json` file, and `pass_var` is
    initialized appropriately for each account.
    """
    global accounts
    with open('accounts.json', 'r') as f:
        accounts = json.load(f)

    accounts['m_to']['pass_var'] = 'M_TO_PASS'
    m_froms = []
    for i in range(len(accounts['m_froms'])):
        account_from = accounts['m_froms'][i]
        account_from['pass_var'] = 'M_FROM' + str(i) + '_PASS'

import json

def load_accounts():
    """A helper function that initializes this module's `accounts` variable.

    `accounts` is initialized from the `accounts.json` file, and `pass_var` is
    initialized appropriately for each account.
    """
    global accounts
    with open('accounts.json', 'r') as f:
        accounts = json.load(f)
        accounts = _to_str(accounts)

    accounts['m_to']['pass_var'] = 'M_TO_PASS'
    for i in range(len(accounts['m_froms'])):
        account_from = accounts['m_froms'][i]
        account_from['pass_var'] = 'M_FROM' + str(i) + '_PASS'

def _to_str(d):
    """Returns `d` with unicode objects converted to str objects.

    `d` can be a `dict`, `list`, or string."""
    if isinstance(d, dict):
        return {_to_str(key): _to_str(value) for key, value in d.iteritems()}
    elif isinstance(d, list):
        return [_to_str(element) for element in d]
    elif isinstance(d, unicode):
        return d.encode('utf-8')
    else:
        return d

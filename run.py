"""Import emails continuously from and to the user's specified accounts.

Everything must already be set up properly for this to work."""

import json
import threading
import mailbox
import load
import time
import sys

load.load_accounts()
accounts = load.accounts
m_to = mailbox.Mailbox(**accounts['m_to'])
threads = []
for account_from in accounts['m_froms']:
    m_from = mailbox.Mailbox(**account_from)
    t = threading.Thread(target=mailbox.Mailbox.idle, args=(m_from, m_to))
    t.start()
    threads.append(t)

# Continuously check if any of the threads crashed, and if so exit (and wait for
# Heroku to restart the script) so that all the mailboxes are actually being
# imported from.
while True:
    for t in threads:
        if not t.is_alive():
            print 'A thread died, exiting'
            # Log out of `m_to`. The other mailboxes will automatically log out
            # before their `idle()` method exits.
            m_to.logout()
            sys.exit(1)
    time.sleep(10)

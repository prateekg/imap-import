Imap-import
===========

A server app that uses the IMAP IDLE command to import email from multiple IMAP
accounts (`from_accounts`) to one Gmail account (`to_account`). The problem with
forwarding email to `to_account` is that if the email isn't directly addressed
to the `from_account`, you can't automatically add a Gmail label to the
forwarded messages and if you have Gmail's "Send mail as" configured, it won't
automatically send from the right account if you reply to the message. Gmail's
Mail Fetcher feature works great, but it checks for new emails infrequently and
is limited to 5 accounts. `imap-import` solves these issues by doing something
similar to Gmail's Mail Fetcher, but it uses the IMAP IDLE command to get
notified when new messages arrive in `from_accounts`, so that new emails are
imported (usually) within a minute of their arrival. Just set it up once on
Heroku (or your own server, with a little more work) and forget about it.

Requirements
------------
The `from_accounts` must support an SSL connection and must support the IDLE
command. The `to_account` must be a Gmail account.

Any messages found in the inbox of `from_accounts` will be imported to
`to_account`. (This is how the app keeps track of which emails have already been
imported and which haven't. Any emails in the inbox are assumed to be new
messages that need importing.) Transferred messages are deleted, or in the case
of Gmail, archived (although you can change this behavior within Gmail's IMAP
settings). It is recommended that initially all the inboxes of the
`from_accounts` are empty.

If you want to set it up on Heroku, you must have the [Heroku
CLI](https://devcenter.heroku.com/articles/heroku-command) installed and set up.

Setup
-----
First run `python setup_accounts.py` to setup the account information. Then, to
run it on Heroku, run `python heroku_setup.py` to get the account passwords
(they are stored as [Heroku config vars](https://devcenter.heroku.com/articles/config-vars)
- it's the most secure way I could find of storing passwords on
Heroku), set up, and start a Heroku app. The app only requires 1 worker dyno, so
it can be run for free.

If you don't want to run it on Heroku, you still need to run `python
setup_accounts.py` first. Then, the app just expects the passwords to be set as
environment variables. The password for `to_account` should be in the
environment variable `M_TO_PASS`, and the passwords for `from_accounts` should
be in `M_FROM<index>_PASS` where `<index>` is the index at which that account
appears in the `accounts.json` file for the key `m_froms`. You can run it with
`python run.py`. Any reasonably recent version of Python 2 should work. You
probably want to log the output somewhere, and make sure that if `run.py` ever
dies it is restarted automatically.

Contact
-------
[Open a new issue](https://github.com/viveksjain/imap-import/issues/new) or
email me at [vivek@vivekja.in](mailto:vivek@vivekja.in).

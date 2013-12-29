import imaplib2
import time
from email.parser import HeaderParser
import os

class Mailbox(object):

    """Stores an IMAP mailbox and handles transferring new messages to another Mailbox."""

    def __init__(self, host, username, pass_var, label='', x_gmail_fetch_info=''):
        """Initialize a new IMAP mailbox.

        `host`, `username`   - those for the corresponding IMAP mailbox
        ``pass_var`          - name of the environment variable containing the
                                   password for this mailbox
        `label`              - optional label to assign when messages from this
                                   mailbox are transferred to another mailbox
        `x_gmail_fetch_info` - optional `X-Gmail-Fetch-Info` to add to messages
                                   before they are transferred to another mailbox
        """
        self._host = host
        self._username = username
        self._pass_var = pass_var
        self._label = label
        self._x_gmail_fetch_info = x_gmail_fetch_info

        self._parser = HeaderParser()
        self._login()

    def _login(self):
        """(Re-)Initialize `self._m`.

        `self._m` is set to a logged in instance of `imaplib2.IMAP4_SSL`
        corresponding to this mailbox.
        """
        self._m = imaplib2.IMAP4_SSL(self._host)
        self._m.login(self._username, os.environ[self._pass_var])

        self._m.select()

    def logout(self):
        """Log out of this mailbox, if it is logged in.

        This method should only be called if the account is logged in (i.e.
        `_login()` has been called successfully and `logout()` has not been
        called since).
        """
        self._m.close()
        self._m.logout()

    def idle(self, m_to):
        """Transfer new emails from this mailbox to `m_to`.

        Uses the IMAP IDLE command to wait for new messages, and any messages
        found in the inbox are transferred to `m_to`. Transferred messages are
        deleted, or in the case of Gmail, archived (although you can change this
        behavior within Gmail's IMAP settings). Logs out of this mailbox before
        exiting.
        """
        retry = False
        try:
            while True:
                msgs = self._m.search(None, 'ALL')[1][0]
                if msgs != '':
                    for msg in msgs.split(' '):
                        typ, data = self._m.fetch('1', '(RFC822)') # Message will always be the first one since we archive previous messages as we go
                        if typ != 'OK' or data[0] is None:
                            print 'Could not get a message for account ' + self._username + ':' + self._host + ', will try again'
                            retry = True
                            break
                        raw = data[0][1]
                        parsed_msg = self._parser.parsestr(raw)
                        if self._x_gmail_fetch_info != '':
                            raw = 'X-Gmail-Fetch-Info: ' + self._x_gmail_fetch_info + '\r\n' + raw

                        if parsed_msg['Subject'] is None:
                            parsed_msg['Subject'] = ''
                        print 'Copying message with subject "' + parsed_msg['Subject'] + '"'
                        msg_id = parsed_msg['Message-ID']
                        # Copy to m_to
                        try:
                            m_to._m.append('INBOX', None, None, raw)
                        except imaplib2.IMAP4.abort:
                            m_to._login()
                            m_to._m.append('INBOX', None, None, raw)
                        # Add label
                        if self._label != '':
                            new_msg = m_to._m.search(None, 'Header', 'Message-ID', msg_id)[1][0]
                            m_to._m.store(new_msg, '+X-GM-LABELS', self._label)
                        # Archive from self._m
                        self._m.store('1', '+FLAGS', '(\Deleted)')
                        self._m.expunge()
                try:
                    if not retry:
                        self._m.idle(timeout=24*60)
                    retry = False
                except:
                    time.sleep(5)
                    self._login()
                    # Don't idle - go back to fetching to check for new messages
        finally:
            self.logout()

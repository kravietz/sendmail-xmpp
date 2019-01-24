#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import email.utils
import fileinput

import sleekxmpp as sleekxmpp

__author__ = 'Pawel Krawczyk'


class Sendmail(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, recipients, message, subject):
        super(Sendmail, self).__init__(jid, password)
        self.recipients = recipients
        self.msg = message
        self.subject = subject
        self.add_event_handler('session_start', self.start)

    def start(self, event):
        self.send_presence()
        for recipient in self.recipients:
            self.send_message(mto=recipient,
                              msubject=self.subject,
                              mbody=self.msg,
                              mtype='normal')

        self.disconnect(wait=True)


if __name__ == '__main__':
    header = {}
    message = ""
    in_header = True

    for line in fileinput.input():
        line = line.strip()
        if in_header:
            if ':' in line:
                name, value = line.split(':', maxsplit=1)
                header[name.lower()] = value
            if len(line) == 0:
                in_header = False
        else:
            message += line

    if not {'to', 'from', 'subject'}.issubset(header.keys()):
        raise ValueError('Message must contain at least To, From, Subject headers', header)

    # extract JID and password from the From header
    from_header = ""
    try:
        from_header = email.utils.getaddresses([header['from']])[0][1]
    except IndexError:
        print('From header must be in format USER_PASSWORD@JABBER.COM')
        exit(1)

    user_pass, domain = from_header.split('@')
    username, password = user_pass.split('_')
    jid = sleekxmpp.basexmpp.JID('{}@{}'.format(username, domain))
    jid.resource = 'sendmail'

    recipients = [x[1] for x in email.utils.getaddresses([header['to']])]

    xmpp = Sendmail(jid, password, recipients, message, header['subject'])
    if xmpp.connect():
        xmpp.process(block=True)
    else:
        print('Unable to connect.')
    exit(1)

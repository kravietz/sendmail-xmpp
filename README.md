# Sendmail-XMPP

A simple XMPP client program that mimics `sendmail` program interface and sends
the received message over XMPP rather than SMTP. Intended for use with daemons
that can send messages through `sendmail` but do not implement XMPP 
messaging natively.

## Installation

     sudo apt install python3 python3-sleekxmpp
     sudo cp sendmail-xmpp.py /usr/local/bin/sendmail-xmpp.py
     sudo chmod 755 /usr/local/bin/sendmail-xmpp.py
     
XMPP requires client authentication and to minimize dependency on 
configuraton files etc the program takes all its data from the message
headers, which are usually configurable in the daemons it's being used with.

Note that the `From` header is special because it must contain XMPP
JID **and** password - the following shows configuration for an user with
JID `sender@xmpp.example.com` and password `password`:

```
From: Wazuh <sender_password@xmpp.example.com>
To: <recipient1@xmpp.example.com>, recipient1@xmpp.example.com
```

Passwords containing non-RFC822 characters or underscore `_`
are currently not supported.

## Integration with Wazuh

This tool was originally written to allow instant alert notifications from
[Wazuh](https://documentation.wazuh.com/current/user-manual/manager/manual-email-report/index.html) which does not support XMPP natively. Respective `ossec.conf`
section:

```
<email_notification>yes</email_notification>
<smtp_server>/usr/local/bin/sendmail-xmpp.py</smtp_server>
<email_from>sender_password@xmpp.example.com</email_from>
<email_to>recipient1@xmpp.example.com,recipient1@xmpp.example.com</email_to>
```

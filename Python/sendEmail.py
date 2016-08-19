# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import random
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

from_addr = "youemail"
password = "email password"
to_addr = "to email"
smtp_server = "smtp.163.com"

msg = MIMEText(u'xxx', 'html', 'utf-8')
msg['From'] = _format_addr(u'xx <%s>' % from_addr)
msg['To'] = _format_addr(u'xx <%s>' % to_addr)
msg['Subject'] = Header(u'xxx'+ str(random.randint(1,9999999)), 'utf-8').encode()

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
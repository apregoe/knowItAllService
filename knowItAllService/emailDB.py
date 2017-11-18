import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

fromAddr = "knowitallusc310@gmail.com"
fromPass = "H52-J5K-Wm7-WFb"
toaddr = "knowitallusc310@gmail.com"

msg = MIMEMultipart()

msg['From'] = fromAddr
msg['To'] = toaddr
msg['Subject'] = "database"

body = "db attached"

msg.attach(MIMEText(body, 'plain'))

filename = "db.sqlite3"
attachment = open("db.sqlite3", "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromAddr, fromPass)
text = msg.as_string()
server.sendmail(fromAddr, toaddr, text)
server.quit()
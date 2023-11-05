from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

def send_email(destination, body, subject):
    try:
        sender = 'josue.medinatest2810@gmail.com'
        password = "wqqkbsfgcbgiodla"
        
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = destination
        message['Subject'] = subject
        
        message.attach(MIMEText(body, 'plain'))
        
        servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        servidor_smtp.starttls()
        
        servidor_smtp.login(sender, password)
        servidor_smtp.sendmail(sender, destination, message.as_string())
        
        servidor_smtp.quit()
        
        return "Correo enviado exitosamente"        
    except Exception as e:
        print(e)
        return ''

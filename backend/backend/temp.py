import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Upgrade the connection to secure
    server.login('krishnarb08@gmail.com', 'esar wesd zrtx vkho')
    print("Connected successfully!")
    server.quit()
except smtplib.SMTPException as e:
    print(f"SMTP connection error: {e}")

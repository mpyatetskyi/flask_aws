import smtplib


def send_email(mail: str) -> None:
    from_email = "m.pyatetskyi.test@gmail.com"
    from_password = "qwerty123456qwerty"
    to_email = mail

    message = "Hey pal!!!!!!!" \
              "It`s absolutely insecure to send password by email"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, from_password)

    server.sendmail(from_email, to_email, message)

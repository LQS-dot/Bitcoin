import smtplib
from email.mime.text import MIMEText
from email.header import Header
from argparse import ArgumentParser


def send_email():
    receivers = "lucifer19961225@163.com" # 接受邮件
    message = MIMEText("lqs",'plain','utf-8')
    message['From'] = "838822954@qq.com "
    message['To'] = "lucifer19961225@163.com"

    # subject = args.subject
    message['Subject'] = Header("congratulations wallet is successfully",'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # smtpObj = smtplib.SMTP("smtp.exmail.qq.com", 465)
        smtpObj.login("838822954@qq.com", "xbvenudyhmapbfgj")
        smtpObj.sendmail("838822954@qq.com ", receivers, message.as_string())
        print("main has been send successfully")
    except smtplib.SMTPException as e:
        smtpObj.sendmail("838822954@qq.com", receivers, message.as_string())
        print("main has been send successfully")


if __name__ == "__main__":
    text = "This is a test"
    # send_email(parser_args1())
    send_email()
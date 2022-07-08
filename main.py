import re
import subprocess
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 获取变量
mail_host = os.getenv('mail_host')  # 设置服务器
mail_user = os.getenv('mail_user')   # 用户名
mail_pass = os.getenv('mail_pass')  # 口令
sender = os.getenv('mail_user')
print(os.getenv('secrets'))
print(mail_host, mail_pass, mail_user, os.getenv('receivers'), os.getenv('domains'))
receivers = os.getenv('receivers').split(';')  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
domains = os.getenv('domains').split(';')


def get_re_match_result(pattern, string):
    match = re.search(pattern, string)
    if match:
        return match.group(1)
    else:
        return None


def parse_time(date_str):
    return datetime.strptime(date_str, "%b %d %H:%M:%S %Y GMT")


def format_time(date_time):
    return datetime.strftime(date_time, "%Y-%m-%d %H:%M:%S")


def get_cert_info(domain):
    """获取证书信息"""
    cmd = f"curl -Ivs https://{domain} --connect-timeout 10"
    exitcode, output = subprocess.getstatusoutput(cmd)
    # 正则匹配
    start_date = get_re_match_result('start date: (.*)', output)
    expire_date = get_re_match_result('expire date: (.*)', output)
    # 解析匹配结果
    if start_date:
        start_date = parse_time(start_date)
        expire_date = parse_time(expire_date)
    return {
        'start_date': start_date,
        'expire_date': expire_date
    }


def get_cert_expire_date(domain):
    """获取证书剩余时间"""
    info = get_cert_info(domain)
    print(info)
    if info['start_date']:
        expire_date = info['expire_date']
    else:
        return None
    # 剩余天数
    return (expire_date - datetime.now()).days


if __name__ == "__main__":

    message = "请注意以下证书有效期：\r\n"
    for domain in domains:
        expire_date = get_cert_expire_date(domain)
        if not expire_date:
            message += f'域名{domain}已过期。\r\n'
        elif expire_date < 25:
            message += f'域名{domain}剩余{expire_date}天到期。\r\n'
    print(expire_date)
    try:
        message = MIMEText(message, 'plain', 'utf-8')
        message['From'] = Header("证书提醒", 'utf-8')
        # message['To'] = Header("", 'utf-8')
        subject = '证书到期预警'
        message['Subject'] = Header(subject, 'utf-8')
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

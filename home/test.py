import os
# import subprocess
import openai
from subprocess import PIPE, run
from django.core.mail import send_mail
from os import path, environ
from sys import path as sys_path
from django import setup

# sys_path.append(<path to django setting.py>)    
# environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
# setup()
# openai.api_key = "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"
# def out(command):
#     result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
#     return result.stdout

# my_output = out("openai api fine_tunes.create -t training_data.jsonl -m davinci")
# print("outputttt", my_output, type(my_output), my_output.split("\n")[0], my_output.split("\n")[1])
# openai.organization = "YOUR_ORG_ID"ft-6FUTpJQJ6bFSIy4aqAymZuag
# file_upload_obj = openai.File.create(
#   file=open("training_data.jsonl", "rb"),
#   purpose='fine-tune'
# )
# os.system("openai api fine_tunes.create -t training_data.jsonl -m davinci")

# response = openai.File.create(
#   file=open("filip19921992@gmail.com-training_data.jsonl", "rb"),
#   purpose='fine-tune'
# )
# finetune = openai.FineTune.create(training_file=response.id)

# response = openai.FineTune.create(training_file = file_upload_obj.id, model="davinci")
# print(file_upload_obj.id)
# print(response)

# answer = openai.Completion.create(
#   model="davinci:ft-augmented-intelligence-research-2023-02-06-17-36-57",
#   prompt="Where did Colleen Delgado work as a Rust Developer?",
#   max_tokens=30, # Change amount of tokens for longer completion
#   temperature=0
# )
# # answer = " davinci:ft-personal-2023-02-06-16-08-23".strip(" ")
# # print(" davinci:ft-personal-2023-02-06-16-08-23")   
# print(answer)   
# answer = openai.Model.list()openai api completions.create -m davinci:ft-personal-2023-02-05-07-33-01 -p "What skills does Colleen Delgado have?"


# proc = subprocess.Popen("echo hello world!!!!", stdout=subprocess.PIPE, shell=True)
# (out, err) = proc.communicate()
# print("up")
# print("program type of output:", out[0], out[1], out[2], out[3], out[4], "err:", err)

# print("down") 

import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content("success!! Hello")
msg['Subject'] = f'Test Email'
msg['From'] = "colleendlgd@gmail.com"
msg['To'] = "joelbird1128@gmail.com"
s = smtplib.SMTP('smtp.gmail.com')
s.send_message(msg)
s.quit()


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
send_mail("subject", "message", "colleendlgd@gmail.com", ["joelbird1128@gmail.com"], fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)
import os
# import subprocess
import openai
from subprocess import PIPE, run

openai.api_key = "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"
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

answer = openai.Completion.create(
  model="davinci:ft-augmented-intelligence-research-2023-02-06-17-36-57",
  prompt="Where did Colleen Delgado work as a Rust Developer?",
  max_tokens=30, # Change amount of tokens for longer completion
  temperature=0
)
# answer = " davinci:ft-personal-2023-02-06-16-08-23".strip(" ")
# print(" davinci:ft-personal-2023-02-06-16-08-23")   
print(answer)   
# answer = openai.Model.list()openai api completions.create -m davinci:ft-personal-2023-02-05-07-33-01 -p "What skills does Colleen Delgado have?"


# proc = subprocess.Popen("echo hello world!!!!", stdout=subprocess.PIPE, shell=True)
# (out, err) = proc.communicate()
# print("up")
# print("program type of output:", out[0], out[1], out[2], out[3], out[4], "err:", err)

# print("down") 
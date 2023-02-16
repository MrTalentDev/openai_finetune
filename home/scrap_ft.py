from bs4 import BeautifulSoup
import requests
import openai
import math
import json
import re
import os
import smtplib
from email.message import EmailMessage
from subprocess import PIPE, run
from django.conf import settings
from django.core.mail import send_mail
from .mqtt_2 import client as mqtt_2_client
openai.api_key = os.getenv("OPENAI_API_KEY")
file_name = "training_data.jsonl"

msg = EmailMessage()
msg.set_content("success!! Hello")

def get_questions(context):
    print('context-----------', context)
    print('aaaaaaa', "write questions as array fommat based on the text below\n\nText: \"" + context + "\"")

    questions = openai.Completion.create(
        model= "text-davinci-003",
        prompt= "write questions as array fommat based on the text below\n\nText: \"" + context + "\"",
        temperature= 0,
        max_tokens= 2000,
        top_p= 1,
        frequency_penalty= 0.5,
        presence_penalty= 0,
    )
    print("questions", questions.choices[0].text[questions.choices[0].text.find('['):questions.choices[0].text.find(']')+1])
    return questions.choices[0].text[questions.choices[0].text.find('['):questions.choices[0].text.find(']')+1]

def get_answers(context, questions):
    response = openai.Completion.create(
        model= "text-davinci-003",
        prompt= "write answers as  array for these questions based on the text below\n\nText: \"" + context + "\"\n\nQuestions:\n" + questions,
        temperature= 0,
        max_tokens= 2000,
        top_p= 1,
        frequency_penalty= 0.5,
        presence_penalty= 0,
    )
    print(response.choices[0].text[response.choices[0].text.find('['):response.choices[0].text.find(']')+1])
    return response.choices[0].text[response.choices[0].text.find('['):response.choices[0].text.find(']')+1]


def scrapFromURL(url:str)->str:
    baseURL = url[0 : url.find('/', 8, 100)]
    print('BaseURL', baseURL)
    resultStr = ''

    page = requests.get(url)
    try:
        soup = BeautifulSoup(page.content, 'html.parser')
    except:
        pass
    aList = soup.find_all('a')
    i = 0
    resultStr += soup.get_text()
    print('related pages number:', len(aList))
    while i < len(aList):
        print("*******************", aList[i].get("href"))
        if(aList[i].get("href") == None):
            i += 1
            continue
        if aList[i].get("href")[0] == '/' or aList[i].get("href").find(baseURL) > 0:
            print('scraping related url', baseURL + aList[i].get("href"))
            resultStr += BeautifulSoup(requests.get(baseURL + aList[i].get("href")).content, 'html.parser').get_text()
        i += 1
    return resultStr
def createTrainData(questionArrayStr, answerArrayStr, userID):
    try:
        questionArray = json.loads(questionArrayStr)
        answerArray = json.loads(answerArrayStr)
    except:
        return
    resultArray = []
    for index in range(len(questionArray)):
        temp = {"prompt":"", "completion": ""}
        temp["prompt"] = questionArray[index] + "\n\n###\n\n"
        temp["completion"] = answerArray[index] + "\n"
        resultArray.append(temp)
    with open(userID+"-"+file_name, "a") as output_file:
        for entry in resultArray:
            json.dump(entry, output_file)
            output_file.write("\n")
def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout
def main( doc_url, userID ):
    pros=0
    try:
        Tcontext = scrapFromURL(doc_url)
    except:
        return {"code": 500, "message": "failed", "body": "We can't get data from your url"}
    Tcontext = Tcontext.strip()
    Tcontext = "".join(re.findall("[a-zA-Z 0-9:!@#$%^&*?/,.<>\|';{}=+-_()]", Tcontext))
    print('-------------Tcontext------------', Tcontext)
    ## progress
    pros+=4
    rc, mid = mqtt_2_client.publish('django/progress/setting/'+userID, pros)
    print(pros, '_rc',rc, 'mid', mid)    
    nToken = len(Tcontext.split())
    print('number of tokens', nToken)
    result = []
    for i in range(math.ceil(len(Tcontext) / 1000)):
        context = Tcontext[i*1000:(i + 1)*1000]
        try:
            questionArrayStr = get_questions(context)
            answerArrayStr = get_answers(context, questionArrayStr)
            createTrainData(questionArrayStr, answerArrayStr, userID)
        except Exception as e:
            pass
    ## progress
    pros+=4
    rc, mid = mqtt_2_client.publish('django/progress/setting/'+userID, pros)
    print(pros, '_rc',rc, 'mid', mid)    
    print("fine tune started!!!")
    try:
        fineTuneConfirm = out("openai api fine_tunes.create -t " + userID + "-training_data.jsonl -m davinci")
        pros+=10
        rc, mid = mqtt_2_client.publish('django/progress/setting/'+userID, pros)
        print(pros, '_rc',rc, 'mid', mid)    
        ## progress
    except:
        return {"code": 500, "message": "failed", "body": "please run \'pip install openai!\'"}
    while fineTuneConfirm.find("succeeded") < 0:
        print("#########", fineTuneConfirm.split("\n"))
        fineTuneConfirm = out(fineTuneConfirm.split("\n")[-3])
        if pros<90:
            pros+=10
            rc, mid = mqtt_2_client.publish('django/progress/setting/'+userID, pros)
            print(pros, '_rc',rc, 'mid', mid)  
    ## 100%
    pros=100
    rc, mid = mqtt_2_client.publish('django/progress/setting/'+userID, pros)
    print(pros, '_rc',rc, 'mid', mid)  
    print("***********", fineTuneConfirm.split("\n"), "=======", fineTuneConfirm.split("\n")[-2])
    email(userID, ' Fine-tune is completed. Test your model. \n ModelID:' + fineTuneConfirm.split("\n")[-2].split(" ")[4])
    return {"code": 200, "message": "success", "body": fineTuneConfirm.split("\n")[-2].split(" ")[4]}

def completion(modelID, prompt):
    print("modelID:", modelID)
    if modelID == "":
        modelID = "text-davinci-003"
    try:
        answer = openai.Completion.create(
            model=modelID,
            prompt=prompt,
            # top_p=1,
            max_tokens=256, # Change amount of tokens for longer completion
            temperature=0
        )
    except Exception as ex:
        return {"code": 500, "message": "failed", "body": type(ex).__name__}
    print("answer---------", answer.choices[0].text)
    if answer.choices[0].text.find("###") > 0:
        return {"code": 200, "message": "success", "body": answer.choices[0].text.split("###")[1].strip().split("\n")[0]}
    return {"code": 200, "message": "success", "body": answer.choices[0].text}

def email(emailAddress, contentText):
    subject = 'SmartResponse'
    # message = ' Fine-tune is completed. Test your model. '
    message = contentText
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [emailAddress]
    send_mail( subject, message, email_from, recipient_list )
    return
# main("")

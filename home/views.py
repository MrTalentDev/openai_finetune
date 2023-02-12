from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login, authenticate
from django.views.generic.detail import DetailView
from .scrap_ft import main, completion
from .models import FineTunedModels
# import openai
# openai.api_key = "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"
# from .forms import SignUpForm

@login_required

class HomeView(DetailView):
    template_name = 'answer.html'

    def get_object(self):
        print(self.request.user)
        
        return self.request.user

@login_required
def answer(request):
    if request.method == 'POST':
        # form = SignUpForm(request.POST)
        form = request.POST
        question = form.get("question", "")
        model_id=""
        print("print_id")
        try:
            print("print_id11111", request.user)
            usr = FineTunedModels.objects.get(user_email=request.user)
            print("user--------",usr)
            model_id = usr.model_id
        except FineTunedModels.DoesNotExist:
            print("print_id 33333333")
            
            pass
        answer = completion(model_id.strip(" "), question)
        print("=============", question)
        # answer = "this is response"
        
        context = {'question':question, 'answer':answer}
        return render(request, 'answer.html', context)
    return render(request, 'answer.html')

@login_required
def setting(request):
    if request.method == 'POST':
        form = request.POST
        doc_url = form.get("doc_url", "")
        print('====================',doc_url)
        model_id=main(doc_url, str(request.user))
        # model_id='adfasdfasdfasdfdf980'
        print('====================',model_id)
        
        print('========================', model_id)
        try:
            FineTunedModels.objects.get(user_email=request.user)
            FineTunedModels.objects.filter(user_email=request.user).update(model_id=model_id)
        except FineTunedModels.DoesNotExist:
            usr = FineTunedModels(user_email=request.user, model_id=model_id) # create new model instance
            usr.save()
        
        context = {'code':200, 'doc_url':doc_url, 'model_id':model_id}
        return render(request, 'setting.html', context)
    return render(request, 'setting.html')


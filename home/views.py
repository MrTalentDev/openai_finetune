from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login, authenticate
from django.views.generic.detail import DetailView
from .scrap_ft import main, completion
from .models import FineTunedModels
from users.models import User 
from django.views.generic.detail import DetailView
from . import mqtt
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
            print("print_id does not exist")
            
        answer = completion(model_id.strip(" "), question)
        print("=============", answer.get('code'))
        # answer = "this is response"
        # answer = json.loads(ans)
        context = {'question':question, 'answer':answer.get('body'), 'code':answer.get('code'), 'message':answer.get('message')}
        return render(request, 'answer.html', context)
    return render(request, 'answer.html')

@login_required
def setting(request):
    print("sssssssss")
    mqtt.client.loop_start()
    usr = User.objects.filter(email=request.user).get()
    context = {
        'is_loading' : usr.is_loading,
        'loading_doc': usr.loading_doc
    }
    return render(request, 'setting.html', context=context)
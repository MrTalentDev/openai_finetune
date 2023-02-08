from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic.detail import DetailView

from .forms import SignUpForm


class UserView(DetailView):
    template_name = 'profile.html'

    def get_object(self):
        print(self.request.user)
        return self.request.user


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # print(form)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, email=user.email, password=raw_password)
            print(user)
            if user is not None:
                login(request, user)
            else:
                print("user is not authenticated")
            return redirect('home:answer')
    form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def reset(request):
    if request.method == 'POST':
        # form = SignUpForm(request.POST)
        # # print(form)
        # if form.is_valid():
        #     user = form.save()
        #     raw_password = form.cleaned_data.get('password1')
        #     user = authenticate(request, email=user.email, password=raw_password)
        #     if user is not None:
        #         login(request, user)
        #     else:
        #         print("user is not authenticated")
        return redirect('users:profile')
    else:
        form = SignUpForm()
    return render(request, 'reset.html')











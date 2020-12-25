from django.shortcuts import render
from django.views import View
from allauth.account.forms import LoginForm
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView

# Create your views here.
class Index(View):
    def get(self,request,*args,**kwargs):
        return render(request,'account/login.html')
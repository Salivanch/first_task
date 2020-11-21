from django.shortcuts import render,redirect, reverse
from django.views.generic import View
from .models import SiteContent, Profile, Question
from .forms import RegistrationForm, LoginForm, QuestionForm
from django.contrib.auth import logout, login, authenticate
from .send_msg import send
from django.contrib.auth.models import User
from django.http import JsonResponse


class LandingPage(View):
    template_name="constructor/LandingPage.html"

    def get_context_data(self, request, ctx={}):

        try:
            content=1 #id сборки блоков
            ctx['content']=SiteContent.objects.get(pk=content)
            ctx['content']=ctx['content'].content.all()

            if ctx['content'].filter(header=True).exists(): #Собираем навигацию
                ctx=self.take_navList(ctx)
        except Exception:
            print("Такой сборки не существует!")

        ctx['RegistrationForm']=RegistrationForm()
        ctx['LoginForm']=LoginForm(domain=request.build_absolute_uri().split("/user")[0])
        ctx['QuestionForm']=QuestionForm()
        return ctx

    def get(self,request):
        return render(request,self.template_name,self.get_context_data(request))

    @staticmethod
    def take_navList(ctx):
        ctx['nav']={}
        for block in ctx['content']:
            if block.header:
                ctx['nav'][block.header.info.title]=block.header.info.name
            if block.have_questions:
                ctx['nav'][block.have_questions.info.title]=block.have_questions.info.name
            if block.send_question:
                ctx['nav'][block.send_question.info.title]=block.send_question.info.name
        return ctx


class Question(View):
    model=Question
    form_class=QuestionForm
    
    def post(self,request,answer={}):
        form=QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            answer['status']=True
        else:
            answer['errors']=form.errors
        return JsonResponse(answer)


class LoginPage(View):
    def post(self,request,answer={}):
        form=LoginForm(request.POST,domain=request.build_absolute_uri().split("/user")[0])
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username, password=password)
            login(request,user)
            answer['link']=request.build_absolute_uri(reverse('landing'))
        else:
            answer['errors']=form.errors
        return JsonResponse(answer)


class RegistrationPage(View):
    def post(self,request,answer={}):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            send(form.cleaned_data['username'],form.cleaned_data['email'],request.build_absolute_uri().split("/user")[0])
            answer['link']=request.build_absolute_uri(reverse('landing'))
        else:
            answer['errors']=form.errors
        return JsonResponse(answer)


class LogoutPage(View):
    def post(self,request):
        logout(request)
        return redirect('landing')


class СonfirmationAccount(View):
    def get(self,request, slug):
        profile=Profile.objects.get(token=slug)
        profile.confirmed=True
        profile.save()
        return redirect('landing')


class UserStats(View):
    model=User
    template_name="constructor/UserStats.html"

    def get_context_data(self, ctx={}):
        ctx['all']=self.model.objects.all()
        ctx['online']=ctx['all'].filter(is_active=True)
        return ctx

    def get(self,request):
        return render(request,self.template_name,self.get_context_data())

from django.shortcuts import render,redirect
from django.http import HttpResponse
from MusicApp.models import Profile,Song
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def Music_HomePage(request):
	return render(request,'Music_HomePage.html')



def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/login_page')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/login_page')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/login_page')
        
        login(request , user)
        return redirect('/music_page')

 
    return render(request,'login_page.html')



def register_page(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		try:
			if User.objects.filter(username = username).first():
				messages.success(request, 'Username is already exists.')
				return redirect('/register_page')

			if User.objects.filter(email = email).first():
				messages.success(request, 'Email is already exists.')
				return redirect('/register_page')
			user_obj = User(username = username , email = email)
			user_obj.set_password(password)
			user_obj.save()
			auth_token = str(uuid.uuid4())


			profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
			profile_obj.save()
			send_mail_after_registration(email , auth_token)
			return redirect('/token_send')
		except Exception as e:
			print(e)		


	return render(request,'register_page.html')



def success(request):
	return render(request,'sucess.html')



def token_send(request):
	return render(request,'token_send.html')



def verify(request,auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/login_page')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/login_page')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/Music_HomePage')


def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

def logout_user(request):
    logout(request)
    return redirect("/Music_HomePage")




#### music page ######
@login_required(login_url="/")
def music_page(request):
    song=Song.objects.all()
    return render(request,'music_page.html',{'song':song})



def basic(request):
      return render(request,'basic.html')



def songpost(request):
    song=Song.objects.all()
    return render(request,'songpost.html',{'song':song})

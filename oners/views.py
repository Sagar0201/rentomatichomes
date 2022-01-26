from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from django.http import request

# create user
from django.contrib.auth.models import User
# PopUp messages
from django.contrib import messages, auth
# Login User
from django.contrib.auth import authenticate, login, logout
# for login required
from django.contrib.auth.decorators import login_required
# for add home page

from oners.models import Rentales
from oners.models import Chat
from django.contrib.auth import get_user_model
# from django.contrib import models
# user update
from oners.forms import UserUpdate, ProfileUpdate


# new user account creation


def SignUp(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']

        # check for errorneous input
        if len(username) > 10:
            messages.error(request, "Plase Enter The User Name Under 10 Char.")
            return redirect('/oners/SignUp')

        if not username.isalnum():
            messages.error(
                request, "Username should only contain letters and number")
            return redirect('/oners/SignUp')

        if User.objects.filter(username=username).exists():
            messages.error(request, "This Username should All Ready Taken")
            return redirect('/oners/SignUp')
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(
            request, f"Account Created sucessfully. Your Username is {username} and Password is {password}")
    return render(request, 'oners/Accounts/SignUp.html')


def Login(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect("home")
            else:
                messages.error(request, "You're Account is Disable")
        else:
            messages.error(
                request, "Invalid Username Or Password please try again")
            return redirect('/oners/Login', {"loginusername": loginusername, "loginpassword": loginpassword})

    return render(request, 'oners/Accounts/Login.html')


@login_required(login_url="/oners/Login/")
def SignOut(request):
    auth.logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("/oners/Login")

# AddRoom here


@login_required(login_url="/oners/Login/")
def AddHome(request):
    if request.method == "POST":
        user_id = request.user.id
        oner_mobile_no = int(request.POST.get('user_mobile_no'))
        home_image = request.FILES['img']
        home_name = request.POST.get('home_name',)
        home_city = request.POST.get('city')
        home_city = home_city.capitalize()
        home_info = request.POST.get('home_info')
        home_address = request.POST.get('home_address')
        home_rent = request.POST.get('rent')

        params = {"user_mobile_no": oner_mobile_no, "home_image": home_image,
                  "home_name": home_name, "city": home_city, "home_info": home_info, "home_address": home_address, "rent": home_rent}

        if type(oner_mobile_no) != int:
            messages.error(request, 'Mobile Number Must Be Intergers.')
            return render(request, "oners/House/AddHome.html", params)

        if len(str(oner_mobile_no)) != 10:
            messages.error(request, "Mobile Number Must Be 10 Degits.")
            return render(request, "oners/House/AddHome.html", params)

        Rentales.objects.create(
            user_id=user_id, oner_mobile_no=oner_mobile_no, home_image=home_image, home_name=home_name, home_city=home_city, home_info=home_info, home_address=home_address, home_rent=home_rent)
        messages.success(request, "Rental House Added Successfully")
    return render(request, 'oners/House/AddHome.html')

# Profile page


@login_required(login_url="/oners/Login/")
def Profile(request):
    if request.method == "POST":
        BookId = request.POST.get('BookId')
        u_form = UserUpdate(request.POST, instance=request.user)
        p_form = ProfileUpdate(request.POST, request.FILES,
                               instance=request.user.profile)
        BookId = request.POST.get('BookId')

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile Update Sucessfully.")

        if BookId is not None:
            RentalesDelete = Rentales.objects.get(pk=BookId)
            RentalesDelete.delete()
            messages.success(request, "Rental Delete Sucessfully")
            return redirect("Profile")
        return redirect("/oners/Profile")

    user_id = request.user.id
    no_messages = len(Chat.objects.filter(receiver=int(user_id)))

    rentales = Rentales.objects.filter(user=user_id)
    rentales_home = []
    for i in rentales:
        rentales_home.append(i)
    Rentales_Posts = len(rentales_home)
    return render(request, 'oners/Accounts/Profile.html', {"rentales": rentales_home, 'Rentales_Posts': Rentales_Posts, "no_messages": no_messages})


@login_required(login_url="/oners/Login/")
def Message(request):
    if request.method == "POST":
        sender_id = request.user.id
        receiver_id = request.POST.get('receiver_id')
        message = request.POST.get('message')
        Rental_id = request.POST.get('Rental_id')

        if sender_id == int(receiver_id):
            messages.warning(request, "You Can't Send Message To Self")
            return redirect("/customers/Rentals/?Rental="+Rental_id)
        if Chat.objects.create(
                sender_id=sender_id, receiver_id=receiver_id, message=message):
            messages.success(request, "Message Send Successfully")
            # return redirect("/customers/AllRentals")
            return redirect("/customers/Rentals/?Rental="+Rental_id)

    return render(request, 'customers/AllRentals.html')


@login_required(login_url="/oners/Login/")
def Message_Chat(request):

    if request.method == "POST":
        receiver_id = request.POST.get('receiver_id')

        if receiver_id is not None:
            senders = set()
            for i in Chat.objects.filter(receiver=int(receiver_id)):
                senders.add(i.sender)
            if len(senders) == 0:
                messages.warning(request, "You Have Zero Messages.")
                return redirect("/oners/Profile")
            return render(request, 'oners/Accounts/Messages.html', {"senders": senders})

        sender_id = request.POST.get('sender_id')
        receiver_id = request.user.id
        message = request.POST.get('message')
        if message != None:
            Chat.objects.create(sender_id=receiver_id,
                                receiver_id=sender_id, message=message)
        senders = set()
        for i in Chat.objects.filter(receiver=int(receiver_id)):
            senders.add(i.sender)

        message_user = set()
        for i in Chat.objects.filter(sender=int(
                sender_id), receiver=int(receiver_id)):
            message_user.add(i.sender)

        chats = []
        for i in Chat.objects.all():
            if i.sender.id == int(sender_id) and i.receiver.id == int(receiver_id):
                chats.append(i)
            if i.sender.id == int(receiver_id) and i.receiver.id == int(sender_id):
                chats.append(i)

        return render(request, 'oners/Accounts/Messages.html', {"senders": senders, "message_user": message_user, "chats": chats})


def forgetpass(request):
    return render(request, 'oners/Accounts/forget.html',)

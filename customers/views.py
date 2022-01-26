from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage


# Create your views here.
from django.http import request
from django.shortcuts import render, HttpResponse, redirect

from django.contrib import messages

from oners.models import Rentales
from customers.models import ContactInfo
from django.contrib.auth.models import User


def Contact(request):
    if request.method == "POST":
        name = request.POST.get('name', 'unknown')
        email_address = request.POST.get('email')
        message_subject = request.POST.get('message_subject')
        message = request.POST.get('message', 'no message')

        print(name, email_address, message_subject, message)

        # send_mail(
        #     # mail subject
        #     f"message from {name} and send from {email_address}",
        #     message,  # message
        #     email_address,  # from email
        #     ['sagarkakade0201@gmail.com'],  # to mail
        # )

        Contact_us = ContactInfo(
            name=name, message_subject=message_subject, email_address=email_address, message=message)
        Contact_us.save()

        messages.success(request, "Message Send  Successfully")

    return render(request, 'customers/Contact.html')


def AllRentals(request):
    page_num = request.GET.get('page')
    if page_num is None:
        page_num = 1
    rentals_posts = Rentales.objects.all()
    p = Paginator(rentals_posts, 4)
    try:
        home_rentals = p.page(page_num)
    except EmptyPage:
        home_rentals = p.page(p.num_pages)
    return render(request, 'customers/AllRentals.html', {"home_rentals": home_rentals})


def Rentals(request):
    Rental_id = request.GET.get('Rental')
    home_rentals = Rentales.objects.filter(id=Rental_id)
    return render(request, 'customers/Rental.html', {"home_rentals": home_rentals, "Rental_id": Rental_id})


def Search(request):
    search = request.GET.get('Query')
    page_num = request.GET.get('page')

    if len(search) > 78:
        all_rentals = Rentales.objects.none()
    else:
        username = Rentales.objects.filter(user__username__icontains=search)
        first_name = Rentales.objects.filter(
            user__first_name__icontains=search)
        last_name = Rentales.objects.filter(user__last_name__icontains=search)
        email = Rentales.objects.filter(user__email__icontains=search)
        oner_mobile_no = Rentales.objects.filter(
            oner_mobile_no__icontains=search)
        home_name = Rentales.objects.filter(
            home_name__icontains=search)
        home_city = Rentales.objects.filter(
            home_city__icontains=search)
        home_info = Rentales.objects.filter(
            home_info__icontains=search)
        home_address = Rentales.objects.filter(
            home_address__icontains=search)
        home_rent = Rentales.objects.filter(
            home_rent__icontains=search)
        all_rentals = oner_mobile_no.union(username, first_name, last_name, email,
                                           home_name, home_city, home_info, home_address, home_rent)

        if page_num is None:
            page_num = 1
        p = Paginator(all_rentals, 4)
        try:
            home_rentals = p.page(page_num)
        except EmptyPage:
            home_rentals = p.page(p.num_pages)

        if all_rentals.count() == 0:
            messages.warning(
                request, "No Search results Found. Please refine your query. Please Try Another KeyWords.")
    return render(request, 'customers/Search.html', {"home_rentals": home_rentals, "Query": search})

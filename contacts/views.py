from django.core.mail import send_mail
from django.shortcuts import render,redirect
from .models import Contacts
from django.contrib import messages

# Create your views here.
def contact(request):
    if request.method == "POST":
        listing_id=request.POST["listing_id"]
        listing=request.POST["listing"]
        name=request.POST["name"]
        email=request.POST["email"]
        phone=request.POST["phone"]
        message=request.POST["message"]
        realtor_email=request.POST["realtor_email"]
        user_id=request.POST["user_id"]

        # Check if user has already made an enquiry
        if request.user.is_authenticated:
            user_id=request.user.id
            hasConneceted=Contacts.objects.all().filter(listing_id=listing_id,user_id=user_id)
            if hasConneceted:
                messages.error(request,"You have already made an enuiry for this property")
                return redirect("/listings/"+listing_id)
        contact=Contacts(listing=listing,listing_id=listing_id,name=name,email=email,message=message,phone=phone,user_id=user_id)

        contact.save()

        # send email

        send_mail(
            'Property listing enquiry',
            'There has been an enquiry for' + listing +'login to admin panel for more',
            'anshu06468@gmail.com',
            ['anshukumar.kumar447@gmail.com',
            realtor_email
            ],
            fail_silently=False,
        )

        messages.success(request,"Your request has been submitted, a realtor will get back to you soon")
        return redirect("/listings/"+listing_id)

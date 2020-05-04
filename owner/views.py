# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from account.models import Profile
from productCreate.models import Products, ProductsImages, Category, SubCategory
from django.db.models import Q
from django.db.models import Count
from django.http import HttpResponseRedirect, Http404,HttpResponse, JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import InformationForm
from django.core.mail import send_mail
import random

@login_required
def my_cart(request):
    myab_list = Products.objects.filter(profile__user=request.user)
    profile = Profile.objects.get(user=request.user)
    ads = Products.objects.filter(active=True)
    lates = Products.objects.all().order_by('-created_date')[:3]
    counts = Products.objects.all().values('category__name').annotate(total=Count('category'))

    paginator = Paginator(myab_list, 6)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get('page')
    try:
        myab = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        myab = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        myab = paginator.page(paginator.num_pages)
    return render(request, 'owner/cart.html', {'myab': myab, 'profile': profile, 'ads': ads, 'lates': lates,
                                                 'counts': counts, 'page_request_var': page_request_var})



def bookmarked(request):
    return render(request, 'owner/bookmarked.html', {})

@login_required
def delete_post(request,pk=None):
    ad = Products.objects.get(id=pk)
    if request.user != ad.profile.user:
        raise Http404()
    ad.is_active = False
    messages.success(request, "Successfuly deleted")
    return redirect('home:allads_list')


@login_required
def hide_post(request,pk=None):
    ad = Products.objects.get(id=pk)
    if request.user != ad.profile.user:
        raise Http404()
    ad.is_active = False
    messages.success(request, "You property has been successfuly deleted")
    return redirect('home:allads_list')

def create_contact(request):
    if request.POST:
        form = InformationForm(request.POST)
        if form.is_valid():
            post_info = form.save(commit=False)
            # post.user = request.user
            post = form.cleaned_data
            subject = post['subject']
            message ='Hello "{}" sent you a message below \n{}'.format( post['name'], post['message'])
            sender = post['email']
            to = ['ezechdr16@gmail.com']
            send_mail(subject, message, sender, to)
            post_info.save()

            # text = form.cleaned_data['headline','content']
            messages.add_message(request, messages.SUCCESS, 'Your message has been recieved')
            form = InformationForm()
            return redirect('others:create_contact')

    else:
        form = InformationForm()

        args = {'form': form}
        return render(request, 'others/contact.html', args)

def about_us(request):
    return render(request, 'others/about.html',)

def faq(request):
    return render(request, 'others/faq.html',)


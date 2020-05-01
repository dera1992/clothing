# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.forms import modelformset_factory, inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Products, ProductsImages, Category,SubCategory
from .forms import AdsImageForm, AdsForm, AdsEditImageForm, AdsEditForm

from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def postAd(request):

    ImageFormSet = modelformset_factory(ProductsImages,
                                        form=AdsImageForm, extra=3)
    if request.method == 'POST':

        postForm = AdsForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=ProductsImages.objects.none())

        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.profile = request.user.profile
            post_form.save()

            for form in formset.cleaned_data:
                if form:
                    product_image = form['product_image']
                    photo = ProductsImages(products=post_form, product_image=product_image)
                    photo.save()
                    messages.success(request,"Your product has been created succcessfully")
            return redirect('home:allads_list')
        else:
            messages.error(request, 'Sorry,Error creating your product')
            print(postForm.errors, formset.errors)
    else:
        postForm = AdsForm()
        formset = ImageFormSet(queryset=ProductsImages.objects.none())
    return render(request, 'advert/post.html',
                  {'postForm': postForm, 'formset': formset})

@login_required
def editAd(request, pk):
    ad = Products.objects.get(id=pk)
    ImageFormSet = modelformset_factory(ProductsImages,fields=('product_image',), extra=3, max_num=3)
    if ad.profile.user != request.user:
        raise Http404()
    if request.method == 'POST':

        postForm = AdsEditForm(request.POST, request.FILES, instance=ad)
        formset = ImageFormSet(request.POST, request.FILES,request.FILES or None)

        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.profile = request.user.profile
            post_form.save()

            data = ProductsImages.objects.filter(products=ad)
            for index, f in enumerate(formset):
                if f.cleaned_data:
                    if f.cleaned_data['id'] is None:
                        photo = ProductsImages(products=ad, product_image=f.cleaned_data.get('product_image'))
                        photo.save()
                    elif f.cleaned_data['product_image'] is False:
                        photo = ProductsImages.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
                        photo.delete()
                    else:
                        photo = ProductsImages(products=ad, product_image=f.cleaned_data.get('product_image'))
                        d = ProductsImages.objects.get(id=data[index].id)
                        d.image = photo.product_image
                        d.save()
            messages.success(request, "{} has been successfully updated!".format(ad.title))
            return redirect('home:allads_list')
        else:
            messages.error(request, 'Sorry,Error updating your food')
            print(postForm.errors, formset.errors)
    else:
        postForm = AdsEditForm(instance=ad)
        formset = ImageFormSet(queryset=ProductsImages.objects.filter(products=ad))
    return render(request, 'advert/post.html',
                  {'postForm': postForm, 'formset': formset})


def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = SubCategory.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'advert/subcategory_dropdown_list_options.html', {'subcategories': subcategories})




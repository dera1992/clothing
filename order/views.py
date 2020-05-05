from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import OrderItem, Order, Lga , Address, State
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from .forms import OrderCreateForm, CheckoutForm
from cart.cart import Cart
from order.extras import generate_order_id
from account.models import Profile
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
# from .tasks import order_created
from productCreate.models import Products, ProductsImages, Category, SubCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

# import stripe
# stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

@login_required()
def order_create(request):
    # cart = Cart(request)
    # user_profile = get_object_or_404(Profile, user=request.user)
    # if request.method == 'POST':
    #     form = OrderCreateForm(request.POST)
    #     if form.is_valid():
    #         form.ref_code = generate_order_id()
    #         order = form.save()
    #         for item in cart:
    #             OrderItem.objects.create(order=order,
    #                                      product=item['product'],
    #                                      price=item['price'],
    #                                      quantity=item['quantity'])
    #         # clear the cart
    #         cart.clear()
    #         order_created.delay(order.id)
    #         messages.success(request, 'You have make order successful')
    #         return render(request,
    #                       'owner/checkout.html',
    #                       {'order': order})
    #         # return redirect(reverse('payment:process'))
    # else:
    #     first_name = user_profile.user.first_name
    #     last_name = user_profile.user.last_name
    #     email = user_profile.user.email
    #     phone = user_profile.phone
    #     address = user_profile.address
    #     data = {'first_name':first_name,'last_name':last_name,'email':email,'phone':phone,'address':address}
    #     form = OrderCreateForm(initial=data)
    return render(request, 'owner/checkout.html')

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, is_ordered=False)
            form = CheckoutForm()
            states = State.objects.all()
            cities = Lga.objects.all()
            context = {
                'form': form,
                'order': order,
                'states':states,
                'cities':cities
            }
            return render(self.request, "owner/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("order:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, is_ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                state = form.cleaned_data.get('state')
                city = form.cleaned_data.get('city')
                same_billing_address = form.cleaned_data.get('same_billing_address')
                save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = Address(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    state = state,
                    city = city
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                if payment_option == '0':
                    return redirect('order:payment', payment_option='online payment')
                elif payment_option == 'T':
                    return redirect('order:transfer', payment_option='transfer')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('order:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("cart:order-summary")

class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        if order.billing_address:
            context = {
                'order': order,
            }
            return render(self.request, "owner/payment.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):

        return redirect("/payment/stripe/")

@login_required
def order_owner(request):
    order_list = Order.objects.filter(user=request.user)
    lates = Products.objects.all().order_by('-created_date')[:3]
    counts = Products.objects.all().values('category__name').annotate(total=Count('category'))

    paginator = Paginator(order_list, 6)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get('page')
    try:
        allorder = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        allorder = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        allorder = paginator.page(paginator.num_pages)
    return render(request, 'owner/order_list.html', {'allorder': allorder,'lates': lates,
                                                 'counts': counts, 'page_request_var': page_request_var})


@login_required
def order_all(request):
    order_list = Order.objects.all()
    lates = Products.objects.all().order_by('-created_date')[:3]
    counts = Products.objects.all().values('category__name').annotate(total=Count('category'))

    paginator = Paginator(order_list, 6)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get('page')
    try:
        allorder = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        allorder = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        allorder = paginator.page(paginator.num_pages)
    return render(request, 'owner/order_list.html', {'allorder': allorder,'lates': lates,
                                                 'counts': counts, 'page_request_var': page_request_var})


def load_cities(request):
    state_id = request.GET.get('state')
    cities = Lga.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'owner/city_dropdown_list_options.html', {'cities': cities})


def transfer(request,self):
    try:
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        order.is_ordered = True
        order.save()
        messages.warning(
            self.request, "Make your payment and your product will get to you")
        return redirect('order:checkout')
    except ObjectDoesNotExist:
        messages.warning(self.request, "You do not have an active order")
        return redirect("cart:order-summary")
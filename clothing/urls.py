from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('social-auth/',include('social_django.urls', namespace='social')),
    path('productcreate/',include('productCreate.urls', namespace='productcreate')),
    path('blog/',include('blog.urls', namespace='blog')),
    path('marketing/',include('marketing.urls', namespace='marketing')),
    path('',include('home.urls', namespace='home')),
    path('order/',include('order.urls', namespace='order')),
    path('owner/',include('owner.urls', namespace='owner')),
    path('product_search/',include('search.urls', namespace='product_search')),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('tracking/', include('tracking.urls')),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings')),
]
if settings.DEBUG:urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
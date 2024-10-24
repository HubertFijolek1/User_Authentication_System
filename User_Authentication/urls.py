from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # Your accounts app URLs
    # path('', include('two_factor.urls', namespace='two_factor')),
]

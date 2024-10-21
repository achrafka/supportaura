from django.contrib import admin
from django.urls import path
from resources.user.views import LoginView, LogoutView


urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path("admin/", admin.site.urls),

]

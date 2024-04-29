"""
URL configuration for Student_Help project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Student_Help import settings
from django.conf.urls.static import static

from myapp.views import all_posts, create_account, create_account_view, create_post, creation_posts, creation_transport, dashbord_view, login_user, login_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_account/',create_account,name = "create_account" ),
    path('create_account_view/',create_account_view,name = "create_account_view"),
    path('loginn/',login_user,name = "loginn"),
    path('login_view/',login_view),
    path('create_post/<type_post>/',create_post),
    path('create_recommendation/',creation_posts,name="create_post_rec"),
    path('creation_transport/',creation_transport,name="creation_transport"),
    path('all_posts/', all_posts, name='all_posts'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
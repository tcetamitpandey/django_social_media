from django.urls import path


from social_app.views import Index
from social_app.views import SignUp
from social_app.views import SignIn
from social_app.views import LikePost
from social_app.views import UploadPost
from social_app.views import profileView
from social_app.views import LogoutView
from social_app.views import followView
from social_app.views import settingsView
from social_app.views import searchView

urlpatterns=[
    path("",Index, name="index"),
    path("signup/",SignUp, name="signup"),
    path("signin/",SignIn, name="signin"),
    path("upload/",UploadPost, name="upload"),
    path("search/",searchView, name="search"),
    path("profile/<str:id>",profileView, name="profile"),
    path("follow/<str:pk>",followView, name="follow"),
    
    path("like-post/<str:id>",LikePost, name="like-post"),
    path("logout/",LogoutView, name="logout"),
    path("settings/",settingsView, name="settings"),
]
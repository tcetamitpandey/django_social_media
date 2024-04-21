from django.contrib import admin

from social_app.models import Profile
from social_app.models import Interest
from social_app.models import Post
from social_app.models import LikeModel
from social_app.models import Followers_Model

admin.site.register(Profile)
admin.site.register(Interest)
admin.site.register(LikeModel)
admin.site.register(Post)
admin.site.register(Followers_Model)
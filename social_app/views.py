from django.shortcuts import render,redirect
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

from social_app.models import Profile
from social_app.models import Post
from social_app.models import Interest
from social_app.models import LikeModel
from social_app.models import Followers_Model

from itertools import chain # convert query list into list

@login_required(login_url="signin")
def Index(req):
    curr_user=User.objects.get(username=req.user.username)
    user_profile=Profile.objects.get(user=curr_user)

    # global feed
    post_data=Post.objects.all()

    """
    # getting all the users whome i follow and iterate over the followers list and getting all posts from that user
    """
    # data of the local feed specific to the user
    user_following_list=[]
    feed=[]

    user_following= Followers_Model.objects.filter(follower=req.user.id)

    for user in user_following:
        # appeding all the users (whome this user follow) there username into this list
        user_following_list.append(user.user)

    for username in user_following_list:
        # getting all post form this user
        feed_lists = Post.objects.filter(user=username)

        feed.append(feed_lists)
    # /Now 'feed variable' is like a query set we have to convert it into list


    local_feed_list = list(chain(*feed))

    context={
        "user_profile" : user_profile,
        "post_data" : post_data, #global feed
        "local_feed_list" : local_feed_list #local feed
    }

    return render(req,"index.html",context)


@login_required(login_url="signin")
def searchView(req):

    user_object=User.objects.get(username=req.user.username)
    user_profile=Profile.objects.get(user=user_object)
    

# load a html with the particular search keyword
# eg: all user whoes name is amit
    data=""

    if(req.method == "POST"):
        search_username=req.POST["username"]

        search_data =User.objects.filter(username__icontains=search_username)

        username_profile=[]
        username_profile_list =[]

        for user in search_data:
            username_profile.append(user.id)
        # Now we have the id lets get all  the profiles 

        for ids in username_profile:
           username_profile_list.append( Profile.objects.filter(id_user=ids) )

        username_profile_list= list(chain(*username_profile_list))

    # -----------------
    selected_interest_ = [interest for interest in user_profile.interest.all()]

    context={
        "all_data_found": username_profile_list,
        "user_profile" : user_profile,
        "interests":selected_interest_
    }
    
    return render(req, "search_page.html",context)


def SignUp(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        # Check if email or username already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("signup")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("signup")

        # Create new user and profile
        try:
            user=User.objects.create_user(username=username,email=email,password=password)
            user.save()
            login(request,user) #loging new user

            curr_user=User.objects.get(username=username)

            user_profile=Profile.objects.create(user=curr_user,id_user=curr_user.id)
            user_profile.save()
            #remaning details will be filled by user himself
            return redirect("settings") 

        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return redirect("signup")

        
    return render(request,"signup.html")

def SignIn(req):
    if req.method=="POST":
        
        username=req.POST.get("username")
        password=req.POST.get("password")

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            login(req,user)
            return redirect("index")
        else:
            messages.info(req,"Credentials invalid")
            return redirect("signin")
    
    return render(req,"signin.html")

@login_required(login_url="signin")
def LogoutView(req):

    logout(req)
    return redirect("signup")

@login_required(login_url="signin")
def settingsView(req):
    # enctype="multipart/form-data" add this in form to handle file submition

    user_profile=Profile.objects.get(user=req.user)

    if req.method=="POST":
        bio = req.POST.get('bio')
        location = req.POST.get('location')
        interests = req.POST.getlist('interests') #getting a list of interests

        if req.FILES.get('profile') is None:
            dpimage=user_profile.profile_img
        else:
            dpimage=req.FILES.get('profile')

        user_profile.bio=bio
        user_profile.location=location
        user_profile.profile_img=dpimage

        # saving multiple interests
        # Clear existing interests and set new ones
        user_profile.interest.clear()  # Clear existing interests
        for interest_id in interests:
            interest = Interest.objects.get(id=interest_id)
            user_profile.interest.add(interest)

        user_profile.save()

        return redirect("index")
    
    #selected interest ids to show in user profile settings
    selected_interest_ids = [interest.id for interest in user_profile.interest.all()]

    context={
        "interest_data": Interest.objects.all(),
        "user_profile": user_profile, #current user data is sent into html
        "selected_interest_ids":selected_interest_ids
        
    }
    return render(req,"settings.html",context)


@login_required(login_url="signin")
def LikePost(req,id):
    post_obj=Post.objects.get(id=id)
    liked_obj=LikeModel.objects.filter(post_id=id, username=req.user.username).first()

    if liked_obj == None:
        new_like=LikeModel.objects.create(post_id=id,username=req.user.username)
        new_like.save()
        post_obj.no_of_likes +=1
        post_obj.save()
        return redirect('index')
    else:
        liked_obj.delete()
        post_obj.no_of_likes -=1
        post_obj.save()
        return redirect('index')
    

@login_required(login_url="signin")
def followView(req,pk):
    curr_user=req.user.username
    # curr_user=User.objects.get(username=curr_user)
    want_to_follow=User.objects.get(username=pk)

    create_follower=Followers_Model.objects.filter(user=curr_user,follower=want_to_follow.username).first()

    if create_follower==None:
        create_follower=Followers_Model.objects.create(user=curr_user,follower=want_to_follow.username)
        create_follower.save()
    else:
        create_follower.delete()

    return redirect("/profile/" + want_to_follow.username)


@login_required(login_url="signin")
def profileView(req,id):
    # here id is that users username

    user_obj=User.objects.get(username=id)
    user_profile=Profile.objects.get(user=user_obj)
    user_posts=Post.objects.filter(user=user_obj)

    # check if user is follow this new user or not
    curr_user=req.user.username
    want_to_follow=id

    if Followers_Model.objects.filter(user=curr_user,follower=want_to_follow).first():
        button_text="Unfollow"
    else:
        button_text="Follow"

    user_followers=Followers_Model.objects.filter(user=id)
    user_followings=Followers_Model.objects.filter(follower=id)
    #we want number of followe for this current profile 
    # print(f"\n\n\n {user_followes}\n\n\n")


    context={
        "user_data" : user_obj,
        "user_profile" : user_profile,
        "user_posts" : user_posts,
        "interests" : user_profile.interest.all(),
        "no_of_posts" : len(user_posts),

        "button_text":button_text,
        "user_followers_list":user_followers,

        "user_followers":len(user_followers),
        "user_followings":len(user_followings),
    }

    return render(req, "profile.html",context)


@login_required(login_url="signin")
def UploadPost(req):
    curr_user=User.objects.get(username=req.user.username)
    user_profile=Profile.objects.get(user=curr_user)

    if req.method =="POST":
        user=curr_user
        post_img=req.FILES.get("image_upload")
        caption=req.POST.get("caption_upload")

        post_data=Post.objects.create(user=user,post_img=post_img,caption=caption)
        post_data.save()

        return redirect("index")

    context={
        "user_profile" : user_profile
    }
 
    return render(req,"post_upload.html",context)
from django.core import files
from django.db import models
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login
from poll.forms import ThumbnailForm, UsersForm, PostMediaForm, PostForm, CommentForm, AlbumPostForm, UploadImageForm, PollAddForm, EditPollForm, ChoiceAddForm
from .models import Album, Album_post, Thumbnail, Users, PostMedia, Post, Comments, Upload, Poll, Choice, Vote
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.core.files import File
from pyffmpeg import FFmpeg
from django.urls import reverse
import os
import subprocess
# from ffvideo import VideoStream

# from video_encoding.backends import get_backend


# Create your views here.


def signup(request):
    form = UsersForm()
    context = {
        'form': form
    }

    if request.method == 'POST':
        form = UsersForm(request.POST, request.FILES)
        if form.is_valid():
            f1 = form.cleaned_data['first_name']
            f2 = form.cleaned_data['last_name']
            e = form.cleaned_data['email']
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            pi = form.cleaned_data['profile_image']
            dob = form.cleaned_data['dob']
            g = form.cleaned_data['gender']
            mn = form.cleaned_data['mobile_number']
            users = Users.objects.create_user(first_name=f1, last_name=f2, username=u,
                                              email=e, password=p, profile_image=pi, dob=dob, gender=g, mobile_number=mn)

            return redirect('/login')
        form = UsersForm(request.POST)
    return render(request, 'signup.html', context)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
                return redirect('/')
            else:
                return HttpResponse("User not found")
    return render(request, "login.html")


def post_create_view(request):
    form1 = PostMediaForm()
    form2 = PostForm()
    context = {
        'form1': form1,
        'form2': form2

    }
    if request.method == 'POST':
        form1 = PostForm(request.POST, request.FILES)
        form2 = PostMediaForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            content = form1.cleaned_data['content']
            user = request.user
            image = form2.cleaned_data['image']
            video = form2.cleaned_data['video']
            post = Post.objects.create(content=content, user=user)
            postmedia = PostMedia.objects.create(
                post=post, video=video)
            for afile in request.FILES.getlist('image'):
                postmedia = PostMedia.objects.create(
                    post=post, image=afile)

            return HttpResponseRedirect('/')
        else:
            form = PostMediaForm()
    return render(request, 'post_create.html', context)


def all_post(request):
    user = request.user
    posts = Post.objects.filter(user=request.user)
    postmedia = PostMedia.objects.filter(post__in=posts)
    comments = Comments.objects.all()

    context = {
        'posts': posts,
        'postmedia': postmedia,
        'user': user,
        'comments': comments
    }
    return render(request, 'index.html', context)


def delete_post(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect('/')


def AddLike(request, pk):
    post = Post.objects.get(pk=pk)
    is_dislike = False
    for dislike in post.dislike.all():
        if dislike == request.user:
            is_dislike = True
            break

    if is_dislike:
        post.dislike.remove(request.user)
    is_like = False
    for like in post.like.all():
        if like == request.user:
            is_like = True
            break
    if not is_like:
        post.like.add(request.user)
    if is_like:
        post.like.remove(request.user)
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)


def AddDislike(request, pk):
    post = Post.objects.get(pk=pk)
    is_like = False
    for like in post.like.all():
        if like == request.user:
            is_like = True
            break
    if is_like:
        post.like.remove(request.user)

    is_dislike = False
    for dislike in post.dislike.all():
        if dislike == request.user:
            is_dislike = True
            break
    if not is_dislike:
        post.dislike.add(request.user)
    if is_dislike:
        post.dislike.remove(request.user)
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)


def PostDetails(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        post = None
    comment = Comments.objects.all()
    try:
        postmedia = PostMedia.objects.all()
    except PostMedia.DoesNotExist:
        postmedia = None
    try:
        user = request.user
    except Users.DoesNotExist:
        user = None

    form = CommentForm()
    context = {
        'post': post,
        'postmedia': postmedia,
        'user': user,
        'comment': comment,
        'form': form
    }
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
        return redirect('/')

    return render(request, 'post_detail.html', context)


def album_post(request):
    form = AlbumPostForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = AlbumPostForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['album_image']
            vid = form.cleaned_data['album_video']
            cont = form.cleaned_data['content']
            n = form.cleaned_data['name']
            user = request.user
            album = Album.objects.create(name=n, user=user)
            post = Album_post.objects.create(
                album=album, album_video=vid, content=cont)

            for afile in request.FILES.getlist('album_image'):
                post = Album_post.objects.create(
                    album=album, album_image=afile)
            return HttpResponseRedirect('/album-all-post')
    return render(request, 'album_post.html', context)



def all_album_post(request):
    albums = Album.objects.filter(user=request.user)
    album_posts = Album_post.objects.filter(album__in=albums)
    context = {
        'albums': albums,
        'album_posts': album_posts
    }
    return render(request, 'album_all_post.html', context)


def delete_album_post(request, id):
    post = Album.objects.get(id=id)
    post.delete()
    return redirect('/album-all-post')


def compress_images(request):
    compressimage = Upload.objects.all()
    context = {
        'compressimage': compressimage
    }
    return render(request, 'compress_photo.html', context)


def uploadImage(request):
    form = UploadImageForm(request.POST, request.FILES)
    context = {
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/all-compress-image')
        else:
            form = UploadImageForm(request.POST, request.FILES)
    return render(request, 'uploading_image.html', context)


def delete_compress_photo(request, id):
    photo = Upload.objects.get(id=id)
    photo.delete()
    return redirect('/all-compress-image')


def delete_poll(request, id):
    poll = Poll.objects.get(id=id)
    poll.delete()
    return redirect('/all-poll')


def all_poll(request):
    polls = Poll.objects.all()
    context = {
        'polls': polls
    }
    return render(request, 'all_poll.html', context)


def create_thumbnail(request):
    form = ThumbnailForm()
    if request.method == 'POST':
        form = ThumbnailForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.cleaned_data['video']

            thum = Thumbnail.objects.create(video=video)
            return redirect('/thumbnail')
    context = {
        'form': form
    }
    return render(request, 'thumbnail_create.html', context)


def all_thumbnail(request):
    thum = Thumbnail.objects.all()
    context = {
        'thum': thum
    }
    return render(request, 'thumbnail.html', context)


def polls_list(request):
    polls = Poll.objects.all()

    context = {
        'polls': polls,


    }
    return render(request, 'polls/polls_list.html', context)


def list_by_user(request):
    all_polls = Poll.objects.filter(owner=request.user)
    paginator = Paginator(all_polls, 7)

    page = request.GET.get('page')
    polls = paginator.get_page(page)

    context = {
        'polls': polls,
    }
    return render(request, 'polls/polls_list.html', context)


def polls_add(request):
    if request.method == 'POST':
        form = PollAddForm(request.POST)
        if form.is_valid:
            poll = form.save(commit=False)
            poll.owner = request.user
            poll.save()
            new_choice1 = Choice(
                poll=poll, choice_text=form.cleaned_data['choice1']).save()
            new_choice2 = Choice(
                poll=poll, choice_text=form.cleaned_data['choice2']).save()
            new_choice3 = Choice(
                poll=poll, choice_text=form.cleaned_data['choice3']).save()

            messages.success(
                request, "Poll & Choices added successfully", extra_tags='alert alert-success alert-dismissible fade show')

            return redirect('list')
    else:
        form = PollAddForm()
    context = {
        'form': form,
    }
    return render(request, 'polls/add_poll.html', context)


def polls_delete(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    if request.user != poll.owner:
        return redirect('/list')
    poll.delete()
    messages.success(request, "Poll Deleted successfully",
                     extra_tags='alert alert-success alert-dismissible fade show')
    return redirect("/list")


def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('/list')

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request, "Choice added successfully", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('/list')
    else:
        form = ChoiceAddForm()
    context = {
        'form': form,
    }
    return render(request, 'polls/add_choice.html', context)


def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if not poll.active:
        return render(request, 'polls/poll_result.html', {'poll': poll})
    loop_count = poll.choice_set.count()
    context = {
        'poll': poll,
        'loop_time': range(0, loop_count),
    }
    return render(request, 'polls/poll_detail.html', context)


def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get('choice')
    if not poll.user_can_vote(request.user):
        messages.error(
            request, "You already voted this poll", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("/list")

    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        vote = Vote(user=request.user, poll=poll, choice=choice)
        vote.save()
        print(vote)
        return render(request, 'polls/poll_result.html', {'poll': poll})
    else:
        messages.error(
            request, "No choice selected", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("detail", poll_id)
    return render(request, 'polls/poll_result.html', {'poll': poll})


def endpoll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('/list')
    if poll.active is True:
        poll.active = False
        poll.save()
        return render(request, 'polls/poll_result.html', {'poll': poll})
    else:
        return render(request, 'polls/poll_result.html', {'poll': poll})


def result(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)

    context = {
        'poll': poll
    }

    return render(request, 'polls/result2.html', context)

def delete_comment(request, id):
    comment = Comments.objects.get(id=id)
    comment.delete()
    return redirect('/')

def delete_poll(request, id):
    poll = Poll.objects.get(id=id)
    poll.delete()
    return redirect('/list')
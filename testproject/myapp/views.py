from django.shortcuts import render
from django.http import HttpResponse
from .models import Tweet
from .forms import tweetForm
from django.shortcuts import get_object_or_404,redirect
# Create your views here.
def homeView(request):
    return render(request,'home.html')

def tweetList(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request,'tweetList.html',{'tweets':tweets})

def tweetCreate(request):
    if request.method =="POST":
        form = tweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweetList')
    else:
        form = tweetForm()
    return render(request,'tweetForm.html',{'form':form})

def tweetEdit(request,tweetId):
    tweet = get_object_or_404(Tweet,pk = tweetId,user = request.user)
    if request.method == 'POST':
        form = tweetForm(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweetList')
    else:
        form = tweetForm(instance=tweet)
    return render(request,'tweetForm.html',{'form':form})

def tweetDelete(request,tweetId):
    tweet = get_object_or_404(Tweet,pk = tweetId,user = request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweetList')
    return render(request,'tweet_delete_form.html',{'tweet':tweet})
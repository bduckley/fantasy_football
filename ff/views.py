from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from .ff_espn_api import League

# Create your views here.
def homepage(request):
	# could have something like leagues = league(league_id)... here?
	return render(request,'ff/homepage.html')

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'ff/post_list.html', {'posts':posts})
	
def post_detail(request,pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'ff/post_detail.html',{'post':post})
	
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail',pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'ff/post_edit.html', {'form':form})
	
def post_edit(request, pk):
	post = get_object_or_404(Post,pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail',pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'ff/post_edit.html', {'form':form})
	
def weekly_scores(request):
	# Get all this info via a form in future. can use username and password apparently instead of espn_s2 and swid
	league_id = 692156
	year = 2019
	espn_s2 = 'AEBlxO7SfF6cuPjEvujvAbpQ5fmvr7oYPxIyQV9qsazYKOuNCN14sb%2FBGr4yOyXwUtLTS8a4igLp2SrraMI6lC1EoWiHHKPhUZyqMiS%2B7JCKSapXyDbqHnX8ur1Ga0q3d7sGe9i4gi8ZKbIqaZWhJBdEqqa2UXBDLrgoxpUade%2BzepUwahpfqOvzOr87TiXACwdcnRIqPmhXGW4SuPU8kMlLqWPgj3zL%2FGLKF%2B%2B2gZ1AQxgHUBXYIXpHatVRgWndZNPLIfehi8FV5Xmi8PZnWP2%2F'
	swid = "{E9BFC86F-E2A7-4FD8-BFC8-6FE2A71FD8B5}"
	league = League(league_id, year, espn_s2, swid)
	teams = league.teams
	top_scorer = league.top_scorer
	matchups = league.scoreboard
	return render(request, 'ff/weekly_scores.html',{'league':league})
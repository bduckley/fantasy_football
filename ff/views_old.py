from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from .ff_espn_api import League
import plotly.offline as opy
import plotly.graph_objs as go
from django.views.generic.base import TemplateView

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
	
class Graph(TemplateView):
    template_name = 'ff/Graph.html'

    def get_context_data(self, **kwargs):
        context = super(Graph, self).get_context_data(**kwargs)

        x = [-2,0,4,6,7]
        y = [q**2-q+3 for q in x]
        trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': 10},
                            mode="lines",  name='1st Trace')

        # data=go.Data([trace1])
        data = [trace1]
        layout=go.Layout(title="Meine Daten", xaxis={'title':'x1'}, yaxis={'title':'x2'})
        figure=go.Figure(data=data,layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')

        context['graph'] = div

        return context
	
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

def weekly_scores_new(request):
	league_id = 692156
	year = 2019
	espn_s2 = 'AEBlxO7SfF6cuPjEvujvAbpQ5fmvr7oYPxIyQV9qsazYKOuNCN14sb%2FBGr4yOyXwUtLTS8a4igLp2SrraMI6lC1EoWiHHKPhUZyqMiS%2B7JCKSapXyDbqHnX8ur1Ga0q3d7sGe9i4gi8ZKbIqaZWhJBdEqqa2UXBDLrgoxpUade%2BzepUwahpfqOvzOr87TiXACwdcnRIqPmhXGW4SuPU8kMlLqWPgj3zL%2FGLKF%2B%2B2gZ1AQxgHUBXYIXpHatVRgWndZNPLIfehi8FV5Xmi8PZnWP2%2F'
	swid = "{E9BFC86F-E2A7-4FD8-BFC8-6FE2A71FD8B5}"
	league = League(league_id, year, espn_s2, swid)
	teams = league.teams
	top_scorer = league.top_scorer
	matchups = league.scoreboard(week=12)
	# print(type(matchups))
	scores = league.box_scores
	data_home = [score.home_score for score in matchups[:]]
	data_away = [score.away_score for score in matchups[:]]
	data = data_home[:] + data_away[:]
#data = [score.home_score + score.away_score for score in matchups]
	# team_names = [score.home_team.team_name + score.away_team.team_name for score in matchups]
	team_names_home = [score.home_team.team_name for score in matchups[:]]
	team_names_away = [score.away_team.team_name for score in matchups[:]]
	team_names = team_names_home[:] + team_names_away[:]
	print(data)
	print(2)
	bars = go.Bar(x = team_names, y = data)
	figure = go.Figure(data = [bars])
	"""figure.update_layout(
		updatemenus=[go.layout.Updatemenu(buttons=list([
			dict(label="None",
				method="relayout",
				args=["
				"""
	plot_div = opy.plot(figure,output_type='div')
	# plot_div = opy([go.Bar(x = team_names, y = data)],output_type='div') 
	return render(request,'ff/weekly_scores_new.html', context ={'plot_div':plot_div})
	
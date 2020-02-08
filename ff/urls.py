from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('',views.homepage, name='homepage'),
	path('post-list',views.post_list, name='post_list'),
	path('post/<int:pk>/',views.post_detail,name='post_detail'),
	path('post/new/', views.post_new, name='post_new'),
	path('post/<int:pk>/edit/',views.post_edit, name='post_edit'),
	path('weekly_scores',views.weekly_scores, name='weekly_scores'),
	path('weekly_scores_new',views.weekly_scores_new, name='weekly_scores_new'),
	url('Graph',views.Graph.as_view(), name='Graph'),
]
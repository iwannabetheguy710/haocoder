from django.urls import path

from . import views

urlpatterns = [
	# contest page
	path('contest/', views.contest_page, name='contest page'),
	path('contest/<str:id>/', views.contest_page, name='contest detail page'),
	path('contest/<str:id>/problem/', views.contest_problem_page, name='contest problem page'),
	path('contest/<str:id>/problem/<str:problem_id>/', views.contest_problem_page, name='contest problem detail page'),
	path('contest/<str:id>/leaderboard/', views.contest_leaderboard_page, name='contest leaderboard page'),
	path('contest/<str:id>/register/', views.contest_register_page, name='contest register page'),
	path('contest/<str:id>/register/check/', views.contest_register_check_page, name='contest register check page'),
	path('contest/<str:id>/unregister/', views.contest_unregister_page, name='contest unregister page'),
]
from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index page'),

	# user and authentication
	path('login/', views.login_page, name='login page'),
	path('logout/', views.logout_page, name='logout page'),
	path('register/', views.register_page, name='register page'),

	# user profile
	path('profile/', views.profile_page, name='profile page'),
	path('profile/<str:qry>/', views.profile_page, name='profile user page'),
	path('ranking/', views.ranking_page, name='ranking page'),
]
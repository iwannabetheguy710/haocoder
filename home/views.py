from django.shortcuts import *
from django.http import *
from django.contrib.auth.models import *
from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError
from .models import *
from contest.models import *
from django.db.models import *

from django_q.tasks import async_task, result
import datetime, time

import warnings
warnings.filterwarnings("ignore")

ratingutil = {
	'Grandmaster': [2800, '#7d0000'],
	'International Master': [2500, '#ff0000'],
	'National Master': [2200, '#ff8800'],
	'Master': [2000, '#ff8800'],
	'Candidate Master': [1800, '#9607a3'],
	'Expert': [1600, '#000dff'],
	'Class A': [1400, '#00badb'],
	'Class B': [1200, '#00d10e'],
	'Class C': [1000, '#00d10e'],
	'Class D': [800, '#a8a8a8'],
	'Class E': [600, '#a8a8a8'],
	'Class F': [400, '#a8a8a8'],
	'Class G': [200, '#a8a8a8'],
	'Class H': [0, '#a8a8a8'],
}
code = {
	"Grandmaster": "GM",
	'International Master': "IM",
	'National Master': "NM",
	"Master": "M",
	"Candidate Master": "CM"
}

contest_time_pool = []

def perform_contest_time(contest_id):
	contest = Contest.objects.filter(contest_status="RUNNING", contest_id=contest_id)
	if contest.exists():
		contest = contest[0]
		elapsed = int((datetime.datetime.now().astimezone() - contest.contest_schedule).total_seconds())
		hour, minute, second = map(int, contest.contest_current_long.split(':'))
		while True:
			time.sleep(1)
			second -= 1
			if second < 0:
				second = 59
				minute -= 1
				if minute < 0:
					minute = 59
					hour -= 1
			if second == 0 and minute == 0 and hour == 0:
				break
			contest.contest_current_long = f"{hour}:{minute}:{second}"
			contest.save()
		contest.contest_status = "ARCHIVED"
		contest.save()

def index(req):
	running_contest = Contest.objects.filter(contest_status="SCHEDULE") | Contest.objects.filter(contest_status="RUNNING")
	"""
	for i in running_contest:
		if i.contest_status == "SCHEDULE" and i.contest_schedule <= datetime.datetime.now().astimezone():
			i.contest_status = "RUNNING"
			i.save()
		if i.contest_status == "RUNNING" and i.contest_id not in contest_time_pool:
			contest_time_pool.append(i.contest_id)
			async_task(perform_contest_time, i.contest_id, timeout=-1)
	"""

	p = Profile.objects.all()
	for i in p:
		for k, v in ratingutil.items():
			if i.ratings >= v[0]:
				i.role = k
				i.color = v[1]
				i.save()
				break
	h = Profile.objects.raw('SELECT * FROM home_profile WHERE ratings > highest_ratings')
	for o in h:
		o.highest_ratings = o.ratings
		for k, v in ratingutil.items():
			if o.highest_ratings >= v[0]:
				o.highest_role = k
				o.highest_color = v[1]
				o.save()
				break

	user_joined = None
	if req.user.is_authenticated:
		user_joined = Leaderboard.objects.filter(profile__user=req.user, contest__contest_status="RUNNING")
		if user_joined.exists():
			user_joined = user_joined[0]

	p = p.order_by('-ratings')
	if len(p)>10:
		p = p[:10]

	annouce = Announcement.objects.filter(visible=True).order_by('-publish_date')
	ongoing_contest = Contest.objects.filter(contest_status="SCHEDULE").order_by('-contest_created')

	return render(req, 'pages/index.html', {"ongoing_contest": ongoing_contest, "top10": p, "role_code": code, "userjoin": user_joined, "annoucement": annouce})

def login_page(req):
	if req.user.is_authenticated:
		return redirect('/')
	if req.method == "POST":
		user = authenticate(username=req.POST['username'], password=req.POST['password'])
		if user is not None:
			login(req, user)
			return JsonResponse({
				"done": "done",
			})
		else:
			return JsonResponse({
				"err-title": "????ng nh???p th???t b???i !",
				"err-description": "T??n t??i kho???n ho???c m???t kh???u kh??ng ????ng.",
			})
	elif req.method == "GET":
		return render(req, 'pages/user_auth/login.html')

def register_page(req):
	if req.method == "GET":
		return render(req, 'pages/user_auth/register.html')
	if req.method == "POST":
		err = {"err-title": "????ng k?? th???t b???i !", "err-description": ""}
		if req.POST['password'] != req.POST['repassword']:
			err["err-description"] += "M???t kh???u v?? m???t kh???u nh???p l???i kh??ng kh???p.<br>"
		username = req.POST['username']
		password = req.POST['password']
		email = req.POST['email']
		if len(password) < 8:
			err["err-description"] += "M???t kh???u ch??? ???????c ??t nh???t 8 k?? t???.<br>"
		for i in username:
			if len(username) < 4 or len(username) > 20:
				err["err-description"] += "T??n t??i kho???n ph???i c?? ????? d??i t??? 4 t???i 20 k?? t???.<br>"
				break
			if i not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_':
				err["err-description"] += "T??n t??i kho???n kh??ng ???????c bao g???m c??c k?? t??? ?????c bi???t ngo???i tr??? '_'.<br>"
		if err["err-description"]:
			return JsonResponse(err)

		try:
			if User.objects.filter(username__iexact=username).exists() or User.objects.filter(email__iexact=email).exists():
				raise Exception()
			user = User.objects.create_user(username, email, password)
			profile = Profile.objects.create(user=user, ratings=0.0)
			return JsonResponse({"done":"done"})
		except:
			err["err-description"] = "T??n t??i kho???n ho???c email ???? ???????c s??? d???ng.<br>"
			return JsonResponse(err)

def logout_page(req):
	if req.user.is_authenticated:
		logout(req)
		return redirect('/')
	else:
		raise Http404

def profile_page(req, qry=None):
	if qry or req.user.is_authenticated:
		usrprof = Profile.objects.filter(user__username=qry or req.user.username)
		if usrprof.exists():
			usrprof = usrprof[0]
			return render(req, 'pages/profile/profile.html', {"usrprof": usrprof, "code": code})
		else:
			return render(req, 'pages/error/hao404.html', {"err_msg": f"V??? huynh ????i ????y ??ang t??m ng?????i t??n l?? \"{qry}\" ????ng kh??ng v???y ? V??? h???o h??n ???? t???i h??? ????y c??ng ch??a t???ng nghe t??n."})
	else:
		raise Http404

def ranking_page(req):
	rank = Profile.objects.all().order_by('-ratings')
	return render(req, 'pages/ranking.html', {'ranking': rank, 'role_code': code})
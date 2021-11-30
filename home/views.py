from django.shortcuts import *
from django.http import *
from django.contrib.auth.models import *
from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError
from .models import *
from django.db.models import *

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

def index(req):
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

	return render(req, 'pages/index.html')

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
				"err-title": "Đăng nhập thất bại !",
				"err-description": "Tên tài khoản hoặc mật khẩu không đúng.",
			})
	elif req.method == "GET":
		return render(req, 'pages/user_auth/login.html')

def register_page(req):
	if req.method == "GET":
		return render(req, 'pages/user_auth/register.html')
	if req.method == "POST":
		err = {"err-title": "Đăng ký thất bại !", "err-description": ""}
		if req.POST['password'] != req.POST['repassword']:
			err["err-description"] += "Mật khẩu và mật khẩu nhập lại không khớp.<br>"
		username = req.POST['username']
		password = req.POST['password']
		email = req.POST['email']
		if len(password) < 8:
			err["err-description"] += "Mật khẩu chỉ được ít nhất 8 ký tự.<br>"
		for i in username:
			if len(username) < 4 or len(username) > 30:
				err["err-description"] += "Tên tài khoản phải có độ dài từ 4 tới 30 ký tự.<br>"
				break
			if i not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_':
				err["err-description"] += "Tên tài khoản không được bao gồm các ký tự đặc biệt ngoại trừ '_'.<br>"
		if err["err-description"]:
			return JsonResponse(err)

		try:
			if User.objects.filter(username__iexact=username).exists() or User.objects.filter(email__iexact=email).exists():
				raise Exception()
			user = User.objects.create_user(username, email, password)
			profile = Profile.objects.create(user=user, ratings=0.0)
			return JsonResponse({"done":"done"})
		except:
			err["err-description"] = "Tên tài khoản hoặc email đã được sử dụng.<br>"
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
			code = {
				"Grandmaster": "GM",
				'International Master': "IM",
				'National Master': "NM",
				"Master": "M",
				"Candidate Master": "CM"
			}
			return render(req, 'pages/profile/profile.html', {"usrprof": usrprof, "code": code})
		else:
			return render(req, 'pages/error/hao404.html', {"err_msg": f"Vị huynh đài đây đang tìm người tên là \"{qry}\" đúng không vậy ? Vị hảo hán đó tại hạ đây cũng chưa từng nghe tên."})
	else:
		raise Http404
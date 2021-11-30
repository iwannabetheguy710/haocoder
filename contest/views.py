from django.shortcuts import *
from django.http import *
from django.contrib.auth.models import *
from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError
from .models import *
from django.db.models import *
from django.views.decorators.csrf import csrf_exempt

def contest_page(req, id=None):
	user_registered = False
	if id is not None:
		contest = Contest.objects.filter(contest_id = id)
		if not contest.exists():
			return render(req, 'pages/error/hao404.html', {"err_msg": f"Có vẻ vị khách quan đang cố gắng truy cập vào kỳ thi bằng id {id} đúng không vậy hả ? Hiện tại kỳ thi này đã bị hủy hoặc bị ẩn đi rồi đó thưa khách quan."})
		contest = contest[0]
		if req.user.is_authenticated:
			user_registered = Leaderboard.objects.filter(profile__user__username=req.user.username, contest=contest).exists()
		return render(req, 'pages/contest/contest_detail.html', {"contest": contest, "user_registered": user_registered})
	contest = Contest.objects.filter(contest_status="RUNNING") | Contest.objects.filter(contest_status="SCHEDULE")
	contest = contest.order_by('-contest_created')
	return render(req, 'pages/contest/contest.html', {"contest": contest})

def contest_register_page(req, id):
	contest = Contest.objects.filter(contest_id=id)
	if contest.exists() and req.method == "POST" and req.user.is_authenticated:
		contest = contest[0]
		if contest.contest_status == "SCHEDULE":
			profile = Profile.objects.filter(user__username=req.user.username)[0]
			if not Leaderboard.objects.filter(profile=profile, contest=contest).exists():
				lb = Leaderboard.objects.create(profile=profile, contest=contest)
				lb.save()
				contest.contestant_count += 1
				contest.save()
			return JsonResponse({})
	raise Http404

def contest_unregister_page(req, id):
	contest = Contest.objects.filter(contest_id=id)
	if contest.exists() and req.method == "POST" and req.user.is_authenticated:
		contest = contest[0]
		if contest.contest_status == "SCHEDULE":
			profile = Profile.objects.filter(user__username=req.user.username)[0]
			lb = Leaderboard.objects.filter(profile=profile, contest=contest)[0]
			lb.delete()
			contest.contestant_count -= 1
			contest.save()
			return JsonResponse({})
	raise Http404

def contest_register_check_page(req, id):
	contest = Contest.objects.filter(contest_id=id)
	if contest.exists() and req.method == "POST" and req.user.is_authenticated:
		contest = contest[0]
		profile = Profile.objects.filter(user__username=req.user.username)[0]
		return JsonResponse({"joined": Leaderboard.objects.filter(contest=contest, profile=profile).exists()})
	raise Http404

def contest_leaderboard_page(req, id):
	contest = Contest.objects.filter(contest_id=id)
	if contest.exists() and req.method == "GET":
		contest = contest[0]
		lb = Leaderboard.objects.filter(contest=contest)
		code = {
			"Grandmaster": "GM",
			'International Master': "IM",
			'National Master': "NM",
			"Master": "M",
			"Candidate Master": "CM"
		}
		problem = Problem.objects.filter(contest=contest).order_by('contest_problem_id')
		return render(req, 'pages/contest/contest_leaderboard.html', {"leaderboard": lb, "contest": contest, "role_code": code, "problem": problem})
	raise Http404

def contest_problem_page(req, id, problem_id=None):
	contest = Contest.objects.filter(contest_id=id)
	lb = Leaderboard.objects.filter(profile__user__username=req.user.username)
	if not lb.exists():
		return render(req, "pages/error/hao404.html", {"err_msg": "Có vẻ vị sư huynh đây đang tính vào phần bài tập mà không cần tham gia kỳ thi đúng không vậy ? Tiếc là tại hạ không thể cho sư huynh vào được rồi !"})
	if contest.exists() and req.method == "GET":
		contest = contest[0]
		code = {
			"Grandmaster": "GM",
			'International Master': "IM",
			'National Master': "NM",
			"Master": "M",
			"Candidate Master": "CM"
		}
		problem = Problem.objects.filter(contest=contest).order_by('contest_problem_id')
		if problem_id is not None:
			problem = Problem.objects.filter(contest=contest, problem_id=problem_id)
			if problem.exists():
				problem = problem[0]
				problem.problem_memory_limit /= 1024
				problem.problem_sample_in = problem.problem_sample_in.split('\r\n\r\n')
				problem.problem_sample_out = problem.problem_sample_out.split('\r\n\r\n')
				for i in range(len(problem.problem_sample_in)):
					problem.problem_sample_in[i] = [problem.problem_sample_in[i], problem.problem_sample_out[i]]
				return render(req,'pages/contest/contest_detail_problem.html', {"contest": contest, "role_code": code, "problem": problem})
			else:
				raise Http404
		return render(req, 'pages/contest/contest_problem.html', {"contest": contest, "role_code": code, "problem": problem})
	raise Http404
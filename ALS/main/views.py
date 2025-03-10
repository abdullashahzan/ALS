from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
import os
import json, random, PyPDF2
from .ai import *
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.files.storage import default_storage
from django.conf import settings

def login_user(request):
    message = ""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.username == "user":
            	next_url = request.GET.get('next', 'web:admin_page')
            else:
	            next_url = request.GET.get('next', 'web:index')
            return redirect(next_url)
        else:
            get_user = User.objects.get(email=username)
            user = authenticate(username=get_user.username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'web:index')
                return redirect(next_url)
        message = "Invalid credentials"
    return render(request, "login.html", {"message": message})

def signup_user(request):
    message = ""
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        selected_courses = request.POST.getlist('courses')
        if email is not None and username is not None and password is not None and selected_courses is not None:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.email = email
                user.save()
                course = ', '.join(selected_courses)
                UserProfile(user=user, course=course).save()
                login(request, user)
                return redirect(reverse('web:index'))
            except IntegrityError:
                message = "Username or email is already taken"
            except:
                message = "Please make sure all the data is filled correctly"
        else:
            message = "Please fill all the fields"
    return render(request, "signup.html", {"message": message})

def logout_user(request):
    logout(request)
    return redirect('web:login_user')

@login_required
def admin_page(request):
	return render(request, "admin.html")

@login_required
def index(request):
	current_user = UserProfile.objects.get(user=request.user)
	user_history = UserHistory.objects.filter(username=request.user.username)
	weak_points = get_weak_points(user_history)
	current_user.needs_improvement = weak_points
	current_user.save()
	courses = current_user.course.split(",")
	return render(request, "index.html", {
		"current_user":current_user,
		"courses": courses,
		"weak_points": weak_points,
		"user_history": user_history		
		})

@login_required
def show_course(request, course_name):
	return render(request, "course.html", {
		"course": course_name
		})

@login_required
def upload_course_content(request, course_name):
	message = ""
	if request.method == "POST":
		if 'file' in request.FILES:
			uploaded_file = request.FILES['file']
			file_path = f"./main/course_content/{course_name}/{uploaded_file.name}"
			saved_path = default_storage.save(file_path, uploaded_file)
			with default_storage.open(saved_path, 'rb') as f:
				pdf_reader = PyPDF2.PdfReader(f)
				text = ""
				for page in pdf_reader.pages:
					text += page.extract_text()
			new_file_path = f"./main/course_content/{course_name}/{course_name}.txt"
			with open(new_file_path, 'a+') as file:
				file.write(text)
			os.remove(saved_path)
			message = "Content added successfully"

	return render(request, "course.html", {
		"course": course_name,
		"status": "admin",
		"message": message
		})

@login_required
def mock_exam(request, course_name):
	course_name = course_name.strip()
	message, question, weak_points, ai_response_for_user = "", "", "", ""
	if request.method == "POST":
		user_question = request.POST['user_question']
		user_answer = request.POST['user_answer']
		ai_response_for_user, weak_points = verify_answer(user_question, user_answer)
		# To check if answer is correct or incorrect
		check_ai_response = " ".join(ai_response_for_user.split(".")[:4])
		if "incorrect" in check_ai_response:
			message = "Wrong answer"
			correct = False
		else:
			message = "Correct answer"
			correct = True
		UserHistory(username=request.user.username, question=user_question, answer=user_answer, suggestion=ai_response_for_user, weak_points=weak_points, correct=correct).save()
	else:
		question = generate_question(course_name)
	return render(request, "mock_exam.html", {
		"course_name":course_name,
		"message": message,
		"question": question,
		"weak_points": weak_points,
		"ai_response": ai_response_for_user,
		})


@login_required
def show_mock_exam(request, question_id):
	question = UserHistory.objects.get(username=request.user.username, id=question_id)
	return render(request, "show_mock_exam.html", {
		"question":question
		})

@login_required
def adaptive_question_generator(request, course_name):
	current_user = UserProfile.objects.get(user=request.user)
	user_history = UserHistory.objects.filter(username=request.user.username)
	question = "The question was saved successfully!"
	if request.method == "POST":
		save_question = request.POST['save_question']
		current_user.saved_questions += f"--!-- {save_question}"
		current_user.save()
	else:
		weak_points = current_user.needs_improvement
		question = generate_practice_question(course_name, weak_points)
	return render(request, "practice_question.html", {
		"question": question,
		"course": course_name,
		})

@login_required
def saved_questions(request):
	current_user = UserProfile.objects.get(user=request.user)
	all_questions = current_user.saved_questions.split("--!-- ")
	return render(request, "practice_question.html", {
		"all_questions":all_questions
		})

def chat(request):
	return render(request, "chat.html")
from django.urls import path
from . import views

app_name = 'web'
urlpatterns = [
	path("login", views.login_user, name="login_user"),
    path("signup", views.signup_user, name="signup_user"),
    path("logout", views.logout_user, name="logout_user"),

	path("", views.index, name='index'),
	path("admin_page", views.admin_page, name="admin_page"),

	path("course/<str:course_name>", views.show_course, name='show_course'),
	path("mock_exam/<str:course_name>", views.mock_exam, name='mock_exam'),
	path("show_mock_exam/<str:question_id>", views.show_mock_exam, name='show_mock_exam'),
	path("generate_question/<str:course_name>", views.adaptive_question_generator, name='generate_question'),
	path("saved_questions/", views.saved_questions, name='saved_questions'),
	path("chat/", views.chat, name="chat"),

	path("upload_course_content/<str:course_name>", views.upload_course_content, name='upload_course_content'),
]

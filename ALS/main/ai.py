from groq import Groq
from django.conf import settings

api_key = "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"

client = Groq(
	    api_key=api_key,
	)

website_content = ""

# Create your views here.
def request_ai(content):
	chat_completion = client.chat.completions.create(
	    messages=[
	        {
	            "role": "user",
	            "content": content
			}
	    ],
	    model="llama-3.3-70b-versatile",
	)

	answer = chat_completion.choices[0].message.content
	return answer

def generate_question(course_name):
	try:
		with open(f"{settings.BASE_DIR}/main/course_content/{course_name}/{course_name}.txt", "r") as f:
			course_content = f.read()
		command = f"Generate a single question for {course_name} which has the following content {course_content}"
	except:
		command = f"Generate a question for {course_name}"
	rules = f"Here are the rules you must follow: Make sure not to generate any answer"
	content = f"{command} {rules}"
	return request_ai(content)

def verify_answer(question, user_answer):
	command = f"Is this answer {user_answer} correct for the question {question}"
	conditions = f"If yes then congratulate the user otherwise explain user why his answer is incorrect"
	rules = f"Here are some rules you must follow: Your first line should always be telling the user if his answer is correct or incorrect."
	content = f"{command} {rules} {conditions}"
	ai_answer = request_ai(content)
	command = f"Based on this response of yours {ai_answer}, what are the 3 main weak points of the user?"
	rules = f"Here are some rules you must follow: Your response should only contain weak points of the user seperated by comma and nothing else."
	content = f"{command} {rules}"
	weak_points = request_ai(content)
	return ai_answer, weak_points

def get_weak_points(user_model):
	weak_points = []
	for i in user_model:
		weak_points_history = i.weak_points.split(",")
		for j in weak_points_history:
			if j not in weak_points:
				weak_points.append(j)
	return weak_points

def generate_practice_question(course_name, weak_points):
	command = f"Generate a single question along with it's answer for the user based on {course_name}. keep in mind user's weak concepts {weak_points} and generate a question to help him strengthen his weak points."
	rules = f"Here are some rules you must follow: Your response should be friendly and helpful"
	content = f"{command} {rules}"
	return request_ai(content)	
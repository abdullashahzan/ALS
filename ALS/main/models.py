from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # User selected course
    course = models.CharField(max_length=256, default="")
    # User course completion progress
    progress = models.FloatField(default=0)
    # User suggestions for weak points
    needs_improvement = models.CharField(max_length=4000, default="")
    # User recent grades
    grades = models.CharField(max_length=4000, default="")
    # User predicted grades
    predicted_grades = models.FloatField(default=0)
    # Saved questions
    saved_questions = models.CharField(max_length=1000000, default="")

    def __str__(self):
        return f"{self.user.username}'s profile"

class UserHistory(models.Model):
	username = models.CharField(max_length=256, default="")
	question = models.CharField(max_length=10000, default="")
	answer = models.CharField(max_length=10000, default="")
	suggestion = models.CharField(max_length=10000, default="")
	weak_points = models.CharField(max_length=1000, default="")
	correct = models.BooleanField(default="False")

	def __str__(self):
		return f"{self.username}'s exam"


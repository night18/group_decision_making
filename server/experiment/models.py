from django.db import models
from django.db.models import JSONField

class Subject(models.Model):
	_id = models.AutoField(auto_created = True, primary_key=True)
	worker_id = models.CharField(max_length=60)
	qualification_assignment_id = models.CharField(max_length=60)
	qualification_hit_id = models.CharField(max_length=60)
	# qualification_task_submit_to = models.CharField(max_length=200)
	assignment_id = models.CharField(max_length=60)
	hit_id = models.CharField(max_length=60)
	# task_submit_to = models.CharField(max_length=200)
	group_id = models.IntegerField(default = -1)
	start_time = models.DateTimeField(default = None, blank=True, null = True)
	end_time = models.DateTimeField(default = None, blank=True, null = True)
	pair_start_time = models.DateTimeField(default = None, blank=True, null = True)
	pair_end_time = models.DateTimeField(default = None, blank=True, null = True)
	'''
	== Condition Setting == 
	0: no devil's advocate
	1: Static devil's advocate for AI
	2: Dynamic devil's advocate for AI
	3: Static devil's advocate for group
	4: Dynamic devil's advocate for group
	'''
	condition = models.IntegerField(default=-1)
	bonus = models.FloatField(default=0)
	is_qualified = models.BooleanField(default=False)
	is_complete = models.BooleanField(default=False)
	is_paid = models.BooleanField(default=False)
	is_interest = models.BooleanField(default=False)
	avatar_name = models.CharField(max_length=60, default = None, null = True)
	avatar_color = models.CharField(max_length=60, default = None, null = True)

	def __str__(self):
		return str(self._id)

class Defendant(models.Model):
	_id = models.AutoField(auto_created = True, primary_key=True)
	race = models.CharField(max_length = 20)
	sex = models.CharField(max_length = 20)
	age = models.IntegerField()
	prior = models.IntegerField()
	felony = models.IntegerField()
	misdemeanor = models.IntegerField()
	charge_degree = models.CharField(max_length = 100)
	charge_reason = models.CharField(max_length = 200)
	charge_explain = models.CharField(max_length = 200)
	model_suggestion = models.CharField(max_length=10)
	ground_truth = models.CharField(max_length=10)
	'''
	-2: Attention Check
	-1: Qualification
	0: Practice phase
	1: Caucasian + reoffend
	2: Caucasian + not reoffend
	3: Black + reoffend
	4: Black + not reoffend
	5: Paired
	'''
	condition = models.IntegerField()
	'''
	Condition 5:
		Same pair id are the same pair defendant
	Condition -1:
		The pair id represent the feature of the defendant
		1: White + High Degree + not reoffend
		2: Black + High Degree + not reoffend
		3: White + High Degree + reoffend
		4: Black + High Degree + reoffend
		5: White + Low Degree + not reoffend
		6: Black + Low Degree + not reoffend
		7: White + Low Degree + reoffend
		8: Black + Low Degree + reoffend
	'''
	pair = models.IntegerField()

	def __str__(self):
		return str(self._id)

class QualifiedRecord(models.Model):
	_id = models.AutoField(auto_created = True, primary_key=True)
	subject_id = models.IntegerField(default = None)
	instance_id = models.IntegerField(default = None)
	task_no = models.IntegerField(default = None)
	human_estimation = models.CharField(max_length=10)
	spend_time = models.FloatField(default = None)

	def __str__(self):
		return str(self._id)

class PracticeRecord(models.Model):
	_id = models.AutoField(auto_created = True, primary_key=True)
	subject_id = models.IntegerField(default = None)
	instance_id = models.IntegerField(default = None)
	task_no = models.IntegerField(default = None)
	initial_answer = models.CharField(max_length=10)
	final_answer = models.CharField(max_length=10)
	spend_time = models.FloatField(default = None)

	def __str__(self):
		return str(self._id)

class FormalRecord(models.Model):
	_id = models.AutoField(auto_created = True, primary_key=True)
	subject_id = models.IntegerField(default = None)
	instance_id = models.IntegerField(default = None)
	task_no = models.IntegerField(default = None)
	# if the subject is individual condition, group_id is -1.
	group_id = models.IntegerField(default = None)
	initial_answer = models.CharField(max_length=10)
	final_answer = models.CharField(max_length=10)
	spend_time = models.FloatField(default = None)

	def __str__(self):
		return str(self._id)

class FormalConfidence(models.Model):
	_id = models.AutoField(auto_created = True, primary_key = True)
	subject_id = models.IntegerField(default = None)
	instance_id = models.IntegerField(default = None)
	task_no = models.IntegerField(default = None)
	confidence = models.IntegerField(default = None)

	def __str__(self):
		return str(self._id)

class GroupAssign(models.Model):
	def memeber_default():
		return {"subject_ids": []}
		# {"subject_ids": []}

	_id = models.AutoField(auto_created = True, primary_key=True)
	size = models.IntegerField(default = 3)
	current_size = models.IntegerField(default = 0)
	is_activated = models.BooleanField(default = True)
	has_capacity = models.BooleanField(default = True)
	condition = models.IntegerField(default = -1)
	member_ids = JSONField(default = memeber_default)
	activate_member_ids = JSONField(default = memeber_default)


	def __str__(self):
		return str(self._id)

class DevilsRecord(models.Model):
	_id = models.AutoField(auto_created = True, primary_key=True)
	group_id = models.IntegerField(default = -1)
	task_no = models.IntegerField(default = None)
	advocate = models.IntegerField(default = -1)

	def __str__(self):
		return str(self._id)

class MessageRecord(models.Model):
	_id = models.AutoField(auto_created = True, primary_key = True)
	subject_id = models.IntegerField(default = None, null = True)
	group_id = models.IntegerField(default = None, null = True)
	instance_id = models.IntegerField(default = None, null = True)
	task_no = models.IntegerField(default = None, null = True)
	message = models.CharField(max_length= 2048, null = True)
	time_stamp = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return str(self._id)

class EstimationRecord(models.Model):
	_id = models.AutoField(auto_created = True, primary_key = True)
	subject_id = models.IntegerField(default = None)
	group_id = models.IntegerField(default = None)
	instance_id = models.IntegerField(default = None)
	task_no = models.IntegerField(default = None)
	estimation = models.CharField(max_length= 280)
	time_stamp = models.DateTimeField(auto_now_add=True, blank=True)

	def __str__(self):
		return str(self._id)

class UnderstandingSurvey(models.Model):
	_id = models.AutoField(auto_created = True, primary_key = True)
	subject_id = models.IntegerField(default = None)
	race = models.IntegerField(default = None)
	sex = models.IntegerField(default = None)
	age = models.IntegerField(default = None)
	prior = models.IntegerField(default = None)
	felony = models.IntegerField(default = None)
	misdemeanor = models.IntegerField(default = None)
	charge_degree = models.IntegerField(default = None)
	charge_issue = models.IntegerField(default = None)

	def __str__(self):
		return str(self._id)

class AccountabilitySurvey(models.Model):
	_id = models.AutoField(auto_created = True, primary_key = True)
	subject_id = models.IntegerField(default = None)
	instance_id = models.IntegerField(default = None)
	task_no = models.IntegerField(default = None)
	acc_me = models.IntegerField(default = None, null = True)
	acc_model = models.IntegerField(default = None, null = True)
	acc_teammates = models.IntegerField(default = None, null = True)

	def __str__(self):
		return str(self._id)


class PreSurvey(models.Model):
	_id = models.AutoField(auto_created=True, primary_key=True)
	subject_id = models.IntegerField(default = None)
	Q1 = models.CharField(max_length=1)
	Q2 = models.CharField(max_length=1)
	Q3 = models.CharField(max_length=1)
	Q4 = models.CharField(max_length=1)
	Q5 = models.CharField(max_length=1)

	def __str__(self):
		return str(self._id)
	
class PostSurvey(models.Model):
	_id = models.AutoField(auto_created=True, primary_key=True)
	subject_id = models.IntegerField(default = None)
	mental_demand = models.CharField(max_length=1)
	physical_demand = models.CharField(max_length=1)
	temporal_demand = models.CharField(max_length=1)
	performance = models.CharField(max_length=1)
	effort = models.CharField(max_length=1)
	frustration = models.CharField(max_length=1)
	timeline = models.CharField(max_length=1)
	precision = models.CharField(max_length=1)
	usefulness = models.CharField(max_length=1)
	da_collaboration = models.CharField(max_length=1)
	da_satisfaction = models.CharField(max_length=1)
	da_quality = models.CharField(max_length=1)
	da_recommend = models.CharField(max_length=1)
	da_future = models.CharField(max_length=1)

	def __str__(self):
		return str(self._id)
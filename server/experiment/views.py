from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .models import Subject, PracticeRecord, GroupAssign, FormalRecord, UnderstandingSurvey, Defendant, PreSurvey, QualifiedRecord, FormalConfidence, AccountabilitySurvey, MessageRecord, PostSurvey
from django.db.models import Count
from .serializers import DefendantModelSerializer, DefendantTruthModelSerializer, DefendantWOTruthModelSerializer
from datetime import datetime
import csv
from random import sample
import random
import json as JSON
from decimal import *
from .gpt import GPT
TEST_MODE = True
QUALIFY_CODE = "CXYJV2CI"
QUALIFY_FAILE_CODE = "C1GTI8NT"
SUCCESS_CODE = "CVGW5BEE"
FAILED_CODE = "C2ZILU9F"
TIMEOUT_CODE = "C3AXEIWP"
IDLE_CODE = "CTH566FU"

# Create your views here.
def home_view(request,*args, **kwargs):
	return HttpResponse("<h1>Hello World</h1>")


@api_view(['POST'])
def create_subject(request):
	worker_id = request.POST.get('worker_id', None)
	study_id = request.POST.get('study_id', None)
	session_id = request.POST.get('session_id', None)
	json = {}

	if worker_id != None:
		if len(Subject.objects.filter(worker_id = worker_id)) == 0:
			'''
			== Condition Setting == 
			0: no devil's advocate
			1: Fixed devil's advocate for AI
			2: Rotated devil's advocate for AI
			3: Fixed devil's advocate for group
			4: Rotated devil's advocate for group
			'''
			# condition = random.choice([0,1,2,3,4])

			sub = Subject.objects.create(worker_id=worker_id, assignment_id=study_id, hit_id=session_id, is_qualified=True)

			json = {
				"subject_id": sub._id,
				"success": True
			}
			return JsonResponse(json)

		else:
			json = {
				"success": False
			}
			return JsonResponse(json)
	raise PermissionDenied("Worker id is missing, please return the HIT before start")



@api_view(['POST'])
def pre_survey(request):
	json = {}
	subject_id = request.POST.get('subject_id', None)
	Q1 = request.POST.get('Q1', None)
	Q2 = request.POST.get('Q2', None)
	Q3 = request.POST.get('Q3', None)
	Q4 = request.POST.get('Q4', None)
	Q5 = request.POST.get('Q5', None)

	if subject_id != None:
		survey = PreSurvey.objects.create(
			subject_id = subject_id,
			Q1 = Q1,
			Q2 = Q2,
			Q3 = Q3,
			Q4 = Q4,
			Q5 = Q5
			)
	
	task_pool_1 = list(Defendant.objects.filter(condition = -1))
	task_pool_2 = list(Defendant.objects.filter(condition = -2))

	new_list = []

	for task in task_pool_1:
		task = DefendantModelSerializer(task)
		new_list.append(task.data)

	for task in task_pool_2:
		task = DefendantModelSerializer(task)
		new_list.append(task.data)

	random.shuffle(new_list)
	if TEST_MODE:
		new_list = random.sample(new_list, k=2)

	json = {
		"task_list" : new_list
	}
	return JsonResponse(json)

@api_view(['POST'])
def get_subject_info(request):
	worker_id = request.POST.get('worker_id', None)
	study_id = request.POST.get('study_id', None)
	session_id = request.POST.get('session_id', None)

	# print(worker_id)

	if worker_id != None:
		if len(Subject.objects.filter(worker_id = worker_id)) == 0:
			raise PermissionDenied("We could not find your information in the server, please make sure you have passed the qualification.")
		else:
			sub = Subject.objects.filter(worker_id = worker_id)[0]
			if sub.is_qualified == False:
				raise PermissionDenied("We could not find your information in the server, please make sure you have passed the qualification.")
			if sub.start_time != None:
				raise PermissionDenied("You can take this HIT only once.")

			sub.assignment_id = study_id
			sub.hit_id = session_id
			sub.start_time = datetime.now()

			sub.save()

			json = {
				"subject_id": sub._id,
				"success": True
			}
			return JsonResponse(json)
	raise PermissionDenied("We could not find your information in the server, please make sure you have passed the qualification.")


@api_view(['POST'])
def create_group_subject(request):
	worker_id = request.POST.get('worker_id', None)
	assignment_id = request.POST.get('assignment_id', None)
	hit_id = request.POST.get('hit_id', None)
	task_submit_to = request.POST.get('task_submit_to', None)
	condition = request.POST.get('condition', None)

	json = {}

	if worker_id != None:
		if len(Subject.objects.filter(worker_id = worker_id)) == 0:
			json = {
				"success": False
			}
		else:
			sub = Subject.objects.filter(worker_id = worker_id)[0]
			if sub.is_qualified == False:
				raise PermissionDenied("We could not find your information in the server, please make sure you have passed the qualification.")
			if sub.start_time != None:
				raise PermissionDenied("You can take this HIT only once.")

			sub.assignment_id = assignment_id
			sub.hit_id = hit_id
			sub.task_submit_to = task_submit_to
			sub.condition = int(condition)
			sub.start_time = datetime.now()

			sub.save()

			json = {
				"subject_id": sub._id,
				"condition": sub.condition,
				"success": True
			}
			return JsonResponse(json)
	raise PermissionDenied("We could not find your information in the server, please make sure you have passed the qualification.")

@api_view(['POST'])
def create_single_subject(request):
	worker_id = request.POST.get('worker_id', None)
	assignment_id = request.POST.get('assignment_id', None)
	hit_id = request.POST.get('hit_id', None)
	task_submit_to = request.POST.get('task_submit_to', None)

	json = {}

	if worker_id != None:
		if len(Subject.objects.filter(worker_id = worker_id)) == 0:
			json = {
				"success": False
			}
		else:
			sub = Subject.objects.filter(worker_id = worker_id)[0]
			if sub.is_qualified == False:
				raise PermissionDenied("You can take this HIT only once.")
			if sub.start_time != None:
				raise PermissionDenied("You can take this HIT only once.")

			sub.assignment_id = assignment_id
			sub.hit_id = hit_id
			sub.task_submit_to = task_submit_to
			sub.condition = 1
			sub.start_time = datetime.now()

			sub.save()

			json = {
				"subject_id": sub._id,
				"success": True
			}
			return JsonResponse(json)
	raise PermissionDenied("We could not find your information in the server, please make sure you have passed the qualification.")

@api_view(['POST'])
def create_without_AI_subject(request):
	worker_id = request.POST.get('worker_id', None)
	assignment_id = request.POST.get('assignment_id', None)
	hit_id = request.POST.get('hit_id', None)
	task_submit_to = request.POST.get('task_submit_to', None)


	json = {}

	if worker_id != None:
		if len(Subject.objects.filter(worker_id = worker_id)) == 0:
			# condition = random.choices([0,1], weights = (4,1), k = 1)[0]
			# Set it to 0 to increase the pairring rate
			condition = 2

			sub = Subject.objects.create(worker_id=worker_id, condition = condition, assignment_id=assignment_id, hit_id=hit_id, task_submit_to=task_submit_to)

			json = {
				"subject_id": sub._id,
				"condition": sub.condition,
				"success": True
			}
			return JsonResponse(json)

		else:
			raise PermissionDenied("You have worked on this HIT before, please return the HIT before start")
			
	raise PermissionDenied("Worker id is missing, please return the HIT before start")

@api_view(['POST'])
def unqualified(request):
	json = {}
	subject_id = request.POST.get('subject_id', None)
	subject = Subject.objects.get(pk = subject_id)
	subject.is_qualified = False
	subject.save()

	return JsonResponse(json)

@api_view(['GET'])
def import_defendant(request):
	json = {
			"status": "failed"
		}
	with open('defendant.csv') as f:
		reader = csv.reader(f)
		next(reader, None)
		for row in reader:
			_, created = Defendant.objects.get_or_create(
				race=row[1],
				sex=row[2],
				age=row[3],
				prior=row[4],
				felony=row[5],
				misdemeanor=row[6],
				charge_degree=row[7],
				charge_reason=row[8],
				charge_explain=row[9],
				model_suggestion=row[10],
				ground_truth=row[11],
				pair=row[12],
				condition=row[13]
				)
		json = {
			"status": "success"
		}
	return JsonResponse(json)


@api_view(['GET'])
def get_train(request):
	task_pool_1 = list(Defendant.objects.filter(condition = 0))
	task_pool_2 = list(Defendant.objects.filter(condition = -2))

	new_list = []

	for task in task_pool_1:
		task = DefendantModelSerializer(task)
		new_list.append(task.data)

	for task in task_pool_2:
		task = DefendantModelSerializer(task)
		new_list.append(task.data)

	random.shuffle(new_list)
	if TEST_MODE:
		new_list = random.sample(new_list, k=2)

	json = {
		"task_list" : new_list
	}
	return JsonResponse(json)

@api_view(['GET'])
def get_formal(request):
	sample_size = 1

	task_pool_1 = Defendant.objects.filter(condition = 1)
	task_pool_2 = Defendant.objects.filter(condition = 2)
	task_pool_3 = Defendant.objects.filter(condition = 3)
	task_pool_4 = Defendant.objects.filter(condition = 4)
	# task_pool_5 = Defendant.objects.filter(condition = 5)

	task_list_1 = sample(list(task_pool_1), sample_size)
	task_list_2 = sample(list(task_pool_2), sample_size)
	task_list_3 = sample(list(task_pool_3), sample_size)
	task_list_4 = sample(list(task_pool_4), sample_size)

	pair_id = random.randint(0, 4)

	# task_list_5 = list(task_pool_5.filter(pair = pair_id))

	new_list = []

	for task in task_list_1:
		task = DefendantWOTruthModelSerializer(task)
		new_list.append(task.data)

	for task in task_list_2:
		task = DefendantWOTruthModelSerializer(task)
		new_list.append(task.data)

	for task in task_list_3:
		task = DefendantWOTruthModelSerializer(task)
		new_list.append(task.data)

	for task in task_list_4:
		task = DefendantWOTruthModelSerializer(task)
		new_list.append(task.data)

	# for task in task_list_5:
	# 	task = DefendantWOTruthModelSerializer(task)
	# 	new_list.append(task.data)

	random.shuffle(new_list)
	if TEST_MODE:
		new_list = random.sample(new_list, k=2)

	json = {
		"task_list" : new_list
	}
	return JsonResponse(json)

@api_view(['POST'])
def formal_start(request):
	subject_id = request.POST.get('subject_id', None)
	if subject_id != None:
		sub = Subject.objects.get(pk=subject_id)
		sub.pair_end_time = datetime.now()
		sub.save()
	json = {
	}
	return JsonResponse(json)



@api_view(['POST'])
def record_qualified_task(request):

	json = {}
	subject_id = request.POST.get('subject_id', None)
	instance_id = request.POST.get('instance_id', None)
	task_no = request.POST.get('task_no', None)
	human_estimation = request.POST.get('human_estimation', None)
	if human_estimation == 'True':
		human_estimation == True
	elif human_estimation == 'False':
		human_estimation == False
	spend_time = request.POST.get('spend_time', None)

	if subject_id != None and instance_id != None and human_estimation != None:
		if len(QualifiedRecord.objects.filter(subject_id = subject_id).filter(instance_id = instance_id)) == 0:
			record = QualifiedRecord.objects.create(subject_id = subject_id, instance_id = instance_id, task_no = task_no, human_estimation = human_estimation, spend_time = spend_time)
		return JsonResponse(json)

	return JsonResponse(json, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def record_practice(request):

	json = {}
	subject_id = request.POST.get('subject_id', None)
	instance_id = request.POST.get('instance_id', None)
	task_no = request.POST.get('task_no', None)
	initial_answer = request.POST.get('initial_answer', None)
	final_answer = request.POST.get('final_answer', None)

	if initial_answer == 'True':
		initial_answer == True
	elif initial_answer == 'False':
		initial_answer == False

	if final_answer == 'True':
		final_answer == True
	elif final_answer == 'False':
		final_answer == False

	spend_time = request.POST.get('spend_time', None)

	if subject_id != None and instance_id != None and initial_answer != None and final_answer != None:
		if len(PracticeRecord.objects.filter(subject_id = subject_id).filter(instance_id = instance_id)) == 0:
			record = PracticeRecord.objects.create(
				subject_id = subject_id,
				instance_id = instance_id,
				task_no = task_no,
				initial_answer = initial_answer,
				final_answer = final_answer,
				spend_time = spend_time)
		return JsonResponse(json)

	return JsonResponse(json, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def record_avatar(request):

	json = {}
	subject_id = request.POST.get('subject_id', None)
	avatar_name = request.POST.get('avatar_name', None)
	avatar_color = request.POST.get('avatar_color', None)

	if subject_id != None and avatar_name != None and avatar_color != None:
		Subject.objects.filter(pk=subject_id).update(avatar_name=avatar_name, avatar_color=avatar_color)
		return JsonResponse(json)

	return JsonResponse(json, status=status.HTTP_400_BAD_REQUEST)


def get_average_waiting_time():
	subjects = Subject.objects.exclude(pair_start_time__isnull=True).exclude(pair_end_time__isnull=True)
	total_waiting_time = 0
	total_count = 0

	for sub in subjects:
		total_waiting_time += (sub.pair_end_time - sub.pair_start_time).total_seconds()
		total_count += 1

	if total_count == 0:
		return 180
	else:
		return total_waiting_time / total_count


@api_view(['POST'])
def pairing(request):
	json = {}
	subject_id = request.POST.get('subject_id', None)
	condition = int(request.POST.get('condition', -1))

	if subject_id != None:
		subject = Subject.objects.get(pk = subject_id)

		if condition != -1: # Internal Testing
			group = GroupAssign.objects.filter(is_activated = True, has_capacity = True, condition=condition).order_by('_id').first()
			if group == None:
				group = GroupAssign.objects.create(condition = condition)
			for member_id in group.member_ids['subject_ids']:
				member = Subject.objects.get(pk = member_id)
				if member.avatar_color + member.avatar_name == subject.avatar_color + subject.avatar_name:
					group = GroupAssign.objects.create(condition = condition)
					break

		elif subject.group_id != -1: # Have assigned
			group = GroupAssign.objects.get(pk = subject.group_id)
		else: # Havn't assigned any group (common situation)
			group = GroupAssign.objects.filter(is_activated = True).filter(has_capacity = True).order_by('_id').first()

			if group == None:
				'''
				== Condition Setting == 
				0: no devil's advocate
				1: Fixed devil's advocate for AI
				2: Rotated devil's advocate for AI
				3: Fixed devil's advocate for group
				4: Rotated devil's advocate for group
				'''
				condition = random.choices([0,1,2,3,4], weights=[0.1, 0.1, 0.1, 0.35, 0.35], k = 1)[0]
				group = GroupAssign.objects.create(condition = condition)

			for member_id in group.member_ids['subject_ids']:
				member = Subject.objects.get(pk = member_id)
				if member.avatar_color + member.avatar_name == subject.avatar_color + subject.avatar_name:
					condition = random.choices([0,1,2,3,4], weights=[0.1, 0.1, 0.1, 0.35, 0.35], k = 1)[0]
					group = GroupAssign.objects.create(condition = condition)
					break

		group.current_size += 1
		# if group.current_size == group.size:
		# 	group.has_capacity = False
		group.member_ids['subject_ids'].append(int(subject_id))
		group.save()

		subject.group_id = group._id
		subject.condition = group.condition
		subject.save()
		# print(type(group.condition))
		json = {
			'group_id': group._id,
			'group_capacity': group.size,
			'condition': group.condition,
			'average_waiting_time': get_average_waiting_time()
		}
		return JsonResponse(json)
	return JsonResponse(json, status=status.HTTP_400_BAD_REQUEST)		


@api_view(['POST'])
def record_single_formal(request):
	# Only for individual users
	json = {}
	subject_id = request.POST.get('subject_id', None)
	instance_id = request.POST.get('instance_id', None)
	task_no = request.POST.get('task_no', None)
	group_id = request.POST.get('group_id', -1)
	human_estimation = request.POST.get('human_estimation', None)
	if human_estimation == 'True':
		human_estimation == True
	elif human_estimation == 'False':
		human_estimation == False
	spend_time = request.POST.get('spend_time', None)

	if subject_id != None and instance_id != None and human_estimation != None:
		if len(FormalRecord.objects.filter(subject_id = subject_id).filter(instance_id = instance_id)) == 0:
			record = FormalRecord.objects.create(subject_id = subject_id, instance_id = instance_id, task_no = task_no, group_id = group_id, human_estimation = human_estimation, spend_time = spend_time)
		return JsonResponse(json)

	return JsonResponse(json, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def record_single_confidence(request):
	json = {}
	subject_id = request.POST.get('subject_id', None)
	instance_id = request.POST.get('instance_id', None)
	task_no = request.POST.get('task_no', None)
	confidence = request.POST.get('confidence', None)

	if subject_id != None and instance_id != None and confidence != None:
		record = FormalConfidence.objects.create(subject_id = subject_id, instance_id = instance_id, task_no = task_no, confidence = confidence)

		return JsonResponse(json)
	return JsonResponse(json, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_correct_answer(request):
	json = {}
	instance_ids = request.POST.get('instance_ids', None)

	if instance_ids == None:
		return JsonResponse(json, status=status.HTTP_400_BAD_REQUEST)

	instance_list = list(map(int,instance_ids.split(',')))

	new_list = []
	for ids in instance_list:
		dfd = Defendant.objects.get(pk = ids)
		new_list.append(DefendantTruthModelSerializer(dfd).data)

	json = {
		"task_list" : new_list
	}
	return JsonResponse(json)

def response_to_int(survey_response):
	if survey_response == 'null':
		return None
	else:
		return int(float(survey_response))

@api_view(['POST'])
def understanding_survey(request):
	subject_id = request.POST.get('subject_id', None)
	race = request.POST.get('race', None)
	sex = request.POST.get('sex', None)
	age = request.POST.get('age', None)
	prior = request.POST.get('prior', None)
	felony = request.POST.get('felony', None)
	misdemeanor = request.POST.get('misdemeanor', None)
	charge_degree = request.POST.get('charge_degree', None)
	charge_issue = request.POST.get('charge_issue', None)

	if subject_id != None:
		UnderstandingSurvey.objects.create(
			subject_id = subject_id,
			race = race,
			sex = sex,
			age = age,
			prior = prior,
			felony = felony,
			misdemeanor = misdemeanor,
			charge_degree = charge_degree,
			charge_issue = charge_issue
			)
		return JsonResponse({})
	return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def accountability_survey(request):
	subject_id = request.POST.get('subject_id', None)
	instance_id = request.POST.get('instance_id', None)
	task_no = request.POST.get('task_no', None)
	acc_me = request.POST.get('me', None)
	acc_model = request.POST.get('the_model', None)
	acc_teammates = request.POST.get('my_teammates', None)

	if subject_id != None:
		AccountabilitySurvey.objects.create(
			subject_id = subject_id,
			instance_id = instance_id,
			task_no = task_no,
			acc_me = response_to_int(acc_me),
			acc_model = response_to_int(acc_model),
			acc_teammates = response_to_int(acc_teammates)
			)

		return JsonResponse({})

	return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def post_survey(request):
	json = {}
	subject_id = request.POST.get('subject_id', None)
	mental_demand = request.POST.get('mental_demand', "")
	physical_demand = request.POST.get('physical_demand', "")
	temporal_demand = request.POST.get('temporal_demand', "")
	performance = request.POST.get('performance', "")
	effort = request.POST.get('effort', "")
	frustration = request.POST.get('frustration', "")
	timeline = request.POST.get('timeline', "")
	precision = request.POST.get('precision', "")
	usefulness = request.POST.get('usefulness', "")
	da_collaboration = request.POST.get('da_collaboration', "")
	da_satisfaction = request.POST.get('da_satisfaction', "")
	da_quality = request.POST.get('da_quality', "")
	da_recommend = request.POST.get('da_recommend', "")
	da_future = request.POST.get('da_future', "")

	if subject_id != None:
		survey = PostSurvey.objects.create(
			subject_id = subject_id,
			mental_demand = mental_demand,
			physical_demand = physical_demand,
			temporal_demand = temporal_demand,
			performance = performance,
			effort = effort,
			frustration = frustration,
			timeline = timeline,
			precision = precision,
			usefulness = usefulness,
			da_collaboration = da_collaboration,
			da_satisfaction = da_satisfaction,
			da_quality = da_quality,
			da_recommend = da_recommend,
			da_future = da_future
			)
		return JsonResponse(json)
	return JsonResponse(json, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def show_bonus(request):
	getcontext().prec = 3
	json = {}

	subject_id = request.POST.get('subject_id', None)
	if subject_id != None:
		subject = Subject.objects.get(pk=subject_id)
		detail = []
		total_bonus = 0

		pair_start_time = subject.pair_start_time 
		pair_end_time = subject.pair_end_time
		if pair_end_time:
			waiting_time_in_seconds = (pair_end_time - pair_start_time).total_seconds()
		else:
			waiting_time_in_seconds = 300
		waiting_time_in_minutes = Decimal(round( (waiting_time_in_seconds / 60), 0 ))

		answer_count = FormalRecord.objects.filter(subject_id = subject_id).count()
		if answer_count != 0:
			completed_task_count = FormalRecord.objects.filter(group_id = subject.group_id).order_by('-task_no').values('task_no').first()['task_no']
		# print(completed_task_count)
		# formal_tasks = FormalRecord.objects.filter(group_id = subject.group_id).order_by('task_no')
			
			for task_no in range(0, completed_task_count + 1):
				
				num_reoffend = 0
				formal_records = FormalRecord.objects.filter(group_id=subject.group_id, task_no=task_no)
				for record in formal_records:
					if record.final_answer == 'True':
						num_reoffend += 1
					else:
						num_reoffend -= 1

				if num_reoffend > 0:
					most_frequent_answer = 'True'
				elif num_reoffend < 0:
					most_frequent_answer = 'False'
				else:
					most_frequent_answer = 'Tie'

				# most_frequent_answer = FormalRecord.objects.filter(group_id=subject.group_id, task_no=task_no).values('final_answer').annotate(count=Count('final_answer')).order_by('-count').first()['final_answer']
				instance_id = FormalRecord.objects.filter(group_id = subject.group_id, task_no=task_no).values('instance_id').first()['instance_id']
				answer = Defendant.objects.get(pk=instance_id).ground_truth
				local_bonus = Decimal('0')
				if most_frequent_answer == answer:
					local_bonus = Decimal('0.4')
				data = {
					"task": int(task_no + 1),
					"user_prediction": most_frequent_answer,
					"ground_truth": answer,
					"bonus": local_bonus
				}
				total_bonus += local_bonus
				detail.append(data)

		waiting_bonus = Decimal('0.15') * waiting_time_in_minutes
		
		total_bonus +=  waiting_bonus
		total_bonus = Decimal(total_bonus)

		subject.bonus = total_bonus
		subject.save()
		json = {
			"detail": detail,
			"total_bonus": total_bonus,
			"waiting_time": waiting_time_in_seconds,
			"waiting_bonus": waiting_bonus
		}
		
		return JsonResponse(json)

@api_view(['POST'])
def complete_qualification(request):
	json = {}
	subject_id = request.POST.get('subject_id', None)
	is_interest = request.POST.get('is_interest', None)
	
	if is_interest == 'True':
		is_interest == True
	else:
		is_interest == False

	if subject_id != None:
		subject = Subject.objects.get(pk = subject_id)
		subject.is_qualified = True
		subject.is_interest = is_interest
		subject.save()

		# mturk_url = ""
		# if "workersandbox" in subject.qualification_task_submit_to:
		# 	mturk_url = "https://workersandbox.mturk.com/mturk/externalSubmit?assignmentId="
		# else:
		# 	mturk_url = "https://www.mturk.com/mturk/externalSubmit?assignmentId="

		# mturk_url = mturk_url + subject.qualification_assignment_id + "&Finished=Submit"
		
		code = QUALIFY_CODE
		prolific_url = "https://app.prolific.co/submissions/complete?cc={code}".format(code=code)
		
		json = {
			"mturk_url" : prolific_url
		}

		return JsonResponse(json)
	raise PermissionDenied("Subject id is missing, please contact the requester.")

@api_view(['POST'])
def failed_qualification(request):
	json = {}
	subject_id = request.POST.get('subject_id', None)

	if subject_id != None:
		subject = Subject.objects.get(pk = subject_id)
		subject.is_qualified = False
		subject.save()

		code = QUALIFY_FAILE_CODE
		prolific_url = "https://app.prolific.co/submissions/complete?cc={code}".format(code=code)
		
		json = {
			"mturk_url" : prolific_url
		}

		return JsonResponse(json)
	raise PermissionDenied("Subject id is missing, please contact the requester.")

@api_view(['POST'])
def submit_to_mtruk(request):
	json = {}
	subject_id = request.POST.get('subject_id', None)
	status = request.POST.get('status', None)
	if subject_id != None:
		subject = Subject.objects.get(pk=subject_id)
		# mturk_url = ""
		# if "workersandbox" in subject.task_submit_to:
		# 	mturk_url = "https://workersandbox.mturk.com/mturk/externalSubmit?assignmentId="
		# else:
		# 	mturk_url = "https://www.mturk.com/mturk/externalSubmit?assignmentId="
		# mturk_url = mturk_url + subject.assignment_id + "&Finished=Submit"
		# print(status)
		if status == 'success':
			code = SUCCESS_CODE
			subject.is_complete = True
		elif status == 'timeout':
			code = TIMEOUT_CODE
			subject.is_complete = True
		elif status == 'idle':
			code = IDLE_CODE
		else:
			code = FAILED_CODE
			subject.is_complete = True
			subject.is_qualified = False


		prolific_url = "https://app.prolific.co/submissions/complete?cc={code}".format(code=code)
		
		subject.end_time = datetime.now()
		subject.save()
		
		json = {
			"mturk_url" : prolific_url
		}
		return JsonResponse(json)
	raise PermissionDenied("Subject id is missing, please contact the requester.")


@api_view(['POST'])
def get_gpt_response(request):
	json = {}

	subject_id = request.POST.get('subject_id', None)
	group_id = request.POST.get('group_id', None)
	instance_id =  request.POST.get('instance_id', None)
	task_no = request.POST.get('task_no', None)
	messagesData = request.POST.get('messages', None)
	initial_prediction = request.POST.get('initial_prediction', None)
	condition = request.POST.get('condition', None)

	task = Defendant.objects.get(pk=instance_id)
	task = DefendantWOTruthModelSerializer(task).data

	if messagesData:
		messages = JSON.loads(messagesData)
	else:
		messages = None
	try:
		gpt_service = GPT(task, int(condition), messages=messages, initial_prediction=initial_prediction)
		gpt_response = gpt_service.get_response()
		# print(gpt_response)
		json = {
			"content": gpt_response
		}
	except Exception as e:
		print(e)
		json = {
			"content": "..."
		}
	return JsonResponse(json)
	
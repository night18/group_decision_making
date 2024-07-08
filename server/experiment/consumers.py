import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Subject, PracticeRecord, GroupAssign, MessageRecord, EstimationRecord, FormalRecord, Defendant, FormalConfidence, DevilsRecord
from .serializers import DefendantWOTruthModelSerializer
from random import sample
import random
from datetime import datetime

TEST_MODE = True 

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.channel_map = {}

        print("Successfully connect chat consumer")
        # Join the room channel
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )
        print("Successfully add to group")
        
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        
        # Check when do they leave the room
        # case 1: leave when pairing, code: 931
        # case 2: leave when formal task, code: 901
        # case 3: leave after completing all task, code: 4000
        print(close_code)
        group = GroupAssign.objects.get(pk = self.room_name)

        if close_code == 4000:
            group.is_activated = False
            group.save()

        subject_id = int(self.channel_map[self.channel_name])
        
        if group.has_capacity == True: # leave when pairing
            group.activate_member_ids['subject_ids'].remove(subject_id)
            group.member_ids['subject_ids'].remove(subject_id)
            group.current_size = group.current_size - 1
            response = {
                "code": 931,
                "leaving_subject": self.channel_map[self.channel_name]
            }
        else: #leave when formal task
            group.activate_member_ids['subject_ids'].remove(self.channel_map[self.channel_name])
            response = {
                "code": 901,
                "leaving_subject": self.channel_map[self.channel_name]
            }
        
        group.save()
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'chat_message',
                'message': response
            }
        )
        

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        code = text_data_json['code']
        print(text_data_json)
        response = self.chat_code_to_message(text_data_json['code'], text_data_json['data'])
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'chat_message',
                'message': response
            }
        )

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    def chat_code_to_message(self, code, data):
        # Enter room
        if code == 100:
            sample_size = 2

            self.channel_map[self.channel_name] = data['subject_id']

            group = GroupAssign.objects.get(pk = self.room_name)
            if int(data['subject_id']) not in group.activate_member_ids['subject_ids']:
                group.activate_member_ids['subject_ids'].append(data['subject_id'])

            user_list = []
            for s_id in group.activate_member_ids['subject_ids']:
                subject = Subject.objects.get(pk = s_id)
                user_list.append({
                    "subject_id": s_id,
                    "avatar_name": subject.avatar_name,
                    "avatar_color": subject.avatar_color,
                    "is_activated": 1,
                    "is_initial": 0,
                    "is_final": 0,
                    "is_ready_vote": 0,
                    "is_confirm": 0,
                    "is_answer_confidence": 0,
                    "is_finish": 0
                })

            startable = 0
            new_list = []

            subject = Subject.objects.get(pk = int(data['subject_id']))
            subject.pair_start_time = datetime.now()
            subject.save()

            if len(group.member_ids['subject_ids']) >= group.size:
                group.has_capacity = False
                startable = 1
                
                sub = Subject.objects.get(pk = int(data['subject_id']))
                sub.pair_end_time = datetime.now()
                sub.save()

                task_pool_1 = Defendant.objects.filter(condition = 1)
                task_pool_2 = Defendant.objects.filter(condition = 2)
                task_pool_3 = Defendant.objects.filter(condition = 3)
                task_pool_4 = Defendant.objects.filter(condition = 4)

                task_list_1 = sample(list(task_pool_1), sample_size)
                task_list_2 = sample(list(task_pool_2), sample_size)
                task_list_3 = sample(list(task_pool_3), sample_size)
                task_list_4 = sample(list(task_pool_4), sample_size)

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

                random.shuffle(new_list)
                if TEST_MODE:
                    new_list = random.sample(new_list, k=2)
            group.save()

            response = {
                "code": 101,
                "user_list": user_list,
                "startable": startable,
                "task_list" : new_list
            }

        elif code == 200: #Send message
            subject_id = data['subject_id']
            group_id = data['group_id']
            instance_id = data['instance_id']
            task_no = data['task_no']
            msg = data['msg']

            message_record = MessageRecord.objects.create(subject_id=subject_id, group_id=group_id, instance_id=instance_id, task_no=task_no, message=msg)

            response = {
                "code": 201,
                "message": {
                    "id": message_record._id,
                    "sender": {
                        "subject_id": subject_id
                    },
                    "content": msg,
                    "timestamp": str(message_record.time_stamp)
                }
            }
        elif code == 300: #Change radio selection
            subject_id = data['subject_id']
            group_id = data['group_id']
            instance_id = data['instance_id']
            task_no = data['task_no']
            estimation = data['final_answer']

            estimate_record = EstimationRecord.objects.create(subject_id=subject_id, group_id=group_id, instance_id=instance_id, task_no=task_no, estimation=estimation)            
            group = GroupAssign.objects.get(pk = self.room_name)
            group.confirm_count = 0
            group.save()

            response = {
                "code": 301,
                "estimation": {
                    "id": estimate_record._id,
                    "sender": {
                        "subject_id": subject_id
                    },
                    "estimation": estimation
                }
            }
        elif code == 350: #Initial answer completed
            subject_id = data['subject_id']
            group_id = data['group_id']
            instance_id = data['instance_id']
            task_no = data['task_no']
            initial_answer = data['initial_answer']

            response = {
                "code": 351,
                "answer": {
                    "sender": {
                        "subject_id": subject_id
                    },
                    "initial": initial_answer
                }
                
            }

        elif code == 380: # Ready to Vote
            subject_id = data['subject_id']
            group_id = data['group_id']
            instance_id = data['instance_id']
            task_no = data['task_no']

            group = GroupAssign.objects.get(pk = self.room_name)
            
            response = {
                "code": 381,
                "sender": {
                    "subject_id": subject_id
                }
            }

        elif code == 390: # Confirm consensus
            subject_id = data['subject_id']
            group_id = data['group_id']
            instance_id = data['instance_id']
            task_no = data['task_no']

            group = GroupAssign.objects.get(pk = self.room_name)
            
            response = {
                "code": 392,
                "sender": {
                    "subject_id": subject_id
                }
            }

        elif code == 400: # final vote
            subject_id = data['subject_id']
            group_id = data['group_id']
            instance_id = data['instance_id']
            task_no = data['task_no']
            initial_answer = data['initial_answer']
            final_answer = data['final_answer']
            spend_time = data['spend_time']

            response = {
                "code": 401,
                "answer": {
                    "sender": {
                        "subject_id": subject_id
                    },
                    "initial": initial_answer,
                    "final": final_answer
                }
            }

            if initial_answer == 'True':
                initial_answer == True
            elif initial_answer == 'False':
                initial_answer == False

            if final_answer == 'True':
                final_answer == True
            elif final_answer == 'False':
                final_answer == False


            # Record the individual activated subject's record
            group = GroupAssign.objects.get(pk = self.room_name)

            if subject_id != None and instance_id != None and initial_answer != None and final_answer != None:
                record = FormalRecord.objects.create(
                    subject_id = subject_id,
                    instance_id = instance_id, 
                    task_no = task_no, 
                    group_id = group_id, 
                    initial_answer = initial_answer, 
                    final_answer = final_answer, 
                    spend_time = spend_time
                )


        elif code == 500: #Formal Tasks consensus
            subject_id = data['subject_id']
            instance_id = data['instance_id']
            task_no = data['task_no']
            confidence = data['confidence']

            confidence_record = FormalConfidence.objects.create(subject_id = subject_id, instance_id = instance_id, task_no = task_no, confidence = confidence)

            # Check Whether all answer the question
            group = GroupAssign.objects.get(pk = self.room_name)
            response = {
                "code": 502,
                "sender": {
                    "subject_id": subject_id
                }
            }

        elif code == 666: #Request Devil's advocate
            task_no = data['task_no']


            group = GroupAssign.objects.get(pk = self.room_name)
            condition = group.condition
            if len(DevilsRecord.objects.filter(group_id = self.room_name, task_no = task_no)) == 0:
                if condition == 0:
                    devil = -1
                elif condition == 1 or condition == 3:
                    devil = min(group.activate_member_ids['subject_ids'])
                elif condition == 2 or condition == 4:
                    devil = random.sample(group.activate_member_ids['subject_ids'], k=1)[0]
                else:
                    devil = -1

                DevilsRecord.objects.create(group_id=group._id, task_no=task_no, advocate=devil)
            else:
                devil = DevilsRecord.objects.filter(group_id = self.room_name, task_no = task_no)[0].advocate

            response = {
                "code": 667,
                "devil": devil
            }
        elif code == 777: # Devil's advocate
            subject_id = -1
            group_id = data['group_id']
            instance_id = data['instance_id']
            task_no = data['task_no']
            msg = data['msg']

            message_record = MessageRecord.objects.create(subject_id=subject_id, group_id=group_id, instance_id=instance_id, task_no=task_no, message=msg)

            response = {
                "code": 778,
                "message": {
                    "id": message_record._id,
                    "sender": {
                        "subject_id": subject_id
                    },
                    "content": msg,
                    "timestamp": str(message_record.time_stamp)
                }
            }
        elif code == 888: # Click OK on the final dialog of each task
            subject_id = data['subject_id']

            response = {
                "code": 888,
                "sender": {
                    "subject_id": subject_id
                }
            }

        return response




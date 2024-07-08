import openai

class GPT:
    '''
	== Condition Setting == 
	0: no devil's advocate
	1: Static devil's advocate for AI
	2: Dynamic devil's advocate for AI
	3: Static devil's advocate for group
	4: Dynamic devil's advocate for group
	'''
    
    def __init__(self, task, condition, messages = None, initial_prediction = None):
        self.task = task
        self.condition = int(condition)
        self.messages = messages
        self.initial_prediction = initial_prediction
        self.token = 40

    def get_system_message(self):
        if self.condition == 1:
            system_message = '''You have to help the jury member rethink the correctness of the suggestion from RiskComp based on the its suggestion and the defendant infomation.

RiskComp is a machine learning model that provides suggestions to the jury member about whether a defendant will reoffend the law within 2 years.

The judge will provide the defendant information and the prediction from RiskComp. But the judge would not respond any question.

Please directly list the 3 short (less than 20 words) critique questions in bullet point format, such as,
'
Critiques:
- Reason 1
'
'''
        elif self.condition == 2:
            system_message = '''You are an assistant that helps the jury member rethink the correctness of the RiskComp's suggestion through Socratic questioning.

RiskComp is a machine learning model that provides suggestions to the jury member about whether a defendant will reoffend the law within 2 years.

The judge will provide the defendant information and the prediction from RiskComp. But the judge would not repond any question. Only the Jury will discuss with you.

Notice that you are an assistant not a jury member. Do not pretend you are jury member.

There are multiple members in the conversation, and they have their uiqnue number as "jury mmber + number". Please notice unique number to load their previous discussion content.

Please say "..." when the jury member's deicsion content is less likely to follow from the RISKComp's suggestions.

Please provide one or two sentences as in a human dialogue and do not repeat your insight. Your return should be in the format of "assistant: ...".'''

        elif self.condition == 3:
            system_message = '''You have to help the jury member rethink the correctness of their initial decision based on the decision and the defendant infomation.

The judge will provide the defendant information and the initial decision from jurt. But the judge would not respond any question.

Please directly list the 3 short (less than 20 words) critique questions in bullet point format, such as,
'
Critiques:
- Reason 1
            '
            '''
        elif self.condition == 4:
            system_message = '''You are an assistant that helps the jury member rethink the correctness of their initial decision.

The judge will provide the defendant information and the prediction from RiskComp. But the judge would not repond any question. Only the Jury will discuss with you.

Notice that you are an assistant not a jury member. Do not pretend you are jury member.

There are multiple members in the conversation, and they have their uiqnue number as "jury mmber + number". Please notice unique number to load their previous discussion content.

Please say "..." when the jury member's deicsion content is less likely to follow from the RISKComp's suggestions.

Please provide one or two sentences as in a human dialogue and do not repeat your insight.Your return should be in the format of "assistant: ...".'''
        else:
            return ""
        return system_message

    def get_judge_message(self):
        if self.condition == 1 or self.condition == 2:
            judge_message = '''A {age}-year-old {sex} {race} defendant has been charged with {charge_reason} as a {charge_degree}.  Specifically, {charge_reason} means {charge_explain}. The defendant has {prior} prior criminal count. The defendant made {misdemeanor} misdemeanors and {felony} felonies before 18.

            RiskComp predicts the defendant will {prediction} reoffend the law within 2 years.'''
        elif self.condition == 3 or self.condition == 4:
            judge_message = '''A {age}-year-old {sex} {race} defendant has been charged with {charge_reason} as a {charge_degree}.  Specifically, {charge_reason} means {charge_explain}. The defendant has {prior} prior criminal count. The defendant made {misdemeanor} misdemeanors and {felony} felonies before 18.

            Jury initial determined the defendant will {prediction} reoffend the law within 2 years.
            '''
        else:
            return ""
        
        if self.task['model_suggestion'] == 'True':
            model_suggestion = ''
        else:
            model_suggestion = 'not'
        if self.initial_prediction  == 'true':
            init_prediction = ''
        else:
            init_prediction = 'not'

        prediction = model_suggestion if self.condition == 1 or self.condition == 2 else init_prediction

        judge_message = judge_message.format(
            age = self.task['age'],
            sex = self.task['sex'],
            race = self.task['race'],
            charge_reason = self.task['charge_reason'].lower(),
            charge_degree = self.task['charge_degree'].lower(),
            charge_explain = self.task['charge_explain'].lower(),
            prior = self.task['prior'],
            misdemeanor = self.task['misdemeanor'],
            felony = self.task['felony'],
            prediction = prediction
        )

        return judge_message
    
    
    def static_devil_advocate(self):
        # Maybe we should keep it in the database to save money
        static = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content":  self.get_system_message()},
                    {"role": "user", "content": "Judge:" + self.get_judge_message()},
                ],
            temperature = 1
            )
        response = static.choices[0].message.content
        # print(response)
        return response.rsplit(":")[1]
   
    def sentenceType(self, content):
        type_message = '''
Please distinguish the content is ["statement"/"question"/"unrelated"] of a prediction task that whether a defendant would reoffend the law within two years.
Here are the explanation of each type:
statement: Statements related to the defendant's demographic, criminal history, crime sentence.
question: Questions to ask other's opinion.
Please provide the type without any reason or punctuation mark.'''
        messages = [
            {"role": "system", "content": type_message},
            {"role": "user", "content": content}
            ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature = 1
            )

        return response.choices[0].message.content.lower().strip()

    def statementType(self, content):
        type_message = '''The statement after ### is from part of the dialogue between the jury members discussed about whether a defendant will reoffend the law.
Please distinguish whether the statement is on the side of that a defendant will reoffend the law.
Please provide [true/false] without any reason or punctuation mark.
true means that he speakers have greater chance to consider the defendant will roffend the law rather than will not reoffend the law.
false means that the speakers have greater chance to consider the defendant will not roffend the law rather than will reoffend the law.
        ###
        {content}\n
        '''
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=type_message.format(content=content),
        max_tokens=10,
        temperature=1
        )

        return response.choices[0].text.lower().strip()

    
    def dynamic_devil_advocate(self):
        if self.messages == None:
            return '...'
        
        messages = [
            {"role": "system", "content": self.get_system_message()},
            {"role": "user", "content": "Judge:" + self.get_judge_message()},
            {"role": "assistant", "content": "..."}
            ]

        # print(self.messages[-1]['content'])
        sent_type = self.sentenceType(self.messages[-1]['content'])
        # print(sent_type)
        if sent_type == 'statement':
            statement_type = self.statementType(self.messages[-1]['content'])
            target_pred = self.task['model_suggestion'] if self.condition == 1 or self.condition == 2 else self.initial_prediction
            # print(target_pred)
            # print(statement_type)
            target_pred = str(target_pred).lower()
            if statement_type == target_pred:               
                for disc in self.messages:
                    content = 'jury member {subject_id}: {content}'.format(
                        subject_id = disc['sender']['subject_id'], 
                        content = disc['content']
                        )
                    messages.append({"role": "user", "content": content})

                # print(messages)
                dynamic = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature = 1
                    )
                gpt_response = dynamic.choices[0].message.content.rsplit(':')[1]
                return gpt_response
        return '...'


    def get_response(self):
        if self.condition == 0:
            return ""
        elif self.condition == 1:
            return self.static_devil_advocate()
        elif self.condition == 2:
            return self.dynamic_devil_advocate()
        elif self.condition == 3:
            return self.static_devil_advocate()
        elif self.condition == 4:
            return self.dynamic_devil_advocate()
        else:
            return ""
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
            system_message = '''
Help the jury member critique the suggestion from RiskComp based on its prediction and the defendant's information.
- You will receive information about the defendant and RiskComp's prediction.
- Formulate critique questions to help reconsider the validity of the prediction.
- Ensure questions focus on evaluating the suggestion's accuracy and fairness without needing further input from the judge.

# Steps
1. Review the defendant's information and RiskComp prediction.
2. Formulate three short critique questions targeting potential weaknesses or oversights in the prediction.
3. Limit each question to under 20 words.

# Output Format
- Provide the critique questions in bullet point format, labeled as "Critiques."

# Examples
Critiques:
- Does the prediction consider recent behavioral changes?
- Is the model biased against similar past cases?
- Are all relevant socio-economic factors considered?

# Notes
- The judge will not respond to any further queries for clarification.
- Keep the critique questions concise (less than 20 words) and relevant to the decision made.'''
        elif self.condition == 2:
            system_message = '''
Assist the jury member in questioning the validity of RiskComp's suggestion using Socratic questioning.

The judge provides the defendant's information and RiskComp's prediction. RiskComp is a machine learning model that suggests whether a defendant will reoffend within 2 years. The jury will discuss it with you, but not the judge.

- Do not act as a jury member; only assist them.
- Each jury member has a unique number for tracking their previous discussion content.
- Indicate decision content that seems unlikely to follow RiskComp's suggestions with "...".

# Output Format

Present insights as one or two sentences in human dialogue format without repeating previous insights. Format your response as: `assistant: response`

# Examples

Input: Jury member number: [statement supports RiskComp's suggestion]
Output: `assistant:  (Provide insights following the Socratic method based on jury discussions and previous content.)'''

        elif self.condition == 3:
            system_message = '''
Review the correctness of an initial jury decision based on defendant's information and the jury's provided decision.
- You will receive information about the defendant and the jury's initial decision.
- Formulate critique questions to help reconsider the validity of the decision.
- Ensure questions focus on evaluating the suggestion's accuracy and fairness without needing further input from the judge.
# Steps
1. Carefully read the jury's initial decision and the defendant's information.
2. Critically evaluate the aspects of the decision.
3. Formulate three critique questions that encourage reconsideration of the jury's initial decision.

# Output Format
- Provide the critique questions in bullet point format, labeled as "Critiques."

# Examples
Critiques:
- Did the jury consider all relevant evidence presented?
- Is there any potential bias in the jury's decision?
- Were the legal instructions followed accurately by the jury?

# Notes
- The judge will not respond to any further queries for clarification.
- Keep the critique questions concise and relevant to the decision made.
'''
        elif self.condition == 4:
            system_message = '''
Assist the jury member in questioning the validity of their initial decision using Socratic questioning.

The judge provides the defendant's information and the jury's initial decision about whether a defendant will reoffend within 2 years. The jury will discuss it with you, but not the judge.

- Do not act as a jury member; only assist them.
- Each jury member has a unique number for tracking their previous discussion content.
- Indicate decision content that seems unlikely to follow the jury's initial decision with "...".

# Output Format

Present insights as one or two sentences in human dialogue format without repeating previous insights. Format your response as: `assistant: response`

# Examples

Input: Jury member number: [Statement supports the jury's initial decision]
Output: `assistant: (Provide insights following the Socratic method based on jury discussions and previous content.)'''
        else:
            return ""
        return system_message

    def get_judge_message(self):
        if self.condition == 1 or self.condition == 2:
            judge_message = '''
A {age}-year-old {race} {sex} defendant has been charged with {charge_reason} as a {charge_degree}.  Specifically, {charge_reason} means {charge_explain}. The defendant has {prior} prior criminal counts. The defendant made {misdemeanor} misdemeanors and {felony} felonies before 18.
---
RiskComp predicts the defendant will {prediction} reoffend the law within 2 years.'''

        elif self.condition == 3 or self.condition == 4:
            judge_message = '''
A {age}-year-old {sex} {race} defendant has been charged with {charge_reason} as a {charge_degree}.  Specifically, {charge_reason} means {charge_explain}. The defendant has {prior} prior criminal count. The defendant made {misdemeanor} misdemeanors and {felony} felonies before 18.
---
The jury initially determined the defendant will {prediction} reoffend the law within 2 years.'''
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
        static = openai.chat.completions.create(
            model="gpt-4o",
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
Determine whether the content provided is a "statement," "question," or "unrelated" in the context of a prediction task regarding whether a defendant would reoffend within two years.

- "statement": Content includes details about the defendant, such as demographics, criminal history, or crime sentence, and determining or reasoning the reoffend opportunity.
- "question": Content involves asking for someone else's opinion.
- "unrelated": Content that does not fit the categories of "statement" or "question."

# Steps

1. Analyze the content to determine its primary purpose.
2. Classify if it matches the definition of "statement," "question," or "unrelated."

# Output Format

Provide the classification type alone (statement/ question/ unrelated), without any explanation or punctuation mark.

# Examples

**Example 1**  
Input: "Too old to commit a crime."  
Output: statement  

**Example 2**  
Input: "Does the defendant have anger management issues that could be treated?"  
Output: question  

**Example 3**  
Input: "LOL."  
Output: unrelated  

# Notes
- Ensure clarity in classification by focusing solely on the content's intention.
- Avoid providing reasons or any additional commentary in the output.'''
        messages = [
            {"role": "system", "content": type_message},
            {"role": "user", "content": content}
            ]
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature = 1
            )
        return response.choices[0].message.content.lower().strip()

    def statementType(self, content):
        type_message = '''
Determine if the statement indicates a belief that a defendant will reoffend.

# Steps
1. Read the given statement carefully.
2. Analyze the content to assess whether it suggests a likelihood that the defendant will reoffend.
3. Decide if the statement leans more towards the belief that the defendant will reoffend or will not reoffend.

# Output Format
Respond with only "true" or "false" without any reason or punctuation mark.
- "true" if the statement suggests a greater chance that the defendant will reoffend.
- "false" if the statement suggests a greater chance that the defendant will not reoffend.'''
        messages = [
            {"role": "system", "content": type_message},
            {"role": "user", "content": content}
        ]
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=2,
            temperature=1
        )
        print(response)
        return response.choices[0].message.content.lower().strip()

    
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
                dynamic = openai.chat.completions.create(
                    model="gpt-4o",
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
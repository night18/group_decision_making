# The Django Server for group discussion
If you would like to customize your own web application, please check the following files and folders:
- /server/settings: Set the ALLOWED_HOSTS, CHANNEL_LAYERS, and DATABASES.
- /experiment/views.py: All restful API should be defined here.
- /experiment/consumers.py: All the logic that control the chat room and any channel-related functions.
- /experiment/gpt.py: Called the OpenAI's API. Set you own agent here.
- /experiment/models.py: Database related function. 
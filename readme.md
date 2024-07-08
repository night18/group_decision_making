## run the chat server
docker run -p 6379:6379 -d redis:5

## run the app server
python manage.py runserver

## run the app client
npm run serve

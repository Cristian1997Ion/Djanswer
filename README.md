# Djanswer (W.I.P.)
Funny, quiplash-like game made with the power of Django Channels.
At the begging of each round, players will write a question, then answer a random question (not their own).
After everybody has answered, a vote will take place to determine the most funny question+answer.
Only the player that asked the question and the player that answered it will receive points.
The player with the most points win!

### Python 3.9.7 | Django 4.0.2 | SQLite | Javascript

# How to run?
1. copy .env-example to .env and ajust
2. (OPTIONAL) run: python3 -m venv env, source env/bin/activate 
3. run: pip install -r requirements
4. run: python manage.py migrate
5. run: python manage.py runserver
6. start a local redis server (docker run -p 6379:6379 -d redis:5)
7. run: python manage.py runworker game_engine

![Game lobby](https://user-images.githubusercontent.com/72604028/154498916-2c9649e4-d9cc-4b9f-8051-379bd3988396.png)

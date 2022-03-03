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

![questions](https://user-images.githubusercontent.com/72604028/156608137-5d07da80-4a15-4fa0-a5a8-ce9f1aa72b31.png)

![vote](https://user-images.githubusercontent.com/72604028/156608158-a98500f0-19a3-4db7-95d0-1d13ec5c21e2.png)

![round summary](https://user-images.githubusercontent.com/72604028/156608170-2d9784cd-e8c3-4081-83d3-61fdb38b8e48.png)
![winner](https://user-images.githubusercontent.com/72604028/156608295-e548b588-769e-4b86-a746-0590fa3893d7.png)

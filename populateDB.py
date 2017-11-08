import requests
import os

# hostname = "http://knowitalllive-dev.us-west-1.elasticbeanstalk.com/api/"
hostname = "http://127.0.0.1:8000/api/"
def register(username, password):
    response = requests.post(hostname + "register?username=" + username + "&password=" + password)
    print(response.text)

def authenticate(username):
    response = requests.get(hostname + "authenticate?username=" + username)
    print(response.text)

#registers and authenticate user
def createUser(username, password):
    print("Creating user: " + username + ". It might take a few secs...")
    register(username, password)
    authenticate(username)

def createPoll(username, category, text, choices, openForever, dayLimit, anonymous, tags):
    response = requests.post(hostname + 'createPoll?username=' + username + '&category=' + category +
                                    '&text=' + text + '&choices=' + choices + '&openForever='+openForever
                                     + '&dayLimit=' + dayLimit + "&anonymous="+anonymous+"&tags="+tags)
    print(response.text)

def main():
    #removing the database
    os.system("rm ~/KnowItAll/knowItAllService/knowItAllService/db.sqlite3")
    #removing migration files and creating __init__.py
    os.system("rm -rf ~/KnowItAll/knowItAllService/knowItAllService/knowItAllAPI/migrations/*")
    #We cannot delete __init__.py
    os.system("git checkout knowItAllService/knowItAllAPI/migrations/__init__.py")
    #makemigrations and migrate
    os.system("python knowItAllService/manage.py makemigrations")
    os.system("python knowItAllService/manage.py migrate")
    #creating superuser
    os.system("python knowItAllService/manage.py createsuperuser")

    #populate db

    #create users
    createUser("prego@usc.edu", "pass123")

    #create categories
    response = requests.post(hostname + "createCategory?populate=true")
    print(response.text)

    #create polls
    createPoll(username="prego@usc.edu", text="Best backend Framework?", choices="Django,Ruby on Rails,Spring"
                ,category="1", openForever="1", dayLimit="0", anonymous="0", tags="coding,hack,programmer,cs")
    createPoll(username="prego@usc.edu", text="Best Burger Place", choices="Five guys,in n out,fatburger,jack in the box"
               , category="2", openForever="1", dayLimit="0", anonymous="1", tags="burger,fat,delicious")





if __name__ == '__main__':
    main()
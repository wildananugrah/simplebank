from locust import HttpUser, between, task, SequentialTaskSet, events
from tasks.simple_user import SimpleUser

users = [
    ("user1", "password", "user0@gmail.com"),
    ("user2", "password", "user1@gmail.com")
]

@events.test_start.add_listener
def on_test_start(**kwargs):
    print("...... initiating load test ...... ON_TEST_START")

@events.test_stop.add_listener
def on_test_stop(**kwargs):
    print("...... load test complete ...... ON_TEST_END")

class MyUser(HttpUser):
    wait_time = between(1,2)
    tasks = [SimpleUser]
    weight = 1

    def on_start(self):
        self.username, self.password, self.email = users.pop()
        print("MyUser: hatching user..")

    def on_stop(self):
        print("MyUser: deleting user..")

    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password
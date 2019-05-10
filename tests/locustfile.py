from locust import HttpLocust, TaskSet, task
import json
import random


class UsersManipulate(TaskSet):
    def on_start(self):
        self._people_list = []
        self._actions = {}
        self.add_user()

    def on_stop(self):
        res = self.client.get('/people')
        people_list = json.loads(res.text)
        failed_count = 0
        for person in people_list:
            if person['_id'] in self._actions:
                expected_aged = self._actions[person['_id']]
                if expected_aged != person['age']:
                    failed_count = failed_count + abs(expected_aged -
                                                      person['age'])
        print("Failed: {}".format(failed_count))

    @task(10)
    def list_user(self):
        self.client.get('/people')

    @task(5)
    def add_user(self):
        new_person = {
            'name': 'foo',
            'age': 0
        }
        res = self.client.post('/person', json=new_person)
        _id = json.loads(res.text)['_id']
        new_person['_id'] = _id
        self._actions[_id] = 0
        self._people_list.append(new_person)

    @task(8)
    def increase_user_age(self):
        person = random.choice(self._people_list)
        res = self.client.patch('/person/{}/increase_age'.format(
            person['_id']))
        if res.status_code == 200:
            _id = person['_id']
            self._actions[_id] = self._actions[_id] + 1


class WebsiteUser(HttpLocust):
    task_set = UsersManipulate
    min_wait = 50
    max_wait = 500

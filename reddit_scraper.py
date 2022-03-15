import requests
from course_list_scraper import InvalidCodeException
import json
import os
from requests.exceptions import ConnectionError
import re


class RedditScraper:
    __url = "https://api.pushshift.io/reddit/search/submission/?subreddit=Dawson"
    __url_comment = "https://api.pushshift.io/reddit/search/comment/?subreddit=Dawson"

    def __init__(self):
        self.__local_data = RedditDataSaver()

    @staticmethod
    # Returns json data from page
    def __request(url, query_params):
        try:
            page = requests.get(url, query_params)
        except ConnectionError:
            return -1
        if page.status_code != 200:
            raise InvalidCodeException("The page status is not 200")
        return json.loads(page.content)['data']

    # Returns json data of submissions
    def search_submission(self, keywords):
        param = ""
        for key in keywords:
            param += key + '|'
        data = self.__request(self.__url, {'q': param[0:-1], 'size': 100})
        if data == -1:
            return self.__local_data.search(keywords)
        self.__local_data.update_data(data)
        return data

    # Returns json data of comments
    def search_comments(self, keyword):
        param = ""
        for key in keyword:
            param += key + '|'
        return self.__request(self.__url_comment, {'q': param[0:-1]})

    # Returns json data of post according to date periods
    def search_dates(self, keyword, periods):
        param = ""
        for key in keyword:
            param += key + '|'
        return self.__request(self.__url, {'q': param[0:-1], 'after': periods[0], 'before': periods[1]})


# Used to read and compare the datasets
class RedditDataSaver:
    file_path = os.path.join('local_data', 'pushshift_data.json')

    def __init__(self):
        if not os.path.isdir(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))
            if not os.path.isfile(self.file_path):
                self.__overwrite_data([])
        with open(self.file_path, 'r') as file:
            self.data = json.load(file)['data']

    def __overwrite_data(self, new_data):
        with open(self.file_path, 'w') as file:
            json.dump({'data': new_data}, file)

    def search(self, keywords):
        findings = []
        for data in self.data:
            if self.__data_has_keyword(data, keywords):
                findings.append(data)
        return findings

    @staticmethod
    def __data_has_keyword(data, keywords):
        for keyword in keywords:
            if re.search(keyword, data['title']) or re.search(keyword, data['selftext']):
                return True
        return False

    # Updates the local file data given that the id's are not the same
    def update_data(self, data):
        self.__update_data_set(data)
        self.__overwrite_data(self.data)

    def get_last_post_date(self):
        return -1 if len(self.data) == 0 else self.data[0]['created_utc']

    # Updates the instanced data set with a new data set given that the id's are not the same
    def __update_data_set(self, new_data):
        for new_value in new_data:
            if not self.__compare_data(new_value):
                self.data.append(new_value)
        self.data = sorted(self.data, key=lambda d: d['created_utc'], reverse=True)

    # compares a new data set from the one instanced.
    # Returns true if the new data set is already contained in the instance
    def __compare_data(self, new_value):
        for old_value in self.data:
            if old_value['id'] == new_value['id']:
                return True
        return False

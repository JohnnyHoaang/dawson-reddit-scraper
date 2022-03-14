import requests
from course_list_scraper import InvalidCodeException
import json
import os
from json.decoder import JSONDecodeError


class RedditScraper:
    __url = "https://api.pushshift.io/reddit/search/submission/?subreddit=Dawson"
    __url_comment = "https://api.pushshift.io/reddit/search/comment/?subreddit=Dawson"

    @staticmethod
    # Returns json data from page
    def __request(url, query_params):
        page = requests.get(url, query_params)
        if page.status_code != 200:
            raise InvalidCodeException("The page status is not 200")
        return json.loads(page.content)['data']

    # Returns json data of submissions
    def search_submission(self, keyword):
        param = ""
        for key in keyword:
            param += key + '|'
        return self.__request(self.__url, {'q': param[0:-1], 'size': 100})

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


if __name__ == '__main__':
    from scraping_test import Analyzer

    r = RedditDataSaver()
    r.update_data([{'id': 'b','created_utc': 12345678}])
    print(r.get_last_post_date())
    # Pushshift API scraper
    # a = Analyzer()
    # s = RedditScraper()
    # data = s.search_submission(a.get_cs_keywords())
    # print(type(data[0]))
    # for b in data[0]:
    #     print(b)
    # for d in data:
    #
    #     if d['title'] == '':
    #         print('(no title)')
    #     else:
    #         print(f"Title: {d['title']}")
    #
    #     if d['selftext'] == '':
    #         print('(no body)')
    #     else:
    #         print(f"Body: {d['selftext']}")
    #
    #     if d['author'] == '':
    #         print('(no author)')
    #     else:
    #         print(f"Author: {d['author']}")
    #
    #     print('______________________________________')

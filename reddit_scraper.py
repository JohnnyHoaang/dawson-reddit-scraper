import requests
from course_list_scraper import InvalidCodeException
import json
import os
from json.decoder import JSONDecodeError

class RedditScraper:
    __url = "https://api.pushshift.io/reddit/search/submission/?subreddit=Dawson"
    __url_comment = "https://api.pushshift.io/reddit/search/comment/?subreddit=Dawson"

    @staticmethod
    def __request(url, query_params):
        # print(query_params)
        page = requests.get(url, query_params)
        if page.status_code != 200:
            raise InvalidCodeException("The page status is not 200")
        return json.loads(page.content)['data']

    def search_submission(self, keyword):
        param = ""
        for key in keyword:
            param += key + '|'
        return self.__request(self.__url, {'q': param[0:-1], 'size': 100})

    def search_comments(self, keyword):
        param = ""
        for key in keyword:
            param += key + '|'
        return self.__request(self.__url_comment, {'q': param[0:-1]})

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
                with open(self.file_path, 'w') as file:
                    pass

    def get_last_post_date(self):
        with open(self.file_path, 'r') as file:
            try:
                data = json.load(file)
            except JSONDecodeError:
                return -1
            return data[0]['created_utc']

    def __compare_data(self, data_set_1, data_set_2):
        pass

    def __save_to_file(self, data: list[dict]):
        with open(self.file_path, 'w') as file:
            json.dump(data, file)


class RedditAPIScraper:
    __user = "dawson_scraper"
    __pwd = "dawsonscrapes123"
    __CLIENT_ID = "81Lszn_qxI8t4gitDsB5hA"
    __SECRET_KEY = "KZXLffRmt_pOnZoisA8pLzE4r3zegQ"
    __headers = None
    __url = 'https://oauth.reddit.com/r/dawson/search/?restrict_sr=dawson'
    __url_comments = 'https://oauth.reddit.com/r/dawson/comments/?restrict_sr=dawson'

    def __assign_headers(self):
        import requests
        auth = requests.auth.HTTPBasicAuth(self.__CLIENT_ID, self.__SECRET_KEY)
        __data = {
            'grant_type': 'password',
            'username': self.__user,
            'password': self.__pwd
        }
        self.__headers = {'User-Agent': 'MyAPI/0.0.1'}
        res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=__data,
                            headers=self.__headers)
        TOKEN = res.json()['access_token']
        self.__headers['Authorization'] = f'bearer {TOKEN}'

    def __request(self, query_params):
        self.__assign_headers()
        return requests.get(self.__url, query_params, headers=self.__headers).json()  # Response 200 but shows html

    def search(self, keyword):
        param = ""
        for key in keyword:
            param += key + '|'
        return self.__request({'q': param[0:-1]})

    def search_dates(self, keyword, periods):
        param = ""
        for key in keyword:
            param += key + '|'
        return self.__request({'q': param[0:-1], 'timestamp': f"{periods[0]}...{periods[1]}"})

    # def search_comments(self, id):
    #     return self.__request({})

if __name__ == '__main__':
    from scraping_test import Analyzer
    r = RedditDataSaver()
    print(r.get_last_post_date())
    # pushshift api scraper
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
    # reddit api scraper
    # ras = RedditAPIScraper()
    # ras_data = ras.search(['computer science'])


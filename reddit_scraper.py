import requests
from course_list_scraper import InvalidCodeException
import json


class RedditScraper:
    __url = "https://api.pushshift.io/reddit/search/submission/?subreddit=Dawson"
    __url_comment = "https://api.pushshift.io/reddit/search/comment/?subreddit=Dawson"

    @staticmethod
    def __request(url, query_params: dict):
        # print(query_params)
        page = requests.get(url, query_params)
        if page.status_code != 200:
            raise InvalidCodeException("The page status is not 200")
        return json.loads(page.content)['data']

    def search_submission(self, keyword: list[str]):
        param = ""
        for key in keyword:
            param += key + '|'
        return self.__request(self.__url, {'q': param[0:-1]})

    def search_comments(self, keyword: list[str]):
        param = ""
        for key in keyword:
            param += key + '|'
        return self.__request(self.__url_comment, {'q': param[0:-1]})

    def search_dates(self, keyword: list[str], periods: list[int]):
        param = ""
        for key in keyword:
            param += key + '|'
        return self.__request(self.__url, {'q': param[0:-1], 'after': periods[0], 'before': periods[1]})


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

    def __request(self, query_params: dict):
        self.__assign_headers()
        return requests.get(self.__url, query_params, headers=self.__headers).json()  # Response 200 but shows html

    def search(self, keyword: list[str]):
        param = ""
        for key in keyword:
            param += key + '|'
        return self.__request({'q': param[0:-1]})

    def search_dates(self, keyword: list[str], periods: list[int]):
        param = ""
        for key in keyword:
            param += key + '|'
        return self.__request({'q': param[0:-1], 'timestamp': f"{periods[0]}...{periods[1]}"})

    # def search_comments(self, id):
    #     return self.__request({})

if __name__ == '__main__':
    # pushshift api scraper
    # s = RedditScraper()
    # data = s.search_submission(['computer science', 'cs'])
    # for d in data:

    #     if d['title'] == '':
    #         print('(no title)')
    #     else:
    #         print(f"Title: {d['title']}")

    #     if d['selftext'] == '':
    #         print('(no body)')
    #     else:
    #         print(f"Body: {d['selftext']}")

    #     if d['author'] == '':
    #         print('(no author)')
    #     else:
    #         print(f"Author: {d['author']}")

    #     print('______________________________________')
    # reddit api scraper
    ras = RedditAPIScraper()
    ras_data = ras.search(['computer science'])


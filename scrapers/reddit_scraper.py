import requests
from course_list_scraper import InvalidCodeException
import json


class RedditScraper:
    __url = "https://api.pushshift.io/reddit/search/submission/?subreddit=Dawson"

    def __request(self, query_params: dict):
        page = requests.get(self.__url, query_params)
        if page.status_code != 200:
            raise InvalidCodeException("The page status is not 200")
        return json.loads(page.content)['data']

    def search(self, keyword: list[str]):
        param = ""
        for key in keyword:
            param += key + ','
        return self.__request({'q': param[0:-1]})


if __name__ == '__main__':
    s = RedditScraper()
    data = s.search(['admission'])
    for d in data:
        print(f"Title: {d['title']}")
        print(f"Body: {d['selftext']}")

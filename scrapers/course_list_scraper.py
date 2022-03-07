import requests
from bs4 import BeautifulSoup


class CourseScrapper:
    url = "https://www.dawsoncollege.qc.ca/computer-science-technology/course-list/"

    def __init__(self):
        self.__course_info = None
        self.__soup = BeautifulSoup(self.__get_page_content(), 'html.parser')
        self.__course_info = self.__soup.find('div', id='include')

    def __get_page_content(self):
        page = requests.get(self.url)
        if page.status_code != 200:
            raise InvalidCodeException("The page status is not 200")
        return page.content

    def get_courses(self):
        terms = self.__course_info.find_all('table', {'class': 'l r b t top-label-table course-grid enable-first'})
        all_courses = []
        term_numbers = self.get_terms()
        total_courses = len(self.__course_info.find_all('tr', {'onmouseout': 'this.style.backgroundColor="#ffffff";'}))
        for j in range(len(terms)):
            for i in range(1, total_courses+1):
                # All the concentration courses have a table with descriptions
                description_row = self.__course_info.find('tr', {'id': f'{i}'})
                if description_row.find('table') is not None:
                    ponderation = self.__course_info.find('td', {'id': f'ponderation{i}'}).text.split(' - ')
                    course = {'term_number': term_numbers[j],
                              'course_number': self.__course_info.find('td', {'id': f'coursenumber{i}'}).text,
                              'course_name': self.__course_info.find('td', {'id': f'title{i}'}).text,
                              'description': description_row.find_all('td')[-1].text,
                              'class_hours': int(ponderation[0]),
                              'lab_hours': int(ponderation[1]),
                              'homework_hours': int(ponderation[2]),
                              'total_hours': int(self.__course_info.find('td', {'id': f'hours{i}'}).text)}
                    all_courses.append(course)

        return all_courses

    def get_terms(self) -> list[int]:
        content = self.__course_info.find_all('h2', {'class': 'noPadding'})
        terms = []
        for term in content:
            terms.append(int(term.text.strip().split(' ')[-1]))
        return terms


class InvalidCodeException(Exception):
    def __init__(self, message=''):
        super().__init__(message)



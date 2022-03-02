url = "https://www.dawsoncollege.qc.ca/computer-science-technology/course-list/"
from sqlite3 import DatabaseError
import requests

page = requests.get(url)
if page.status_code == 200:
    content = page.content
    import bs4

    soup = bs4.BeautifulSoup(content, 'html.parser')
    headers = soup.findAll('h2', class_='noPadding')
    table = soup.findAll('table', class_="l r b t top-label-table course-grid enable-first")
    numberCourses = 1
    courses_list = []
    for i in range(0, 6):
        import re

        # length of courses in one term
        length = int(len(table[i].findAll('tr', style=re.compile(r'display:none;'))) / 2)
        for j in range(0, length):
            course = {'course_number': None, 'course_title': None, 'course_description': None, 'term_number': None}
            # searching by id tags
            termNumber = int(headers[i].text[-1])
            courseN = table[i].find('td', {"id": f"coursenumber{numberCourses}"})
            title = table[i].find('td', {"id": f"title{numberCourses}"})
            description_row = table[i].find('tr', {"id": f"{numberCourses}"})
            try:
                # concentration courses have table with descriptions
                if description_row.find('table') is not None:
                    description = description_row.findAll('td')
                    course['course_number'] = courseN.text
                    course['course_title'] = title.text
                    course['course_description'] = description[2].text
                    course['term_number'] = termNumber
                    courses_list.append(course)
            except Exception as e:
                pass
            numberCourses += 1
    print(len(courses_list))

    import cx_Oracle
    import Config

    cx_Oracle.init_oracle_client(lib_dir=Config.lib)
    dsn = cx_Oracle.makedsn('198.168.52.211',
                            1521,
                            service_name='pdbora19c.dawsoncollege.qc.ca')
    with cx_Oracle.connect(Config.user, Config.pwd, dsn) as conn:
        print('Connected')
        conn.autocommit = True
        with conn.cursor() as cur:
            # try:
            #     cur.execute("DROP TABLE COURSES CASCADE CONSTRAINTS")
            #     cur.execute("DROP TABLE TERMS CASCADE CONSTRAINTS")
            #     cur.execute("DROP TABLE COURSES_TERMS CASCADE CONSTRAINTS")
            # except DatabaseError as e:
            #     pass
            # cur.execute('''CREATE TABLE COURSES (
            #         course_number VARCHAR2(100) PRIMARY KEY, 
            #         course_name VARCHAR2(100),
            #         description VARCHAR2(1000))'''
            # )
            # cur.execute('''CREATE TABLE TERMS (
            #        term_number NUMBER(2) PRIMARY KEY)'''
            # )
            # cur.execute('''CREATE TABLE COURSES_TERMS (
            #         term_number NUMBER(2),
            #         course_number VARCHAR2(100) PRIMARY KEY,
            #         CONSTRAINT term_fk
            #         FOREIGN KEY (term_number)
            #         REFERENCES terms (term_number),
            #         CONSTRAINT course_fk
            #         FOREIGN KEY (course_number)
            #         REFERENCES courses (course_number))'''
            # )
            for course in courses_list:
                courses_info = [course['course_number'], course['course_title'], course['course_description']]
                courses_term_info = [course['term_number'], course['course_number']]
                insert_courses = "INSERT INTO COURSES VALUES(:1,:2,:3)"
                insert_courses_terms = "INSERT INTO COURSES_TERMS VALUES(:1,:2)"
                try:
                    cur.execute(insert_courses, courses_info)
                    cur.execute(insert_courses_terms, courses_term_info)
                except cx_Oracle.DatabaseError as e:
                    print(e)

else:
    print("Connection not established")

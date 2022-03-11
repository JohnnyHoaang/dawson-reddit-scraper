import cx_Oracle
from cx_Oracle import DatabaseError
from db_config import Config
from file_reader import SQLFileReader
from course_list_scraper import CourseScrapper

cx_Oracle.init_oracle_client(lib_dir=Config.lib)


class OracleDB:

    def __init__(self):
        link = cx_Oracle.makedsn('198.168.52.211',
                                 1521,
                                 service_name='pdbora19c.dawsoncollege.qc.ca')
        self.conn = cx_Oracle.connect(Config.user, Config.pwd, dsn=link)
        self.conn.autocommit = True

    # Populates a table with a list of values
    def populate_table(self, table_name: str, values: tuple):
        insert_statement = f'insert into {table_name} values ('
        for value in range(len(values)):
            insert_statement += f':{value + 1}'
            if value != len(values) - 1:
                insert_statement += ','
        insert_statement += ')'
        with self.conn.cursor() as cur:
            cur.execute(insert_statement, values)

    # reads from the db using a query and returns a list of the rows returned
    def select(self, query: str) -> list[dict]:
        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            col_names = [row[0] for row in cur.description]
        data = []
        for row in rows:
            value = {}
            for i in range(len(col_names)):
                value[col_names[i].lower()] = row[i]
            data.append(value)
        return data

    # Executes and arbitrary string of sql code
    def execute_statement(self, query: str, silent=False) -> None:
        try:
            with self.conn.cursor() as cur:
                cur.execute(query)
        except DatabaseError as e:
            if not silent:
                raise e

    # Deletes a table from the Database forcefully
    def force_table_drop(self, table_name: str):
        drop_query = f'drop table {table_name} cascade constraints'
        try:
            self.execute_statement(drop_query)
        except DatabaseError:
            pass

    def drop_table(self, table_name: str):
        del_query = f"drop table {table_name}"
        self.execute_statement(del_query)

    # Closes the connection
    def close(self):
        self.conn.close()

    # Used with a with statement and returns the instance
    def __enter__(self):
        return self

    # Closes the connection when exiting the with statement
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class CourseScrapingDatabase:
    def __init__(self):
        self.__database = OracleDB()

    def setup_database(self, setup_file: str):
        file_reader = SQLFileReader(setup_file)
        for statement in file_reader.read_statements():
            self.__database.execute_statement(statement, True)

    def populate_terms(self, data: list[int]):
        for term_number in data:

            self.__database.populate_table('terms', (term_number,))

    # Populates the courses tables with a list of dictionaries containing the course data
    def populate_courses(self, data: list[dict]):
        for course in data:
            values = (course['course_number'],
                      course['course_name'],
                      course['description'],
                      course['class_hours'],
                      course['lab_hours'],
                      course['homework_hours'],
                      course['total_hours'])
            self.__database.populate_table('courses', values)

    def get_all_course_info(self):
        return self.__database.select('''select * from courses
        inner join courses_terms
        using (course_number)
        inner join terms
        using (term_number)''')

    # populates the course_terms tables with a list of dictionaries containing the
    def populate_course_terms(self, data: list[dict]):
        for course in data:
            values = (course['term_number'], course['course_number'])
            self.__database.populate_table('courses_terms', values)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__database.close()

    def close(self):
        self.__database.close()


def build_cs_database():
    with CourseScrapingDatabase() as database:
        database.setup_database('database_resources/Setup.sql')
        scrapper = CourseScrapper()
        database.populate_terms(scrapper.get_terms())
        database.populate_courses(scrapper.get_courses())
        database.populate_course_terms(scrapper.get_courses())

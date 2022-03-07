import cx_Oracle
from cx_Oracle import DatabaseError
from db_config import Config
from file_io import SQLFileReader

cx_Oracle.init_oracle_client(lib_dir=Config.lib)


class OracleDB:

    def __init__(self):
        link = cx_Oracle.makedsn('198.168.52.211',
                                 1521,
                                 service_name='pdbora19c.dawsoncollege.qc.ca')
        self.conn = cx_Oracle.connect(Config.user, Config.pwd, dsn=link)
        self.conn.autocommit = True

    # Populates a table with a list of values
    def populate_table(self, table_name: str, values: list | tuple):
        insert_statement = f'insert into {table_name} values ('
        for value in range(len(values)):
            insert_statement += f':{value + 1}'
            if value != len(values) - 1:
                insert_statement += ','
        insert_statement += ')'
        with self.conn.cursor() as cur:
            cur.execute(insert_statement, values)

    # reads from the db using a query and returns a list of the rows returned
    def select(self, query: str) -> list[tuple]:
        data = []
        with self.conn.cursor() as cur:
            for row in cur.execute(query):
                data.append(row)
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


class CSDatabase:
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
            print(values)
            self.__database.populate_table('courses', values)

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


if __name__ == '__main__':
    from scrapers.course_list_scraper import CourseScrapper
    database = CSDatabase()
    print('Setting up the database...')
    database.setup_database('Setup.sql')
    print('Getting the course info...')
    scrapper = CourseScrapper()
    print('Populating the database...')
    database.populate_terms(scrapper.get_terms())
    database.populate_courses(scrapper.get_courses())
    database.populate_course_terms(scrapper.get_courses())
    print('done!')

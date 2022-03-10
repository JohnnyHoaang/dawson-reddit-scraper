DROP TABLE COURSES_TERMS;
DROP TABLE COURSES;
DROP TABLE TERMS;
CREATE TABLE COURSES (
    course_number CHAR(10) PRIMARY KEY,
    course_name VARCHAR2(100) NOT NULL,
    description VARCHAR2(1000) NOT NULL,
    class_hours NUMBER(2) NOT NULL,
    lab_hours NUMBER(2) NOT NULL,
    homework_hours NUMBER(2) NOT NULL,
    total_hours NUMBER(3) NOT NULL
);

CREATE TABLE TERMS (
    term_number NUMBER(2) PRIMARY KEY
);

CREATE TABLE COURSES_TERMS (
    term_number NUMBER(2) NOT NULL,
    course_number CHAR(10) NOT NULL,
    CONSTRAINT term_fk FOREIGN KEY (term_number) REFERENCES terms (term_number),
    CONSTRAINT course_fk FOREIGN KEY (course_number) REFERENCES courses (course_number),
    CONSTRAINT pk_courses_terms PRIMARY KEY (term_number, course_number)

);
commit;
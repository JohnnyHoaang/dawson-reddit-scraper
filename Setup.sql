DROP TABLE COURSES_TERMS CASCADE CONSTRAINTS;
DROP TABLE COURSES CASCADE CONSTRAINTS;
DROP TABLE TERMS CASCADE CONSTRAINTS;
CREATE TABLE COURSES (
    course_number CHAR(10) PRIMARY KEY,
    course_name VARCHAR2(100),
    description VARCHAR2(1000),
    class_hours NUMBER(2),
    lab_hours NUMBER(2),
    homework_hours NUMBER(2),
    total_hours NUMBER(3)
);

CREATE TABLE TERMS (
    term_number NUMBER(2) PRIMARY KEY
);

CREATE TABLE COURSES_TERMS (
    term_number NUMBER(2),
    course_number CHAR(10),
    CONSTRAINT term_fk FOREIGN KEY (term_number) REFERENCES terms (term_number),
    CONSTRAINT course_fk FOREIGN KEY (course_number) REFERENCES courses (course_number),
    CONSTRAINT pk_courses_terms PRIMARY KEY (term_number, course_number)

);

insert into terms VALUES(1);
insert into terms VALUES(2);
insert into terms VALUES(3);
insert into terms VALUES(4);
insert into terms VALUES(5);
insert into terms VALUES(6);
commit;
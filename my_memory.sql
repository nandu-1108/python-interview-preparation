create database my_memory;
use my_memory;

-- first i need to create subject table to store sbjects i want 
-- for the colums we need that is sub_id and subject_name
create table subjects(
sub_id int primary key not null auto_increment,
sub_name varchar(50) not null
);

-- then here i am creating topic table to know the subjects topics and definationas here
-- for that colums we need topic_id ,topic_name,computer_defination, my_defination
create table topics(
topic_id int primary key not null auto_increment,
sub_id int  NOT NULL ,
topic_name varchar(50) not null,
computer_definationa varchar(200) not null,
my_defination varchar(200) not null,
FOREIGN KEY (sub_id) REFERENCES subjects(sub_id));

-- --here we have to create companies table to connect everything here 

create table company(
comp_id int primary key auto_increment,
comp_name varchar(50) not null,
location varchar(50)
);


create table interview(
interview_id int primary key not null auto_increment,
job_role varchar(50) ,
inteview_date date,
rounds int ,
comp_id int,
FOREIGN KEY (comp_id) REFERENCES company(comp_id));



create table inter_questions(
question_no int primary key auto_increment,
question text,
question_type varchar(20) ,
interview_id int,
FOREIGN KEY (interview_id) REFERENCES interview(interview_id)
);

ALTER TABLE inter_questions
ADD COLUMN answer TEXT,
ADD COLUMN practice_status VARCHAR(20) DEFAULT 'Not Started',
ADD COLUMN confidence_level TINYINT DEFAULT 0,
ADD COLUMN last_practiced DATE;


DESCRIBE subjects;
DESCRIBE topics;
DESCRIBE company;
DESCRIBE interview;
DESCRIBE inter_questions;

select * from topics;

select * from subjects s left join topics t on s.sub_id=t.sub_id;



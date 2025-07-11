create table employees (
    id int,
    name string,
    age int,
    age int,
    salary float,
    join_date date
);

insert into employees values
(1, 'Alice', 28, 5000.0, '2022-01-10'),
(2, 'Bob', 35, 7000.0, '2021-03-15'),
(3, 'Charlie', 40, 6500.0, '2020-07-20'),
(4, 'David', 25, 4800.0, '2023-05-01'),
(5, 'Eve', 30, 7200.0, '2019-11-11');

select name, salary
from employees;

select *
from employees
where age > 30;

select *
from employees
where name like "%li%";



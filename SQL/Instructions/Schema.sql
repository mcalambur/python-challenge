-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Modified SQL

-- Main employees table with emp_no as unique and primary key:
DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
    emp_no INT UNIQUE NOT NULL,
	birth_date DATE NOT NULL CHECK(birth_date > '1900-01-01'),
    first_name VARCHAR(25) NOT NULL,
    last_name VARCHAR(25) NOT NULL,
    gender CHAR(1) NOT NULL,
	hire_date DATE NOT NULL CHECK(hire_date > birth_date),
    CONSTRAINT "pk_employees" PRIMARY KEY (emp_no)
);
-- Validate that dat was loaded
SELECT * FROM employees LIMIT 5

-- Salaries table, with constraints salary > 0, to_date needs to be at least same as hire_date but not earlier
DROP TABLE IF EXISTS salaries;
CREATE TABLE salaries (
    emp_no INTEGER NOT NULL,
    salary NUMERIC(10,2) NOT NULL CHECK(salary > 0),
    from_date DATE NOT NULL CHECK(from_date > '1900-01-01'),
    to_date DATE NOT NULL CHECK(to_date >= from_date),
	FOREIGN KEY (emp_no) REFERENCES employees(emp_no)
);
-- Validate that dat was loaded
SELECT * FROM salaries LIMIT 5

-- departments table with constraints to enforce unique department number and unique name 
DROP TABLE IF EXISTS departments;
CREATE TABLE departments (
    dept_no VARCHAR(5) UNIQUE NOT NULL,
    dept_name VARCHAR(25) UNIQUE NOT NULL,
    CONSTRAINT "pk_departments" PRIMARY KEY (dept_no)
);
-- Validate that dat was loaded
SELECT * FROM departments

-- titles table, with constraints to_date needs to be at least same as from_date but not earlier
DROP TABLE IF EXISTS titles;
CREATE TABLE titles (
    emp_no INTEGER NOT NULL,
    title VARCHAR(25) NOT NULL,
    from_date DATE NOT NULL CHECK(from_date > '1900-01-01'),
    to_date DATE NOT NULL CHECK(to_date >= from_date),
	FOREIGN KEY (emp_no) REFERENCES employees(emp_no)
);
-- Validate that dat was loaded
SELECT * FROM titles LIMIT 5

-- dept_emp table, with constraints to_date needs to be at least same as from_date but not earlier
DROP TABLE IF EXISTS dept_emp;
CREATE TABLE dept_emp (
    emp_no INTEGER NOT NULL REFERENCES employees(emp_no),
    dept_no VARCHAR(5) NOT NULL REFERENCES departments(dept_no),
    from_date DATE NOT NULL CHECK(from_date > '1900-01-01'),
    to_date DATE NOT NULL CHECK(to_date >= from_date),
	PRIMARY KEY(emp_no, dept_no)
);

-- Validate that dat was loaded
SELECT * FROM dept_emp LIMIT 5

-- dept_manager table, with constraints to_date needs to be at least same as from_date but not earlier
DROP TABLE IF EXISTS dept_manager;
CREATE TABLE dept_manager (
    dept_no VARCHAR(5) NOT NULL REFERENCES departments(dept_no),
    emp_no INTEGER NOT NULL REFERENCES employees(emp_no),
    from_date DATE NOT NULL CHECK(from_date > '1900-01-01'),
    to_date DATE NOT NULL CHECK(to_date >= from_date),
	PRIMARY KEY(emp_no, dept_no)
);

-- Validate that dat was loaded
SELECT * FROM dept_manager LIMIT 5
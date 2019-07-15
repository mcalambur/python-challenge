-- Homework queries 

-- 1. List the following details of each employee: employee number, last name, first name, gender, and salary.
SELECT employees.emp_no, employees.last_name, employees.first_name, employees.gender, salaries.salary
FROM employees 
INNER JOIN salaries ON
employees.emp_no = salaries.emp_no
LIMIT 20

-- 2. List employees who were hired in 1986.
SELECT employees.emp_no, employees.last_name, employees.first_name
FROM employees 
WHERE hire_date BETWEEN '01/01/1986' AND '12/31/1986'
LIMIT 20

--3. List the manager of each department with the following information: department number, department name, 
-- the manager's employee number, last name, first name, and start and end employment dates.

SELECT departments.dept_no, departments.dept_name, dept_manager.emp_no, employees.last_name, employees.first_name,
		dept_emp.from_date, dept_emp.to_date
FROM employees, dept_manager, departments, dept_emp
WHERE employees.emp_no = dept_manager.emp_no
	AND	dept_emp.emp_no = dept_manager.emp_no
	AND	employees.emp_no = dept_emp.emp_no
	AND	departments.dept_no = dept_manager.dept_no
	AND departments.dept_no = dept_emp.dept_no
	AND dept_manager.dept_no = dept_emp.dept_no
LIMIT 25

-- 4. List the department of each employee with the following information: employee number, last name, first name, and department name.
SELECT employees.emp_no, employees.last_name, employees.first_name, departments.dept_name 
FROM employees, dept_emp, departments
WHERE employees.emp_no = dept_emp.emp_no
AND dept_emp.dept_no = departments.dept_no
LIMIT 20

-- 5. List all employees whose first name is "Hercules" and last names begin with "B."
SELECT employees.emp_no, employees.last_name, employees.first_name, employees.gender
FROM employees
WHERE employees.first_name = 'Hercules'
AND employees.last_name like 'B%'
LIMIT 20

-- 6. List all employees in the Sales department, including their employee number, last name, first name, and department name.
SELECT employees.emp_no, employees.last_name, employees.first_name, departments.dept_name 
FROM employees, dept_emp, departments
WHERE employees.emp_no = dept_emp.emp_no
AND dept_emp.dept_no = departments.dept_no
AND departments.dept_name = 'Sales'
LIMIT 20

-- 7. List all employees in the Sales and Development departments, including their employee number, last name, first name, and department name.
SELECT employees.emp_no, employees.last_name, employees.first_name, departments.dept_name 
FROM employees, dept_emp, departments
WHERE employees.emp_no = dept_emp.emp_no
AND dept_emp.dept_no = departments.dept_no
AND departments.dept_name in ('Sales', 'Development')
LIMIT 20

-- 8. In descending order, list the frequency count of employee last names, i.e., how many employees share each last name.

SELECT e.last_name, count(e.last_name) lcount
FROM employees e
GROUP BY e.last_name
ORDER  BY lcount desc
LIMIT 20






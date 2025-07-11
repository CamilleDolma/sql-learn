以下是你请求的 Hive SQL 习题集的 **参考答案与解析**，每题都配有简要说明，帮助你理解背后的逻辑和语法。

---

## ✅ 模块一：基础语法与数据类型

### 1. 创建表
```sql
CREATE TABLE employees (
  id INT,
  name STRING,
  age INT,
  salary FLOAT,
  join_date DATE
);
```
**解析**：定义字段及其数据类型，Hive 支持常见 SQL 类型。

---

### 2. 插入数据
```sql
INSERT INTO employees VALUES
(1, 'Alice', 28, 5000.0, '2022-01-10'),
(2, 'Bob', 35, 7000.0, '2021-03-15'),
(3, 'Charlie', 40, 6500.0, '2020-07-20'),
(4, 'David', 25, 4800.0, '2023-05-01'),
(5, 'Eve', 30, 7200.0, '2019-11-11');
```

---

### 3. 查询姓名和工资
```sql
SELECT name, salary FROM employees;
```

---

### 4. 查询年龄大于 30 岁
```sql
SELECT * FROM employees WHERE age > 30;
```

---

### 5. 查询姓名包含 "li"
```sql
SELECT * FROM employees WHERE name LIKE '%li%';
```
**解析**：`%` 是通配符，表示任意字符。

---

## ✅ 模块二：聚合函数与分组

### 6. 每个年龄段员工数量
```sql
SELECT age, COUNT(*) AS num_employees
FROM employees
GROUP BY age;
```

---

### 7. 平均、最高、最低工资
```sql
SELECT 
  AVG(salary) AS avg_salary,
  MAX(salary) AS max_salary,
  MIN(salary) AS min_salary
FROM employees;
```

---

### 8. 工资总和大于 10000 的年龄段
```sql
SELECT age, SUM(salary) AS total_salary
FROM employees
GROUP BY age
HAVING SUM(salary) > 10000;
```

---

### 9. 平均工资大于 5000 的分组
```sql
SELECT age, AVG(salary) AS avg_salary
FROM employees
GROUP BY age
HAVING AVG(salary) > 5000;
```

---

## ✅ 模块三：连接操作（JOIN）

### 10. 创建部门表
```sql
CREATE TABLE departments (
  dept_id INT,
  dept_name STRING
);
```

---

### 11. 添加 `dept_id` 字段
```sql
ALTER TABLE employees ADD COLUMNS (dept_id INT);
```

插入数据示例：
```sql
INSERT INTO departments VALUES
(1, 'HR'), (2, 'Engineering'), (3, 'Marketing');

-- 更新员工表（Hive 不支持 UPDATE，需重新插入或使用临时表）
```

---

### 12. INNER JOIN
```sql
SELECT e.name, d.dept_name
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id;
```

---

### 13. LEFT JOIN
```sql
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id;
```

---

### 14. RIGHT JOIN
```sql
SELECT e.name, d.dept_name
FROM employees e
RIGHT JOIN departments d ON e.dept_id = d.dept_id;
```

---

## ✅ 模块四：窗口函数

### 15. 工资排名（按部门）
```sql
SELECT 
  name,
  dept_id,
  salary,
  RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS salary_rank
FROM employees;
```

---

### 16. 平均工资（按部门）
```sql
SELECT 
  name,
  dept_id,
  salary,
  AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg_salary
FROM employees;
```

---

### 17. 与部门内最高工资差值
```sql
SELECT 
  name,
  dept_id,
  salary,
  MAX(salary) OVER (PARTITION BY dept_id) - salary AS salary_gap
FROM employees;
```

---

## ✅ 模块五：子查询与嵌套查询

### 18. 工资高于公司平均工资
```sql
SELECT * FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

---

### 19. 工资最高的员工
```sql
SELECT * FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees);
```

---

### 20. 每个部门工资最高的员工
```sql
SELECT * FROM (
  SELECT *,
         RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
) t
WHERE rnk = 1;
```

---

## ✅ 模块六：数据清洗与转换

### 21. 年龄分类
```sql
SELECT name, age,
  CASE 
    WHEN age < 30 THEN '青年'
    WHEN age BETWEEN 30 AND 45 THEN '中年'
    ELSE '老年'
  END AS age_group
FROM employees;
```

---

### 22. 处理空值工资
```sql
SELECT name, COALESCE(salary, 0) AS salary FROM employees;
```

---

### 23. 提取姓名中的字母
```sql
SELECT name, REGEXP_EXTRACT(name, '[A-Za-z]+', 0) AS letters_only
FROM employees;
```

---

### 24. 转换工资为整数
```sql
SELECT name, CAST(salary AS INT) AS salary_int FROM employees;
```

---

## ✅ 模块七：分区与桶表

### 25. 创建分区表
```sql
CREATE TABLE employees_partitioned (
  id INT,
  name STRING,
  age INT,
  salary FLOAT,
  join_date DATE
)
PARTITIONED BY (dept_id INT);
```

---

### 26. 创建桶表
```sql
CREATE TABLE employees_bucketed (
  id INT,
  name STRING,
  age INT,
  salary FLOAT
)
CLUSTERED BY (age) INTO 4 BUCKETS;
```

---

### 27. 查询某个分区
```sql
SELECT * FROM employees_partitioned WHERE dept_id = 2;
```

---

### 28. 查询某个桶（需开启桶映射）
```sql
-- Hive 查询桶数据通常依赖 MapReduce，不能直接指定桶号查询
-- 可通过 `CLUSTER BY` 或 `DISTRIBUTE BY` 控制分桶行为
```

---

## ✅ 模块八：性能优化与实际应用

### 29. 查看执行计划
```sql
EXPLAIN SELECT * FROM employees WHERE salary > 6000;
```

---

### 30. 部门员工数量与平均工资
```sql
SELECT dept_id, COUNT(*) AS num_employees, AVG(salary) AS avg_salary
FROM employees
GROUP BY dept_id
ORDER BY avg_salary DESC;
```

---

如果你希望我将这些内容整理成一个 **PDF 文件或 Markdown 文档**，我可以立即帮你生成。是否需要我为你导出文件？
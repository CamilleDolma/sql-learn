太棒了！以下是你请求的 **高级 Hive SQL 应用题集的参考答案与解析**，共分为 6 个模块，每题都配有详细的 SQL 示例和解析说明，帮助你深入理解高级 SQL 技巧在数据挖掘中的应用。

---

## ✅ 模块一：复杂窗口函数与排名分析

### 1. 连续增长工资的员工识别
```sql
SELECT employee_id
FROM (
  SELECT employee_id, month, salary,
         LAG(salary, 1) OVER (PARTITION BY employee_id ORDER BY month) AS prev_salary_1,
         LAG(salary, 2) OVER (PARTITION BY employee_id ORDER BY month) AS prev_salary_2
  FROM monthly_salary
) t
WHERE salary > prev_salary_1 AND prev_salary_1 > prev_salary_2;
```
**解析**：使用 `LAG` 函数获取前两个月的工资，判断是否连续增长。

---

### 2. 工资百分位排名
```sql
SELECT employee_id, dept_id, salary,
       PERCENT_RANK() OVER (PARTITION BY dept_id ORDER BY salary) AS salary_percentile
FROM employees;
```
**解析**：`PERCENT_RANK()` 返回当前行在分组中的百分位排名。

---

### 3. 入职时间排名与工资差异
```sql
SELECT dept_id,
       MAX(CASE WHEN rnk = 1 THEN salary END) AS earliest_salary,
       MAX(CASE WHEN rnk = last_rnk THEN salary END) AS latest_salary,
       MAX(CASE WHEN rnk = last_rnk THEN salary END) - MAX(CASE WHEN rnk = 1 THEN salary END) AS salary_diff
FROM (
  SELECT *,
         RANK() OVER (PARTITION BY dept_id ORDER BY join_date ASC) AS rnk,
         COUNT(*) OVER (PARTITION BY dept_id) AS last_rnk
  FROM employees
) t
GROUP BY dept_id;
```
**解析**：使用 `RANK` 和 `COUNT` 获取最早和最晚入职员工的工资。

---

## ✅ 模块二：多层嵌套查询与复杂逻辑

### 4. 工资高于部门平均工资的员工
```sql
SELECT * FROM employees e
WHERE salary > (
  SELECT AVG(salary) FROM employees WHERE dept_id = e.dept_id
);
```
**解析**：子查询按部门计算平均工资。

---

### 5. 工资排名前 10% 的员工
```sql
SELECT * FROM (
  SELECT *, NTILE(10) OVER (ORDER BY salary DESC) AS decile
  FROM employees
) t
WHERE decile = 1;
```
**解析**：`NTILE(10)` 将数据分为 10 组，取第 1 组即前 10%。

---

### 6. 连续两个月工资下降的员工
```sql
SELECT employee_id
FROM (
  SELECT employee_id, month, salary,
         LAG(salary, 1) OVER (PARTITION BY employee_id ORDER BY month) AS prev_salary_1,
         LAG(salary, 2) OVER (PARTITION BY employee_id ORDER BY month) AS prev_salary_2
  FROM monthly_salary
) t
WHERE salary < prev_salary_1 AND prev_salary_1 < prev_salary_2;
```

---

## ✅ 模块三：数据质量检查与异常检测

### 7. 检测重复记录
```sql
SELECT name, join_date, COUNT(*) AS cnt
FROM employees
GROUP BY name, join_date
HAVING COUNT(*) > 1;
```

---

### 8. 工资异常值（高于 3 倍中位数）
```sql
WITH salary_stats AS (
  SELECT percentile(salary, 0.5) AS median_salary FROM employees
)
SELECT e.*
FROM employees e
JOIN salary_stats s ON e.salary > 3 * s.median_salary;
```
**解析**：使用 `percentile()` 计算中位数。

---

### 9. 部门员工数量异常
```sql
SELECT dept_id, COUNT(*) AS num_employees
FROM employees
GROUP BY dept_id
HAVING COUNT(*) < 2 OR COUNT(*) > 100;
```

---

## ✅ 模块四：ETL 与数据转换逻辑

### 10. 按年龄段和部门汇总
```sql
SELECT dept_id,
       CASE 
         WHEN age < 30 THEN '青年'
         WHEN age BETWEEN 30 AND 45 THEN '中年'
         ELSE '老年'
       END AS age_group,
       COUNT(*) AS employee_count,
       AVG(salary) AS avg_salary
FROM employees
GROUP BY dept_id, 
         CASE 
           WHEN age < 30 THEN '青年'
           WHEN age BETWEEN 30 AND 45 THEN '中年'
           ELSE '老年'
         END;
```

---

### 11. 转换为季度并统计入职人数
```sql
SELECT CONCAT(YEAR(join_date), 'Q', CEIL(MONTH(join_date)/3)) AS quarter,
       COUNT(*) AS num_joins
FROM employees
GROUP BY CONCAT(YEAR(join_date), 'Q', CEIL(MONTH(join_date)/3));
```

---

### 12. 工资标准化为 Z 分数
```sql
WITH stats AS (
  SELECT AVG(salary) AS mean_salary, STDDEV(salary) AS std_salary FROM employees
)
SELECT e.*, 
       (e.salary - s.mean_salary) / s.std_salary AS z_score
FROM employees e
JOIN stats s ON TRUE
WHERE (e.salary - s.mean_salary) / s.std_salary > 2;
```

---

## ✅ 模块五：性能优化与资源控制

### 13. 查看执行计划
```sql
EXPLAIN
SELECT d.dept_name, AVG(e.salary)
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
GROUP BY d.dept_name;
```

---

### 14. 使用 MAPJOIN 优化连接
```sql
SET hive.auto.convert.join=true;

SELECT /*+ MAPJOIN(departments) */ e.name, d.dept_name
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id;
```
**解析**：适用于小表连接大表的场景。

---

### 15. 使用 DISTRIBUTE BY 和 SORT BY
```sql
SELECT name, salary
FROM employees
DISTRIBUTE BY dept_id
SORT BY salary DESC;
```
**解析**：`DISTRIBUTE BY` 控制数据分布，`SORT BY` 控制每个 reducer 内排序。

---

## ✅ 模块六：数据建模与分区策略设计

### 16. 分区 + 桶表设计
```sql
CREATE TABLE employees_partitioned_bucketed (
  id INT,
  name STRING,
  age INT,
  salary FLOAT,
  join_date DATE
)
PARTITIONED BY (dept_id INT, year INT)
CLUSTERED BY (age) INTO 5 BUCKETS;
```

---

### 17. 工资增长率统计
```sql
WITH last_year AS (
  SELECT employee_id, dept_id, salary
  FROM salary_history
  WHERE year = 2024
),
this_year AS (
  SELECT employee_id, dept_id, salary
  FROM salary_history
  WHERE year = 2025
)
SELECT t.dept_id,
       AVG((t.salary - l.salary) / l.salary) AS avg_growth_rate
FROM this_year t
JOIN last_year l ON t.employee_id = l.employee_id
GROUP BY t.dept_id;
```

---

### 18. 合并年度员工表
```sql
SELECT * FROM employees_2023
UNION ALL
SELECT * FROM employees_2024
UNION ALL
SELECT * FROM employees_2025;
```

统计：
```sql
SELECT COUNT(*) AS total_employees, AVG(salary) AS avg_salary
FROM (
  SELECT * FROM employees_2023
  UNION ALL
  SELECT * FROM employees_2024
  UNION ALL
  SELECT * FROM employees_2025
) t;
```

---

如果你希望我将这份完整的题集和答案导出为 **PDF 或 Markdown 文件**，我可以立即帮你生成。是否需要我为你创建一个文件？
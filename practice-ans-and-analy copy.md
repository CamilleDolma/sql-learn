以下是你请求的 Hive SQL 实战题集的 **参考答案与解析**，共分为 5 个场景，每题都配有 SQL 示例和简要说明，帮助你理解在真实业务场景中如何应用 Hive SQL。

---

## 🧪 Hive SQL 实战题参考答案与解析

---

### ✅ 场景一：员工绩效分析

#### 1. 查询每位员工最近一年的绩效评分
```sql
SELECT p.id, p.year, p.rating
FROM performance p
JOIN (
  SELECT id, MAX(year) AS latest_year
  FROM performance
  GROUP BY id
) latest ON p.id = latest.id AND p.year = latest.latest_year;
```
**解析**：使用子查询获取每位员工的最新年份，再与原表连接。

---

#### 2. 查询连续两年绩效评分为 5 的员工
```sql
SELECT id
FROM (
  SELECT id, year, rating,
         LAG(rating) OVER (PARTITION BY id ORDER BY year) AS prev_rating
  FROM performance
) t
WHERE rating = 5 AND prev_rating = 5;
```
**解析**：使用 `LAG` 获取前一年评分，判断是否连续为 5。

---

#### 3. 查询每个部门的平均绩效评分（按年统计）
```sql
SELECT e.dept_id, p.year, AVG(p.rating) AS avg_rating
FROM employees e
JOIN performance p ON e.id = p.id
GROUP BY e.dept_id, p.year;
```

---

#### 4. 查询绩效评分为 1 的员工，并统计他们的工资是否低于部门平均水平
```sql
SELECT e.id, e.name, e.salary, dept_avg.avg_salary
FROM employees e
JOIN (
  SELECT dept_id, AVG(salary) AS avg_salary
  FROM employees
  GROUP BY dept_id
) dept_avg ON e.dept_id = dept_avg.dept_id
JOIN performance p ON e.id = p.id
WHERE p.rating = 1 AND e.salary < dept_avg.avg_salary;
```

---

#### 5. 查询绩效评分提升最多的员工
```sql
SELECT id, rating - prev_rating AS rating_diff
FROM (
  SELECT id, year, rating,
         LAG(rating) OVER (PARTITION BY id ORDER BY year) AS prev_rating
  FROM performance
) t
WHERE prev_rating IS NOT NULL
ORDER BY rating_diff DESC
LIMIT 1;
```

---

### ✅ 场景二：用户行为分析

#### 6. 查询每天的活跃用户数
```sql
SELECT DATE(action_time) AS day, COUNT(DISTINCT user_id) AS active_users
FROM user_actions
WHERE action_type = 'login'
GROUP BY DATE(action_time);
```

---

#### 7. 查询每位用户的首次购买时间
```sql
SELECT user_id, MIN(action_time) AS first_purchase
FROM user_actions
WHERE action_type = 'purchase'
GROUP BY user_id;
```

---

#### 8. 查询用户在登录后 1 小时内完成购买的比例
```sql
WITH logins AS (
  SELECT user_id, action_time AS login_time
  FROM user_actions
  WHERE action_type = 'login'
),
purchases AS (
  SELECT user_id, action_time AS purchase_time
  FROM user_actions
  WHERE action_type = 'purchase'
)
SELECT COUNT(*) AS total_logins,
       COUNT(p.user_id) AS purchases_within_1hr,
       COUNT(p.user_id) * 1.0 / COUNT(*) AS ratio
FROM logins l
LEFT JOIN purchases p ON l.user_id = p.user_id AND p.purchase_time BETWEEN l.login_time AND l.login_time + INTERVAL 1 HOUR;
```

---

#### 9. 查询连续三天都有登录行为的用户
```sql
SELECT user_id
FROM (
  SELECT user_id, DATE(action_time) AS login_day
  FROM user_actions
  WHERE action_type = 'login'
  GROUP BY user_id, DATE(action_time)
) t
WINDOW w AS (PARTITION BY user_id ORDER BY login_day)
SELECT user_id
FROM (
  SELECT user_id, login_day,
         LAG(login_day, 1) OVER w AS day1,
         LAG(login_day, 2) OVER w AS day2
  FROM t
) x
WHERE DATEDIFF(login_day, day1) = 1 AND DATEDIFF(day1, day2) = 1;
```

---

#### 10. 查询每种行为的日均发生次数
```sql
SELECT action_type, COUNT(*) / COUNT(DISTINCT DATE(action_time)) AS avg_daily_count
FROM user_actions
GROUP BY action_type;
```

---

### ✅ 场景三：电商订单分析

#### 11. 查询每个用户的总订单金额
```sql
SELECT user_id, SUM(amount) AS total_spent
FROM orders
GROUP BY user_id;
```

---

#### 12. 查询每个商品类别的销售总额
```sql
SELECT p.category, SUM(oi.quantity * p.price) AS total_sales
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category;
```

---

#### 13. 查询退货订单的比例
```sql
SELECT COUNT(*) FILTER (WHERE status = 'returned') * 1.0 / COUNT(*) AS return_rate
FROM orders;
```

---

#### 14. 查询每月的订单增长率
```sql
WITH monthly_orders AS (
  SELECT DATE_FORMAT(order_date, 'yyyy-MM') AS month, COUNT(*) AS order_count
  FROM orders
  GROUP BY DATE_FORMAT(order_date, 'yyyy-MM')
)
SELECT month, order_count,
       order_count - LAG(order_count) OVER (ORDER BY month) AS growth,
       (order_count - LAG(order_count) OVER (ORDER BY month)) * 1.0 / LAG(order_count) OVER (ORDER BY month) AS growth_rate
FROM monthly_orders;
```

---

#### 15. 查询购买最多的商品
```sql
SELECT product_id, SUM(quantity) AS total_quantity
FROM order_items
GROUP BY product_id
ORDER BY total_quantity DESC
LIMIT 1;
```

---

### ✅ 场景四：数据质量与异常检测

假设客户数据表结构如下：

```sql
customers(id, name, email, age, signup_date)
```

---

#### 1. 查询重复的邮箱地址

```sql
SELECT email, COUNT(*) AS cnt
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;
```

**解析**：使用 `GROUP BY` 和 `HAVING` 筛选重复邮箱。

---

#### 2. 查询年龄字段中异常值（如 < 10 或 > 100）

```sql
SELECT *
FROM customers
WHERE age < 10 OR age > 100;
```

**解析**：直接使用 `WHERE` 条件筛选年龄异常值。

---

#### 3. 查询注册日期为空或格式错误的记录

```sql
SELECT *
FROM customers
WHERE signup_date IS NULL
   OR signup_date NOT RLIKE '^\\d{4}-\\d{2}-\\d{2}$';
```

**解析**：使用 `RLIKE` 正则表达式检查日期格式是否为 `YYYY-MM-DD`。

---

### 4. 使用正则表达式筛选出非法邮箱格式

```sql
SELECT *
FROM customers
WHERE email NOT RLIKE '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$';
```

**解析**：使用 Hive 的 `RLIKE` 匹配邮箱格式，注意转义点号 `\\.`。

---

### 5. 查询每月新增客户数，并识别增长异常的月份

#### 每月新增客户数：

```sql
SELECT date_format(signup_date, 'yyyy-MM') AS month,
       COUNT(*) AS new_customers
FROM customers
GROUP BY date_format(signup_date, 'yyyy-MM')
ORDER BY month;
```

#### 增长异常（增长率 > 50% 或 < -50%）：

```sql
WITH monthly_growth AS (
  SELECT date_format(signup_date, 'yyyy-MM') AS month,
         COUNT(*) AS new_customers
  FROM customers
  GROUP BY date_format(signup_date, 'yyyy-MM')
),
growth_rate AS (
  SELECT curr.month,
         curr.new_customers,
         prev.new_customers AS prev_customers,
         ROUND((curr.new_customers - prev.new_customers) / prev.new_customers * 100, 2) AS growth_rate
  FROM monthly_growth curr
  JOIN monthly_growth prev
    ON curr.month = date_format(add_months(concat(prev.month, '-01'), 1), 'yyyy-MM')
)
SELECT *
FROM growth_rate
WHERE growth_rate > 50 OR growth_rate < -50;
```

---

### ✅ 场景五：趋势与预测准备

假设销售记录表结构如下：

```sql
sales(date, region, product_id, quantity, revenue)
```

---

#### 1. 查询每个地区每月的销售总额

```sql
SELECT region,
       date_format(date, 'yyyy-MM') AS month,
       SUM(revenue) AS total_revenue
FROM sales
GROUP BY region, date_format(date, 'yyyy-MM')
ORDER BY region, month;
```

---

#### 2. 查询销售额同比增长率（今年 vs 去年）

```sql
WITH monthly_sales AS (
  SELECT year(date) AS year,
         month(date) AS month_num,
         SUM(revenue) AS total_revenue
  FROM sales
  GROUP BY year(date), month(date)
),
yearly_comparison AS (
  SELECT curr.year AS current_year,
         curr.month_num,
         curr.total_revenue AS current_revenue,
         prev.total_revenue AS previous_revenue,
         ROUND((curr.total_revenue - prev.total_revenue) / prev.total_revenue * 100, 2) AS yoy_growth
  FROM monthly_sales curr
  JOIN monthly_sales prev
    ON curr.month_num = prev.month_num AND curr.year = prev.year + 1
)
SELECT *
FROM yearly_comparison;
```

---

#### 3. 查询销售额环比增长率（本月 vs 上月）

```sql
WITH monthly_sales AS (
  SELECT date_format(date, 'yyyy-MM') AS month,
         SUM(revenue) AS total_revenue
  FROM sales
  GROUP BY date_format(date, 'yyyy-MM')
),
month_over_month AS (
  SELECT curr.month,
         curr.total_revenue AS current_revenue,
         prev.total_revenue AS previous_revenue,
         ROUND((curr.total_revenue - prev.total_revenue) / prev.total_revenue * 100, 2) AS mom_growth
  FROM monthly_sales curr
  JOIN monthly_sales prev
    ON curr.month = date_format(add_months(concat(prev.month, '-01'), 1), 'yyyy-MM')
)
SELECT *
FROM month_over_month;
```

---

#### 4. 查询销售额连续三个月增长的产品

```sql
WITH monthly_product_sales AS (
  SELECT product_id,
         date_format(date, 'yyyy-MM') AS month,
         SUM(revenue) AS total_revenue
  FROM sales
  GROUP BY product_id, date_format(date, 'yyyy-MM')
),
ranked_sales AS (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY month) AS rn
  FROM monthly_product_sales
),
growth_check AS (
  SELECT a.product_id
  FROM ranked_sales a
  JOIN ranked_sales b ON a.product_id = b.product_id AND a.rn = b.rn - 1
  JOIN ranked_sales c ON a.product_id = c.product_id AND a.rn = c.rn - 2
  WHERE a.total_revenue < b.total_revenue AND b.total_revenue < c.total_revenue
)
SELECT DISTINCT product_id
FROM growth_check;
```

---

#### 5. 查询销售额下降超过 30% 的地区和月份

```sql
WITH monthly_sales AS (
  SELECT region,
         date_format(date, 'yyyy-MM') AS month,
         SUM(revenue) AS total_revenue
  FROM sales
  GROUP BY region, date_format(date, 'yyyy-MM')
),
decline_check AS (
  SELECT curr.region,
         curr.month,
         curr.total_revenue AS current_revenue,
         prev.total_revenue AS previous_revenue,
         ROUND((curr.total_revenue - prev.total_revenue) / prev.total_revenue * 100, 2) AS decline_rate
  FROM monthly_sales curr
  JOIN monthly_sales prev
    ON curr.region = prev.region AND curr.month = date_format(add_months(concat(prev.month, '-01'), 1), 'yyyy-MM')
)
SELECT *
FROM decline_check
WHERE decline_rate < -30;
```

好的，我们就以 **Hive SQL** 为蓝本，进行一套系统、详细、实例丰富的 **SQL 教学**。Hive SQL 是基于 Hadoop 的数据仓库工具，语法上与标准 SQL 类似，但也有其独特之处。我们将从基础语法开始，逐步深入到复杂查询、窗口函数、分区与分桶等高级特性。

---

## 🧭 教学结构总览

我们将按以下模块进行讲解，每个模块都配有实例和语法细节说明：

1. **基础语法与数据类型**
2. **建表与数据导入**
3. **基本查询（SELECT）**
4. **WHERE 条件过滤**
5. **GROUP BY 与聚合函数**
6. **JOIN 多表连接**
7. **子查询与 WITH 子句**
8. **窗口函数（OVER）**
9. **分区表与分桶表**
10. **视图与临时表**
11. **Hive 特有语法与优化技巧**

---

## 📘 第1章：基础语法与数据类型

### 1.1 SQL 基本结构

Hive SQL 的基本查询结构如下：

```sql
SELECT column1, column2
FROM table_name
WHERE condition
GROUP BY column
ORDER BY column
LIMIT n;
```

### 1.2 常见数据类型

| 类型         | 描述                         |
|--------------|------------------------------|
| `INT`        | 整数                         |
| `BIGINT`     | 长整型                       |
| `FLOAT`      | 单精度浮点数                 |
| `DOUBLE`     | 双精度浮点数                 |
| `STRING`     | 字符串                       |
| `BOOLEAN`    | 布尔值（TRUE/FALSE）         |
| `TIMESTAMP`  | 时间戳                       |
| `DATE`       | 日期                         |
| `ARRAY<T>`   | 数组                         |
| `MAP<K,V>`   | 键值对                       |
| `STRUCT`     | 结构体（类似 JSON 对象）     |

---

## 📌 示例：创建一个简单的表

```sql
CREATE TABLE employees (
  id INT,
  name STRING,
  age INT,
  salary DOUBLE,
  hire_date DATE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

### 说明：

- `ROW FORMAT DELIMITED`：指定字段分隔符。
- `FIELDS TERMINATED BY ','`：字段之间用逗号分隔。
- `STORED AS TEXTFILE`：以文本文件格式存储。

---

## ✅ 小练习

你可以尝试回答以下问题来巩固：

1. Hive 中 `BIGINT` 和 `INT` 有什么区别？
2. 如果你要存储员工的多个电话号码，应该使用哪种数据类型？
3. Hive 中如何指定字段分隔符为制表符（Tab）？

---

我可以继续讲解下一章：**建表与数据导入**，你想继续吗？或者你有特定的模块想先学？


好的，我们就以 **Hive SQL** 为蓝本，进行一套系统、详细、实例丰富的 **SQL 教学**。Hive SQL 是基于 Hadoop 的数据仓库工具，语法上与标准 SQL 类似，但也有其独特之处。我们将从基础语法开始，逐步深入到复杂查询、窗口函数、分区与分桶等高级特性。

---

## 🧭 教学结构总览

我们将按以下模块进行讲解，每个模块都配有实例和语法细节说明：

1. **基础语法与数据类型**
2. **建表与数据导入**
3. **基本查询（SELECT）**
4. **WHERE 条件过滤**
5. **GROUP BY 与聚合函数**
6. **JOIN 多表连接**
7. **子查询与 WITH 子句**
8. **窗口函数（OVER）**
9. **分区表与分桶表**
10. **视图与临时表**
11. **Hive 特有语法与优化技巧**

---

## 📘 第1章：基础语法与数据类型

### 1.1 SQL 基本结构

Hive SQL 的基本查询结构如下：

```sql
SELECT column1, column2
FROM table_name
WHERE condition
GROUP BY column
ORDER BY column
LIMIT n;
```

### 1.2 常见数据类型

| 类型         | 描述                         |
|--------------|------------------------------|
| `INT`        | 整数                         |
| `BIGINT`     | 长整型                       |
| `FLOAT`      | 单精度浮点数                 |
| `DOUBLE`     | 双精度浮点数                 |
| `STRING`     | 字符串                       |
| `BOOLEAN`    | 布尔值（TRUE/FALSE）         |
| `TIMESTAMP`  | 时间戳                       |
| `DATE`       | 日期                         |
| `ARRAY<T>`   | 数组                         |
| `MAP<K,V>`   | 键值对                       |
| `STRUCT`     | 结构体（类似 JSON 对象）     |

---

## 📌 示例：创建一个简单的表

```sql
CREATE TABLE employees (
  id INT,
  name STRING,
  age INT,
  salary DOUBLE,
  hire_date DATE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

### 说明：

- `ROW FORMAT DELIMITED`：指定字段分隔符。
- `FIELDS TERMINATED BY ','`：字段之间用逗号分隔。
- `STORED AS TEXTFILE`：以文本文件格式存储。

---

## ✅ 小练习

你可以尝试回答以下问题来巩固：

1. Hive 中 `BIGINT` 和 `INT` 有什么区别？
2. 如果你要存储员工的多个电话号码，应该使用哪种数据类型？
3. Hive 中如何指定字段分隔符为制表符（Tab）？

---

我可以继续讲解下一章：**建表与数据导入**，你想继续吗？或者你有特定的模块想先学？


好的，我们继续进入第3章：**基本查询（SELECT）**。这是 Hive SQL 中最常用的语法之一，用于从表中提取数据。我们将详细讲解字段选择、别名、表达式、去重、排序等内容。

---

## 📘 第3章：基本查询（SELECT）

### 3.1 查询所有字段

```sql
SELECT * FROM students;
```

- `*` 表示选择所有字段。
- 通常用于快速查看表内容。

---

### 3.2 查询指定字段

```sql
SELECT id, name, age FROM students;
```

- 只选择需要的字段，避免不必要的数据加载。

---

### 3.3 使用字段别名（AS）

```sql
SELECT name AS student_name, age AS student_age FROM students;
```

- `AS` 用于给字段起别名，便于阅读或后续处理。
- Hive 中 `AS` 是可选的，也可以写成：`SELECT name student_name`

---

### 3.4 使用表达式计算新字段

```sql
SELECT name, age, age + 1 AS age_next_year FROM students;
```

- 可以在查询中使用算术运算。
- 支持 `+`, `-`, `*`, `/` 等基本运算符。

---

### 3.5 去重查询（DISTINCT）

```sql
SELECT DISTINCT grade FROM students;
```

- 返回唯一的 `grade` 值。
- 常用于统计分类字段的种类。

---

### 3.6 排序查询（ORDER BY）

```sql
SELECT name, age FROM students
ORDER BY age ASC;
```

- `ORDER BY` 用于排序。
- `ASC`：升序（默认），`DESC`：降序。

---

### 3.7 限制返回行数（LIMIT）

```sql
SELECT * FROM students
LIMIT 5;
```

- 只返回前5行数据。
- 常用于调试或预览数据。

---

### 3.8 条件表达式（CASE WHEN）

```sql
SELECT name,
       age,
       CASE
         WHEN age < 18 THEN 'Minor'
         WHEN age >= 18 AND age < 60 THEN 'Adult'
         ELSE 'Senior'
       END AS age_group
FROM students;
```

- `CASE WHEN` 用于实现条件逻辑。
- 类似于编程语言中的 `if-else`。

---

### ✅ 小练习题

1. 如何查询所有学生的姓名和年龄，并将年龄加5后显示为新字段？
2. 如何查询所有不同的年级（grade）？
3. 如何按年龄从大到小排序，并只显示前10名学生？

---

下一章我们将讲解 **WHERE 条件过滤**，用于筛选满足特定条件的数据。如果你有自己的数据表结构或想练习写查询语句，也可以告诉我，我来帮你分析和优化。是否继续？


非常好，我们继续进入第4章：**WHERE 条件过滤**。这是 SQL 查询中最重要的部分之一，用于从表中筛选出满足特定条件的记录。

---

## 📘 第4章：WHERE 条件过滤

### 4.1 基本语法

```sql
SELECT column1, column2
FROM table_name
WHERE condition;
```

- `WHERE` 子句用于指定筛选条件。
- 只返回满足条件的记录。

---

### 4.2 常见比较运算符

| 运算符 | 说明           | 示例                      |
|--------|----------------|---------------------------|
| `=`    | 等于           | `age = 18`                |
| `!=` 或 `<>` | 不等于     | `grade != 'A'`            |
| `>`    | 大于           | `salary > 5000`           |
| `<`    | 小于           | `age < 30`                |
| `>=`   | 大于等于       | `age >= 18`               |
| `<=`   | 小于等于       | `age <= 60`               |

---

### 4.3 逻辑运算符

| 运算符 | 说明           | 示例                                      |
|--------|----------------|-------------------------------------------|
| `AND`  | 与（同时满足） | `age > 18 AND grade = 'A'`                |
| `OR`   | 或（满足其一） | `grade = 'A' OR grade = 'B'`              |
| `NOT`  | 非（取反）     | `NOT (grade = 'F')`                       |

---

### 4.4 范围查询（BETWEEN）

```sql
SELECT * FROM students
WHERE age BETWEEN 18 AND 25;
```

- 包含边界：等价于 `age >= 18 AND age <= 25`

---

### 4.5 集合查询（IN）

```sql
SELECT * FROM students
WHERE grade IN ('A', 'B', 'C');
```

- 等价于多个 `OR` 条件：`grade = 'A' OR grade = 'B' OR grade = 'C'`

---

### 4.6 模糊匹配（LIKE）

```sql
SELECT * FROM students
WHERE name LIKE 'J%';
```

- `%` 表示任意长度的任意字符。
- `_` 表示任意单个字符。
- 示例：`'J%'` 匹配以 J 开头的名字，如 "John", "Jane"

---

### 4.7 空值判断（IS NULL / IS NOT NULL）

```sql
SELECT * FROM students
WHERE grade IS NULL;
```

- 用于判断字段是否为空。
- Hive 中不能使用 `= NULL`，必须使用 `IS NULL`

---

### ✅ 综合示例

```sql
SELECT name, age, grade
FROM students
WHERE age >= 18
  AND grade IN ('A', 'B')
  AND name LIKE 'J%'
  AND grade IS NOT NULL;
```

---

### ✅ 小练习题

1. 查询年龄在 20 到 30 岁之间的学生。
2. 查询 grade 不为 'F' 且 age 小于 18 的学生。
3. 查询名字以 "A" 开头，且 grade 字段为空的学生。

---

下一章我们将讲解 **GROUP BY 与聚合函数**，用于统计、分组和汇总数据。如果你有自己的数据结构或想练习写 WHERE 查询语句，也可以告诉我，我来帮你分析和优化。是否继续？



非常棒，我们继续进入第5章：**GROUP BY 与聚合函数**。这是 Hive SQL 中用于数据统计和分组分析的核心语法，适用于报表、数据分析、业务指标计算等场景。

---

## 📘 第5章：GROUP BY 与聚合函数

### 5.1 什么是 GROUP BY？

`GROUP BY` 用于将数据按某个字段分组，然后对每组数据进行聚合计算。

---

### 5.2 常见聚合函数

| 函数        | 说明                         | 示例                          |
|-------------|------------------------------|-------------------------------|
| `COUNT()`   | 计数                         | `COUNT(*)`, `COUNT(name)`     |
| `SUM()`     | 求和                         | `SUM(salary)`                 |
| `AVG()`     | 平均值                       | `AVG(age)`                    |
| `MAX()`     | 最大值                       | `MAX(score)`                  |
| `MIN()`     | 最小值                       | `MIN(score)`                  |

---

### 5.3 基本示例：按年级统计人数

```sql
SELECT grade, COUNT(*) AS student_count
FROM students
GROUP BY grade;
```

- 将学生按 `grade` 分组。
- 每组统计人数。

---

### 5.4 多字段分组

```sql
SELECT grade, age, COUNT(*) AS count
FROM students
GROUP BY grade, age;
```

- 按 `grade` 和 `age` 组合分组。
- 每组统计人数。

---

### 5.5 使用聚合函数计算平均值、最大值等

```sql
SELECT grade,
       AVG(age) AS avg_age,
       MAX(age) AS max_age,
       MIN(age) AS min_age
FROM students
GROUP BY grade;
```

- 每个年级的平均年龄、最大年龄、最小年龄。

---

### 5.6 使用 HAVING 筛选分组结果

`HAVING` 用于对分组后的结果进行过滤（类似 `WHERE`，但用于聚合之后）。

```sql
SELECT grade, COUNT(*) AS student_count
FROM students
GROUP BY grade
HAVING COUNT(*) > 10;
```

- 只显示人数超过10的年级。

---

### 5.7 GROUP BY 与 ORDER BY 联合使用

```sql
SELECT grade, COUNT(*) AS student_count
FROM students
GROUP BY grade
ORDER BY student_count DESC;
```

- 按人数降序排列分组结果。

---

### ✅ 综合示例

```sql
SELECT grade,
       COUNT(*) AS total_students,
       AVG(age) AS average_age,
       MAX(age) AS oldest,
       MIN(age) AS youngest
FROM students
GROUP BY grade
HAVING AVG(age) > 20
ORDER BY total_students DESC;
```

---

### ✅ 小练习题

1. 查询每个年级的学生人数。
2. 查询每个年级的平均年龄，并只显示平均年龄大于 18 的年级。
3. 查询每个年级中年龄最大的学生年龄，并按降序排列。

---

下一章我们将讲解 **JOIN 多表连接**，这是处理多个数据表时不可或缺的技能。如果你有自己的数据结构或想练习 GROUP BY 查询语句，也可以告诉我，我来帮你分析和优化。是否继续？


非常好，我们继续进入第6章：**JOIN 多表连接**。在实际业务中，数据往往分布在多个表中，JOIN 是将这些表关联起来的关键操作。Hive SQL 支持多种连接方式，语法与标准 SQL 类似。

---

## 📘 第6章：JOIN 多表连接

### 6.1 JOIN 的基本语法

```sql
SELECT a.column1, b.column2
FROM table_a a
JOIN table_b b
ON a.id = b.id;
```

- `JOIN`：默认是 **INNER JOIN**，只返回两个表中匹配的记录。
- `ON`：指定连接条件。

---

### 6.2 JOIN 类型一览

| 类型           | 描述                                                                 |
|----------------|----------------------------------------------------------------------|
| `INNER JOIN`   | 只返回两个表中连接字段匹配的记录                                     |
| `LEFT JOIN`    | 返回左表所有记录，右表匹配不到的字段为 NULL                         |
| `RIGHT JOIN`   | 返回右表所有记录，左表匹配不到的字段为 NULL                         |
| `FULL OUTER JOIN` | 返回两个表所有记录，匹配不到的字段为 NULL                       |
| `CROSS JOIN`   | 笛卡尔积，返回两个表所有组合（慎用）                                 |

---

### 6.3 示例：INNER JOIN

```sql
SELECT s.name, s.age, c.course_name
FROM students s
JOIN courses c
ON s.id = c.student_id;
```

- 查询学生姓名、年龄及所选课程。
- 只返回有课程记录的学生。

---

### 6.4 示例：LEFT JOIN

```sql
SELECT s.name, c.course_name
FROM students s
LEFT JOIN courses c
ON s.id = c.student_id;
```

- 返回所有学生，即使他们没有选课。
- 没有课程的学生 `course_name` 为 NULL。

---

### 6.5 示例：RIGHT JOIN

```sql
SELECT s.name, c.course_name
FROM students s
RIGHT JOIN courses c
ON s.id = c.student_id;
```

- 返回所有课程记录，即使没有对应学生信息。

---

### 6.6 示例：FULL OUTER JOIN

```sql
SELECT s.name, c.course_name
FROM students s
FULL OUTER JOIN courses c
ON s.id = c.student_id;
```

- 返回所有学生和所有课程记录。
- 没有匹配的字段为 NULL。

---

### 6.7 多表连接（链式 JOIN）

```sql
SELECT s.name, c.course_name, t.teacher_name
FROM students s
JOIN courses c ON s.id = c.student_id
JOIN teachers t ON c.teacher_id = t.id;
```

- 三表连接：学生 → 课程 → 教师。

---

### 6.8 使用别名简化查询

```sql
SELECT s.name, c.course_name
FROM students AS s
JOIN courses AS c
ON s.id = c.student_id;
```

- 使用 `AS` 给表起别名，简化字段引用。

---

### ✅ 小练习题

1. 查询所有学生及其课程（包括没有选课的学生）。
2. 查询所有课程及其对应学生（包括没有学生的课程）。
3. 查询学生、课程和授课教师的完整信息。

---

下一章我们将讲解 **子查询与 WITH 子句**，用于构建更复杂的查询逻辑。如果你有自己的表结构或想练习 JOIN 查询语句，也可以告诉我，我来帮你分析和优化。是否继续？



非常好，我们继续进入第7章：**子查询与 WITH 子句（公共表表达式）**。这是构建复杂 SQL 查询的重要工具，能让你将查询逻辑模块化、分层处理，提升可读性和复用性。

---

## 📘 第7章：子查询与 WITH 子句

---

### 7.1 什么是子查询？

子查询是嵌套在其他 SQL 查询中的查询语句，通常用于：

- 作为筛选条件
- 作为虚拟表参与 JOIN
- 用于聚合或排序前的预处理

---

### 7.2 子查询作为筛选条件

```sql
SELECT name, age
FROM students
WHERE age > (
  SELECT AVG(age)
  FROM students
);
```

- 查询年龄高于平均年龄的学生。
- 子查询返回一个标量值。

---

### 7.3 子查询作为虚拟表参与 JOIN

```sql
SELECT s.name, avg_scores.avg_score
FROM students s
JOIN (
  SELECT student_id, AVG(score) AS avg_score
  FROM scores
  GROUP BY student_id
) avg_scores
ON s.id = avg_scores.student_id;
```

- 子查询先计算每个学生的平均分。
- 主查询再与学生表连接。

---

### 7.4 使用 IN 的子查询

```sql
SELECT name
FROM students
WHERE id IN (
  SELECT student_id
  FROM scores
  WHERE score > 90
);
```

- 查询成绩超过90分的学生姓名。

---

### 7.5 使用 EXISTS 的子查询

```sql
SELECT name
FROM students s
WHERE EXISTS (
  SELECT 1
  FROM scores sc
  WHERE sc.student_id = s.id AND sc.score > 90
);
```

- 与 `IN` 类似，但性能在某些场景更优。

---

## 📘 WITH 子句（公共表表达式）

### 7.6 什么是 WITH 子句？

`WITH` 子句用于定义一个临时的命名子查询，供主查询使用。它可以让复杂查询更清晰。

---

### 7.7 基本语法

```sql
WITH avg_scores AS (
  SELECT student_id, AVG(score) AS avg_score
  FROM scores
  GROUP BY student_id
)
SELECT s.name, avg_scores.avg_score
FROM students s
JOIN avg_scores
ON s.id = avg_scores.student_id;
```

- `avg_scores` 是一个临时表。
- 可以像普通表一样参与 JOIN。

---

### 7.8 多个 WITH 子句

```sql
WITH
  high_scores AS (
    SELECT student_id, score
    FROM scores
    WHERE score > 90
  ),
  student_info AS (
    SELECT id, name
    FROM students
  )
SELECT si.name, hs.score
FROM student_info si
JOIN high_scores hs
ON si.id = hs.student_id;
```

- 可以定义多个子查询。
- 每个子查询都可以复用，提高可读性。

---

### ✅ 小练习题

1. 查询所有成绩高于平均分的学生姓名。
2. 使用 WITH 子句查询每个学生的平均分，并显示学生姓名和平均分。
3. 使用子查询找出选修课程数量最多的学生。

---

下一章我们将讲解 **窗口函数（OVER）**，用于实现排名、累计、分组内统计等高级分析功能。如果你有自己的业务场景或数据结构，也可以告诉我，我来帮你设计子查询或 WITH 子句。是否继续？


好的，我们跳过第8章的**窗口函数（OVER）**，继续进入第9章：**分区表与分桶表**。这是 Hive 中非常重要的性能优化手段，尤其在处理大规模数据时，合理的分区和分桶可以显著提升查询效率。

---

## 📘 第9章：分区表与分桶表

---

### 9.1 什么是分区表（Partitioned Table）？

分区表是将表的数据按某个字段的值划分为多个子目录（分区），每个分区对应一个物理目录。

#### 优点：

- 查询时可以只扫描相关分区，提升性能。
- 管理更灵活（如按日期、地区等分区）。

---

### 9.2 创建分区表

```sql
CREATE TABLE sales (
  id INT,
  product STRING,
  amount DOUBLE
)
PARTITIONED BY (sale_date STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

- `PARTITIONED BY` 指定分区字段。
- 分区字段不在主表结构中，而是作为目录存在。

---

### 9.3 加载数据到分区

```sql
LOAD DATA LOCAL INPATH '/path/to/sales_2025-07-01.csv'
INTO TABLE sales
PARTITION (sale_date='2025-07-01');
```

- 每次加载一个分区的数据。
- Hive 会在 HDFS 中创建对应的目录：`/warehouse/sales/sale_date=2025-07-01/`

---

### 9.4 查询分区表

```sql
SELECT * FROM sales
WHERE sale_date = '2025-07-01';
```

- Hive 会自动只扫描该分区，提高效率。

---

### 9.5 动态分区（可选）

```sql
SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;

INSERT INTO TABLE sales PARTITION (sale_date)
SELECT id, product, amount, sale_date
FROM staging_sales;
```

- 自动根据数据中的 `sale_date` 字段创建分区。

---

## 📘 分桶表（Bucketed Table）

---

### 9.6 什么是分桶表？

分桶是将表中的数据按某个字段的哈希值划分为多个文件（桶），适用于：

- 提高 JOIN 性能（尤其是大表与大表）
- 支持采样查询（`TABLESAMPLE`）

---

### 9.7 创建分桶表

```sql
CREATE TABLE users (
  id INT,
  name STRING
)
CLUSTERED BY (id) INTO 4 BUCKETS
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

- `CLUSTERED BY` 指定分桶字段。
- `INTO 4 BUCKETS` 表示分成4个桶。

---

### 9.8 插入数据到分桶表（必须使用 `INSERT OVERWRITE`）

```sql
SET hive.enforce.bucketing = true;

INSERT OVERWRITE TABLE users
SELECT * FROM staging_users;
```

- Hive 会根据 `id` 的哈希值将数据分配到不同桶中。

---

### 9.9 分桶采样查询

```sql
SELECT * FROM users TABLESAMPLE(BUCKET 1 OUT OF 4 ON id);
```

- 只查询第1个桶的数据（共4个桶）。
- 适用于大数据集的快速抽样分析。

---

### ✅ 小练习题

1. 创建一个按 `region` 分区的销售表，并加载某个地区的数据。
2. 创建一个按 `user_id` 分桶的用户表，分成 8 个桶。
3. 写一条查询语句，只查询 `sale_date = '2025-07-01'` 的销售记录。

---

下一章我们将讲解 **视图与临时表**，用于封装复杂查询逻辑、简化代码和提高复用性。如果你有自己的业务场景或数据结构，也可以告诉我，我来帮你设计分区或分桶策略。是否继续？



非常好，我们继续进入第10章：**视图与临时表**。这是 Hive SQL 中用于封装复杂查询逻辑、提高代码复用性和可读性的强大工具，尤其适合构建数据分析流程或报表系统。

---

## 📘 第10章：视图与临时表

---

### 10.1 什么是视图（View）？

视图是一个虚拟表，它是基于 SQL 查询结果定义的。视图本身不存储数据，而是对原始表的查询封装。

#### 优点：

- 简化复杂查询
- 提高代码复用性
- 便于权限控制和数据抽象

---

### 10.2 创建视图

```sql
CREATE VIEW student_summary AS
SELECT grade, COUNT(*) AS student_count, AVG(age) AS avg_age
FROM students
GROUP BY grade;
```

- 创建一个名为 `student_summary` 的视图。
- 查询每个年级的学生人数和平均年龄。

---

### 10.3 查询视图

```sql
SELECT * FROM student_summary
WHERE avg_age > 20;
```

- 像查询普通表一样使用视图。

---

### 10.4 更新视图（替换）

```sql
CREATE OR REPLACE VIEW student_summary AS
SELECT grade, COUNT(*) AS student_count
FROM students
GROUP BY grade;
```

- 使用 `CREATE OR REPLACE` 更新视图定义。

---

### 10.5 删除视图

```sql
DROP VIEW student_summary;
```

- 删除视图，不影响原始数据表。

---

## 📘 临时表（Temporary Table）

---

### 10.6 什么是临时表？

临时表是会话级别的表，只在当前 Hive 会话中存在，适合中间计算或调试。

---

### 10.7 创建临时表（使用 `WITH` 或 `CREATE TEMPORARY TABLE`）

Hive 不直接支持标准 SQL 的 `CREATE TEMPORARY TABLE`，但可以通过 `WITH` 子句或临时存储表实现类似功能。

#### 示例：使用 `WITH` 子句模拟临时表

```sql
WITH temp_table AS (
  SELECT grade, COUNT(*) AS student_count
  FROM students
  GROUP BY grade
)
SELECT * FROM temp_table
WHERE student_count > 10;
```

---

### 10.8 使用 INSERT 创建中间表

```sql
CREATE TABLE temp_summary AS
SELECT grade, COUNT(*) AS student_count
FROM students
GROUP BY grade;
```

- 创建一个中间表用于后续分析。
- 可在分析流程中临时使用，之后删除。

---

### 10.9 删除临时表

```sql
DROP TABLE temp_summary;
```

---

### ✅ 小练习题

1. 创建一个视图，显示每个年级的学生人数和平均年龄。
2. 查询该视图中平均年龄大于 18 的年级。
3. 使用 `WITH` 子句创建一个临时表，统计每个课程的选课人数。

---

下一章我们将讲解最后一章：**Hive 特有语法与优化技巧**，包括 `MAPJOIN`、`LATERAL VIEW`、`explode()`、文件格式优化等内容。如果你有自己的业务场景或想练习视图设计，也可以告诉我，我来帮你构建。是否继续？



非常好，我们进入最后一章：**Hive 特有语法与优化技巧**。这一章将介绍 Hive SQL 中一些独有的功能和性能优化方法，适用于处理大数据时的高级场景。

---

## 📘 第11章：Hive 特有语法与优化技巧

---

### 11.1 MAPJOIN（小表广播连接）

当一个表很小（如维度表），可以使用 `MAPJOIN` 将其广播到所有 Mapper，提高 JOIN 性能。

#### 示例：

```sql
SELECT /*+ MAPJOIN(dept) */
       emp.name, dept.dept_name
FROM employees emp
JOIN departments dept
ON emp.dept_id = dept.id;
```

- `/*+ MAPJOIN(table_name) */` 是 Hive 的 Hint 语法。
- Hive 会将小表加载到内存中，避免 Shuffle。

---

### 11.2 LATERAL VIEW 与 explode()

用于处理复杂数据类型，如 `ARRAY`、`MAP`、`STRUCT`，将其展开为多行。

#### 示例：展开数组字段

```sql
SELECT name, hobby
FROM students
LATERAL VIEW explode(hobbies) AS hobby;
```

- `hobbies` 是一个数组字段。
- `explode()` 将数组中的每个元素展开为一行。

---

### 11.3 使用 JSON 数据（get_json_object）

Hive 支持从 JSON 字符串中提取字段。

#### 示例：

```sql
SELECT get_json_object(json_col, '$.user.name') AS user_name
FROM logs;
```

- `json_col` 是 JSON 格式的字符串字段。
- `$.user.name` 是 JSON 路径表达式。

---

### 11.4 文件格式优化（ORC、Parquet）

Hive 支持多种高效的列式存储格式，推荐使用：

- **ORC（Optimized Row Columnar）**
- **Parquet**

#### 示例：创建 ORC 表

```sql
CREATE TABLE sales_orc (
  id INT,
  product STRING,
  amount DOUBLE
)
STORED AS ORC;
```

- ORC 支持压缩、索引、快速查询。
- Parquet 与 ORC 类似，适合与 Spark 等工具协同使用。

---

### 11.5 压缩设置（Snappy、Zlib）

可以在 Hive 中启用压缩，提高存储效率。

```sql
SET hive.exec.compress.output=true;
SET mapred.output.compression.codec=org.apache.hadoop.io.compress.SnappyCodec;
```

- 推荐使用 Snappy 压缩，速度快，兼容性好。

---

### 11.6 查询优化建议

| 技巧                         | 说明                                       |
|------------------------------|--------------------------------------------|
| 使用 `LIMIT` 预览数据        | 减少资源消耗                               |
| 使用 `PARTITION` 过滤        | 只扫描相关分区                             |
| 使用 `MAPJOIN` 加速小表连接 | 减少 Shuffle                               |
| 使用列式存储格式             | 提高查询性能                               |
| 避免 SELECT *                | 只选需要的字段，减少 IO                    |
| 使用 `WITH` 子句分解逻辑     | 提高可读性和可维护性                       |

---

### ✅ 小练习题

1. 使用 `explode()` 展开一个数组字段 `tags`。
2. 使用 `get_json_object()` 提取 JSON 字段中的 `user_id`。
3. 创建一个使用 ORC 格式存储的销售表。
4. 使用 `MAPJOIN` 优化一个小表连接查询。

---

## 🎯 总结：Hive SQL 学习路径回顾

我们已经系统学习了 Hive SQL 的各个模块：

1. 基础语法与数据类型  
2. 建表与数据导入  
3. 基本查询（SELECT）  
4. WHERE 条件过滤  
5. GROUP BY 与聚合函数  
6. JOIN 多表连接  
7. 子查询与 WITH 子句  
8. 分区表与分桶表  
9. 视图与临时表  
10. Hive 特有语法与优化技巧  

---

如果你希望我帮你整理成一份完整的 Hive SQL 教学文档、生成练习题集、或者构建一个实际项目的 SQL 模板，我可以继续帮你完成。你接下来想做什么呢？例如：

- 📄 整理成 PDF 教程  
- 🧪 设计练习题和答案  
- 🏗️ 构建一个数据仓库项目示例  
- 📊 分析你自己的数据文件（可以上传）  

告诉我你的目标，我来帮你继续！



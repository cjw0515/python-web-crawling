import pymysql
import pymysql.cursors
from datetime import date, datetime, timedelta
from pymysql.connections import err

config = {
}

connection = pymysql.connect(**config)

# ************* 테이블 조회 *************

with connection.cursor() as cursor:
    sql = ("""
        select *
      from nvs_best_keyword_item 
      limit 100
    """)
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)

# ************* DB 생성 *************
DB_NAME = 'nvs'

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except pymysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

# try:
#     cursor.execute("USE {}".format(DB_NAME))
# except pymysql.connector.Error as err:
#     print("Database {} does not exists.".format(DB_NAME))
#     if err.errno == err.ER_BAD_DB_ERROR:
#         create_database(cursor)
#         print("Database {} created successfully.".format(DB_NAME))
#         connection.database = DB_NAME
#     else:
#         print(err)
#         exit(1)
# ************* 테이블 생성 *************

TABLES = {}
TABLES['employees'] = (
    "CREATE TABLE `employees` ("
    "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `birth_date` date NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  `gender` enum('M','F') NOT NULL,"
    "  `hire_date` date NOT NULL,"
    "  PRIMARY KEY (`emp_no`)"
    ") ENGINE=InnoDB")

TABLES['titles'] = (
    "CREATE TABLE `titles` ("
    "  `emp_no` int(11) NOT NULL,"
    "  `title` varchar(50) NOT NULL,"
    "  `from_date` date NOT NULL,"
    "  `to_date` date DEFAULT NULL,"
    "  PRIMARY KEY (`emp_no`,`title`,`from_date`), KEY `emp_no` (`emp_no`),"
    "  CONSTRAINT `titles_ibfk_1` FOREIGN KEY (`emp_no`)"
    "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

for table_name in TABLES:
    table_description = TABLES[table_name]

    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except pymysql.connector.Error as err:
        if err.errno == err.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

# ************* INSERT *************

tomorrow = datetime.now().date() + timedelta(days=1)

add_employee = ("""INSERT INTO employees 
               (first_name, last_name, hire_date, gender, birth_date) 
               VALUES (%s, %s, %s, %s, %s)""")

data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))

cursor.execute(add_employee, data_employee)

add_salary = ("""INSERT INTO salaries 
              (emp_no, salary, from_date, to_date) 
              VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)""")

emp_no = cursor.lastrowid

data_salary = {
  'emp_no': emp_no,
  'salary': 50000,
  'from_date': tomorrow,
  'to_date': date(9999, 1, 1),
}

cursor.execute(add_salary, data_salary)
connection.commit()

cursor.close()
connection.close()



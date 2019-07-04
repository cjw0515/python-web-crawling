import sqlite_db

def main():
    sql = """
      select *
    from best100_1300k
      """
    db = sqlite_db.SqliteDatabase('1300k_best.db')
    result = db.query(sql)
    print(result)

if __name__ == "__main__":
    main()
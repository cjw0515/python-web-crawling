import sys
import htmlcrawler
import sqlite_db


def main():
    with sqlite_db.SqliteDatabase('test.db') as db:
        # db.execute('CREATE TABLE comments(pkey INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR, comment_body VARCHAR, date_posted TIMESTAMP)')
        # db.execute('INSERT INTO comments (username, comment_body, date_posted) VALUES (?, ?, current_date)',
        #            ('tom', 'this is a comment'))
        # comments = db.query('SELECT * FROM comments')
        # print(comments)
        create_table_sql = """
        create table if not exists best100_1300k(
            "Idx"	INTEGER PRIMARY KEY AUTOINCREMENT,
            "Category"	TEXT,
            "Rank"	INTEGER,
            "ImageURL"	TEXT,
            "ItemCode"	INTEGER,
            "Brand"	TEXT,
            "ItemName"	TEXT,
            "Price"	INTEGER,
            "SalePrice"	INTEGER,
            "NumOfReview"	INTEGER,
            "NumOfLike"	INTEGER
        )
        """
        db.execute(create_table_sql)



if __name__ == "__main__":
    main()
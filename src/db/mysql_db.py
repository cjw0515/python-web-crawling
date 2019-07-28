import sqlalchemy as db
from dotenv import load_dotenv, find_dotenv
import os

class MysqlDatabase:
    def __init__(self):
        load_dotenv(find_dotenv())
        db_options = "mysql+pymysql://{user}:{pwd}@{ip}/{db}".format(
            user=os.getenv("USER"),
            pwd=os.getenv("PASSWORD"),
            ip=os.getenv("IP"),
            db=os.getenv("DB"),
        )
        self._engine = db.create_engine(db_options)
        self._connection = self._engine.connect()
        self._metadata = db.MetaData()

    def create_1300k_table(self):
        tbl_best100 = db.Table('best100_1300k', self._metadata,
                      db.Column('Idx', db.Integer(), primary_key=True, autoincrement=True),
                      db.Column('Category', db.String(100)),
                      db.Column('Rank', db.Integer()),
                      db.Column('ImageURL', db.String(255)),
                      db.Column('ItemCode', db.Integer()),
                      db.Column('Brand', db.String(100)),
                      db.Column('ItemName', db.String(100)),
                      db.Column('Price', db.Integer()),
                      db.Column('SalePrice', db.Integer()),
                      db.Column('NumOfReview', db.Integer()),
                      db.Column('NumOfLike', db.Integer()),
                      db.Column('RegDate', db.DateTime, default=db.func.now()),
                      db.Column('MatchedItem', db.String(255))
                   )
        self._metadata.create_all(self._engine)


if __name__ == "__main__":
    my_db = MysqlDatabase()
    my_db.create_1300k_table()
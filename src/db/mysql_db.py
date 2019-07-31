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
        self._table = None

    def create_1300k_table(self):
        tbl_best100 = db.Table('best100_1300k', self._metadata,
                      db.Column('Idx', db.Integer(), primary_key=True, autoincrement=True),
                      db.Column('Category', db.String(100)),
                      db.Column('Rank', db.Integer()),
                      db.Column('ImageURL', db.String(255)),
                      db.Column('ItemCode', db.String(255)),
                      db.Column('Brand', db.String(100)),
                      db.Column('ItemName', db.String(100)),
                      db.Column('Price', db.Integer()),
                      db.Column('SalePrice', db.Integer()),
                      db.Column('NumOfReview', db.Integer()),
                      db.Column('NumOfLike', db.Integer()),
                      db.Column('RegDate', db.DateTime, default=db.func.now()),
                      db.Column('MatchedItem', db.String(255))
                   )
        self._table = tbl_best100
        self._metadata.create_all(self._engine)

    def insert_1300k_data(self, item_arr):
        for item in item_arr:
            obj = {
                'Category': item[0],
                'Rank': item[1],
                'ImageURL': item[2],
                'ItemCode': item[3],
                'Brand': item[4],
                'ItemName': item[5],
                'Price': item[6],
                'SalePrice': item[7],
                'NumOfReview': item[8],
                'NumOfLike': item[9],
            }
            stmt = db.insert(self._table)
            self._connection.execute(stmt, obj)

    def select_1300k_data(self, category):
        query = db.select([self._table]).where(self._table.columns.Category == category)
        rp = self._connection.execute(query)
        rs = rp.fetchall()
        return rs

    def select_1300k_mached_data(self, category, itemcode):
        query = db.select([self._table.columns.MatchedItem]).where(db.and_(
            self._table.columns.Category == category,
            self._table.columns.ItemCode == itemcode
            )
        )
        rp = self._connection.execute(query)
        rs = rp.fetchall()
        return rs

    def update_1300k_matched_data(self, category, itemcode, matched_item):
        query = db.update(self._table).values(MatchedItem=matched_item)
        query = query.where(
            db.and_(
                self._table.columns.Category == category,
                self._table.columns.ItemCode == itemcode,
            )
        )
        self._connection.execute(query)

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    db_options = "mysql+pymysql://{user}:{pwd}@{ip}/{db}".format(
        user=os.getenv("USER"),
        pwd=os.getenv("PASSWORD"),
        ip=os.getenv("IP"),
        db=os.getenv("DB"),
    )
from sqlalchemy import Column, Integer, String
from data.db_session import SqlAlchemyBase

# таблица пользователей
class RandomUser(SqlAlchemyBase):
    __tablename__ = "random_users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    gender = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    email = Column(String)
    city = Column(String)
    country = Column(String)
    picture = Column(String)

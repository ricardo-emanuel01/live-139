from sqlalchemy import create_engine, String, Integer, Column
from sqlalchemy.orm import sessionmaker, declarative_base

from pprint import pprint

engine = create_engine('sqlite:///test1.db', echo=False)
# Em letra maiuscula pois sessionmaker() retorna uma classe
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Person(Base):
    __tablename__ = "persons"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    def __repr__(self):
        return f"Person(name = {self.name}, age = {self.age})"

Base.metadata.create_all(engine)

# p1 = Person(name="Mariana", age=20)
# p2 = Person(name="Ricardo", age=21)
# p3 = Person(name="Rosa", age=81)
# p4 = Person(name="Renata", age=32)
# p5 = Person(name="Somebody", age=0)

# session.add_all([p1, p2, p3, p4])

# session.commit()

pprint(session.query(Person).first())

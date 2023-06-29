# Use this to test which kind of error could happen

from sqlalchemy import create_engine, String, Integer, Float, Column, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from pprint import pprint

engine = create_engine('sqlite:///test3.db', echo=False)
# Em letra maiuscula pois sessionmaker() retorna uma classe
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    person_id = Column(Integer, ForeignKey('persons.id'))
    person = relationship("Person")

    def __repr__(self):
        return f"Product(id = {self.id}, name = {self.name}, owner = {self.person})"
    
class Person(Base):
    __tablename__ = "persons"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    products = relationship(Product, backref='persons')

    def __repr__(self):
        return f"Person(id = {self.id}, name = {self.name}, age = {self.age})"
    
Base.metadata.create_all(engine)

p1 = Person(name="Mariana", age=20)
p2 = Person(name="Ricardo", age=21)
p3 = Person(name="Rosa", age=81)
p4 = Person(name="Renata", age=32)
p5 = Person(name="Somebody", age=0)

session.add_all([p1, p2, p3, p4])

session.commit()

pprint(session.query(Person).first())
from sqlalchemy import create_engine, String, Integer, Float, Column, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from pprint import pprint

engine = create_engine('sqlite:///test1.db', echo=False)
# Em letra maiuscula pois sessionmaker() retorna uma classe
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    person_id = Column(Integer, ForeignKey('persons.id'))
    person = relationship("Person", back_populates="products")

    def __repr__(self):
        return (
            f"Product(id = {self.id}, "
            f"name = {self.name}, "
            f"owner = {self.person})"
        )
    
class Person(Base):
    __tablename__ = "persons"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    products = relationship("Product", back_populates='person')

    def __repr__(self):
        return (
            f"Person(id = {self.id}, "
            f"name = {self.name}, "
            f"age = {self.age}"
            #f"products = {self.products})"
        )
    
Base.metadata.create_all(engine)

p1 = Person(name="Mariana", age=20)
p2 = Person(name="Ricardo", age=21)
pd1 = Product(name="Livro", person=p1)
pd2 = Product(name="Tenis", person=p1)
pd3 = Product(name="Livro", person=p2)

session.add_all([p1, pd1, pd2, p2, pd3])

# Os dados só persistem após o commit
session.commit()

"""
Me joga um warning dizendo que existe um produto cartesiano
entre as duas tabelas, o que significa que ele nao sabe
qual a combinacao certa das linhas e contém todas as
combinacoes possiveis e entao eu devo explicitamente 
dizer como eu quero que elas sejam agrupadas

session.query(Product).filter(Person.name == "Mariana").first()

session.query(Product).join(Product.person).filter(Person.name == "Mariana").first()
"""

# Retorna todos os produtos associados a pessoa com name == "Mariana"
pprint(session.query(Product).join(Product.person).filter(Person.name == "Mariana").all())
# Retorna todos os produtos com name == "Livro" associados a pessoa com name == "Mariana"
pprint(session.query(Product).join(Product.person).filter(Product.name == "Livro", Person.name == "Mariana").all())
# Retorna todas as pessoas associadas ao produto com name == "Livro"
pprint(session.query(Person).join(Person.products).filter(Product.name == "Livro").all())
# Retorna todas as pessoas associadas ao produto com name == "Tenis"
pprint(session.query(Person).all())
# Retorna todos os Livros de Ricardo kasjda
pprint(session.query(Person).join(Person.products).filter(Product.name == "Livro", Person.name == "Ricardo").all())

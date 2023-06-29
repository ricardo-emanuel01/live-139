from sqlalchemy import create_engine, String, Integer, Column
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///test.db', echo=True)
# Em letra maiuscula pois sessionmaker() retorna uma classe
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Pessoa(Base):
    __tablename__ = "pessoas"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)

Base.metadata.create_all(engine)

p1 = Pessoa(name="Mariana")
p2 = Pessoa(name="Ricardo")
p3 = Pessoa(name="Rosa")
p4 = Pessoa(name="Renata")
p5 = Pessoa(name="Somebody")

session.add_all([p1, p2, p3, p4])

session.commit()

session.add(p5)
# Limpa a sessão e p5 não aparecerá no banco de dados
# Visto que isso não foi commitado
session.flush()

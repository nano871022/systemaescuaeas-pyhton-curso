import sqlite3
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, Table, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker


engine = create_engine("sqlite:///:memory:")
Base = declarative_base()
Session = sessionmaker(bind=engine)

alumno_curso = Table(
    "alumno_curso",
    Base.metadata,
    Column("alumno_id",ForeignKey("alumno.id"),primary_key=True),
    Column("curso_id",ForeignKey("curso.id"),primary_key=True)
)

class Alumno(Base):
    __tablename__ = "alumno"
    id = Column(Integer,Sequence("seq_alumno_id"), primary_key=True)
    nombres = Column(String)
    apellidos = Column(String)
    cursos = relationship("Curso",secondary=alumno_curso,back_populates="alumnos")

    def __repr__(self):
        return "{} {}".format(self.nombres,self.apellidos)

class Profesor(Base):
    __tablename__ = "profesor"
    id = Column(Integer,Sequence("seq_profesor_id"), primary_key=True)
    nombres = Column(String)
    apellidos = Column(String)
    horarios = relationship("Horario",order_by="Horario.id",back_populates="profesores")

    def __repr__(self):
        return "Profersor {} {}".format(self.nombres,self.apellidos)

class Curso(Base):
    __tablename__ = "curso"
    id = Column(Integer,Sequence("seq_curso_id"), primary_key=True)
    nombre = Column(String)
    alumnos = relationship("Alumno",secondary=alumno_curso,back_populates="cursos")
    horarios = relationship("Horario",order_by="Horario.id",back_populates="cursos")

    def __repr__(self):
        return self.nombre

class Horario(Base):
    __tablename__ = "horario"
    id = Column(Integer,Sequence("seq_horario_id"), primary_key=True)
    dia = Column(String)
    horainicio = Column(String)
    horafin = Column(String)

    curso_id = Column(Integer,ForeignKey("curso.id"))
    cursos = relationship("Curso",back_populates="horarios")
    
    profesor_id = Column(Integer,ForeignKey("profesor.id"))
    profesores = relationship("Profesor",back_populates="horarios")

    def __repr__(self):
        return "{} {} {}".format(self.dia, self.horainicio, self.horafin)

Base.metadata.create_all(engine)

class Exports(object):
    def alumno_curso(self):
        resultado=session.query(Alumno).join(alumno_curso).join(Curso).all()
        print(resultado)

    def horario_profesor(self):
        resultado=session.query(Horario).join(Profesor).all()
        print(resultado)

    def horario_curso(self):
        resultado=session.query(Horario).join(Curso).all()
        print(resultado)


print("BD cargada...")

Session= sessionmaker(bind=engine)
session = Session()

print("Cursos",session.query(Curso).all())
print("Profesores:",session.query(Profesor).all())
print("Alumnos:",session.query(Alumno).all())
print("Horarios",session.query(Horario).all())

export=Exports()
print("Alumno-Curso:",export.alumno_curso())
print("Horario-Profesor:",export.horario_profesor())
print("Horario-Curso:",export.horario_curso())
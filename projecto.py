import sqlite3
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, Table, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
import csv


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

def crearSession():
    Session=sessionmaker(bind=engine)
    return Session()
    
class Operaciones(object):
    def __init__(self):
        self.session = crearSession()


class Exports(Operaciones):
    def exportarArchivo(self,nombreArchivo,*headers,*body):
        with open(nombreArchivo,"w") as File:
            writer=csv.write(File)
            writer.writerows(headers)      
            writer.writerows(resultado)        
        
class Cursos(Exports):
    nombreArchivo="curso_alumno.csv"
    def append(self,curso):
        self.session.add(curso)
    def delete(self,curso):
        self.session.delete(curso)
    def updated(self,curso):
        self.session.update(curso)
    def get(self,curso):
        self.session.query(Curso).filter(curso).all()
    def all(self):
        self.session.query(Curso).all()
    def export(self):
        result=self.session.query(Curso).join(alumno_curso).join(Alumno).all()
        headers=[]
        self.exportarArchivo(self.nombreArchivo,headers,result)
        print("El archivo",self.nombreArchivo,"generado.")

class Profesores(Exports):
    nombreArchivo="profesor_horario.csv"
    def append(self,profesor):
        self.session.add(profesor)
    def delete(self,profesor):
        self.session.delete(profesor)
    def updated(self,profesor):
        self.session.update(profesor)
    def get(self,curso):
        self.session.query(Profesor).filter(profesor).all()
    def all(self):
        self.session.query(Profesor).all()
    def export(self):
        result=self.session.query(Profesor).join(Horario).join(Curso).all()
        headers=[]
        self.exportarArchivo(self.nombreArchivo,headers,result)
        print("El archivo",self.nombreArchivo,"generado.")

class Alumnos(Exports):
    nombreArchivo="alumno_curso.csv"
    def append(self,alumno):
        self.session.add(alumno)
    def delete(self,alumno):
        self.session.delete(alumno)
    def updated(self,alumno):
        self.session.update(alumno)
    def get(self,curso):
        self.session.query(Alumno).filter(alumno).all()
    def all(self):
        self.session.query(Alumno).all()
    def export(self):
        result=self.session.query(Alumno).join(alumno_curso).join(Curso).all()
        headers=[]
        self.exportarArchivo(self.nombreArchivo,headers,result)
        print("El archivo",self.nombreArchivo,"generado.")

class Horarios(Exports):
    nombreArchivo="horario_curso.csv"
    def append(self,horario):
        self.session.add(horario)
    def delete(self,horario):
        self.session.delete(horario)
    def updated(self,horario):
        self.session.update(horario)
    def get(self,horario):
        self.session.query(Horario).filter(horario).all()
    def all(self):
        self.session.query(Horario).all()        
    def export(self):
        result=self.session.query(Horario).join(Curso).all()
        headers=[]
        self.exportarArchivo(self.nombreArchivo,headers,result)
        print("El archivo",self.nombreArchivo,"generado.")
        
print("BD cargada...")

cursos=Cursos()
alumnos=Alumnos()
profesores=Profesores()
horarios=Horarios()
print("Cursos",cursos.all())
print("Profesores:",profesores.all())
print("Alumnos:",alumnos.all())
print("Horarios",horarios.all())

export=Exports()
print("Alumno-Curso:"    ,cursos.export())
print("Horario-Profesor:",profesores.export())
print("Horario-Curso:"   ,horarios.export())

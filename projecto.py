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
    horarios = relationship("Horario",back_populates="profesor")

    def __repr__(self):
        return "Profersor {} {}".format(self.nombres,self.apellidos)

class Curso(Base):
    __tablename__ = "curso"
    id = Column(Integer,Sequence("seq_curso_id"), primary_key=True)
    nombre = Column(String)
    alumnos = relationship("Alumno",secondary=alumno_curso,back_populates="cursos")
    horarios = relationship("Horario",back_populates="curso")

    def __repr__(self):
        return self.nombre

class Horario(Base):
    __tablename__ = "horario"
    id = Column(Integer,Sequence("seq_horario_id"), primary_key=True)
    dia = Column(String)
    horainicio = Column(String)
    horafin = Column(String)

    curso_id = Column(Integer,ForeignKey("curso.id"))
    curso = relationship("Curso",back_populates="horarios")
    
    profesor_id = Column(Integer,ForeignKey("profesor.id"))
    profesor = relationship("Profesor",back_populates="horarios")

    def __repr__(self):
        return "{} {} {}".format(self.dia, self.horainicio, self.horafin)

Base.metadata.create_all(engine)
class Sessions(object):
    def __init__(self):
        Session=sessionmaker(bind=engine)
        self.session=Session()
    def crearSession(self):
        return self.session
sessions=Sessions()
    
class Operaciones(object):
    def __init__(self):
        self.session = sessions.crearSession()
    def commit(self):
        self.session.commit()


class Exports(Operaciones):
    def exportarArchivo(self,nombreArchivo,headers,body):
        out=map(lambda x: dict(zip(headers,x)),body)
        with open(nombreArchivo,"w") as File:
            writer=csv.writer(File,delimiter=";",quotechar='"')
            writer.writerow(headers)
            writer.writerows(body)        
        
class Cursos(Exports):
    nombreArchivo="curso_alumno.csv"
    def append(self,curso):
        return self.session.add(curso)
    def delete(self,curso):
        return self.session.delete(curso)
    def updated(self,curso):
        return self.session.save(curso)
    def get(self,curso):
        return self.session.query(Curso).filter(curso).all()
    def all(self):
        return self.session.query(Curso).all()
    def addAlumnos(self,curso,alumno):
        return curso.alumnos.append(alumno)
    def export(self,idCurso):
        result=self.session.query(Curso).join(alumno_curso).join(Alumno).filter(Curso.id==idCurso).one()
        headers=["nombres","apellidos"]
        nombreArchivo=self.nombreArchivo.replace("curso",result.nombre)
        self.exportarArchivo(nombreArchivo,headers,map(lambda x: [x.nombres,x.apellidos], result.alumnos))
        print("El archivo",nombreArchivo,"generado.")

class Profesores(Exports):
    nombreArchivo="profesor_horario.csv"
    def append(self,profesor):
        return self.session.add(profesor)
    def delete(self,profesor):
        return self.session.delete(profesor)
    def updated(self,profesor):
        return self.session.save(profesor)
    def get(self,profesor):
        return self.session.query(Profesor).filter(profesor).all()
    def all(self):
        return self.session.query(Profesor).all()
    def export(self,idProfesor):
        result=self.session.query(Profesor).join(Horario).join(Curso).filter(Profesor.id==idProfesor).one()
        headers=["DIA","INICIO","FIN"]
        nombreArchivo=self.nombreArchivo.replace("profesor","{}_{}".format(result.nombres,result.apellidos))
        self.exportarArchivo(nombreArchivo,headers,map(lambda x: [x.dia,x.horainicio,x.horafin], result.horarios))
        print("El archivo",nombreArchivo,"generado.")

class Alumnos(Exports):
    nombreArchivo="alumno_curso.csv"
    def append(self,alumno):
        return self.session.add(alumno)
    def delete(self,alumno):
        return self.session.delete(alumno)
    def updated(self,alumno):
        return self.session.save(alumno)
    def get(self,alumno):
        return self.session.query(Alumno).filter(alumno).all()
    def all(self):
        return self.session.query(Alumno).all()
    def export(self):
        result=self.session.query(Alumno).join(alumno_curso).join(Curso).all()
        headers=["nombres","curso"]
        self.exportarArchivo(self.nombreArchivo,headers,map(lambda x: ["{} {}".format(x.nombres,x.apellidos),x.cursos.nombre], result))
        print("El archivo",self.nombreArchivo,"generado.")

class Horarios(Exports):
    nombreArchivo="horario_curso.csv"
    def append(self,horario):
        return self.session.add(horario)
    def delete(self,horario):
        return self.session.delete(horario)
    def updated(self,horario):
        return self.session.save(horario)
    def get(self,horario):
        return self.session.query(Horario).filter(horario).all()
    def all(self):
        return self.session.query(Horario).all()        
    def addProfesor(self,horario,profesor):
        horario.profesor = profesor
        self.commit()
    def addCurso(self,horario,curso):
        horario.curso = curso
        self.commit()
    def export(self):
        result=self.session.query(Horario).join(Curso).all()
        headers=['DIA','INICIO','FIN','CURSO','PROFESOR']
        listas=list(map(lambda x: [
            x.dia,
        x.horainicio,
        x.horafin,
        x.curso.nombre,
        "{} {}".format(x.profesor.nombres,x.profesor.apellidos)
        ],result))
        self.exportarArchivo(self.nombreArchivo,headers,listas)
        print("El archivo",self.nombreArchivo,"generado.")
        
print("BD cargada...")


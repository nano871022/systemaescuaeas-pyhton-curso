from projecto import *

cursos=Cursos()
alumnos=Alumnos()
profesores=Profesores()
horarios=Horarios()
print("Cursos",cursos.all())
print("Profesores:",profesores.all())
print("Alumnos:",alumnos.all())
print("Horarios",horarios.all())

export=Exports()

#print("Alumno-Curso:"    ,cursos.export())
#print("Horario-Profesor:",profesores.export())
#print("Horario-Curso:"   ,horarios.export())

alumnos.append(Alumno(id=1,nombres="alejo",apellidos="parra"))
alumnos.append(Alumno(id=2,nombres="lore",apellidos="mahecha"))

cursos.append(Curso(id=1,nombre="java"))

horarios.append(Horario(id=1,dia="lunes",horainicio="06:00",horafin="08:00"))
horarios.append(Horario(id=2,dia="miercoles",horainicio="06:00",horafin="08:00"))
horarios.append(Horario(id=3,dia="viernes",horainicio="06:00",horafin="08:00"))

profesores.append(Profesor(id=1,nombres="camilo",apellidos="duzan"))
profesores.append(Profesor(id=2,nombres="ubbe",apellidos="ragnason"))

curso=cursos.get(Curso.id==1)[0]
alumno1=alumnos.get(Alumno.id==1)[0]
alumno2=alumnos.get(Alumno.id==2)[0]
cursos.addAlumnos(curso,alumno1)
cursos.addAlumnos(curso,alumno2)

horario1=horarios.get(Horario.id==1)[0]
horario2=horarios.get(Horario.id==2)[0]
horario3=horarios.get(Horario.id==3)[0]
horarios.addCurso(horario1,curso)
horarios.addCurso(horario3,curso)
horarios.addCurso(horario2,curso)

profesor1=profesores.get(Profesor.id==1)[0]
profesor2=profesores.get(Profesor.id==2)[0]
horarios.addProfesor(horario1,profesor1)
horarios.addProfesor(horario2,profesor2)
horarios.addProfesor(horario3,profesor1)

print("Cursos",cursos.all())
print("Profesores:",profesores.all())
print("Alumnos:",alumnos.all())
print("Horarios",horarios.all())

cursos.export(1)
profesores.export(1)
horarios.export()

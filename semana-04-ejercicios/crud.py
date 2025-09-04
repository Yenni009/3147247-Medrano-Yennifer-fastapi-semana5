from sqlalchemy.orm import Session
import models

def buscar_libros_por_titulo(db: Session, busqueda: str):
    return db.query(models.Libro).filter(
        models.Libro.titulo.contains(busqueda)
    ).all()

def buscar_libros_por_autor(db: Session, nombre_autor: str):
    return db.query(models.Libro).join(models.Autor).filter(
        models.Autor.nombre.contains(nombre_autor)
    ).all()

def obtener_libros_por_precio(db: Session, precio_min: float, precio_max: float):
    return db.query(models.Libro).filter(
        models.Libro.precio >= precio_min,
        models.Libro.precio <= precio_max
    ).all()

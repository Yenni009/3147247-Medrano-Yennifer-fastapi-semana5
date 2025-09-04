from sqlalchemy.orm import Session, joinedload
import models, schemas

# CRUD para Categorías
def crear_categoria(db: Session, categoria: schemas.CategoriaCreate):
    db_categoria = models.Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def obtener_categorias(db: Session):
    return db.query(models.Categoria).all()

def obtener_categoria(db: Session, categoria_id: int):
    return db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()

def obtener_categoria_con_productos(db: Session, categoria_id: int):
    return db.query(models.Categoria).options(
        joinedload(models.Categoria.productos)
    ).filter(models.Categoria.id == categoria_id).first()

# CRUD para Productos
def obtener_productos_con_categoria(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Producto).options(
        joinedload(models.Producto.categoria)
    ).offset(skip).limit(limit).all()

def obtener_productos_por_categoria(db: Session, categoria_id: int):
    return db.query(models.Producto).filter(
        models.Producto.categoria_id == categoria_id
    ).all()

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

import models, schemas, crud
from database import SessionLocal, engine, get_db

# Crear tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Productos con Categorías")

# Endpoints Categorías
@app.post("/categorias/", response_model=schemas.Categoria)
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return crud.crear_categoria(db=db, categoria=categoria)

@app.get("/categorias/")
def listar_categorias(db: Session = Depends(get_db)):
    return crud.obtener_categorias(db)

@app.get("/categorias/{categoria_id}", response_model=schemas.CategoriaConProductos)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = crud.obtener_categoria_con_productos(db, categoria_id=categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

# Endpoints Productos
@app.get("/productos/", response_model=List[schemas.ProductoConCategoria])
def listar_productos_con_categoria(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return crud.obtener_productos_con_categoria(db, skip=skip, limit=limit)

@app.get("/categorias/{categoria_id}/productos/")
def productos_por_categoria(categoria_id: int, db: Session = Depends(get_db)):
    productos = crud.obtener_productos_por_categoria(db, categoria_id=categoria_id)
    return {
        "categoria_id": categoria_id,
        "productos": productos,
        "total": len(productos)
    }

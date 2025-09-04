from pydantic import BaseModel
from typing import List, Optional

# Schemas para Categoría
class CategoriaBase(BaseModel):
    nombre: str
    descripcion: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int

    class Config:
        from_attributes = True

# Schemas para Producto
class ProductoBase(BaseModel):
    nombre: str
    precio: float
    descripcion: str
    categoria_id: Optional[int] = None

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: str = None
    precio: float = None
    descripcion: str = None
    categoria_id: int = None

# Producto con info de categoría
class ProductoConCategoria(ProductoBase):
    id: int
    categoria: Optional[Categoria] = None

    class Config:
        from_attributes = True

# Categoría con lista de productos
class CategoriaConProductos(Categoria):
    productos: List[ProductoBase] = []

    class Config:
        from_attributes = True

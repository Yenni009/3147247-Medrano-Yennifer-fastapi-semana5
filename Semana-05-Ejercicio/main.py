from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from database import engine
from models import Base, User
from auth import (
    get_db,
    create_user,
    authenticate_user,
    create_access_token,
    get_current_user,
    require_admin,
    get_all_users,
    update_user_role,
    create_admin_user,
    get_user_by_username
)
from schemas import (
    UserRegister,
    UserLogin,
    UserResponse,
    Token,
    UserRoleUpdate,
    PostCreate,
    PostResponse
)

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI #3147247")

# Lista en memoria para simular posts
posts = []


# CREAR PRIMER ADMIN

@app.post("/create-admin", response_model=UserResponse)
def create_first_admin(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_admin = db.query(User).filter(User.role == "admin").first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Ya existe un administrador")

    if get_user_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    admin_user = create_admin_user(db, user_data.username, user_data.email, user_data.password)
    return UserResponse(
        id=admin_user.id,
        username=admin_user.username,
        email=admin_user.email,
        is_active=admin_user.is_active,
        role=admin_user.role
    )

# REGISTER

@app.post("/register", response_model=UserResponse)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    new_user = create_user(db, user_data.username, user_data.email, user_data.password)
    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        is_active=new_user.is_active,
        role=new_user.role
    )


# LOGIN

@app.post("/login", response_model=Token)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrecta")

    token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=30)
    )
    return Token(access_token=token, token_type="bearer")

# PERFIL

@app.get("/users/me", response_model=UserResponse)
def read_users_me(current_user=Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
        role=current_user.role
    )


# ADMIN ENDPOIN
@app.get("/admin/users", response_model=list[UserResponse])
def list_all_users(admin_user=Depends(require_admin), db: Session = Depends(get_db)):
    users = get_all_users(db)
    return [
        UserResponse(
            id=u.id,
            username=u.username,
            email=u.email,
            is_active=u.is_active,
            role=u.role
        ) for u in users
    ]

@app.put("/admin/users/{user_id}/role", response_model=UserResponse)
def change_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    admin_user=Depends(require_admin),
    db: Session = Depends(get_db)
):
    if user_id == admin_user.id:
        raise HTTPException(status_code=400, detail="No puedes cambiar tu propio rol")

    updated_user = update_user_role(db, user_id, role_data.role)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return UserResponse(
        id=updated_user.id,
        username=updated_user.username,
        email=updated_user.email,
        is_active=updated_user.is_active,
        role=updated_user.role
    )


# POSTS CRUD (en memoria)

@app.post("/posts", response_model=PostResponse)
def create_post(post_data: PostCreate, current_user=Depends(get_current_user)):
    new_post = {
        "id": len(posts) + 1,
        "title": post_data.title,
        "content": post_data.content,
        "author": current_user.username
    }
    posts.append(new_post)
    return PostResponse(**new_post)

@app.get("/posts", response_model=list[PostResponse])
def get_posts():
    return [PostResponse(**p) for p in posts]

@app.get("/posts/my", response_model=list[PostResponse])
def get_my_posts(current_user=Depends(get_current_user)):
    return [PostResponse(**p) for p in posts if p["author"] == current_user.username]

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, current_user=Depends(get_current_user)):
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")

    if post["author"] != current_user.username:
        raise HTTPException(status_code=403, detail="No tienes permiso para borrar este post")

    posts.remove(post)
    return {"message": "Post eliminado exitosamente"}

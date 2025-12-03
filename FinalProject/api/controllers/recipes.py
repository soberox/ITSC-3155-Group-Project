from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from ..models import recipes as model
from ..models import menu_items as menu_model
from ..models import resources as resource_model
from ..schemas.recipes import RecipeCreate, RecipeUpdate


def create(db: Session, request: RecipeCreate):
    new_recipe = model.Recipe(
        menu_item_id=request.menu_item_id,
        resource_id=request.resource_id,
        amount=request.amount
    )

    try:
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_recipe


def read_all(db: Session):
    try:
        return db.query(model.Recipe).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def read_one(db: Session, recipe_id: int):
    try:
        recipe = (
            db.query(model.Recipe)
            .filter(model.Recipe.id == recipe_id)
            .first()
        )
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe ID not found"
            )
        return recipe

    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def update(db: Session, recipe_id: int, request: RecipeUpdate):
    try:
        recipe_query = db.query(model.Recipe).filter(model.Recipe.id == recipe_id)
        recipe_db = recipe_query.first()

        if not recipe_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe ID not found"
            )

        # Support Pydantic v2 `.model_dump` and v1 `.dict`
        if hasattr(request, "model_dump"):
            update_data = request.model_dump(exclude_unset=True, exclude_none=True)
        else:
            update_data = request.dict(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

        # If client is changing FK values, verify referenced parent rows exist to avoid DB FK errors
        if "menu_item_id" in update_data:
            menu = db.query(menu_model.MenuItem).filter(menu_model.MenuItem.id == update_data["menu_item_id"]).first()
            if not menu:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"menu_item_id {update_data['menu_item_id']} not found")

        if "resource_id" in update_data:
            res = db.query(resource_model.Resource).filter(resource_model.Resource.id == update_data["resource_id"]).first()
            if not res:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"resource_id {update_data['resource_id']} not found")

        recipe_query.update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(recipe_db)
        return recipe_db

    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


def delete(db: Session, recipe_id: int):
    try:
        recipe_query = db.query(model.Recipe).filter(model.Recipe.id == recipe_id)
        recipe_db = recipe_query.first()

        if not recipe_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe ID not found"
            )

        recipe_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Recipe deleted successfully"}

    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
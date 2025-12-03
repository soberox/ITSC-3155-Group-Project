from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import order_details as model
from ..models.menu_items import MenuItem
from ..models.customers import Customers
from ..models.orders import Order
from sqlalchemy.exc import SQLAlchemyError
from ..models import menu_items as menu_model
from ..models import orders as order_model


def create(db: Session, request):
    order = (
        db.query(Order)
        .filter(Order.id == request.order_id)
        .order_by(Order.id.desc())
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No order found for this order ID."
        )
    
    item = (
        db.query(MenuItem)
        .filter(MenuItem.id == request.menu_item_id)
        .order_by(MenuItem.id.desc())
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No menu item found for this menu item ID."
        )
    
    customer = (
        db.query(Customers)
        .filter(Customers.id == order.customer_id)
        .order_by(Customers.id.desc())
        .first()
    )

    # Determine amount: prefer explicit amount, else compute from quantity*price
    qty = getattr(request, "quantity", None)
    prc = getattr(request, "price", None)
    amt = getattr(request, "amount", None)

    if amt is None:
        # If amount not provided, both quantity and price must be provided
        if qty is None or prc is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Provide either `amount` or both `quantity` and `price`"
            )
        try:
            amt = float(qty) * float(prc)
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid quantity or price")

    new_item = model.OrderDetail(
        order_id=request.order_id,
        menu_item_id=request.menu_item_id,
        customer_name=customer.customerName,
        item_name=item.name,
        order_status=order.order_status,
        order_type=order.type,
        billing_address=order.billing_address,
        tracking_number=order.tracking_number,
        amount=amt
    )
    # Attach transient attributes for API consumers/tests (not persisted fields)
    try:
        if qty is not None:
            new_item.quantity = qty
        if prc is not None:
            new_item.price = prc
    except Exception:
        pass

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.OrderDetail).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def update_status(db: Session, id: int):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.update({"order_status": "Completed"}, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()

def read_one(db: Session, item_id):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        # support v2/v1
        if hasattr(request, "model_dump"):
            update_data = request.model_dump(exclude_unset=True, exclude_none=True)
        else:
            update_data = request.dict(exclude_unset=True)

        # If client provides quantity+price, compute and set `amount` before persisting
        qty = update_data.get("quantity")
        prc = update_data.get("price")
        if qty is not None and prc is not None:
            try:
                update_data["amount"] = float(qty) * float(prc)
            except Exception:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid quantity or price")

        # Validate any FK changes
        if "menu_item_id" in update_data:
            menu = db.query(menu_model.MenuItem).filter(menu_model.MenuItem.id == update_data["menu_item_id"]).first()
            if not menu:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"menu_item_id {update_data['menu_item_id']} not found")

        if "order_id" in update_data:
            ord_obj = db.query(order_model.Order).filter(order_model.Order.id == update_data["order_id"]).first()
            if not ord_obj:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"order_id {update_data['order_id']} not found")

        # Remove transient fields that aren't columns in the DB
        update_data.pop('quantity', None)
        update_data.pop('price', None)

        if not update_data:
            return item.first()

        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', str(e)))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

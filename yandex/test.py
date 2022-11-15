from app.database import get_db
from app import models, schemas as schemas
from sqlalchemy import and_, or_, not_s


def get_active_orders():
    yandex_order_ids = []
    ids = []
    db = get_db()
    orders = next(db).query(models.Order).filter(or_(
                                                    models.Order.status == "search_car",
                                                    models.Order.status == "assigned")).all()
from typing import Dict, Any
from sqlalchemy.orm import Session
from src.db.database import SessionLocal
from src.db.models import Customer


def _get_db() -> Session:
    return SessionLocal()


# ---------- SELECT ----------
def db_select_customers(filters: Dict[str, Any]) -> Dict[str, Any]:
    db = _get_db()
    try:
        q = db.query(Customer)

        if filters and "city" in filters:
            q = q.filter(Customer.city == filters["city"])

        rows = q.all()
        out = [{"id": r.id, "name": r.name, "city": r.city} for r in rows]
        return {"ok": True, "rows": out, "count": len(out)}
    finally:
        db.close()


# ---------- INSERT ----------
def db_insert_customer(values: Dict[str, Any]) -> Dict[str, Any]:
    db = _get_db()
    try:
        if not values or "name" not in values or "city" not in values:
            return {"ok": False, "error": "missing_fields: name, city required"}

        row = Customer(name=values["name"], city=values["city"])
        db.add(row)
        db.commit()
        db.refresh(row)

        return {
            "ok": True,
            "inserted": {"id": row.id, "name": row.name, "city": row.city},
        }
    finally:
        db.close()


# ---------- UPDATE ----------
def db_update_customer(filters: Dict[str, Any], values: Dict[str, Any]) -> Dict[str, Any]:
    """
    Supported:
      - filter by name (case-insensitive)
      - update city
    """
    db = _get_db()
    try:
        name = (filters or {}).get("name")
        new_city = (values or {}).get("city")

        if not name:
            return {"ok": False, "error": "missing_filter: name required"}
        if not new_city:
            return {"ok": False, "error": "missing_values: city required"}

        q = db.query(Customer).filter(Customer.name.ilike(name))
        rows = q.all()

        if not rows:
            return {"ok": False, "error": f"not_found: customer name={name}"}

        for r in rows:
            r.city = new_city

        db.commit()

        updated = [{"id": r.id, "name": r.name, "city": r.city} for r in rows]
        return {"ok": True, "updated": updated, "count": len(updated)}
    finally:
        db.close()


# ---------- DELETE ----------
def db_delete_customers(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Supported:
      - delete by name (case-insensitive)
      - or delete by city
    """
    db = _get_db()
    try:
        name = (filters or {}).get("name")
        city = (filters or {}).get("city")

        q = db.query(Customer)

        if name:
            q = q.filter(Customer.name.ilike(name))
        elif city:
            q = q.filter(Customer.city == city)
        else:
            return {"ok": False, "error": "missing_filter: name or city required"}

        count = q.count()
        if count == 0:
            return {"ok": False, "error": "not_found"}

        q.delete(synchronize_session=False)
        db.commit()
        return {"ok": True, "deleted_count": count}
    finally:
        db.close()


# ---------- ADMIN ----------
def reset_customers() -> Dict[str, Any]:
    db = _get_db()
    try:
        db.query(Customer).delete()
        db.commit()
        return {"ok": True, "message": "db reset", "count": 0}
    finally:
        db.close()


def seed_customers() -> Dict[str, Any]:
    db = _get_db()
    try:
        db.query(Customer).delete()
        db.add_all(
            [
                Customer(name="Asha", city="Dubai"),
                Customer(name="Neha", city="Mumbai"),
                Customer(name="Ishita", city="Dubai"),
            ]
        )
        db.commit()

        count = db.query(Customer).count()
        return {"ok": True, "message": "db seeded", "count": count}
    finally:
        db.close()

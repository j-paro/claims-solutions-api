from typing import List

from claims_solutions_api.models import db


class CompanyModel(db.Model):
    __tablename__ = "companies"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.Integer)
    address_1 = db.Column(db.String(80))
    address_2 = db.Column(db.String(80))
    city = db.Column(db.String(80))
    state = db.Column(db.String(2))
    zip = db.Column(db.Integer())

    @classmethod
    def find_by_name(cls, name: str) -> "CompanyModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["CompanyModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
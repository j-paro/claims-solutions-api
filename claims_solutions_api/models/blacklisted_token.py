from claims_solutions_api.models import db


class BlacklistedToken(db.Model):
    __tablename__ = "blacklisted_tokens"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    @classmethod
    def find_by_jti(cls, jti) -> "BlacklistedToken":
        return cls.query.filter_by(jti=jti).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
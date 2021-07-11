from typing import Any, Union

from flask_bcrypt import Bcrypt  # type: ignore
from flask_caching import Cache  # type: ignore
from flask_cors import CORS  # type: ignore
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate  # type: ignore
from flask_sqlalchemy import SQLAlchemy, Model


class CRUDMixin(Model):
    @classmethod
    def create(cls, **kwargs: Any) -> Any:
        """Create a new record and save it the database."""
        instance = cls(**kwargs)  # type: ignore
        return instance.save()

    def update(self, commit: bool = True, **kwargs: Any) -> Union[Any, "CRUDMixin"]:
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit: bool = True) -> Union[Any, "CRUDMixin"]:
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit: bool = True) -> Union[Any, "CRUDMixin"]:
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


bcrypt = Bcrypt()
db = SQLAlchemy(model_class=CRUDMixin)
migrate = Migrate()
cache = Cache()
cors = CORS()

from flask_realworld.utils import jwt_identity, identity_loader

jwt = JWTManager()
jwt.user_lookup_loader(jwt_identity)
jwt.user_identity_loader(identity_loader)

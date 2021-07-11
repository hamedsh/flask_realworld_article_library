from flask_realworld.database import db, Model, Column, SurrogatePK


class Tags(Model, SurrogatePK):
    __tablename__ = "tags"

    tag_name = Column(db.String(100))

    def __init__(self, tag_name: str) -> None:
        Model.__init__(self, tag_name=tag_name)

    def __repr__(self) -> str:
        return self.tag_name

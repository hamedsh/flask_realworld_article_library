from flask_realworld.extensions import db

tag_assoc = db.Table(
    "tag_assoc",
    db.Column("tag", db.Integer, db.ForeignKey("tags.id")),
    db.Column("article", db.Integer, db.ForeignKey("article.id")),
)

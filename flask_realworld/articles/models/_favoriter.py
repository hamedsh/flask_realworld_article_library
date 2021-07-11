from flask_realworld.extensions import db

favoriter_assoc = db.Table(
    "favoritor_assoc",
    db.Column("favoriter", db.Integer, db.ForeignKey("userprofile.id")),
    db.Column("favorited_article", db.Integer, db.ForeignKey("article.id")),
)

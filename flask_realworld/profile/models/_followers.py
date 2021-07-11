from flask_realworld.extensions import db

followers_assoc = db.Table(
    "followers_assoc",
    db.Column("follower", db.Integer, db.ForeignKey("userprofile.user_id")),
    db.Column("followed_by", db.Integer, db.ForeignKey("userprofile.user_id")),
)

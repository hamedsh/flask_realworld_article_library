from flask import jsonify
from flask import Blueprint

from flask_realworld.articles.models.tags import Tags

ENDPOINT_PREFIX = 'tags'
tags_bp = Blueprint('tage', __name__)


@tags_bp.route('tags', methods=('GET', ), endpoint='get_tags')
def get_tags():
    return jsonify({'tags': [tag.name for tag in Tags.query.all()]})

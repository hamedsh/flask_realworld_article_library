from typing import Any

from flask import jsonify


def template(data, code=500):
    return {
        'message': {
            'errors': {
                'body': data
            }
        },
        'status_code': code
    }


USER_NOT_FOUND = template(['user not found'], code=404)
USER_ALREADY_REGISTERED = template(['User already registered'], code=422)
UNKNOWN_ERROR = template([], code=500)
ARTICLE_NOT_FOUND = template(['Article not found'], code=404)
COMMENT_NOT_OWNED = template(['Not your article'], code=422)


class InvalidUsage(Exception):
    status_code = 200

    def __init__(self, message: str, status_code: int = None, payload: Any = None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        message = self.message
        return jsonify(message)

    @classmethod
    def user_not_found(cls) -> object:
        return cls(**USER_NOT_FOUND)

    @classmethod
    def user_already_registered(cls) -> object:
        return cls(**USER_ALREADY_REGISTERED)

    @classmethod
    def unknown_error(cls) -> object:
        return cls(**UNKNOWN_ERROR)

    @classmethod
    def article_not_found(cls) -> object:
        return cls(**ARTICLE_NOT_FOUND)

    @classmethod
    def comment_not_owned(cls) -> object:
        return cls(**COMMENT_NOT_OWNED)

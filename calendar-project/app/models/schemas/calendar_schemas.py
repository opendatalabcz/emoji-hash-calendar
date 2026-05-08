from marshmallow import Schema, fields, validate

class CalendarLinkSchema(Schema):
    base_url = fields.Url(required=True)
    ics_url = fields.Url(required=True)
    method = fields.Str(
        required=True,
        validate=validate.OneOf([
            "dictionary",
            "embedding - all-MiniLM-L6-v2",
            "embedding - all-MiniLM-L12-v2",
            "embedding - balanced",
            "embedding - multilingual",
            "embedding - bge"
        ])
    )
    dictionary_id = fields.Int(required=False, allow_none=True)
    user_mapping = fields.Dict(required=False)

class CalendarTransformSchema(Schema):
    ics_url = fields.Url(required=True)
    method = fields.Str(
        required=True,
        validate=validate.OneOf([
            "dictionary",
            "embedding - all-MiniLM-L6-v2",
            "embedding - all-MiniLM-L12-v2",
            "embedding - balanced",
            "embedding - multilingual",
            "embedding - bge"
        ])
    )
    dictionary_id = fields.Int(required=False, allow_none=True)
    user_mapping = fields.Dict(required=False)

class TransformTextSchema(Schema):
    text = fields.Str(required=True, validate=validate.Length(min=1))
    method = fields.Str(
        required=True,
        validate=validate.OneOf([
            "dictionary",
            "embedding - all-MiniLM-L6-v2",
            "embedding - all-MiniLM-L12-v2",
            "embedding - balanced",
            "embedding - multilingual",
            "embedding - bge"
        ])
    )
    dictionary_id = fields.Int(required=False, allow_none=True)
    user_mapping = fields.Dict(required=False)

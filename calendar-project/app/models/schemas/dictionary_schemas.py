from marshmallow import Schema, fields, validate

class DictionaryEntrySchema(Schema):
    id = fields.Int(dump_only=True)
    word = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    emoji = fields.Str(required=True, validate=validate.Length(min=1, max=5))
    dictionary_id = fields.Int(dump_only=True)


class DictionaryEntryCreateSchema(Schema):
    word = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    emoji = fields.Str(required=True, validate=validate.Length(min=1, max=5))

class DictionarySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    language = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    description = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)


class DictionaryCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=80))
    language = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    description = fields.Str(required=False, allow_none=True)

from marshmallow import Schema, fields, validate, missing

class MappingSchema(Schema):
    id = fields.Int(dump_only=True)
    word = fields.Str(required=True, validate=validate.Length(min=1))
    emoji = fields.Str(required=True, validate=validate.Length(min=1, max=5))


class MappingCreateSchema(Schema):
    word = fields.Str(required=True, validate=validate.Length(min=1))
    emoji = fields.Str(required=True, validate=validate.Length(min=1, max=5))


class MappingSetSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    mappings = fields.List(fields.Nested(MappingSchema))


class MappingSetCreateSchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50)
    )
    mappings = fields.List(fields.Nested(MappingCreateSchema), required=False)

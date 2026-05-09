from flask import Blueprint, request, Response
from app.services.calendar_service import CalendarService
from app.models.schemas.calendar_schemas import (CalendarLinkSchema, CalendarTransformSchema, TransformTextSchema)

from app.constants import EMBEDDING_MODELS

calendar_bp = Blueprint("calendar", __name__)
service = CalendarService()

link_schema = CalendarLinkSchema()
calendar_transform_schema = CalendarTransformSchema()
transform_text_schema = TransformTextSchema()

@calendar_bp.route("/link", methods=["POST"])
def generate_calendar_link():
    """
    Generates a Google Calendar subscription URL for the transformed ICS feed.
    ---
    tags:
      - Calendar
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            base_url:
              type: string
            ics_url:
              type: string
            method:
              type: string
            dictionary_id:
              type: integer
            user_mapping:
              type: object

    responses:
      200:
        description: Generated subscription URL
        schema:
          type: object
          properties:
            url:
              type: string
    """
    data = link_schema.load(request.get_json())
    url = service.generate_subscription_link(
        data["base_url"],
        data["ics_url"],
        data["method"],
        data.get("dictionary_id"),
        data.get("user_mapping")
    )
    return {"url": url}, 200

@calendar_bp.route("/feed", methods=["GET"])
def calendar_feed():
    """
    Google Calendar subscription endpoint.
    Returns a transformed iCal (.ics) feed as raw text/calendar.
    ---
    tags:
      - Calendar
    produces:
      - text/calendar
    parameters:
      - in: query
        name: ics_url
        type: string
        required: true
        description: URL of the source .ics calendar file to fetch and transform

      - in: query
        name: method
        type: string
        required: true
        enum: ["dictionary", "embedding - all-MiniLM-L6-v2", "embedding - all-MiniLM-L12-v2", "embedding - balanced", "embedding - multilingual", "embedding - bge"]
        description: Transformation method used to convert calendar events into emojis or other representations

      - in: query
        name: dictionary_id
        type: integer
        required: false
        description: ID of a stored emoji dictionary to use for transformation

      - in: query
        name: user_mapping
        type: string
        required: false
        description: Optional JSON string of user-defined emoji mappings that override dictionary values

    responses:
      200:
        description: Successfully transformed calendar feed
        content:
          text/calendar:
            schema:
              type: string

      400:
        description: Bad request (missing parameters or invalid input)

      500:
        description: Internal server error
    """
    ics_url = request.args.get("ics_url")
    method = request.args.get("method")
    dictionary_id = request.args.get("dictionary_id"),
    user_mapping = request.args.get("user_mapping")

    if not ics_url or not method:
        return {"message": "Missing required parameters"}, 400

    ics_bytes = service.generate_feed(
        ics_url,
        method,
        dictionary_id,
        user_mapping
    )

    return Response(
        ics_bytes,
        mimetype="text/calendar",
        headers={
            "Content-Disposition": "inline; filename=calendar.ics"
        }
    )

@calendar_bp.route("/transform", methods=["POST"])
def transform_calendar():
    """
    Transform an iCal (.ics) calendar to use emojis for events.
    ---
    tags:
      - Calendar
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            ics_url:
              type: string
              description: url of .ics file
            method:
              type: string
              enum: ["dictionary", "embedding - all-MiniLM-L6-v2", "embedding - all-MiniLM-L12-v2", "embedding - balanced", "embedding - multilingual", "embedding - bge"]
              description: Transformation method
            dictionary_id:
              type: integer
              description: ID of dictionary stored in database
            user_mapping:
              type: object
              description: Optional user-defined emoji mappings
    responses:
      200:
        description: Transformed .ics file
        content:
          text/calendar:
            schema:
              type: string
      400:
        description: Invalid request
      500:
        description: Internal server error
    """
    data = calendar_transform_schema.load(request.get_json())
    result = service.transform_calendar(
        data["ics_url"],
        data["method"],
        data.get("dictionary_id"),
        data.get("user_mapping")
    )
    return result, 200

@calendar_bp.route("/transform-file", methods=["POST"])
def transform_calendar_file():
    """
    Transform an uploaded iCal (.ics) file using emoji transformation.
    ---
    tags:
      - Calendar
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: file
        type: file
        required: true
        description: ICS file to transform

      - in: formData
        name: method
        type: string
        required: true
        enum: ["dictionary", "embedding - all-MiniLM-L6-v2", "embedding - all-MiniLM-L12-v2", "embedding - balanced", "embedding - multilingual", "embedding - bge"]

      - in: formData
        name: dictionary_id
        type: integer
        required: false

      - in: formData
        name: user_mapping
        type: string
        required: false
        description: Optional JSON string of user-defined emoji mappings

    responses:
      200:
        description: Transformed ICS file (base64 + preview)
      400:
        description: Invalid input
      500:
        description: Internal server error
    """
    uploaded = request.files.get("file")
    if not uploaded:
        return {"message": "ICS file is required"}, 400

    method = request.form.get("method")
    if not method:
        return {"message": "Transformation method is required"}, 400

    dictionary_id = request.form.get("dictionary_id")
    user_mapping_raw = request.form.get("user_mapping")

    import json
    user_mapping = json.loads(user_mapping_raw) if user_mapping_raw else None

    result = service.transform_calendar_from_bytes(
        uploaded.read(),
        method,
        dictionary_id,
        user_mapping
    )
    return result, 200


@calendar_bp.route("/transform-text", methods=["POST"])
def transform_text():
    """
    Transform text into emoji(s).
    ---
    tags:
      - Calendar
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            text:
              type: string
              description: The text to transform
            method:
              type: string
              enum: ["dictionary", "embedding - all-MiniLM-L6-v2", "embedding - all-MiniLM-L12-v2", "embedding - balanced", "embedding - multilingual", "embedding - bge"]
              description: Transformation method
            dictionary_id:
              type: integer
            user_mapping:
              type: object
              description: Optional user-defined emoji mappings
    responses:
      200:
        description: Transformed emoji string
        content:
          application/json:
            schema:
              type: object
              properties:
                emoji:
                  type: string
      400:
        description: Bad request
      500:
        description: Internal server error
    """
    data = transform_text_schema.load(request.get_json())
    emoji = service.transform_text(
        data["text"],
        data["method"],
        data.get("dictionary_id"),
        data.get("user_mapping")
    )
    return {"emoji": emoji}, 200


@calendar_bp.route("/methods", methods=["GET"])
def get_methods():
    """
    Get available transformation methods.
    ---
    tags:
      - Calendar
    responses:
      200:
        description: List of available transformation methods
        schema:
          type: object
          properties:
            methods:
              type: array
              items:
                type: string
    """
    return {"methods": ["dictionary"] + list(EMBEDDING_MODELS.keys())}, 200
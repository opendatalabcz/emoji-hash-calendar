import requests
import base64
from io import BytesIO
from flask import Blueprint, request, jsonify
from services.calendar_service import CalendarService
from services.dictionary_service import DictionaryService


calendar_bp = Blueprint("calendar", __name__, url_prefix="/api/calendars")
service = CalendarService()

@calendar_bp.route("/transformation", methods=["POST"])
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
                  enum: ["dictionary", "embedding"]
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
            description: Bad request
          500:
            description: Internal server error
        """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON payload required"}), 400

        ics_url = data.get("ics_url")
        method = data.get("method")
        dictionary_id = data.get("dictionary_id")
        user_mapping = data.get("user_mapping", None)

        if not ics_url or not method:
            return jsonify({"error": "ics_url and method are required"}), 400

        #if method not in ["dictionary", "embedding"]:
        #    return jsonify({"error": f"Invalid method: {method}"}), 400

        # Download
        resp = requests.get(ics_url, timeout=10)
        if resp.status_code != 200:
            return jsonify({"error": "Failed to download ICS file"}), 400

        content_type = resp.headers.get("Content-Type", "").lower()
        if "calendar" not in content_type and "octet-stream" not in content_type:
            return jsonify({"error": "URL did not return a calendar file"}), 400

        input_stream = BytesIO(resp.content)

        db_dict = {}
        if dictionary_id:
            db_dict = DictionaryService.to_dict(dictionary_id)

        # Merge with user overrides (user wins)
        final_mapping = db_dict.copy()
        if user_mapping:
            final_mapping.update(user_mapping)

        # Transform
        output_stream, preview = service.transform_calendar_stream(
            input_stream,
            method,
            final_mapping
        )

        output_stream.seek(0)
        output_base64 = base64.b64encode(output_stream.read()).decode("utf-8")

        return jsonify({
            "message": "Transformation complete",
            "ics_base64": output_base64,
            "preview": preview[:10]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
              enum: ["dictionary", "embedding"]
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
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON payload required"}), 400

        text = data.get("text")
        method = data.get("method")
        user_mapping = data.get("user_mapping", {})
        dictionary_id = data.get("dictionary_id")

        if not text or not method:
            return jsonify({"error": "text and method are required"}), 400

        #if method not in ["dictionary", "embedding"]:
        #    return jsonify({"error": f"Invalid method: {method}"}), 400

        db_dict = {}
        if dictionary_id:
            db_dict = DictionaryService.to_dict(dictionary_id)

        final_mapping = db_dict.copy()
        if user_mapping:
            final_mapping.update(user_mapping)

        transformed_emoji = service.transform_text_to_emoji(text, method, final_mapping)

        return jsonify({"emoji": transformed_emoji}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
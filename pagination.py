@app.get("/notes")
def get_notes():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    pagination = Note.query.filter_by(user_id=user_id).paginate(
        page=page, per_page=per_page, error_out=False
    )

    notes = [
        {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "user_id": note.user_id
        }
        for note in pagination.items
    ]

    return jsonify({
        "notes": notes,
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev
    }), 200
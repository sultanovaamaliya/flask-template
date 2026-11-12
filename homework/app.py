from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, url_for

from db import get_db, init_app

"Гостевая книга: отзывы с автором и текстом"

app = Flask(__name__)
app.config["DATABASE"] = Path(app.instance_path) / "guestbook.sqlite3"
init_app(app)

MAX_AUTHOR_LENGTH = 80
MAX_TEXT_LENGTH = 2000


def read_reviews(author=None):
    db = get_db()
    if author:
        return db.execute(
            "SELECT id, author, review, created "
            "FROM recall WHERE author = ? ORDER BY created DESC",
            (author,),
        ).fetchall()
    return db.execute(
        "SELECT id, author, review, created "
        "FROM recall ORDER BY created DESC"
    ).fetchall()


def review_error(author, text): #возвращает список ошибок
    errors = []
    if not isinstance(author, str) or not author.strip():
        errors.append("Имя не может быть пустым.")
    elif len(author.strip()) > MAX_AUTHOR_LENGTH:
        errors.append(f"Имя — не больше {MAX_AUTHOR_LENGTH} символов.")
    if not isinstance(text, str) or not text.strip():
        errors.append("Отзыв не может быть пустым.")
    elif len(text.strip()) > MAX_TEXT_LENGTH:
        errors.append(f"Отзыв — не больше {MAX_TEXT_LENGTH} символов.")
    return errors


def save_review(author, text):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO recall (author, review) VALUES (?, ?)",
        (author.strip(), text.strip()),
    )
    db.commit()
    return cursor.lastrowid


def review_json(r):
    return {
        "id": r["id"],
        "author": r["author"],
        "review": r["review"],
        "created": r["created"],
    }


@app.get("/")
def index():
    return redirect(url_for("reviews_page"))


@app.get("/reviews")
def reviews_page():
    author = request.args.get("author", "").strip() or None
    return render_template(
        "review.html",
        reviews=read_reviews(author),
        current_author=author or "",
    )


@app.post("/reviews")
def review_create():
    author = request.form.get("author", "")
    text = request.form.get("text", "")
    errors = review_error(author, text)
    if errors:
        return render_template(
            "review.html",
            reviews=read_reviews(),
            errors=errors,
            form_author=author,
            form_text=text,
            current_author="",
        ), 400
    save_review(author, text)
    return redirect(url_for("reviews_page"), code=303)


@app.get("/api/recall")
def api_review_list():
    author = request.args.get("author", "").strip() or None
    rows = read_reviews(author)
    return {"reviews": [review_json(r) for r in rows]}


@app.post("/api/recall")
def api_review_create():
    if not request.is_json:
        return {"error": "Отправьте JSON с Content-Type: application/json."}, 415
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return {"error": "Тело запроса должно быть JSON-объектом."}, 400
    author = data.get("author", "")
    review = data.get("review", "")
    errors = review_error(author, review)
    if errors:
        return {"error": errors}, 400
    rid = save_review(author, review)
    return {"id": rid, "author": author.strip(), "review": review.strip()}, 201


if __name__ == "__main__":
    app.run(load_dotenv=False)
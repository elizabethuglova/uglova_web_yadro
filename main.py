import requests
from flask import Flask, render_template, request
from sqlalchemy import func

from data import db_session
from data.random_users import RandomUser

app = Flask(__name__)
app.secret_key = 'some'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# основная страница
@app.route("/", methods=["GET", "POST"])
def index():
    count = request.form.get("count", 50)
    try:
        count = int(count)
    except ValueError:
        count = 50

    db = db_session.create_session()
    users = db.query(RandomUser).order_by(RandomUser.id.desc()).limit(count).all()
    return render_template("index.html", users=users, count=count)


# загрузка 1000 пользователей с API
def load_initial_users():
    db = db_session.create_session()
    if db.query(RandomUser).first():
        return

    response = requests.get("https://randomuser.me/api/?results=1000")
    if response.status_code != 200:
        print("Ошибка загрузки данных из API.")
        return

    for i in response.json()["results"]:
        person = RandomUser(
            gender=i["gender"],
            first_name=i["name"]["first"],
            last_name=i["name"]["last"],
            phone=i["phone"],
            email=i["email"],
            city=i["location"]["city"],
            country=i["location"]["country"],
            picture=i["picture"]["thumbnail"]
        )
        db.add(person)
    db.commit()

# страница конкретного пользователя
@app.route("/user/<int:user_id>")
def user_detail(user_id):
    db = db_session.create_session()
    user = db.get(RandomUser, user_id)
    if not user:
        return "Пользователь не найден", 404
    return render_template("user_detail.html", user=user)


# страница рандомного пользователя
@app.route("/random")
def random_user():
    db = db_session.create_session()
    user_detail = db.query(RandomUser).order_by(func.random()).first()
    if not user_detail:
        return "Нет пользователей в базе данных", 404
    return render_template("user_detail.html", user=user_detail)


if __name__ == '__main__':
    db_session.global_init("db.sqlite")
    load_initial_users()
    app.run(port=8080, host='127.0.0.1')

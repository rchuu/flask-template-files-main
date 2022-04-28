from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user


class Show:
    db = "shows_schema"

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.network = data['network']
        self.release_date = data['release_date']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = ''

    @classmethod
    def save(cls, data):
        query = "INSERT INTO shows (title, description, network, release_date, user_id) VALUES (%(title)s,%(description)s,%(network)s,%(release_date)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = """SELECT * FROM shows
        WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows;"
        results = connectToMySQL(cls.db).query_db(query)
        all_shows = []
        for row in results:
            all_shows.append(cls(row))
        return all_shows

    @classmethod
    def get_user_shows(cls, data):
        query = """SELECT * FROM shows
        JOIN users
        ON shows.user_id = users.id
        WHERE shows.id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        for row in results:
            one_show = cls(row)
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": "not telling",
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }

            one_show.creator = user.User(user_data)
        return one_show

    @classmethod
    def update(cls, data):
        query = """UPDATE shows 
        SET title= %(title)s,
        network= %(network)s,
        release_date= %(release_date)s,
        description= %(description)s,
        updated_at= NOW()
        WHERE id= %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = """DELETE FROM shows
        WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_show(show):
        is_valid = True
        if len(show['title']) < 3:
            is_valid = False
            flash("Title is too short", "show")
        if len(show['network']) < 3:
            is_valid = False
            flash("Network name is too short", "show")
        if len(show['description']) < 2:
            is_valid = False
            flash("Description is too short", "show")
        if len(show['release_date']) == "":
            is_valid = False
            flash("missing a date", "show")
        return is_valid

    @classmethod
    def get_user_likes(cls, data):
        query = "SELECT * FROM shows LEFT JOIN likes ON likes.show_id = shows.id LEFT JOIN users ON likes.user_id = user.id WHERE shows.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        show = cls(results[0])
        for row in results:
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["shows.created_at"],
                "updated_at": row["shows.updated_at"]
            }
            show.on_users.append(user.User(user_data))
        return show

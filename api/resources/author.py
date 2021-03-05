from api import Resource, reqparse, db
from api.models.author import AuthorModel
#from api.schemas.author import author_schema, authors_schema


class Author(Resource):

    def get(self, id=None):
        if id is None:
            authors = AuthorModel.query.all()
            #authors = authors_schema.dump(authors)
            if not authors:
                return "There is no author yet", 200
        else:
            author = AuthorModel.query.get(id)
            if not author:
                return f"No author with id={id}", 404
            authors = [author]
        authors_lst = [author.to_dict() for author in authors]
        #authors_lst = authors_schema.dump(authors)

        return authors_lst, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        parser.add_argument("surname", required=True)
        author_data = parser.parse_args()

        author = AuthorModel.query.filter(AuthorModel.name == author_data["name"],
                                          AuthorModel.surname == author_data["surname"]).all()
        if author:
            if author[0].name == author_data["name"] or author[0].surname == author_data["surname"]:
                return "An author with such name or surname already exists. " \
                       "You can only add a unique name and surname", 400

        author = AuthorModel(author_data["name"], author_data["surname"])

        try:
            db.session.add(author)
            db.session.commit()
            return author.to_dict(), 201
        except:
            return "An error occurred while adding new author" \
                   "or an author with such name or surname already exists. " \
                    "You can only add a unique name and surname", 404

    def put(self, id):
        author = AuthorModel.query.get(id)
        if not author:
            return f"No author with id={id}", 404
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("surname")
        author_data = parser.parse_args()

        if author.name == author_data["name"] and author.surname == author_data["surname"]:
            return "The name and surname of the author you want to change" \
                   " matches the ones you pass in the request." \
                   " Enter another name or surname of the author." \
                   " The changes will not be applied.", 400

        author.name = author_data["name"] or author.name
        author.surname = author_data["surname"] or author.surname

        try:
            db.session.add(author)
            db.session.commit()
            return author.to_dict(), 200
        except:
            return "An error occurred while changing the author. " \
                   "Maybe The name and surname of the author you want to change" \
                   " matches the ones you pass in the request." \
                   " Enter another name or surname of the author." \
                   " The changes will not be applied.", 404

    def delete(self, id):
        author = AuthorModel.query.get(id)
        if not author:
            return f"No author with id={id}", 404
        try:
            db.session.delete(author)
            db.session.commit()
            return f"Author with id={id} deleted", 200
        except:
            return "An error occurred while deleting the author", 404

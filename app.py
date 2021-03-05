from api import api, app
from config import Config
from api.resources.author import Author
from api.resources.quote import Quotes


api.add_resource(Author, "/authors", "/authors/<int:id>")

api.add_resource(Quotes, "/quotes",
                         "/authors/<int:author_id>/quotes",
                         "/authors/<int:author_id>/quotes/<int:quote_id>")

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)

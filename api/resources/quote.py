from api import Resource, reqparse, db
from api.models.author import AuthorModel
from api.models.quote import QuoteModel
#from api.schemas.quote import quote_schema, quotes_schema

class Quotes(Resource):

    def get(self, author_id=None, quote_id=None):
        if author_id is None and quote_id is None:
            quotes = QuoteModel.query.all()
            if not quotes:
                return "There are no quotes yet", 200

        if author_id is not None and quote_id is None:
            quotes = QuoteModel.query.filter(QuoteModel.author_id == author_id).all()
            if not quotes:
                return f"Author with id={author_id} has no quotes or author is not exists", 404

        if author_id is not None and quote_id is not None:
            quote = QuoteModel.query.filter(QuoteModel.author_id == author_id, QuoteModel.id == quote_id).all()
            if not quote:
                return f"Author with id={author_id} has no quote with id={quote_id} or author is not exists", 404
            quotes = quote

        quotes_lst = [quote.to_dict() for quote in quotes]
        return quotes_lst, 200

    def post(self, author_id):
        parser = reqparse.RequestParser()
        parser.add_argument("quote")
        quote_data = parser.parse_args()

        author = AuthorModel.query.get(author_id)
        if not author:
            return f"Author with id={author_id} is not exists."
        quote = QuoteModel(author, quote_data["quote"])
        db.session.add(quote)
        db.session.commit()

        return quote.to_dict(), 201

    def put(self, author_id, quote_id):
        quote = QuoteModel.query.filter(QuoteModel.author_id == author_id, QuoteModel.id == quote_id).all()
        if not quote:
            return f"This author has no quote with id={quote_id}", 404
        parser = reqparse.RequestParser()
        parser.add_argument("quote")
        quote_data = parser.parse_args()

        quote[0].quote = quote_data["quote"] or quote[0].quote

        db.session.add(quote[0])
        db.session.commit()
        return quote[0].to_dict(), 200

    def delete(self, author_id, quote_id):

        quote = QuoteModel.query.filter(QuoteModel.author_id == author_id, QuoteModel.id == quote_id).all()
        if not quote:
            return f"No quote with id={quote_id}", 404

        db.session.delete(quote[0])
        db.session.commit()

        return f"Quote with id={quote_id} deleted", 200
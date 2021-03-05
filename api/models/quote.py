from api import db
from api.models.author import AuthorModel


class QuoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id))
    quote = db.Column(db.String(255), unique=False)

# пример способа связи из доки зефирок
# class QuoteModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id))
#     quote = db.Column(db.String(255), unique=False)
#     author = db.relationship('AuthorModel', backref='quote', lazy='joined')
#     cascade = "all, delete-orphan" - в этом случае не работает

    def __init__(self, author: AuthorModel, quote: str):
        self.author_id = author.id
        self.quote = quote

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))
        d["author"] = self.author.to_dict()
        return d
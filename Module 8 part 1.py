from mongoengine import connect, Document, StringField, DateTimeField, ReferenceField, ListField

# Крок 1: Підключення до бази даних MongoDB
connect('my_database', host='mongodb://username:password@host:port/my_database')

# Крок 2: Створення моделей
class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)

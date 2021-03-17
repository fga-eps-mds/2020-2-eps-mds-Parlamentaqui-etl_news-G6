from mongoengine import *

class Deputy(Document):
    id = IntField(primary_key=True)
    name = StringField(required=True)
    photo_url = StringField()
    initial_legislature_id = IntField(required=True)
    final_legislature_id = IntField()
    initial_legislature_year = IntField(required=True)
    final_legislature_year = IntField()
    last_activity_date = DateTimeField()
    full_name = StringField()
    sex = StringField()
    email = StringField()
    birth_date = DateTimeField()
    death_date = DateTimeField()
    federative_unity = StringField()
    party = StringField()
    instagram_username = StringField()
    twitter_username = StringField()
    facebook_username = StringField()

class News(Document):
    id = IntField(primary_key=True)
    deputy_id = IntField()
    link = StringField()
    photo = StringField()
    title = StringField()
    abstract = StringField()
    deputy_name = StringField()
    update_date = DateTimeField()
    source = StringField()

# class Tweet(Document):
#     tweet_id = IntField(primary_key=True)
#     deputy_id = IntField()
#     name = StringField()
#     twitter_username = StringField()
#     date = DateTimeField()


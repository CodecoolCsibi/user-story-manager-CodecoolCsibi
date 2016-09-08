from peewee import *
db = SqliteDatabase('userstories.db')


class BaseModel(Model):

    class Meta:
        database = db


class Story(BaseModel):
    story_id = PrimaryKeyField()
    story_title = CharField(unique=True, null=False)
    user_story = CharField(null=False)
    acceptance_criteria = CharField(null=False)
    business_value = IntegerField(null=False)
    estimation = DoubleField()
    status = CharField(default='Planning')



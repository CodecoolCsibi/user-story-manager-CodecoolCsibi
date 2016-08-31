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

    def check_if_valid(self):
        if 100 <= int(self.business_value) <= 1500 and 0.5 <= float(self.estimation) <= 40 and float(self.estimation) % 0.5 == 0:
            return True
        else:
            return False




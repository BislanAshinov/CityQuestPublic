from peewee import *
import config


class BaseModel(Model):
    class Meta:
        database = config.db


class Team(Model):
    id = IntegerField()
    chat_id = IntegerField(default=-1)
    username = CharField(default="")
    name = CharField(default="")
    longitude = DoubleField(default=-1)
    latitude = DoubleField(default=-1)
    is_login = BooleanField(default=False)
    wheres_going = IntegerField(default=-1)
    wait_cp_ans = IntegerField(default=-1)
    main_cp1 = BooleanField(default=False)
    main_cp2 = BooleanField(default=False)
    main_cp3 = BooleanField(default=False)
    main_cp4 = BooleanField(default=False)
    begin_time = DoubleField(default=-1)
    quest_timer_id = IntegerField(default=-1)
    answer = BooleanField(default=False)
    all_info = TextField(default="Доступная информация:\n")
    dop_task = IntegerField(default=0)

    class Meta:
        database = config.db


class Admin(Model):
    chat_id = IntegerField(default=-1)
    username = CharField(default="")

    class Meta:
        database = config.db


class MainCheckPoint(Model):
    id = IntegerField()
    name = CharField(default="")
    teams_going = IntegerField(default=-0)
    code_word = CharField(default="")
    info = TextField(default="")

    class Meta:
        database = config.db



class DopTask(Model):
    id = IntegerField()
    task_text = TextField(default="")
    answer = CharField(default="")

    class Meta:
        database = config.db


class SolvedTask(Model):
    id_task = IntegerField(default=-1)
    id_team = IntegerField(default=-1)

    class Meta:
        database = config.db
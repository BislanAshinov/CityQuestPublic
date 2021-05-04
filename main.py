import config
import utils
import models


@config.the_bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.start(message)


@config.the_bot.message_handler(commands=['reg'])
def reg(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.reg(message)


@config.the_bot.message_handler(commands=['mainc'])
def mainc(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.mainc(message)


@config.the_bot.message_handler(commands=['dop_task'])
def dop_task(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.dop_task(message)


@config.the_bot.message_handler(commands=['time'])
def time(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.rem_time(message)


@config.the_bot.message_handler(commands=['info'])
def info(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.info(message)


@config.the_bot.message_handler(commands=['mc'])
def mc(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.mc(message)


@config.the_bot.message_handler(commands=['cancel'])
def mc(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.cancel(message)


@config.the_bot.message_handler(commands=['map'])
def map(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.map(message.chat.id)


@config.the_bot.message_handler(commands=['answer'])
def answer(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.answer(message)


@config.the_bot.callback_query_handler(func=lambda call: True)
def callback(call):
    utils.keyboard_callback(call)


@config.the_bot.message_handler(commands=['help'])
def help(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.help(message)


@config.the_bot.message_handler(commands=['admin'])
def admin(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.admin(message)


@config.the_bot.message_handler(commands=['begin'])
def begin(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.begin(message)


@config.the_bot.message_handler(commands=['end'])
def end(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.end(message)


@config.the_bot.message_handler(commands=['check_cp'])
def check_cp(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.check_cp(message)


@config.the_bot.message_handler(commands=['check_team'])
def check_team(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.check_team(message)


@config.the_bot.message_handler(commands=['add_team'])
def add_team(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.add_team(message)


@config.the_bot.message_handler(commands=['delete_team'])
def delete_team(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.delete_team(message)


@config.the_bot.message_handler(commands=['delete_cp'])
def delete_cp(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.delete_cp(message)


@config.the_bot.message_handler(commands=['add_dop_task'])
def add_dop_task(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.add_dop_task(message)


@config.the_bot.message_handler(commands=['add_mainc'])
def add_mainc(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.add_mainc(message)


@config.the_bot.message_handler(commands=['the_end'])
def the_end(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.the_end(message)


@config.the_bot.message_handler(content_types=['text'])
def new_message(message):
    if message.chat.id != config.group_id:
        config.the_bot.forward_message(config.group_id, message.chat.id, message.message_id)
    utils.new_message(message)


if __name__ == '__main__':
    config.db.connect()
    config.db.create_tables([models.Team, models.Admin, models.MainCheckPoint, models.DopTask])
    config.the_bot.infinity_polling()
    config.db.close()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import models
import config
import peewee
import threading
import time

from geopy import distance
from telebot import types


def help_admin(message):
    config.the_bot.send_message(message.chat.id, text="/begin id - начать квест для команды с номером id\n"
                                                      "/end id - дисквалифицировать команду с номером id\n"
                                                      "/check_cp - проверить состояние ГГ\n"
                                                      "/check_team - проверить состояние Команды\n"
                                                      "/all_info - вся информация о командах\n"
                                                      "/add_team id - добавить команду\n"
                                                      "/add_dop_task answer*переход на новую строку*text"
                                                      " - добавить доп задание\n"
                                                      "/add_mainc Name code_word*переход на новую строку*info"
                                                      " - добавить главного героя\n"
                                                      "/delete_team id - удалить команду\n"
                                                      "/the_end - разослать командам конечное сообщение\n"
                                                      "Развлекайтесь!)")


def help_team(message=None, team_id=None):
    chat_id = 0
    if message is None and team_id is not None:
        team = models.Team.get(models.Team.id == team_id)
        chat_id = team.chat_id
    elif message is not None and team_id is None:
        chat_id = message.chat.id
    else:
        return
    config.the_bot.send_message(chat_id, text="/info - вся доступная информация о происходящем\n"
                                              "/time - оставшееся время\n"
                                              "/mainc - выбор Главного героя, к которому Вы хотите направиться\n"
                                              "/cancel - отменить выбор Главного героя\n"
                                              "/map - карта\n"
                                              "/dop_task - дополнительная задача\n"
                                              "/answer text - сдать ответ, \"text\" - текст Вашего ответа\n"
                                              "/help - выдает этот текст\n")


def quest_timeout(team_id):
    team = models.Team.get(models.Team.id == team_id)
    team.quest_timer_id = -1
    team.save()
    config.the_bot.send_message(team.chat_id, text="Ваше время почти вышло! У Вас осталось 10 минут\n"
                                                   "Пора записывать ответ, если Вы этого еще не "
                                                   "сделали\n"
                                                   "Для этого введите команду\n"
                                                   "/answer text\n"
                                                   "где text = текст Вашего ответа")


def begin_quest(team_id):
    team = models.Team.get(models.Team.id == team_id)

    config.the_bot.send_message(team.chat_id, text=config.video)
    mess = config.the_bot.send_message(team.chat_id, text="Добро пожаловать! Квест начался\n"
                                                   "В начале Вам доступны 4 главных героя(отмечены на карте)\n"
                                                   "Квест длится 4.5 часа. Отсчет пошел!"
                                                   "Итак, вам предстоит ответить на следующие вопросы:\n"
                                                    "1. Было ли совершено убийство?\n"
"2. Если ответ положительный, кто это сделал? Каковы мотивы?\n"
"Чтобы ответить на данные вопросы, вам нужно опросить как можно "
                                                   "больше подозреваемых. Не забывайте, они не всегда "
                                                   "говорят правду, и всю информацию стоит перепроверять.\n"
"Постарайтесь грамотно распорядиться своим временем," 
    "чтобы успеть пообщаться с большим количеством людей.\n"
"Фиксируйте информацию, которую вам сообщают подозреваемые. "
"Кроме этого, у вас есть возможность помочь компании "
    "восстановиться после краха сделки.\n Введите команду "
                                                   "«/dop_task» для получения заданий. Данный пункт не является "
                                                   "обязательным, но положительно отражается на вашей карме:)\n Желаем удачи!")

    now = time.time()
    t2 = threading.Timer(60 * 270 - 600, quest_timeout, team_id)
    l = len(config.timers)
    config.timers.append(t2)
    team.begin_time = now
    team.cp_timer_id = l
    team.quest_timer_id = l
    team.save()

    help_team(mess)


def start(message):
    config.the_bot.send_message(message.chat.id, text="Приветствую Вас, мои детективы!\n"
                                                      "Сегодня я буду играть роль Ватсона и помогать Вам расследовать "
                                                      "преступление(или не преступление?...)"
                                                      "\nПредставьтесь - введите команду\n"
                                                      "/reg id Name\n"
                                                      "id - выданный Вам идентификатор\n"
                                                      "Name - название Вашей команды")


def help(message):
    try:
        team = models.Team.get(models.Team.chat_id == message.chat.id)
        help_team(message)
    except peewee.DoesNotExist:
        try:
            admin = models.Admin.get(models.Admin.chat_id == message.chat.id)
            help_admin(message)
        except peewee.DoesNotExist:
            start(message)


def reg(message):   #/reg id Name
    mes = message.text.split()
    if len(mes) <= 2:
        config.the_bot.send_message(message.chat.id, text="Неверный формат команды")
        return
    try:
        team = models.Team.get(models.Team.chat_id == message.chat.id)
        config.the_bot.send_message(message.chat.id, text="Вы уже зарегистрированы!")
    except peewee.DoesNotExist:
        team_id = int(mes[1])
        try:
            team = models.Team.get(models.Team.id == team_id)
            if team.is_login:
                config.the_bot.send_message(message.chat.id, text="Эта команда уже зарегистрирована, "
                                                                  "может Вы потерялись?...")
                return
            name = ""
            for m in mes[2:]:
                name += m
            try:
                this_name = models.Team.get(models.Team.name == name)
                config.the_bot.send_message(message.chat.id, text="Очень оригинально! Но переделайте.\n"
                                                                  "Команда с таким названием уже есть в игре.")
            except peewee.DoesNotExist:
                team.name = name
                team.chat_id = message.chat.id
                team.username = message.from_user.username
                team.is_login = True
                team.save()
                config.the_bot.send_message(message.chat.id, text="Вы успешно зарегистрированы!\n"
                                                                  "Ожидайте начала квеста и дальнейших инструкций")
        except peewee.DoesNotExist:
            config.the_bot.send_message(message.chat.id, text="Такого идентификатора не существует, проверьте правильность"
                                                              "данных")


def mainc(message):
    try:
        team = models.Team.get(models.Team.chat_id == message.chat.id)
        if team.wait_cp_ans > 0:
            config.the_bot.send_message(message.chat.id, text="Я жду ответа для одного из героев!")
            return
        if team.wheres_going > 0:
            config.the_bot.send_message(message.chat.id, text="Вы уже направляетесь к главному герою!\n"
                                                              "Чтобы отменить это, введите команду /cancel")
            return
        keyboard = types.InlineKeyboardMarkup()
        if not team.main_cp1:
            maincp = models.MainCheckPoint.get(models.MainCheckPoint.id == 1)
            button = types.InlineKeyboardButton(text=maincp.name, callback_data="main 1")
            keyboard.add(button)
        if not team.main_cp2:
            maincp = models.MainCheckPoint.get(models.MainCheckPoint.id == 2)
            button = types.InlineKeyboardButton(text=maincp.name, callback_data="main 2")
            keyboard.add(button)
        if not team.main_cp3:
            maincp = models.MainCheckPoint.get(models.MainCheckPoint.id == 3)
            button = types.InlineKeyboardButton(text=maincp.name, callback_data="main 3")
            keyboard.add(button)
        if not team.main_cp4:
            maincp = models.MainCheckPoint.get(models.MainCheckPoint.id == 4)
            button = types.InlineKeyboardButton(text=maincp.name, callback_data="main 4")
            keyboard.add(button)
        button = types.InlineKeyboardButton(text="Отмена", callback_data="main 5 " + str(team.id))
        keyboard.add(button)
        config.the_bot.send_message(message.chat.id, text="Выберите героя", reply_markup=keyboard)
    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")


def keyboard_callback(call):
    data = call.data.split()
    try:
        team = models.Team.get(models.Team.chat_id == call.message.chat.id)
        if data[0] == "main":
            if int(data[1]) == 5:
                config.the_bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.id,
                                                         reply_markup="")
                return
            if team.wheres_going > 0:
                config.the_bot.send_message(call.message.chat.id, text="Эй! Вы уже направляетесь к главному герою!")
                config.the_bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.id,
                                                         reply_markup="")
                return
            try:
                maincp = models.MainCheckPoint.get(models.MainCheckPoint.id == int(data[1]))
                if maincp.teams_going > 0:
                    keyboard = types.InlineKeyboardMarkup()
                    button = types.InlineKeyboardButton(text="Да", callback_data="change yes " + data[1])
                    keyboard.add(button)
                    button = types.InlineKeyboardButton(text="Нет", callback_data="change no " + data[1])
                    keyboard.add(button)
                    config.the_bot.send_message(call.message.chat.id, text="Предупреждение!\n"
                                                                       "К этому главному герою уже направляются "
                                                                       "команды.\n"
                                                                       "Хотите поменять выбор?", reply_markup=keyboard)
                    return
                team.wheres_going = int(data[1])
                maincp.teams_going += 1
                team.save()
                maincp.save()
                config.the_bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.id,
                                                         reply_markup="")
                config.the_bot.send_message(call.message.chat.id, text="Вы направляетесь к герою " + maincp.name + "\nВ"
                                                                        "ведите кодовое слово после изучения героя.")
            except peewee.DoesNotExist:
                return
        elif data[0] == "change":
            if data[1] == "yes":
                config.the_bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.id,
                                                         reply_markup="")
                mainc(call.message)
                return
            if data[1] == "no":
                team.wheres_going = int(data[2])
                team.save()
                config.the_bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.id,
                                                         reply_markup="")
                config.the_bot.send_message(call.message.chat.id, text="Отлично! Продолжайте свой путь!")
                return
    except peewee.DoesNotExist:
        config.the_bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.id, reply_markup="")


def dop_task(message):
    try:
        team = models.Team.get(models.Team.chat_id == message.chat.id)
        try:
            dop_task = models.DopTask.get(models.DopTask.id == team.dop_task + 1)
            if dop_task.id % 2:
                config.the_bot.send_message(message.chat.id, text="Нам нужна дополнительная помощь в расследовании!"
                                                                  "Я буду ждать ответа на эту задачу, просто напишите "
                                                                  "сообщение с ответом")
                config.the_bot.send_message(message.chat.id, text=dop_task.task_text)
            else:
                config.the_bot.send_message(message.chat.id, text="Отвлекитесь и расслабьтесь. Вот Вам тестик)\n"
                                                                  "Я буду ждать Ваш результат, просто напишите "
                                                                  "сообщение с ответом")
                config.the_bot.send_message(message.chat.id, text=dop_task.task_text)
        except peewee.DoesNotExist:
            config.the_bot.send_message(message.chat.id, text="Упс... дополнительные задачи закончились(")
    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")


def cancel(message):
    try:
        team = models.Team.get(models.Team.chat_id == message.chat.id)
        if team.wheres_going > 0:
            try:
                maincp = models.MainCheckPoint.get(models.MainCheckPoint.id == team.wheres_going)
                maincp.teams_going -= 1
                maincp.save()
                team.wheres_going = -1
                team.save()
                config.the_bot.send_message(message.chat.id, text="Вы отменили свой выбор главного героя")
                return
            except peewee.DoesNotExist:
                return
        config.the_bot.send_message(message.chat.id, text="Вы не выбрали героя. Нечего отменять")
    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")


def rem_time(message):
    try:
        team = models.Team.get(models.Team.chat_id == message.chat.id)
        begin_time = team.begin_time
        now = time.time()
        remain = 5 * 60 * 60 - 30 * 60 - int(now - begin_time)
        text = "Осталось времени: " + str(remain // 3600) + "ч " + str((remain % 3600) // 60) + "м"
        config.the_bot.send_message(message.chat.id, text=text)
    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")


def info(message):
    try:
        team = models.Team.get(models.Team.chat_id == message.chat.id)
        all_info = team.all_info
        config.the_bot.send_message(message.chat.id, text=all_info)
    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")


def mc(message):
    try:
        team = models.Team.get(models.Team.chat_id == message.chat.id)
        config.the_bot.send_message(message.chat.id, text="https://www.google.com/maps/d/u/0/viewer?mid=1mDIh-"
                                                          "hKETMACOug0BuJttVnTwkBAwqC-&ll=55.750737670652555%2"
                                                          "C37.621622150000015&z=13\nВы нашли пасхалку! Держите карту "
                                                          "с ближайшими маками!")
    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")


def map(chat_id):
    config.the_bot.send_message(chat_id, text=config.map)


def answer(message): ###/answer text
    try:
        team = models.Team.get(models.Team.chat_id == message.chat.id)
        if len(message.text) < 8:
            config.the_bot.send_message(message.chat.id, text="Неверный формат команды")
            return
        if team.answer:
            config.the_bot.send_message(message.chat.id, text="Вы уже ввели ответ! Настоящий детектив не совершает "
                                                              "ошибок и не отказывается от своих слов!")
        else:
            team.answer = True
            team.save()
            config.the_bot.send_message(message.chat.id, text="Ваш ответ принят!")
    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")


def new_message(message):
    try:
        team = models.Team.get(models.Team.chat_id == message.chat.id)
        if team.wheres_going > 0:
            maincp = models.MainCheckPoint.get(models.MainCheckPoint.id == team.wheres_going)
            if message.text.lower() == maincp.code_word.lower():
                maincp.teams_going -= 1
                maincp.save()
                team.all_info += "\n" + maincp.name + "\n" + maincp.info
                if team.wheres_going == 1:
                    team.main_cp1 = True
                if team.wheres_going == 2:
                    team.main_cp2 = True
                if team.wheres_going == 3:
                    team.main_cp3 = True
                if team.wheres_going == 4:
                    team.main_cp4 = True
                team.wheres_going = -1
                team.save()
                config.the_bot.send_message(message.chat.id, text="Правильно! Теперь я верю, что Вы изучили этого героя")
                config.the_bot.send_message(message.chat.id, text="Подробности о герое добавлены в доступную информацию\n"
                                                                  "Для ее получения введите /info")
                return
            try:
                dop_task = models.DopTask.get(models.DopTask.id == team.dop_task + 1)
                config.the_bot.send_message(message.chat.id,
                                                text="Ответ принят, спасибо!")
                team.dop_task += 1
                team.save()
            except peewee.DoesNotExist:
                config.the_bot.send_message(message.chat.id,
                                            text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")
        else:
            try:
                dop_task = models.DopTask.get(models.DopTask.id == team.dop_task + 1)
                if message.text.lower() == dop_task.answer.lower():
                    config.the_bot.send_message(message.chat.id,
                                                text="Дополнительная задача решена правильно! Продолжайте в том же духе!")
                    team.dop_task += 1
                    team.save()
            except peewee.DoesNotExist:
                config.the_bot.send_message(message.chat.id,
                                            text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")
    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")


def admin(message):   #/admin password
    pswd = message.text[7:]
    if pswd != config.pswd:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")
    else:
        admin = models.Admin.create(chat_id=message.chat.id, username=message.from_user.username)
        admin.save()
        config.the_bot.send_message(message.chat.id, text="Да ладно, Богдан норм чел")
        help_admin(message)


def begin(message):   #/begin id
    try:
        this_admin = models.Admin.get(models.Admin.chat_id == message.chat.id)
        team_id = int(message.text[7:])
        try:
            team = models.Team.get(models.Team.id == team_id)
            begin_quest(team_id)
            config.the_bot.send_message(message.chat.id, text="Команда начала квест! Отсчет пошел")
            map(team.chat_id)

        except peewee.DoesNotExist:
            config.the_bot.send_message(message.chat.id, text="Такого идентификатора не существует, проверьте правильность"
                                                              "данных")

    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")


def end(message):    #/end id
    try:
        this_admin = models.Admin.get(models.Admin.chat_id == message.chat.id)
        team_id = int(message.text[5:])
        try:
            team = models.Team.get(models.Team.id == team_id)
            mess = config.the_bot.send_message(team.chat_id, text="Вы были дисквалифицированы за нарушение правил!\n"
                                                                  "Преступление не раскрыто.\n")
            config.timers[team.quest_timer_id].cancel()
            team.chat_id = -1
            team.save()
            mc(mess)

        except peewee.DoesNotExist:
            config.the_bot.send_message(message.chat.id, text="Такого идентификатора не существует, проверьте "
                                                              "правильность данных")
    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")


def check_cp(message):
    try:
        this_admin = models.Admin.get(models.Admin.chat_id == message.chat.id)
        text = ''
        for cp in models.MainCheckPoint.select():
            text += cp.name + ". Сюда идут " + str(cp.teams_going) + " команд\n"
        config.the_bot.send_message(message.chat.id, text=text)
    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")


def check_team(message):   #/check_team id
    try:
        this_admin = models.Admin.get(models.Admin.chat_id == message.chat.id)
        team_id = int(message.text[12:])
        try:
            team = models.Team.get(models.Team.id == team_id)
            text = str(team.id) + " " + team.name + " "
            if team.is_login:
                text += "logged in\n"
            else:
                text += "not logged in\n"
            text += "Пройдено главных героев: "
            cnt = int(team.main_cp1) + int(team.main_cp2) + int(team.main_cp3) + int(team.main_cp4)
            text += str(cnt) + "\n"
            text += "Побочных задач: " + str(team.dop_task) + "\n"
            text += "Идут к " + str(team.wheres_going) + " герою\n"
            if team.answer:
                text += "Ответ введен\n"
            else:
                text += "Ответ не введен\n"

            begin_time = team.begin_time
            now = time.time()
            remain = 5 * 60 * 60 - int(now - begin_time)
            if remain > 0:
                text += "Осталось времени: " + str(remain // 3600) + "ч + " + str((remain % 3600) // 60) + "м"
            config.the_bot.send_message(message.chat.id, text=text)

        except peewee.DoesNotExist:
            config.the_bot.send_message(message.chat.id, text="Такого идентификатора не существует, проверьте "
                                                              "правильность данных")

    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")


def add_team(message):   ###/add_team id
    try:
        admin = models.Admin.get(models.Admin.chat_id == message.chat.id)
        new_team = models.Team.create(id=int(message.text[10:]))
        new_team.save()
        config.the_bot.send_message(message.chat.id, text="Команда создана")
    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")


def add_dop_task(message): ###/add_dop_task answer\ntext
    try:
        admin = models.Admin.get(models.Admin.chat_id == message.chat.id)
        mess = message.text[14:].split('\n')
        task_text = ""
        for m in mess[1:]:
            task_text += m
        cnt = models.DopTask.select().count()
        new_dop_task = models.DopTask.create(id=cnt + 1, answer=mess[0], task_text=task_text)
        new_dop_task.save()
        config.the_bot.send_message(message.chat.id, text="Задача добавлена")
    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")


def add_mainc(message):  ###/add_mainc Name code_word\nTextinfo
    try:
        admin = models.Admin.get(models.Admin.chat_id == message.chat.id)
        mess = message.text[11:].split('\n')
        fmess = mess[0].split()
        text_info = ""
        for m in mess[1:]:
            text_info += m
        cnt = models.MainCheckPoint.select().count()
        new_maincp = models.MainCheckPoint.create(id=cnt + 1, name=fmess[0], code_word=fmess[1], info=text_info)
        new_maincp.save()
        config.the_bot.send_message(message.chat.id, text="Главный герой добавлен")
    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")


def delete_team(message):   ###/delete_team id
    try:
        admin = models.Admin.get(models.Admin.chat_id == message.chat.id)
        mess = message.text[13:]
        try:
            team = models.Team.get(models.Team.id == int(mess))
            team.delete_instance()
            config.the_bot.send_message(message.chat.id, text="Запись о команде удалена")
        except peewee.DoesNotExist:
            config.the_bot.send_message(message.chat.id, text="Такой команды не существует")
    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")


def delete_cp(message):   ###/delete_cp Name
    try:
        admin = models.Admin.get(models.Admin.chat_id == message.chat.id)
        mess = message.text[11:]
        try:
            mainc = models.MainCheckPoint.get(models.MainCheckPoint.name == mess)
            mainc.delete_instance()
            config.the_bot.send_message(message.chat.id, text="Запись о герое удалена")
        except peewee.DoesNotExist:
            config.the_bot.send_message(message.chat.id, text="Такого героя не существует")
    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")


def all_info(message):
    try:
        admin = models.Admin.get(models.Admin.chat_id == message.chat.id)
        for team in models.Team.select():
            mess = message
            mess.text + " " + str(team.id)
            check_cp(mess)
    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")


def the_end(message):
    try:
        admin = models.Admin.get(models.Admin.chat_id == message.chat.id)
        for team in models.Team.select():
            config.the_bot.send_message(team.chat_id, text=config.message1)
            config.the_bot.send_message(team.chat_id, text=config.message2)
            config.the_bot.send_message(team.chat_id, text=config.message3)
            config.the_bot.send_message(team.chat_id, text=config.message4)
            config.the_bot.send_message(team.chat_id, text=config.message5)
        config.the_bot.send_message(message.chat.id, text="Сообщения отправлены")
    except peewee.DoesNotExist:
        config.the_bot.send_message(message.chat.id, text="Не понимаю Вас! Соберитесь, мы здесь по важному делу!")
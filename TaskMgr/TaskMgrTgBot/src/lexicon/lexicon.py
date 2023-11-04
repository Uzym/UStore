from emoji import emojize

START_COMMAND = "start"
HELP_COMMAND = "help"
PROJECTS_COMMAND = "projects"
NEW_PROJECT_COMMAND = "new_project"

COMMANDS: list[tuple[str, str]] = [
    (START_COMMAND, "перейти в главное меню"),
    (HELP_COMMAND, "открыть справку"),
    (PROJECTS_COMMAND, "открыть проекты"),
    (NEW_PROJECT_COMMAND, "создать проект")
]

LEXICON: dict[str, str] = {
    "main_window": emojize(":up_arrow:Главное меню"),
    "get_me": emojize(":factory_worker:Мой аккаунт"),
    "projects": emojize(":file_folder:Ваши проекты"),
    "new_project": emojize(":building_construction:Создать проект"),
    "back": emojize(":BACK_arrow:Назад"),
    "cancel": emojize(":stop_sign:Отменить"),
    "main_menu_button": emojize(":up_arrow:Главное меню"),
    "help_button": emojize(":red_question_mark:Помощь"),
    "new_project_title": "Введите название проекта",
    "new_project_description": "Введите описание проекта",
    "ok": emojize(":green_circle:Подтвердить"),
    "update_project_title": "Изменить имя",
    "update_project_description": "Изменить описание",
    "users": emojize(":construction_worker:Люди"),
    "add": emojize(":plus:Добавить"),
    "sections": emojize(":books:Списки"),
    "update_section": "Изменить список",
    "update_section_title": "Изменить название",
    "update": emojize(":memo: Изменить"),
    "card_update_title": "Изменить название",
    "card_update_description": "Изменить описание",
    "card_update_tags": "Изменить теги",
    "card_update_tags_message": "Чтобы добавить тег отправте сообщение с текстом тега, чтобы удалить "
                                "тег нажмите на соотвествующую кнопку на клавиатуре",
    "card_update_due": "Изменить дедлайн",
    "card_update_section": emojize(":ON!_arrow:Переместить карточку"),
    "await_user_role_select": "Выберите роль пользователя",
    "add_message": "Отправте сообщение",
    "comments": emojize(":e-mail:Комментарии"),
    # Commands
    "skip": "Пропущенно",
    "start": "Для создания проекта используйте команду /new_project название\nДля просмотра текущих проектов используйте /projects",
    "help": "Данный бот служит для управления и командной работы над несколькими проектами",
    "not_found": "Данный элемент не найден",
    "loading": "Выполняется запрос",
    "bad_input": "Неправильный ввод",
    "new_project_good": "Проект успешно создан!",
    "update_project": "Изменить проект",
    "get_project": "Получить проект",
    "add_section_project": "Добавить список",
    "get_section_project": "Открыть списки",
    "add_user_project": "Добавить человека",
    "get_user_project": "Получить список людей",
    "start_add_user": "Отправте имя человека которого хотите добавить",
    "add_user_keyboard": "добавить с правами:",
    "add_user_message": "Для удостоверения в том что это тот человек нажмите на кнопку с его именем, далее под ним вы можете выбрать роль с которой добавлять пользователя",
    "end_add_user": "Пользователь добавлен",
    "start_add_section": "Отправте название списка",
    "end_add_section": "Список создан",
    "start_update_project": "Введите новое название и описание двумя сообщениями",
    "end_update_project": "Проект изменен",
    "defualt_description_project": "Это ваш проект",
    "get_section": "Получить список",
    "add_card_section": "Добавить карточку",
    "get_card_section": "Получить список карточек",
    "post_section": "Создать список",
    "get_cards": "Список карточек"
}
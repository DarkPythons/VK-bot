from vk_api.keyboard import VkKeyboard, VkKeyboardColor

class KeyBoard:
    """Клавиатура с начальными кнопками выбора функции"""
    keyboard_hello = VkKeyboard(one_time=True)
    keyboard_hello.add_button('Информация из Wiki', color=VkKeyboardColor.POSITIVE)
    keyboard_hello.add_line()
    keyboard_hello.add_button('Получить интереный факт', color=VkKeyboardColor.POSITIVE)
    keyboard_hello.add_line()
    keyboard_hello.add_button('Заметки', color=VkKeyboardColor.POSITIVE)
    keyboard_hello.add_line()
    keyboard_hello.add_button('Информация о погоде', color=VkKeyboardColor.POSITIVE)
    keyboard_hello.add_line()
    keyboard_hello.add_openlink_button('GitHub проекта', 'https://github.com/VoblaSuperFish/VkBot')

    """Клавиатура, если человек ввёл команду, которой нет"""
    keyboard_no_command = VkKeyboard(one_time=True)
    keyboard_no_command.add_button('Помощь', color=VkKeyboardColor.POSITIVE)
    keyboard_no_command.add_line()
    #Ссылка поддержки может быть любой
    keyboard_no_command.add_openlink_button('Поддержка', link='https://github.com/VoblaSuperFish/VkBot')

    """Клавитура для отмены ввода"""
    keyboard_exit = VkKeyboard(one_time=False)
    keyboard_exit.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)

    """Клавиатура для рассылки админом"""
    keyboard_mailing = VkKeyboard(one_time=True)
    keyboard_mailing.add_button('Рассылка напоминания', color=VkKeyboardColor.POSITIVE)
    keyboard_mailing.add_line()
    keyboard_mailing.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)

    """Клавиатура для заметок"""
    keyboard_notes = VkKeyboard(one_time=True)
    keyboard_notes.add_button('Добавить заметку', color=VkKeyboardColor.POSITIVE)
    keyboard_notes.add_line()
    keyboard_notes.add_button('Получить свои заметки', color=VkKeyboardColor.PRIMARY)
    keyboard_notes.add_line()
    keyboard_notes.add_button('Удалить заметки', color=VkKeyboardColor.NEGATIVE)

    """Клавитура для заметок, когда пользователь в процессе вода"""
    keyboard_stopped_input = VkKeyboard(one_time=False)
    keyboard_stopped_input.add_button('Остановить ввод', color=VkKeyboardColor.NEGATIVE)

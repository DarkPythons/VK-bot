from vk_api.keyboard import VkKeyboard, VkKeyboardColor

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


keyboard_no_command = VkKeyboard(one_time=True)
keyboard_no_command.add_button('Помощь', color=VkKeyboardColor.POSITIVE)
keyboard_no_command.add_line()
#Ссылка поддержки может быть любой
keyboard_no_command.add_openlink_button('Поддержка', link='https://github.com/VoblaSuperFish/VkBot')

keyboard_exit = VkKeyboard(one_time=False)
keyboard_exit.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)

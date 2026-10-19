# ss14-dwarf-accent
программа имитирующая акцент дворфов из ss14 | a program that simulates the dwarf accent from SS14
ЭТО НЕ ВИРУС!!! КОД ОТКРЫТ, ЧИТАЙТЕ ЕСЛИ СОМНЕВАЕТЕСЬ!!

Фичи

    Глобальный хук: Работает поверх любых окон, перехватывая ввод на уровне ОС.

    Поддержка раскладок: Корректно понимает русские буквы, даже если физически нажаты клавиши английской раскладки (использует системные вызовы Windows).

    Умные предлоги: Распознает предлоги (в, на, от, для и т.д.). Если после предлога идет слово, скрипт сначала проверяет их совместное значение (например, в принципе -> в прынцыпэ), и только потом — само слово.

    Сохранение регистра: Автоматически адаптирует регистр (Привет -> Прывэт, ПРИВЕТ -> ПРЫВЭТ).

    Защита от зацикливания: Отслеживает собственные синтетические нажатия, чтобы не обрабатывать их повторно.

Как это работает (Техническая часть)

Скрипт использует низкоуровневые хуки библиотеки keyboard и ctypes из стандартной библиотеки Python.

    Перехват (Low-Level Hook):
    Функция keyboard.hook(_on_key) вешает хук на все физические нажатия клавиш. События летят в отдельном потоке.

    Определение символа (scan_to_char):
    Библиотека keyboard по умолчанию отдает названия клавиш в английской раскладке. Чтобы понять, что пользователь нажал «привет», а не «ghbdtn», используется ctypes.windll.user32:

        GetForegroundWindow и GetWindowThreadProcessId получают ID активного окна и его потока.

        GetKeyboardLayout вытаскивает текущую раскладку (русскую/английскую).

        ToUnicodeEx конвертирует скан-код нажатой клавиши в реальный Unicode-символ с учетом зажатого Shift.

    Буферизация:
    Каждый распознанный символ падает в список _buffer. При нажатии на «границу» (Space, Enter, Tab) буфер собирается в строку — это и есть слово, которое нужно проверить.

    Логика замен (_process_word):

        Проверяет, был ли предыдущий обработанный токен предлогом.

        Если да — ищет комбо "предлог + слово" в словаре DWARF_REPLACEMENTS.

        Если комбо нет — ищет просто "слово".

        Если найдено — запоминает длину строки, которую надо удалить.

    Инъекция (Ввод):

        Скрипт стирает исходное слово, отправляя N-ное количество Backspace через keyboard.send().

        Печатает новое слово через keyboard.write().

        Самое важное: на время этой операции выставляется флаг _injecting, чтобы хук игнорировал искусственно созданные нажатия и программа не ушла в бесконечный цикл.

Установка и запуск

    Установите зависимости:
    bash

    pip install keyboard

    Запустите скрипт (желательно от имени администратора, так как не все приложения разрешают перехватывать ввод без прав):
    bash

    python Main.py

    Печатайте в любой программе.

    Выход из программы: Ctrl + Alt + Q.
ВАЖНО!!
    я не несу ответственность за любые баны из-за этой программы, на различных серверах это могут расценить как чит, заранее          уточняйте можно ли использовать эту программу на сервере!!!


Features

    Global hook: Works over any windows, intercepting input at the OS level.

    Layout support: Correctly understands Russian letters, even if the keys for the English layout are physically pressed (uses Windows system calls).

    Smart prepositions: Recognizes prepositions (in, on, from, for, etc.). If a word follows a preposition, the script first checks their combined meaning (for example, in principle -> in pryntsype), and only then the word itself.

    Case preservation: Automatically adapts the case (Hello -> Privet, HELLO -> PRIVET).

    Loop protection: Tracks its own synthetic keystrokes to avoid processing them repeatedly.

How it works (Technical part)

The script uses low-level hooks from the keyboard and ctypes libraries from the standard Python library.

    Interception (Low-Level Hook):
    The keyboard.hook(_on_key) function attaches a hook to all physical key presses. Events are delivered in a separate thread.

    Character detection (scan_to_char):
    By default, the keyboard library returns key names in the English layout. To understand that the user pressed “hello” and not “ghbdtn,” ctypes.windll.user32 is used:

        GetForegroundWindow and GetWindowThreadProcessId retrieve the ID of the active window and its thread.

        GetKeyboardLayout retrieves the current keyboard layout (Russian/English).

        ToUnicodeEx converts the scan code of the pressed key into a real Unicode character, taking into account the Shift key being held down.

    Buffering:
    Each recognized character is added to the _buffer list. When a “boundary” is pressed (Space, Enter, Tab), the buffer is assembled into a string — this is the word that needs to be checked.

    Replacement logic (_process_word):

        Checks whether the previous processed token was a preposition.

        If yes, it searches for the “preposition + word” combo in the DWARF_REPLACEMENTS dictionary.

        If the combo is not found, it searches for just “word”.

        If found, it stores the length of the string that needs to be deleted.

    Injection (Input):

        The script erases the original word by sending N number of Backspaces via keyboard.send().

 It then types the new word via keyboard.write().

 The most important thing is that during this operation, the _injecting flag is set so that the hook ignores the artificially created keystrokes and the program doesn’t get stuck in an infinite loop.

 Installation and launch

    Install the dependencies:
    bash

    pip install keyboard

    Run the script (preferably as an administrator, as not all applications allow intercepting input without permissions):
    bash

    python Main.py

    Type in any program.

    Exit the program: Ctrl + Alt + Q.
IMPORTANT!!
    I am not responsible for any bans caused by this program; on various servers, this may be considered a cheat. Please check in advance whether it is allowed to use this program on the server!!!

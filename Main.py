import ctypes
import os
import time
from ctypes import wintypes

import keyboard

user32 = ctypes.windll.user32


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_size_t),
    ]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_size_t),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]


class _INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    ]


class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", _INPUT_UNION),
    ]


INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
VK_BACK = 0x08
VK_SPACE = 0x20
VK_RETURN = 0x0D
VK_TAB = 0x09

_BOUNDARY_VK = {
    "space": VK_SPACE,
    "enter": VK_RETURN,
    "tab": VK_TAB,
}


def _ki(vk, scan, flags):
    inp = INPUT()
    inp.type = INPUT_KEYBOARD
    inp.union.ki.wVk = vk
    inp.union.ki.wScan = scan
    inp.union.ki.dwFlags = flags
    inp.union.ki.time = 0
    inp.union.ki.dwExtraInfo = 0
    return inp


def _send_batch(inputs):
    if not inputs:
        return 0
    arr = (INPUT * len(inputs))(*inputs)
    return user32.SendInput(len(inputs), arr, ctypes.sizeof(INPUT))


def scan_to_char(scan_code):
    if not scan_code or scan_code > 0x100:
        return None
    try:
        vk = user32.MapVirtualKeyW(scan_code, 1)
        if not vk:
            return None
        hwnd = user32.GetForegroundWindow()
        thread_id = user32.GetWindowThreadProcessId(hwnd, None)
        layout = user32.GetKeyboardLayout(thread_id)
        state = (ctypes.c_ubyte * 256)()
        user32.GetKeyboardState(state)
        if user32.GetAsyncKeyState(0x10) & 0x8000:
            state[0x10] = 0x80
        else:
            state[0x10] = 0
        buf = ctypes.create_unicode_buffer(8)
        res = user32.ToUnicodeEx(vk, scan_code, state, buf, 8, 0, layout)
        if res > 0:
            return buf[0]
    except Exception:
        pass
    return None


DWARF_REPLACEMENTS = {
    "ты": "тый",
    "вы": "вый",
    "он": "он",
    "она": "она",
    "они": "оны",
    "это": "это",
    "этот": "этот",
    "такой": "такый",
    "такая": "такайа",
    "такое": "такойэ",
    "кто": "кто",
    "кого": "кого",
    "кому": "кому",
    "вас": "вас",
    "нас": "нас",
    "вам": "вам",
    "нам": "нам",
    "пожалуйста": "пожалста",
    "спасибо": "спасыбо",
    "извини": "извыны",
    "извините": "извынытэ",
    "прости": "просыты",
    "простите": "просыытэ",
    "пока": "пока",
    "прощай": "прощай",
    "здравствуйте": "здарова",
    "добрый": "добрый",
    "доброе": "добройэ",
    "утро": "утро",
    "день": "дэнь",
    "вечер": "вэчэр",
    "знаю": "знайу",
    "знаешь": "знаеш",
    "понимаю": "понымайу",
    "понимаешь": "понымаеш",
    "вижу": "выжу",
    "видишь": "выдыш",
    "хочу": "хочшу",
    "хочешь": "хочэш",
    "хотим": "хочшым",
    "могу": "могу",
    "можешь": "можэш",
    "идти": "йиты",
    "идем": "йдэм",
    "пошли": "пошлы",
    "купи": "купы",
    "купить": "купыт",
    "продать": "продат",
    "дать": "дат",
    "брать": "брат",
    "взять": "взят",
    "жить": "жыть",
    "умереть": "умэрэть",
    "любить": "любыт",
    "ненавидеть": "нэнавыдэт",
    "работать": "роботат",
    "играть": "играт",
    "спать": "спат",
    "бухать": "бухат",
    "курить": "курыт",
    "смотреть": "сматрэт",
    "слушать": "слушэт",
    "сказал": "сказал",
    "сказала": "сказала",
    "говорил": "говорыл",
    "думать": "думат",
    "время": "врэмйа",
    "место": "мэсто",
    "город": "город",
    "страна": "страна",
    "жизнь": "жызнь",
    "смерть": "смэрть",
    "любовь": "любофь",
    "деньги": "дэнэг",
    "работа": "робота",
    "игра": "игра",
    "компьютер": "кампухтэр",
    "телефон": "тэлэфон",
    "интернет": "ынтэрнэт",
    "музыка": "музыка",
    "песня": "пэснйа",
    "кино": "кыно",
    "фильм": "фыльм",
    "книга": "кныга",
    "хороший": "хорошый",
    "плохой": "плохой",
    "красивый": "красывый",
    "умный": "умный",
    "глупый": "глупый",
    "новый": "новый",
    "старый": "старый",
    "быстрый": "быстрый",
    "медленный": "мэдлэнный",
    "сложный": "сложный",
    "легкий": "лёхкый",
    "холодный": "холодный",
    "горячий": "горячшый",
    "очень": "очшэн",
    "много": "многа",
    "мало": "мала",
    "быстро": "быстра",
    "медленно": "мэдлэнна",
    "здесь": "здэсь",
    "там": "там",
    "всегда": "всэгда",
    "никогда": "ныкогда",
    "теперь": "тэпэр",
    "потом": "потом",
    "хорошо": "хорошо",
    "плохо": "плоха",
    "хуй": "хуйэ",
    "хуйня": "хуйнйа",
    "блядь": "блят",
    "нахуй": "нахуйэ",
    "заебал": "зайэбал",
    "заебали": "зайэбалы",
    "долбоёб": "долбойоб",
    "пидор": "пыдор",
    "мудак": "мудак",
    "тварь": "тварь",
    "говно": "гавно",
    "станция": "станцыйа",
    "инженер": "инжэнэр",
    "офицер": "офыцэр",
    "предатель": "прэдатэль",
    "оружие": "оружыйэ",
    "стрелять": "стрылят",
    "взрыв": "взрыв",
    "ремонт": "рэмонт",
    "смена": "смэна",
    "раунд": "раунд",
    "космос": "космас",
    "корабль": "карабыль",
    "агент": "агэнт",
    "убийца": "убыцйа",
    "приветствую": "прывэтству",
    "привет": "прывэт",
    "все": "всэ",
    "от": "од",
    "здравия": "здравыйа",
    "мальчик": "малчшык",
    "меня": "мэнйа",
    "тебя": "тэбйа",
    "себя": "сэбйа",
    "где": "гдэ",
    "ой": "ойё",
    "маленький": "мэлкый",
    "большой": "громадный",
    "сука": "сукэ",
    "даа": "дайэ",
    "конечно": "конэчшно",
    "мужчина": "мужчшына",
    "да": "дэ",
    "тоже": "тожэ",
    "мой": "мойё",
    "нет": "нэт",
    "папа": "уру",
    "мама": "дельва",
    "срочник": "свэжак",
    "новичок": "свэжак",
    "стажёр": "свэжак",
    "профессионал": "бывалый",
    "женщина": "женчшына",
    "ветеран": "бывалый",
    "если": "эслы",
    "следует": "слэдуэт",
    "сделал": "сдэлал",
    "никто": "ныкто",
    "делайте": "дэлать",
    "здравствуй": "здарова",
    "очко": "дыра",
    "делать": "дэлат",
    "синдикатовцы": "сырдикатовцы",
    "капитан": "кэпытан",
    "беги": "дэри ноги",
    "волосы": "борода",
    "выпить": "выпыт",
    "имею": "ымэу",
    "не": "нэ",
    "блин": "рыбьы головэжкы",
    "в принципе": "в прынцыпэ",
    "короче": "корочэ",
    "вообще": "вообчшэ",
    "ну": "нуэ",
    "еда": "жратва",
    "еды": "жратвы",
    "эй": "эйэ",
    "что": "чшто",
    "нее": "нээ",
    "зачем": "зачэм",
    "почему": "почэму",
    "сказать": "сказанут",
    "своим": "своым",
    "её": "йейё",
    "двигай": "двыгай",
    "двигаться": "двыгатсйа",
    "сейчас": "сэйчшас",
    "волшебник": "вельдуност",
    "я": "йа",
    "маг": "вельнудост",
    "чтобы": "чштобы",
    "для": "длйа",
    "даже": "дажэ",
    "ай": "айэ",
    "мышь": "мыш",
    "клоун": "шут",
    "друг": "брат",
    "проблема": "проблэма",
    "есть": "йэст",
    "разрешите": "разрэшытэ",
    "брифинг": "совет",
    "врач": "лекарь",
    "говорить": "говорит",
    "разговаривать": "разговарыват",
    "звоните": "звонытэ",
    "подарить": "подарытэ",
    "дайте": "дайтэ",
    "выдайте": "выдайтэ",
    "ксено": "грызун",
    "шаттл": "судно",
    "думаю": "думайу",
    "крысы": "грызуны",
    "сб": "стража",
    "ебать": "йэбать",
}

PREPOSITIONS = {
    "в", "во", "без", "безо", "для", "до", "за", "из", "изо",
    "к", "ко", "кроме", "между", "на", "над", "о", "об", "обо",
    "от", "ото", "перед", "передо", "по", "под", "подо", "при",
    "про", "ради", "с", "со", "сквозь", "у", "через",
    "благодаря", "вопреки", "согласно", "вблизи", "вдоль",
    "вокруг", "впереди", "вслед", "мимо", "напротив", "около",
    "поверх", "позади", "после", "посреди", "прежде", "против",
    "сверх", "среди", "меж", "пред", "предо",
}

_buffer = []
_last_word = ""
_last_was_prep = False
_mods = set()

_ALL_MODS = {
    "shift", "left shift", "right shift",
    "ctrl", "left ctrl", "right ctrl",
    "alt", "left alt", "right alt", "alt gr",
    "windows", "left windows", "right windows",
}
_BLOCKING_MODS = {
    "ctrl", "left ctrl", "right ctrl",
    "alt", "left alt", "right alt", "alt gr",
    "windows", "left windows", "right windows",
}
_RESET_KEYS = {
    "esc", "delete", "left", "right", "up", "down",
    "home", "end", "page up", "page down", "insert",
}
_BOUNDARY_KEYS = {"space", "enter", "tab"}
_PUNCT = {",", ".", "!", "?", ";", ":", "…"}

_inject_until = 0.0


def _injecting():
    return time.time() < _inject_until


def _mark_inject(duration=0.08):
    global _inject_until
    _inject_until = max(_inject_until, time.time() + duration)


def _preserve_case(original, replacement):
    if not original:
        return replacement
    if original.isupper():
        return replacement.upper()
    if original[0].isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement


def _send_replace_and_boundary(delete_len, text, boundary=None):
    inputs = []
    for _ in range(delete_len):
        inputs.append(_ki(VK_BACK, 0, 0))
        inputs.append(_ki(VK_BACK, 0, KEYEVENTF_KEYUP))
    for ch in text:
        code = ord(ch)
        inputs.append(_ki(0, code, KEYEVENTF_UNICODE))
        inputs.append(_ki(0, code, KEYEVENTF_UNICODE | KEYEVENTF_KEYUP))
    if boundary:
        if boundary in _PUNCT:
            code = ord(boundary)
            inputs.append(_ki(0, code, KEYEVENTF_UNICODE))
            inputs.append(_ki(0, code, KEYEVENTF_UNICODE | KEYEVENTF_KEYUP))
        else:
            bvk = _BOUNDARY_VK.get(boundary)
            if bvk:
                inputs.append(_ki(bvk, 0, 0))
                inputs.append(_ki(bvk, 0, KEYEVENTF_KEYUP))
    _mark_inject(0.08)
    _send_batch(inputs)


def _process_word(word, boundary=None):
    global _last_word, _last_was_prep

    if not word:
        return False

    lower = word.lower()
    replacement = None
    delete_len = 0

    if _last_was_prep and _last_word:
        combo = _last_word.lower() + " " + lower
        if combo in DWARF_REPLACEMENTS:
            replacement = DWARF_REPLACEMENTS[combo]
            replacement = _preserve_case(_last_word + " " + word, replacement)
            delete_len = len(_last_word) + 1 + len(word)

    if replacement is None and lower in DWARF_REPLACEMENTS:
        replacement = DWARF_REPLACEMENTS[lower]
        replacement = _preserve_case(word, replacement)
        delete_len = len(word)

    if replacement is None:
        _last_word = word
        _last_was_prep = lower in PREPOSITIONS
        return False

    delete_len = min(delete_len, 100)
    _send_replace_and_boundary(delete_len, replacement, boundary=boundary)

    rep_parts = replacement.split()
    if rep_parts:
        _last_word = rep_parts[-1]
        _last_was_prep = _last_word.lower() in PREPOSITIONS
    else:
        _last_word = ""
        _last_was_prep = False
    return True


def _on_key(event):
    try:
        name = event.name

        if event.event_type == "down":
            if _injecting():
                return True

            if name in _ALL_MODS:
                _mods.add(name)
                return True

            if any(m in _mods for m in _BLOCKING_MODS):
                _buffer.clear()
                return True

            if name in _BOUNDARY_KEYS:
                word = "".join(_buffer)
                _buffer.clear()
                changed = _process_word(word, boundary=name)
                return not changed

            if name == "backspace":
                if _buffer:
                    _buffer.pop()
                return True

            if name in _RESET_KEYS:
                _buffer.clear()
                return True

            ch = scan_to_char(event.scan_code)
            if not ch or len(ch) != 1 or ch.isspace():
                return True

            if ch in _PUNCT:
                word = "".join(_buffer)
                _buffer.clear()
                changed = _process_word(word, boundary=ch)
                return not changed

            if len(_buffer) < 64:
                _buffer.append(ch)
            return True

        elif event.event_type == "up":
            if name in _ALL_MODS:
                _mods.discard(name)
            return True
    except Exception:
        return True


def main():
    print("Dwarf accent запущен в фоне.")
    print("Печатай в любой программе. Выход: Ctrl + Alt + Q")

    def shutdown():
        print("\nОстанавливаюсь...")
        try:
            keyboard.unhook_all()
        except Exception:
            pass
        os._exit(0)

    keyboard.add_hotkey("ctrl+alt+q", shutdown)
    keyboard.hook(_on_key, suppress=True)

    try:
        keyboard.wait()
    except KeyboardInterrupt:
        shutdown()


if __name__ == "__main__":
    main()

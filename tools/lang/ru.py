# SPDX-License-Identifier: GPL-3.0-only
# Rainbow mode in Russian: what the screen says, the friends' and hats' names, and FOLLOW's songs. Same rules as pt.py.
# Written in Cyrillic capitals (SCRIPT = "cyrillic": 5 x 7 letters on the usual 6 px step, tools/gen_kid_lang.py CYR).
# The notes start as ДО РЕ МИ, as Russian children learn them (the grown-ups' switch still turns them to C D E).
# The button names (SEQ, PLAY, HOME, SAVE, PRESETS, ALGORITHM) stay as they are printed on the FM-1.
SCRIPT = "cyrillic"
DOREMI = True

SUBS = {'{"ACID", 124, KD_BOTH': '{"ХАУС", 124, KD_BOTH',   # the ACID beat's own name ("ACID" is also a sound kid.c looks up)
        '{"DO", "DO#", "RE", "RE#", "MI", "FA", "FA#", "SOL", "SOL#", "LA", "LA#", "SI"}':
        '{"ДО", "ДО#", "РЕ", "РЕ#", "МИ", "ФА", "ФА#", "СОЛЬ", "СОЛЬ#", "ЛЯ", "ЛЯ#", "СИ"}',
        # the drum friends' words that are also compared with a kit's lane names (str_eq), so only the list of words changes
        '"TOM", "CONGA",': '"ТОМ", "КОНГА",', '"CLAVE", "': '"КЛАВЕ", "'}

PAGE = {   # its page on the site (web/make_lang_page.py)
    'lang': 'ru',
    'title': 'Rainbow mode по-русски',
    'lede': 'Музыкальная игрушка для маленьких рук, теперь по-русски. Бесплатная прошивка, которая превращает синтезатор M-VAVE FM-1 в инструмент, на котором играет даже малыш.',
    'try': 'Попробовать в браузере',
    'install': 'Установить на FM-1',
    'note': 'Нет FM-1? Играть всё равно можно: клавишами на экране или клавиатурой компьютера. Установщик и страница с браузерной версией пока на английском, а сама игрушка общается на русском.',
    'inside': 'Что внутри',
    'facts': ['Всё на экране по-русски, а ноты подписаны «до», «ре», «ми», как в школе. Каждая клавиша показывает свою ноту, крупно и своим цветом.',
              '95 друзей, у каждого свой рисунок, звук, небо и любимый ритм, и у всех русские имена: ЕДИНОРОГ, СНЕГОВИК, МОРСКОЙ КОНЁК.',
              'В игре УЧИМ ПЕСНЮ загорается следующая клавиша, а песен в ней 10, среди них ЁЛОЧКА, ВО ПОЛЕ БЕРЁЗА и КОЛЫБЕЛЬНАЯ Брамса.',
              'Для взрослых: подержите HOME секунду, потом OCT- или OCT+ для громкости, или поверните KNOB 1 влево, чтобы убрать нотный стан. HOME и SAVE вместе на 3 секунды переключают в полноценный режим Felucca.'],
    'songs': 'Песни',
    'source': 'Ноты русских песен, «Ёлочки» Леонида Бекмана и «Во поле берёза стояла», взяты из партитур в статьях Википедии о них. Остальные восемь песен знают во всём мире.',
    'footer': 'Бесплатно и с открытым кодом (GPL-3.0), сделано на основе Felucca Лео Курошиты и Hügelton Instruments. Проект поклонников: M-VAVE его не делала и не поддерживает.',
}

WORDS = {
    # ALGORITHM
    "1 FRIEND": "1 ДРУГ", "3 FRIENDS": "3 ДРУГА", "STRUM": "АРФА", "ACCORDION": "АККОРДЕОН", "GUESS": "УГАДАЙ",
    "FOLLOW": "УЧИМ ПЕСНЮ", "CHORDS": "АККОРДЫ", "COPY ME": "ПОВТОРИ",
    # the cards (ALGORITHM turned): up to 3 lines of 17
    "EVERY KEY PLAYS\\nONE NOTE\\nTRY THE KNOBS TOO": "КАЖДАЯ КЛАВИША\\nИГРАЕТ НОТУ\\nКРУТИ РУЧКИ",
    "EVERY KEY PLAYS\\nA BIG CHORD\\nFIND MAGIC ONES": "КАЖДАЯ КЛАВИША\\nИГРАЕТ АККОРД\\nИЩИ ВОЛШЕБНЫЕ",
    "BLACK KEY CHORDS\\nSWEEP THE WHITE\\nKEYS TO STRUM": "ЧЁРНАЯ ВЫБИРАЕТ\\nАККОРД ВЕДИ\\nПО БЕЛЫМ КЛАВИШАМ",
    "HOLD A BLACK KEY\\nPLAY A TUNE ON\\nTHE WHITE KEYS": "ДЕРЖИ ЧЁРНУЮ\\nИГРАЙ МЕЛОДИЮ\\nНА БЕЛЫХ КЛАВИШАХ",
    "A FRIEND SINGS\\nFIND THE NOTE\\nPLAY HEARS AGAIN": "ДРУГ ПОЁТ\\nНАЙДИ НОТУ\\nPLAY ЕЩЁ РАЗ",
    "PLAY THE KEY\\nTHAT LIGHTS UP\\nSEQ PICKS A SONG": "НАЖМИ КЛАВИШУ\\nКОТОРАЯ СВЕТИТСЯ\\nSEQ ДРУГАЯ ПЕСНЯ",
    "HOLD ALL THE KEYS\\nTHAT LIGHT UP\\nSEQ PICKS LESSONS": "ДЕРЖИ ВСЕ КЛАВИШИ\\nКОТОРЫЕ СВЕТЯТСЯ\\nSEQ ВЫБИРАЕТ УРОК",
    "LISTEN TO THE\\nFRIEND\\nTHEN PLAY IT BACK": "СЛУШАЙ ДРУГА\\nИ ПОВТОРИ",
    # the top row's tricks
    "HICCUP": "ЗАПИНКА", "BACKWARDS": "НАОБОРОТ", "SLEEPY": "СОННЫЙ", "SQUEAKY": "МАЛЫШ", "GIANT": "ВЕЛИКАН",
    "FREEZE": "ЗАМРИ",
    # the knobs
    "BIG": "БОЛЬШОЙ", "SMALL": "МАЛЕНЬКИЙ", "DAY": "ДЕНЬ", "SUNSET": "ЗАКАТ", "NIGHT": "НОЧЬ", "ECHO": "ЭХО",
    "WIGGLE": "КАЧКА", "SLOW": "МЕДЛЕННО", "WALK": "ШАГОМ", "FAST": "БЫСТРО", "MEDIUM": "СРЕДНЕ",
    # the beats
    "DANCE": "ТАНЕЦ", "MARCH": "МАРШ", "SPOOKY": "ПРИВИДЕНИЕ", "TRAIN": "ПОЕЗД", "LULLABY": "КОЛЫБЕЛЬНАЯ",
    "HOEDOWN": "КАНТРИ", "POLKA": "ПОЛЬКА", "NO BEAT": "БЕЗ БИТА",
    "ROCK": "РОК", "DISCO": "ДИСКО", "HIP HOP": "ХИП-ХОП", "SAMBA": "САМБА", "REGGAE": "РЕГГИ", "LOFI": "ЛОУФАЙ", "LOFI JAZZ": "ЛОУФАЙ ДЖАЗ",
    "BOSSA": "БОССА-НОВА", "FUNK": "ФАНК", "SKA": "СКА", "TRAP": "ТРЭП", "SALSA": "САЛЬСА", "SHUFFLE": "ШАФФЛ",
    "BREAK": "БРЕЙК",
    # games, secrets, the grown-ups' settings
    "YES!": "ДА!", "TRY AGAIN": "ЕЩЁ РАЗ", "LISTEN": "СЛУШАЙ", "YOUR TURN": "ТВОЙ ХОД", "YAY!": "УРА!",
    "STAR!": "ЗВЕЗДА!", "NEW HAT!": "НОВАЯ ШЛЯПА!", "NEW FRIEND!": "НОВЫЙ ДРУГ!", "NEW SKY!": "НОВОЕ НЕБО!",
    "NEW SONG": "НОВАЯ ПЕСНЯ", "NO HAT": "БЕЗ ШЛЯПЫ", "STARS": "ЗВЁЗДЫ", "LOOK-ALIKES OFF": "ДВОЙНИКИ ВЫКЛ",
    "STAFF ON": "НОТЫ ВКЛ", "STAFF OFF": "НОТЫ ВЫКЛ", "KEY": "ТОН", "VOLUME": "ГРОМКОСТЬ", "LOOP": "ПО КРУГУ",
    "LOOK-ALIKES ON": "ДВОЙНИКИ ВКЛ", "HI!": "ПРИВЕТ!", "HI": "ХЭЙ", "YOUR NAME": "ТВОЁ ИМЯ",
    "PRESETS  LETTER": "PRESETS  БУКВА", "ALGORITHM  NEXT": "ALGORITHM  ДАЛЬШЕ", "SAVE  KEEP IT": "SAVE  ОСТАВИТЬ",
    "HOME  LEAVE IT": "HOME  ВЫЙТИ", "SPARKLE": "ПЕРЕЛИВ", "SPARKLE TUNE": "ПЕРЕЛИВ МЕЛОДИИ", "SPARKLE ALL": "ПЕРЕЛИВ ВЕЗДЕ",
    "WRITE": "СОЧИНЯЙ", "DO RE MI": "ДО РЕ МИ",
    # chords and lessons
    "MAJOR": "МАЖОР", "MINOR": "МИНОР", "SEVEN": "СЕПТ", "NINE": "НОНА",
    "C_MAJOR=": "C_МАЖОР=", "F_MAJOR=": "F_МАЖОР=", "G_MAJOR=": "G_МАЖОР=", "A_MINOR=": "A_МИНОР=", "G_SEVEN=": "G_СЕПТ=",
    "FIRST CHORDS": "ПЕРВЫЕ АККОРДЫ", "POP FOUR": "ПОП-АККОРДЫ", "SEVENTHS": "СЕПТЫ",
    # the drums' names
    "KICK": "БОЧКА", "SNARE": "РАБОЧИЙ", "CLAP": "ХЛОПОК", "HI-HAT": "ХАЙ-ХЭТ", "OPEN HAT": "ОТКРЫТЫЙ ХЭТ", "RIM": "ОБОД",
    "COWBELL": "КОВБЕЛЛ", "CYMBAL": "ТАРЕЛКА",
}

NAMES = {   # the friends (and the look-alikes' stand-ins): one line of 13, or two words of 13 and 15 in all
    "DUCKY": "УТЁНОК", "PINK DUCKY": "РОЗОВЫЙ УТЁНОК", "COOL DUCKY": "КРУТОЙ УТЁНОК", "AXOLOTL": "АКСОЛОТЛЬ",
    "UNICORN": "ЕДИНОРОГ", "GIRAFFE": "ЖИРАФ", "GOO": "СЛИЗЬ", "GOOBERT": "ГУБЕРТ", "BLUE PUP": "СИНИЙ ЩЕНОК",
    "RED MONSTER": "КРАСНЫЙ МОНСТР", "BLUE MONSTER": "СИНИЙ МОНСТР", "APRIL": "АПРЕЛЬ", "SCISSORS": "НОЖНИЦЫ",
    "GHOST": "ПРИЗРАК", "WEB HERO": "ПАУК-ГЕРОЙ", "BUTTERFLY": "БАБОЧКА", "KITTY": "КИСА", "FROG": "ЛЯГУШКА",
    "ROBOT": "РОБОТ", "RAINBOW": "РАДУГА", "PRINCESS DUCKY": "ПРИНЦЕССА УТКА", "RED PUP": "КРАСНЫЙ ЩЕНОК",
    "YELLOW BIRD": "ЖЁЛТАЯ ПТИЦА", "SLIMY": "СЛИЗНЯК", "BUNNY": "ЗАЙКА", "PANDA": "ПАНДА", "PENGUIN": "ПИНГВИН",
    "OWL": "СОВА", "BEE": "ПЧЕЛА", "LADYBUG": "БОЖЬЯ КОРОВКА", "DINO": "ДИНО", "WHALE": "КИТ", "OCTOPUS": "ОСЬМИНОГ",
    "FISH": "РЫБКА", "TURTLE": "ЧЕРЕПАХА", "ICE CREAM": "МОРОЖЕНОЕ", "CUPCAKE": "КЕКС", "ROCKET": "РАКЕТА",
    "STRAWBERRY": "КЛУБНИКА", "STAR": "ЗВЕЗДА", "T-REX": "Т-РЕКС", "SKELETON": "СКЕЛЕТ", "RANCHER": "ФЕРМЕР",
    "RODEO": "КОВБОЙ", "VACUUM": "ПЫЛЕСОС", "SPACE HERO": "КОСМОНАВТ", "BEAT BOT": "БИТ-РОБОТ",
    "TOY DRUM": "БАРАБАНЧИК", "BONGO": "БОНГО", "MONKEY": "ОБЕЗЬЯНКА", "ELEPHANT": "СЛОН", "RACE CAR": "ГОНОЧНАЯ МАШИНА",
    "JELLYFISH": "МЕДУЗА", "BEAR": "МЕДВЕДЬ", "SNOWMAN": "СНЕГОВИК", "CRAB": "КРАБ", "WOLF": "ВОЛК",
    "CAMEL": "ВЕРБЛЮД", "SCIENTIST": "УЧЁНЫЙ", "FLYTRAP": "МУХОЛОВКА", "SUNFLOWER": "ПОДСОЛНУХ",
    "SPIDER MOM": "МАМА-ПАУК", "DRAGON DUCK": "УТКА-ДРАКОН", "SPIDER GRANDMA": "БАБУШКА-ПАУК",
    "NIGHT LIGHT": "НОЧНИК", "GREEN QUEEN": "ЗЕЛЁНАЯ ЦАРИЦА", "KING AXOLOTL": "ЦАРЬ АКСОЛОТЛЬ",
    "FAIRY MONSTER": "МОНСТР-ФЕЯ", "MORNING GLORY": "ВЬЮНОК", "GROUCH": "ВОРЧУН", "TIGER CUB": "ТИГРЁНОК",
    "RACCOON": "ЕНОТ", "GOLDENROD": "ЗОЛОТАРНИК", "PIANO PAL": "ПИАНИНО", "FLUTE BIRD": "ПТИЦА-ФЛЕЙТА",
    "SAX CAT": "КОТ-САКСОФОН", "COW": "КОРОВА", "PIG": "СВИНКА", "SHEEP": "ОВЕЧКА", "SHARK": "АКУЛА",
    "SEAHORSE": "МОРСКОЙ КОНЁК", "STARFISH": "МОРСКАЯ ЗВЕЗДА", "SNAIL": "УЛИТКА", "CATERPILLAR": "ГУСЕНИЦА",
    "FIREFLY": "СВЕТЛЯЧОК", "TRICERATOPS": "ТРИЦЕРАТОПС", "STEGOSAURUS": "СТЕГОЗАВР", "PIZZA": "ПИЦЦА",
    "DONUT": "ПОНЧИК", "BANANA": "БАНАН", "TRAIN": "ПОЕЗД", "FIRE TRUCK": "ПОЖАРНАЯ МАШИНА", "SCHOOL BUS": "АВТОБУС",
    "HELICOPTER": "ВЕРТОЛЁТ", "GOLD DUCKY": "ЗОЛОТОЙ УТЁНОК", "PEACOCK": "ПАВЛИН",
    "SPOTTY PUP": "ПЯТНИСТЫЙ ЩЕНОК", "FOX": "ЛИСА", "FUZZY": "ПУШИСТИК", "BIG BLUE": "БОЛЬШОЙ СИНИЙ", "SPIDER": "ПАУК",
    "PUMPKIN": "ТЫКВА", "CHICK": "ЦЫПЛЁНОК", "BAT": "ЛЕТУЧАЯ МЫШЬ", "HORSE": "ЛОШАДЬ", "CACTUS": "КАКТУС",
    "ALIEN": "ИНОПЛАНЕТЯНИН", "RAINBOW MOM": "МАМА-РАДУГА", "GREEN GRANNY": "ЗЕЛЁНАЯ БАБУЛЯ", "PIXIE": "ФЕЯ",
    "ALLEY CAT": "ДВОРОВЫЙ КОТ", "LION CUB": "ЛЬВЁНОК", "SQUIRREL": "БЕЛОЧКА",
}

HATS = {"PARTY": "КОЛПАК", "CROWN": "КОРОНА", "TOP HAT": "ЦИЛИНДР", "BUCKET": "ПАНАМКА", "WIZARD": "ВОЛШЕБНИК",
        "BEANIE": "ШАПКА", "WESTERN": "КОВБОЙ", "CHEF": "ПОВАР", "PROPELLER": "ПРОПЕЛЛЕР", "FLOWERS": "ЦВЕТЫ",
        "STAR": "ЗВЕЗДА"}

# FOLLOW's songs: "ЁЛОЧКА" (Beckman, 1903) is read from the score in Wikipedia's article on it ("В лесу родилась
# ёлочка (in F).svg": its pickup, repeat and endings written out, moved down 5 semitones to C major: white keys only);
# "ВО ПОЛЕ БЕРЁЗА" (a folk song, Rimsky-Korsakov's no. 39 of 100 Russian Folk Songs, op. 24, 1877) is read from the
# score in the Russian Wikipedia article (Rimsky-Korsakov_Vo_pole_bereza_stoyala.jpg, in E minor, moved down 7 semitones to A minor:
# white keys only); then the ones known everywhere, the same notes as kid.c's English list under Russian names.
# Each fits the keys at OCT 0 (F3 .. G5).
# FOLLOW's songs' pictures: a friend each (gen_kid_art.py FRIENDS), shown beside the song's name and while it plays, so a
# child who can't read yet knows which song it is (u/jrej); no two the same. The songs known everywhere have the English
# list's friends; Ёлочка has the Bunny and Во поле берёза the Goldenrod.
SONG_PICS = {
    'ЁЛОЧКА': 'BUNNY',
    'ВО ПОЛЕ БЕРЁЗА': 'GOLDENROD',
    'ЗВЁЗДОЧКА': 'STAR',
    'БРАТЕЦ ЯКОВ': 'BEAR',
    'ОДА К РАДОСТИ': 'PIANO PAL',
    'БУБЕНЦЫ': 'SNOWMAN',
    'ДЕНЬ РОЖДЕНИЯ': 'CUPCAKE',
    'ТИХАЯ НОЧЬ': 'NIGHT LIGHT',
    'РАДУЙСЯ МИР': 'ROCKET',
    'КОЛЫБЕЛЬНАЯ': 'PANDA',
}

SOLFA_SONGS = []
SONGS = [
    ("ЁЛОЧКА", "G3 E4 E4 D4 E4 C4 G3 G3 G3 E4 E4 D4 A4 G4 G4 A3 A3 F4 F4 E4 D4 C4 G3 E4 E4 D4 E4 C4 G4 A3 A3 F4 F4 E4 D4 C4 G3 E4 E4 D4 E4 C4"),
    ("ВО ПОЛЕ БЕРЁЗА", "E4 E4 E4 E4 D4 C4 C4 B3 A3 E4 E4 G4 E4 D4 C4 C4 B3 A3 B3 C4 D4 C4 C4 B3 A3 B3 C4 D4 E4 C4 C4 B3 A3"),
    ("ЗВЁЗДОЧКА", "C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4 G4 G4 F4 F4 E4 E4 D4 G4 G4 F4 F4 E4 E4 D4 C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4"),
    ("БРАТЕЦ ЯКОВ", "C4 D4 E4 C4 C4 D4 E4 C4 E4 F4 G4 E4 F4 G4 G4 A4 G4 F4 E4 C4 G4 A4 G4 F4 E4 C4 C4 G3 C4 C4 G3 C4"),
    ("ОДА К РАДОСТИ", "E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4 E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 D4 C4 C4"),
    ("БУБЕНЦЫ", "E4 E4 E4 E4 E4 E4 E4 G4 C4 D4 E4 F4 F4 F4 F4 F4 E4 E4 E4 E4 G4 G4 F4 D4 C4"),
    ("ДЕНЬ РОЖДЕНИЯ", "G3 G3 A3 G3 C4 B3 G3 G3 A3 G3 D4 C4 G3 G3 G4 E4 C4 B3 A3 F4 F4 E4 C4 D4 C4"),
    ("ТИХАЯ НОЧЬ", "G4 A4 G4 E4 G4 A4 G4 E4 D5 D5 B4 C5 C5 G4 A4 A4 C5 B4 A4 G4 A4 G4 E4 A4 A4 C5 B4 A4 G4 A4 G4 E4 D5 D5 F5 D5 B4 C5 E5 C5 G4 E4 G4 F4 D4 C4"),
    ("РАДУЙСЯ МИР", "C5 B4 A4 G4 F4 E4 D4 C4 G4 A4 A4 B4 B4 C5 C5 C5 B4 A4 G4 G4 F4 E4 C5 C5 B4 A4 G4 G4 F4 E4 E4 E4 E4 E4 E4 F4 G4 F4 E4 D4 D4 D4 D4 D4 E4 F4 E4 D4 C4"),
    ("КОЛЫБЕЛЬНАЯ", "E4 E4 G4 E4 E4 G4 E4 G4 C5 B4 A4 A4 G4 D4 E4 F4 D4 D4 E4 F4 D4 F4 B4 A4 G4 B4 C5 C4 C4 C5 A4 F4 G4 E4 C4 F4 G4 A4 G4 C4 C4 C5 A4 F4 G4 E4 C4 F4 E4 D4 C4"),
]

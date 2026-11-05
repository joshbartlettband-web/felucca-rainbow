# Rainbow mode in Spanish (for Spanish-speaking kids everywhere: neutral words, Latin American where they differ):
# what the screen says, the friends' and hats' names, and FOLLOW's songs. Same rules as pt.py.
DOREMI = True                          # the note names start as DO RE MI (HOME held 1 s, then KNOB 2: C D E)

PAGE = {   # its page on the site (web/make_lang_page.py)
    'lang': 'es',
    'title': 'Rainbow mode en español',
    'lede': 'Un juguete musical para manos pequeñas, ahora en español. Un firmware gratis que convierte el sintetizador M-VAVE FM-1 en algo que un niño pequeño puede tocar.',
    'install': 'Ponlo en el FM-1',
    'note': '¿No tienes un FM-1? Igual se puede tocar, con las teclas de la pantalla o el teclado de la computadora. El instalador y la página del navegador siguen en inglés, pero el juguete habla español.',
    'inside': 'Qué tiene',
    'facts': ['Todo en la pantalla está en español, y las notas se llaman DO RE MI. Cada tecla muestra su nota, grande y en su color.', '94 amigos, cada uno con su dibujo, su sonido, su cielo y su ritmo favorito, todos con nombre en español: UNICORNIO, AJOLOTE, CABALLITO.', 'SIGUE enciende la próxima tecla de 10 canciones, como Las mañanitas, La cucaracha, Martinillo y Mambrú.', 'Para los grandes: mantén HOME un segundo y luego OCT- u OCT+ para el volumen, o gira KNOB 1 a la izquierda para quitar el pentagrama. HOME y SAVE juntos durante 3 segundos vuelven al sintetizador Felucca.'],
    'songs': 'Las canciones',
    'source': 'Las notas de cada canción vienen de la partitura de su artículo en Wikipedia.',
    'footer': 'Gratis y de código abierto (GPL-3.0), hecho sobre Felucca de Leo Kuroshita y Hügelton Instruments. Un proyecto de fans: M-VAVE no lo hizo y no lo respalda.',
    'try': 'Pruébalo en el navegador',
}

WORDS = {
    # ALGORITHM
    "1 FRIEND": "1 AMIGO", "3 FRIENDS": "3 AMIGOS", "STRUM": "ARPA", "ACCORDION": "ACORDEÓN", "GUESS": "ADIVINA",
    "FOLLOW": "SIGUE", "CHORDS": "ACORDES", "COPY ME": "IMÍTAME",
    # the cards (ALGORITHM turned): up to 3 lines of 17
    "EVERY KEY PLAYS\\nONE NOTE\\nTRY THE KNOBS TOO": "CADA TECLA TOCA\\nUNA NOTA\\nGIRA LOS BOTONES",
    "EVERY KEY PLAYS\\nA BIG CHORD\\nFIND MAGIC ONES": "CADA TECLA TOCA\\nUN ACORDE\\nBUSCA LOS MÁGICOS",
    "BLACK KEY CHORDS\\nSWEEP THE WHITE\\nKEYS TO STRUM": "LA TECLA NEGRA\\nELIGE EL ACORDE\\nROZA LAS BLANCAS",
    "HOLD A BLACK KEY\\nPLAY A TUNE ON\\nTHE WHITE KEYS": "SOSTÉN UNA NEGRA\\nTOCA LA MELODÍA\\nEN LAS BLANCAS",
    "A FRIEND SINGS\\nFIND THE NOTE\\nPLAY HEARS AGAIN": "UN AMIGO CANTA\\nBUSCA LA NOTA\\nPLAY LA REPITE",
    "PLAY THE KEY\\nTHAT LIGHTS UP\\nSEQ PICKS A SONG": "TOCA LA TECLA\\nQUE SE ENCIENDE\\nSEQ ELIGE CANCIÓN",
    "HOLD ALL THE KEYS\\nTHAT LIGHT UP\\nSEQ PICKS LESSONS": "SOSTÉN LAS TECLAS\\nQUE SE ENCIENDEN\\nSEQ ELIGE LECCIÓN",
    "LISTEN TO THE\\nFRIEND\\nTHEN PLAY IT BACK": "ESCUCHA AL AMIGO\\nY TOCA IGUAL",
    # the top row's tricks
    "HICCUP": "HIPO", "BACKWARDS": "AL REVÉS", "SLEEPY": "DORMIDO", "SQUEAKY": "AGUDITO", "GIANT": "GIGANTE",
    "FREEZE": "CONGELA",
    # the knobs
    "BIG": "GRANDE", "SMALL": "PEQUEÑO", "DAY": "DÍA", "SUNSET": "ATARDECER", "NIGHT": "NOCHE", "ECHO": "ECO",
    "WIGGLE": "TEMBLOR", "SLOW": "LENTO", "WALK": "PASEO", "FAST": "RÁPIDO", "MEDIUM": "MEDIANO",
    # the beats
    "DANCE": "BAILE", "MARCH": "MARCHA", "SPOOKY": "MIEDO", "TRAIN": "TREN", "LULLABY": "NANA",
    "HOEDOWN": "RANCHERA", "POLKA": "POLCA", "NO BEAT": "SIN RITMO",
    # games, secrets, the grown-ups' settings
    "YES!": "SÍ!", "TRY AGAIN": "OTRA VEZ", "LISTEN": "ESCUCHA", "YOUR TURN": "TU TURNO", "YAY!": "BIEN!",
    "STAR!": "ESTRELLA!", "NEW HAT!": "GORRO NUEVO!", "NEW FRIEND!": "AMIGO NUEVO!", "NEW SKY!": "CIELO NUEVO!",
    "NEW SONG": "OTRA CANCIÓN", "NO HAT": "SIN GORRO", "STARS": "ESTRELLAS", "LOOK-ALIKES OFF": "PARECIDOS NO",
    "STAFF ON": "PAUTA SÍ", "STAFF OFF": "PAUTA NO",
    "LOOK-ALIKES ON": "PARECIDOS SÍ", "HI!": "HOLA!", "HI": "HOLA", "YOUR NAME": "TU NOMBRE",
    "PRESETS  LETTER": "PRESETS  LETRA", "ALGORITHM  NEXT": "ALGORITHM  SIGUE", "SAVE  KEEP IT": "SAVE  GUARDA",
    "HOME  LEAVE IT": "HOME  SALIR", "SPARKLE": "BRILLO", "SPARKLE TUNE": "BRILLA MELODÍA", "SPARKLE ALL": "BRILLA TODO",
    "WRITE": "COMPONER",
    # chords and lessons
    "MAJOR": "MAYOR", "MINOR": "MENOR", "SEVEN": "SÉPTIMA", "NINE": "NOVENA",
    "C_MAJOR=": "C_MAYOR=", "F_MAJOR=": "F_MAYOR=", "G_MAJOR=": "G_MAYOR=", "A_MINOR=": "A_MENOR=", "G_SEVEN=": "G_SÉPTIMA=",
    "FIRST CHORDS": "PRIMEROS", "POP FOUR": "CUATRO POP", "SEVENTHS": "SÉPTIMAS",
    # the drums' names
    "KICK": "BOMBO", "SNARE": "CAJA", "CLAP": "PALMAS", "HI-HAT": "CHARLES", "OPEN HAT": "PLATO ABIERTO", "RIM": "ARO",
    "COWBELL": "CENCERRO", "CYMBAL": "PLATILLO",
}

NAMES = {   # the friends (and the look-alikes' stand-ins): one line of 13, or two words of 13 and 15 in all
    "DUCKY": "PATITO", "PINK DUCKY": "PATITO ROSA", "COOL DUCKY": "PATO GENIAL", "AXOLOTL": "AJOLOTE",
    "UNICORN": "UNICORNIO", "GIRAFFE": "JIRAFA", "GOO": "MOCO", "GOOBERT": "GOOBERT", "BLUE PUP": "PERRITO AZUL",
    "RED MONSTER": "MONSTRUO ROJO", "BLUE MONSTER": "MONSTRUO AZUL", "APRIL": "APRIL", "SCISSORS": "TIJERAS",
    "GHOST": "FANTASMA", "WEB HERO": "HÉROE ARAÑA", "BUTTERFLY": "MARIPOSA", "KITTY": "GATITO", "FROG": "RANA",
    "ROBOT": "ROBOT", "RAINBOW": "ARCOÍRIS", "PRINCESS DUCKY": "PATA PRINCESA", "RED PUP": "PERRITO ROJO",
    "YELLOW BIRD": "PÁJARO", "SLIMY": "BABOSO", "BUNNY": "CONEJITO", "PANDA": "PANDA", "PENGUIN": "PINGÜINO",
    "OWL": "BÚHO", "BEE": "ABEJA", "LADYBUG": "MARIQUITA", "DINO": "DINO", "WHALE": "BALLENA", "OCTOPUS": "PULPO",
    "FISH": "PEZ", "TURTLE": "TORTUGA", "ICE CREAM": "HELADO", "CUPCAKE": "PASTELITO", "ROCKET": "COHETE",
    "STRAWBERRY": "FRESA", "STAR": "ESTRELLA", "T-REX": "T-REX", "SKELETON": "ESQUELETO", "RANCHER": "RANCHERO",
    "RODEO": "VAQUERO", "VACUUM": "ASPIRADORA", "SPACE HERO": "ASTRONAUTA", "BEAT BOT": "ROBOT RITMO",
    "TOY DRUM": "TAMBORCITO", "BONGO": "BONGÓ", "MONKEY": "MONO", "ELEPHANT": "ELEFANTE", "RACE CAR": "AUTO",
    "JELLYFISH": "MEDUSA", "BEAR": "OSO", "SNOWMAN": "MUÑECO DE NIEVE", "CRAB": "CANGREJO", "WOLF": "LOBO",
    "CAMEL": "CAMELLO", "SCIENTIST": "CIENTÍFICA", "FLYTRAP": "ATRAPAMOSCAS", "SUNFLOWER": "GIRASOL",
    "SPIDER MOM": "MAMÁ ARAÑA", "DRAGON DUCK": "PATO DRAGÓN", "SPIDER GRANDMA": "ABUELA ARAÑA",
    "NIGHT LIGHT": "LUCECITA", "GREEN QUEEN": "REINA VERDE", "KING AXOLOTL": "REY AJOLOTE",
    "FAIRY MONSTER": "MONSTRUO HADA", "MORNING GLORY": "CAMPANILLA", "GROUCH": "GRUÑÓN", "TIGER CUB": "TIGRITO",
    "RACCOON": "MAPACHE", "GOLDENROD": "FLOR DORADA", "PIANO PAL": "PIANITO", "FLUTE BIRD": "PÁJARO FLAUTA",
    "SAX CAT": "GATO SAXO", "COW": "VACA", "PIG": "CERDITO", "SHEEP": "OVEJA", "SHARK": "TIBURÓN",
    "SEAHORSE": "CABALLITO", "STARFISH": "ESTRELLA DE MAR", "SNAIL": "CARACOL", "CATERPILLAR": "ORUGA",
    "FIREFLY": "LUCIÉRNAGA", "TRICERATOPS": "TRICERATOPS", "STEGOSAURUS": "ESTEGOSAURIO", "PIZZA": "PIZZA",
    "DONUT": "DONA", "BANANA": "PLÁTANO", "TRAIN": "TREN", "FIRE TRUCK": "BOMBEROS", "SCHOOL BUS": "AUTOBÚS",
    "HELICOPTER": "HELICÓPTERO", "GOLD DUCKY": "PATITO DE ORO",
    "SPOTTY PUP": "PERRO MANCHAS", "FOX": "ZORRO", "FUZZY": "PELUDITO", "BIG BLUE": "AZULÓN", "SPIDER": "ARAÑA",
    "PUMPKIN": "CALABAZA", "CHICK": "POLLITO", "BAT": "MURCIÉLAGO", "HORSE": "CABALLO", "CACTUS": "CACTUS",
    "ALIEN": "MARCIANO", "RAINBOW MOM": "MAMÁ ARCOÍRIS", "GREEN GRANNY": "ABUELA VERDE", "PIXIE": "DUENDE",
    "ALLEY CAT": "GATO CALLEJERO", "LION CUB": "LEONCITO", "SQUIRREL": "ARDILLA",
}

HATS = {"PARTY": "FIESTA", "CROWN": "CORONA", "TOP HAT": "CHISTERA", "BUCKET": "PESCADOR", "WIZARD": "MAGO",
        "BEANIE": "GORRITO", "WESTERN": "VAQUERO", "CHEF": "CHEF", "PROPELLER": "HÉLICE", "FLOWERS": "FLORES",
        "STAR": "ESTRELLA"}

# FOLLOW's songs: songs Spanish-speaking children sing, each taken note for note from the score in a Wikipedia article (named above
# it; the article's LilyPond rendered to MIDI and its tune read back, tools: see RAINBOW.md), and moved, where
# it says, to fit the keys at OCT 0 (F3 .. G5) with the fewest black keys. A score that repeats itself whole
# is played once. Then a few known everywhere, the same notes as kid.c's English list.
SOLFA_SONGS = []
SONGS = [
    # Las mañanitas (other.wikipedia.org, its score, moved +3)
    ("LAS MAÑANITAS", "G4 G4 C5 C5 B4 C5 D5 B4 C5 D5 E5 C5 D5 E5 F5 F5 F5 E5 D5 C5 B4 D5 C5 B4 C5 D5 E5 F5 D5 C5 E5 D5 B4 B4 C5 D5 E5 C5 E5 D5 B4 B4 C5 D5 E5 C5 C5 F5 F5 G5 F5 E5 C5 B4 C5 D5 E5 F5 D5 C5"),
    # La cucaracha (other.wikipedia.org, its score, moved -5)
    ("LA CUCARACHA", "G3 G3 G3 C4 E4 G3 G3 G3 C4 E4 C4 C4 B3 B3 A3 A3 G3 G3 G3 G3 B3 D4 G3 G3 G3 B3 D4 G4 A4 G4 F4 E4 D4 C4 G3 G3 C4 C4 E4 E4 G4 E4 G4 A4 G4 F4 E4 G4 F4 D4 G3 G3 B3 B3 D4 D4 F4 D4 G4 A4 G4 F4 E4 D4 E4 C4 G3 G3 G3 C4 E4 G3 G3 G3 C4 E4 C4 C4 B3 B3 A3 A3 G3 G3 G3 G3 B3 D4 G3 G3 G3 B3 D4 G4 A4 G4 F4 E4 D4 C4"),
    # Frère Jacques (Martinillo) (fr.wikipedia.org, its score)
    ("MARTINILLO", "G4 A4 B4 G4 G4 A4 B4 G4 B4 C5 D5 B4 C5 D5 D5 E5 D5 C5 B4 G4 D5 E5 D5 C5 B4 G4 G4 D4 G4 G4 D4 G4"),
    # Malbrough s'en va-t-en guerre (Mambrú se fue a la guerra) (fr.wikipedia.org, its score)
    ("MAMBRÚ", "D4 B4 B4 B4 A4 C5 B4 C5 B4 A4 A4 A4 A4 G4 A4 B4 G4 D4 B4 B4 B4 A4 C5 B4 D5 B4 G4 A4 A4 G4 D5 D5 B4 E5 E5 D5 D5 D5 B4 E5 E5 D5"),
    # Guten Abend, gut' Nacht (Brahms) (de.wikipedia.org, its score, moved -3)
    ("ARRORRÓ", "E4 E4 G4 E4 E4 G4 E4 G4 C5 B4 A4 A4 G4 D4 E4 F4 D4 D4 E4 F4 D4 F4 B4 A4 G4 B4 C5 C4 C4 C5 A4 F4 G4 E4 C4 F4 G4 A4 E4 G4 C4 C4 C5 A4 F4 G4 E4 C4 F4 G4 F4 E4 D4 C4"),
    ("ESTRELLITA", "C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4 G4 G4 F4 F4 E4 E4 D4 G4 G4 F4 F4 E4 E4 D4 C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4"),   # known everywhere (as kid.c's English list)
    ("CUMPLEAÑOS", "G3 G3 A3 G3 C4 B3 G3 G3 A3 G3 D4 C4 G3 G3 G4 E4 C4 B3 A3 F4 F4 E4 C4 D4 C4"),   # known everywhere (as kid.c's English list)
    ("HIMNO ALEGRÍA", "E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4 E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 D4 C4 C4"),   # known everywhere (as kid.c's English list)
    ("CASCABEL", "E4 E4 E4 E4 E4 E4 E4 G4 C4 D4 E4 F4 F4 F4 F4 F4 E4 E4 E4 E4 G4 G4 F4 D4 C4"),   # known everywhere (as kid.c's English list)
    # Stille Nacht, heilige Nacht (de.wikipedia.org, its score, moved -2)
    ("NOCHE DE PAZ", "G4 A4 G4 E4 G4 A4 G4 E4 D5 CS5 D5 B4 C5 B4 C5 G4 A4 A4 C5 B4 A4 G4 A4 G4 E4 A4 A4 C5 B4 A4 G4 A4 G4 E4 B4 B4 B4 D5 C5 B4 C5 E5 C5 G4 E4 G4 F4 D4 C4"),
]

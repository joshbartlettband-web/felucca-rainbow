# Rainbow mode in Dutch: what the screen says, the friends' and hats' names, and FOLLOW's songs. Same rules as pt.py.
# The notes stay C D E F G A B, as Dutch children learn them.
DOREMI = False

PAGE = {   # its page on the site (web/make_lang_page.py)
    'lang': 'nl',
    'title': 'Rainbow mode in het Nederlands',
    'lede': 'Een muziekspeeltje voor kleine handjes, nu in het Nederlands. Gratis firmware die de M-VAVE FM-1 synthesizer verandert in iets wat een klein kind kan bespelen.',
    'install': 'Zet het op de FM-1',
    'note': 'Geen FM-1? Je kunt toch spelen, met de toetsen op het scherm of het toetsenbord van je computer. De installer en de browserpagina zijn nog in het Engels, maar het speeltje spreekt Nederlands.',
    'inside': 'Wat erin zit',
    'facts': ['Alles op het scherm is in het Nederlands, en de noten heten C D E F G A B. Elke toets laat zijn noot zien, groot en in zijn eigen kleur.', '94 vriendjes, elk met een eigen tekening, geluid, lucht en lievelingsbeat, allemaal met een Nederlandse naam: EENHOORN, SNEEUWPOP, ZEEPAARDJE.', 'VOLGEN laat de volgende toets oplichten van 9 liedjes, zoals Vader Jacob, Lang zal hij leven en Altijd is Kortjakje ziek.', 'Voor grote mensen: houd HOME een seconde vast, dan OCT- of OCT+ voor het volume, of KNOB 1 naar links om de notenbalk te verbergen. HOME en SAVE samen 3 seconden vasthouden gaat terug naar de Felucca-synth.'],
    'songs': 'De liedjes',
    'source': 'De noten van elk liedje komen uit de partituur in het Wikipedia-artikel erover.',
    'footer': 'Gratis en open source (GPL-3.0), gebouwd op Felucca van Leo Kuroshita en Hügelton Instruments. Een fanproject: M-VAVE heeft het niet gemaakt en steunt het niet.',
    'try': 'Probeer het in je browser',
}

WORDS = {
    # ALGORITHM
    "1 FRIEND": "1 VRIENDJE", "3 FRIENDS": "3 VRIENDJES", "STRUM": "HARP", "ACCORDION": "ACCORDEON", "GUESS": "RADEN",
    "FOLLOW": "VOLGEN", "CHORDS": "AKKOORDEN", "COPY ME": "DOE MIJ NA",
    # the cards (ALGORITHM turned): up to 3 lines of 17
    "EVERY KEY PLAYS\\nONE NOTE\\nTRY THE KNOBS TOO": "ELKE TOETS\\nSPEELT EEN NOOT\\nDRAAI DE KNOPPEN",
    "EVERY KEY PLAYS\\nA BIG CHORD\\nFIND MAGIC ONES": "ELKE TOETS\\nSPEELT AKKOORDEN\\nZOEK DE MAGIE",
    "BLACK KEY CHORDS\\nSWEEP THE WHITE\\nKEYS TO STRUM": "ZWART KIEST HET\\nAKKOORD STRIJK\\nOVER DE WITTE",
    "HOLD A BLACK KEY\\nPLAY A TUNE ON\\nTHE WHITE KEYS": "HOUD ZWART VAST\\nSPEEL DE MELODIE\\nOP DE WITTE",
    "A FRIEND SINGS\\nFIND THE NOTE\\nPLAY HEARS AGAIN": "EEN VRIEND ZINGT\\nZOEK DE NOOT\\nPLAY NOG EEN KEER",
    "PLAY THE KEY\\nTHAT LIGHTS UP\\nSEQ PICKS A SONG": "SPEEL DE TOETS\\nDIE OPLICHT\\nSEQ ANDER LIED",
    "HOLD ALL THE KEYS\\nTHAT LIGHT UP\\nSEQ PICKS LESSONS": "HOUD DE TOETSEN\\nDIE OPLICHTEN\\nSEQ KIEST EEN LES",
    "LISTEN TO THE\\nFRIEND\\nTHEN PLAY IT BACK": "LUISTER GOED\\nEN SPEEL HET NA",
    # the top row's tricks
    "HICCUP": "HIK", "BACKWARDS": "ACHTERUIT", "SLEEPY": "SLAPERIG", "SQUEAKY": "PIEPSTEM", "GIANT": "REUS",
    "FREEZE": "BEVRIEZEN",
    # the knobs
    "BIG": "GROOT", "SMALL": "KLEIN", "DAY": "DAG", "SUNSET": "AVOND", "NIGHT": "NACHT", "ECHO": "ECHO",
    "WIGGLE": "WIEBELEN", "SLOW": "LANGZAAM", "WALK": "LOPEN", "FAST": "SNEL", "MEDIUM": "MIDDEL",
    # the beats
    "DANCE": "DANS", "MARCH": "MARS", "SPOOKY": "SPOOKY", "TRAIN": "TREIN", "LULLABY": "SLAAPLIEDJE",
    "HOEDOWN": "COUNTRY", "POLKA": "POLKA", "NO BEAT": "GEEN BEAT",
    # games, secrets, the grown-ups' settings
    "YES!": "JA!", "TRY AGAIN": "NOG EENS", "LISTEN": "LUISTER", "YOUR TURN": "JIJ NU", "YAY!": "JOEPIE!",
    "STAR!": "STER!", "NEW HAT!": "NIEUWE HOED!", "NEW FRIEND!": "NIEUWE VRIEND!", "NEW SKY!": "NIEUWE LUCHT!",
    "NEW SONG": "NIEUW LIEDJE", "NO HAT": "GEEN HOED", "STARS": "STERREN", "LOOK-ALIKES OFF": "LOOKALIKES UIT",
    "STAFF ON": "NOTENBALK AAN", "STAFF OFF": "NOTENBALK UIT",
    "LOOK-ALIKES ON": "LOOKALIKES AAN", "HI!": "HOI!", "HI": "HOI", "YOUR NAME": "JOUW NAAM",
    "PRESETS  LETTER": "PRESETS  LETTER", "ALGORITHM  NEXT": "ALGORITHM  VERDER", "SAVE  KEEP IT": "SAVE  BEWAREN",
    "HOME  LEAVE IT": "HOME  TERUG", "SPARKLE": "GLITTER", "SPARKLE TUNE": "GLITTER MELODIE", "SPARKLE ALL": "GLITTER ALLES",
    "WRITE": "COMPONEREN",
    # chords and lessons
    "MAJOR": "MAJEUR", "MINOR": "MINEUR", "SEVEN": "SEPTIEM", "NINE": "NONE",
    "C_MAJOR=": "C_MAJEUR=", "F_MAJOR=": "F_MAJEUR=", "G_MAJOR=": "G_MAJEUR=", "A_MINOR=": "A_MINEUR=", "G_SEVEN=": "G_SEPTIEM=",
    "FIRST CHORDS": "DE EERSTE", "POP FOUR": "VIER POP", "SEVENTHS": "SEPTIEMEN",
    # the drums' names
    "KICK": "BASDRUM", "SNARE": "SNAREDRUM", "CLAP": "KLAP", "HI-HAT": "HI-HAT", "OPEN HAT": "OPEN HI-HAT", "RIM": "RAND",
    "COWBELL": "KOEBEL", "CYMBAL": "BEKKEN",
}

NAMES = {   # the friends (and the look-alikes' stand-ins): one line of 13, or two words of 13 and 15 in all
    "DUCKY": "EENDJE", "PINK DUCKY": "ROZE EENDJE", "COOL DUCKY": "STOER EENDJE", "AXOLOTL": "AXOLOTL",
    "UNICORN": "EENHOORN", "GIRAFFE": "GIRAF", "GOO": "SLIJM", "GOOBERT": "GOOBERT", "BLUE PUP": "BLAUW HONDJE",
    "RED MONSTER": "ROOD MONSTER", "BLUE MONSTER": "BLAUW MONSTER", "APRIL": "APRIL", "SCISSORS": "SCHAAR",
    "GHOST": "SPOOK", "WEB HERO": "WEBHELD", "BUTTERFLY": "VLINDER", "KITTY": "POESJE", "FROG": "KIKKER",
    "ROBOT": "ROBOT", "RAINBOW": "REGENBOOG", "PRINCESS DUCKY": "PRINSES EEND", "RED PUP": "ROOD HONDJE",
    "YELLOW BIRD": "GELE VOGEL", "SLIMY": "SLIJMIE", "BUNNY": "KONIJNTJE", "PANDA": "PANDA", "PENGUIN": "PINGUÏN",
    "OWL": "UIL", "BEE": "BIJ", "LADYBUG": "LIEVEHEERTJE", "DINO": "DINO", "WHALE": "WALVIS", "OCTOPUS": "OCTOPUS",
    "FISH": "VIS", "TURTLE": "SCHILDPAD", "ICE CREAM": "IJSJE", "CUPCAKE": "CUPCAKE", "ROCKET": "RAKET",
    "STRAWBERRY": "AARDBEI", "STAR": "STER", "T-REX": "T-REX", "SKELETON": "SKELET", "RANCHER": "BOER",
    "RODEO": "COWBOY", "VACUUM": "STOFZUIGER", "SPACE HERO": "ASTRONAUT", "BEAT BOT": "BEATROBOT",
    "TOY DRUM": "TROMMELTJE", "BONGO": "BONGO", "MONKEY": "AAP", "ELEPHANT": "OLIFANT", "RACE CAR": "RACEAUTO",
    "JELLYFISH": "KWAL", "BEAR": "BEER", "SNOWMAN": "SNEEUWPOP", "CRAB": "KRAB", "WOLF": "WOLF",
    "CAMEL": "KAMEEL", "SCIENTIST": "UITVINDER", "FLYTRAP": "VLIEGENVAL", "SUNFLOWER": "ZONNEBLOEM",
    "SPIDER MOM": "SPINMAMA", "DRAGON DUCK": "DRAKENEEND", "SPIDER GRANDMA": "SPINOMA",
    "NIGHT LIGHT": "NACHTLAMPJE", "GREEN QUEEN": "GROENE KONINGIN", "KING AXOLOTL": "KONING AXOLOTL",
    "FAIRY MONSTER": "FEEMONSTER", "MORNING GLORY": "WINDE", "GROUCH": "MOPPERKONT", "TIGER CUB": "TIJGERTJE",
    "RACCOON": "WASBEER", "GOLDENROD": "GULDENROEDE", "PIANO PAL": "PIANOTJE", "FLUTE BIRD": "FLUITVOGEL",
    "SAX CAT": "SAXKAT", "COW": "KOE", "PIG": "BIGGETJE", "SHEEP": "SCHAAP", "SHARK": "HAAI",
    "SEAHORSE": "ZEEPAARDJE", "STARFISH": "ZEESTER", "SNAIL": "SLAK", "CATERPILLAR": "RUPS",
    "FIREFLY": "VUURVLIEGJE", "TRICERATOPS": "TRICERATOPS", "STEGOSAURUS": "STEGOSAURUS", "PIZZA": "PIZZA",
    "DONUT": "DONUT", "BANANA": "BANAAN", "TRAIN": "TREIN", "FIRE TRUCK": "BRANDWEER", "SCHOOL BUS": "SCHOOLBUS",
    "HELICOPTER": "HELIKOPTER", "GOLD DUCKY": "GOUDEN EENDJE",
    "SPOTTY PUP": "VLEKKENHOND", "FOX": "VOS", "FUZZY": "PLUIZIG", "BIG BLUE": "GROTE BLAUWE", "SPIDER": "SPIN",
    "PUMPKIN": "POMPOEN", "CHICK": "KUIKEN", "BAT": "VLEERMUIS", "HORSE": "PAARD", "CACTUS": "CACTUS",
    "ALIEN": "MARSMANNETJE", "RAINBOW MOM": "BONTE MAMA", "GREEN GRANNY": "GROENE OMA", "PIXIE": "KABOUTER",
    "ALLEY CAT": "STRAATKAT", "LION CUB": "LEEUWTJE", "SQUIRREL": "EEKHOORN",
}

HATS = {"PARTY": "FEEST", "CROWN": "KROON", "TOP HAT": "HOGE HOED", "BUCKET": "VISSERSHOED", "WIZARD": "TOVENAAR",
        "BEANIE": "MUTS", "WESTERN": "COWBOY", "CHEF": "KOK", "PROPELLER": "PROPELLER", "FLOWERS": "BLOEMEN",
        "STAR": "STER"}

# FOLLOW's songs: songs Dutch children sing, each taken note for note from the score in a Wikipedia article (named above
# it; the article's LilyPond rendered to MIDI and its tune read back, tools: see RAINBOW.md), and moved, where
# it says, to fit the keys at OCT 0 (F3 .. G5) with the fewest black keys. A score that repeats itself whole
# is played once. Then a few known everywhere, the same notes as kid.c's English list.
SOLFA_SONGS = []
SONGS = [
    # Frère Jacques (Vader Jacob) (fr.wikipedia.org, its score)
    ("VADER JACOB", "G4 A4 B4 G4 G4 A4 B4 G4 B4 C5 D5 B4 C5 D5 D5 E5 D5 C5 B4 G4 D5 E5 D5 C5 B4 G4 G4 D4 G4 G4 D4 G4"),
    # Lang zal hij leven (other.wikipedia.org, its score, moved +2)
    ("LANG ZAL HIJ", "G4 G4 G4 G4 D4 B4 B4 B4 B4 G4 D5 D5 D5 E5 D5 C5 B4 A4 A4 A4 D5 C5 B4 C5 D5 E5 C5 B4 A4 G4"),
    ("KORTJAKJE", "C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4 G4 G4 F4 F4 E4 E4 D4 G4 G4 F4 F4 E4 E4 D4 C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4"),   # known everywhere (as kid.c's English list)
    # Schlaf, Kindlein, schlaf (Slaap, kindje, slaap) (de.wikipedia.org, its score, moved +2)
    ("SLAAP KINDJE", "B4 A4 A4 G4 G4 B4 D5 D5 C5 C5 B4 B4 C5 C5 A4 A4 D5 D5 B4 B4 C5 C5 A4 A4 D5 D5 B4 C5 A4 A4 G4"),
    # Hopp, hopp, hopp, Pferdchen (Hop, hop, hop, paardje) (de2.wikipedia.org, its score, moved +5)
    ("HOP HOP HOP", "C5 E5 G5 G5 F5 E5 D5 C5 D5 D5 B4 G4 G5 G5 E5 C5 D5 D5 B4 G4 G5 G5 E5 C5 C5 D5 E5 F5 G5 G5 F5 E5 D5 C5"),
    # O Tannenbaum (O denneboom) (de.wikipedia.org, its score, moved -7)
    ("O DENNENBOOM", "G3 C4 C4 C4 D4 E4 E4 E4 E4 D4 E4 F4 B3 D4 C4 G4 G4 E4 A4 G4 G4 F4 F4 F4 F4 D4 G4 F4 F4 E4 E4 G3 C4 C4 C4 D4 E4 E4 E4 E4 D4 E4 F4 B3 D4 C4"),
    ("ODE VREUGDE", "E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4 E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 D4 C4 C4"),   # known everywhere (as kid.c's English list)
    ("JINGLE BELLS", "E4 E4 E4 E4 E4 E4 E4 G4 C4 D4 E4 F4 F4 F4 F4 F4 E4 E4 E4 E4 G4 G4 F4 D4 C4"),   # known everywhere (as kid.c's English list)
    # Stille Nacht, heilige Nacht (de.wikipedia.org, its score, moved -2)
    ("STILLE NACHT", "G4 A4 G4 E4 G4 A4 G4 E4 D5 CS5 D5 B4 C5 B4 C5 G4 A4 A4 C5 B4 A4 G4 A4 G4 E4 A4 A4 C5 B4 A4 G4 A4 G4 E4 B4 B4 B4 D5 C5 B4 C5 E5 C5 G4 E4 G4 F4 D4 C4"),
]

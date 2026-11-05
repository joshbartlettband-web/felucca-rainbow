# Rainbow mode in Danish: what the screen says, the friends' and hats' names, and FOLLOW's songs. Same rules as pt.py.
# The notes are C D E F G A H, as Danish children learn them (SUBS: kid.c's note names with H for B).
DOREMI = False

SUBS = {'"A", "A#", "B"};': '"A", "A#", "H"};'}

PAGE = {   # its page on the site (web/make_lang_page.py)
    'lang': 'da',
    'title': 'Rainbow mode på dansk',
    'lede': 'Et musiklegetøj til små hænder, nu på dansk. Gratis firmware, der gør M-VAVE FM-1-synthen til noget, et lille barn kan spille på.',
    'install': 'Læg det på FM-1',
    'note': 'Ingen FM-1? Man kan spille alligevel, med tangenterne på skærmen eller computerens tastatur. Installationen og browsersiden er stadig på engelsk, men legetøjet taler dansk.',
    'inside': 'Hvad der er i det',
    'facts': ['Alt på skærmen er på dansk, og tonerne hedder C D E F G A H, som i skolen. Hver tangent viser sin tone, stort og i sin egen farve.', '94 venner, hver med sin egen tegning, lyd, himmel og yndlingsrytme, alle med danske navne: ENHJØRNING, SNEMAND, SØHEST.', 'FØLG tænder den næste tangent i 9 sange, som Mester Jakob, Den lille Ole med paraplyen, Jeg ved en lærkerede og Glade jul.', 'For voksne: hold HOME et sekund og så OCT- eller OCT+ for lydstyrken, eller drej KNOB 1 til venstre for at skjule nodelinjerne. HOME og SAVE sammen i 3 sekunder går tilbage til Felucca-synthen.'],
    'songs': 'Sangene',
    'source': 'Tonerne i hver sang kommer fra noderne i Wikipedias artikel om den.',
    'footer': 'Gratis og open source (GPL-3.0), bygget på Felucca af Leo Kuroshita og Hügelton Instruments. Et fanprojekt: M-VAVE har ikke lavet det og står ikke bag det.',
    'try': 'Prøv det i browseren',
}

WORDS = {
    # ALGORITHM
    "1 FRIEND": "1 VEN", "3 FRIENDS": "3 VENNER", "STRUM": "HARPE", "ACCORDION": "HARMONIKA", "GUESS": "GÆT",
    "FOLLOW": "FØLG", "CHORDS": "AKKORDER", "COPY ME": "EFTERLIGN",
    # the cards (ALGORITHM turned): up to 3 lines of 17
    "EVERY KEY PLAYS\\nONE NOTE\\nTRY THE KNOBS TOO": "HVER TANGENT\\nSPILLER EN TONE\\nDREJ PÅ KNAPPERNE",
    "EVERY KEY PLAYS\\nA BIG CHORD\\nFIND MAGIC ONES": "HVER TANGENT\\nSPILLER AKKORD\\nFIND DE MAGISKE",
    "BLACK KEY CHORDS\\nSWEEP THE WHITE\\nKEYS TO STRUM": "SORT VÆLGER\\nAKKORDEN STRYG\\nOVER DE HVIDE",
    "HOLD A BLACK KEY\\nPLAY A TUNE ON\\nTHE WHITE KEYS": "HOLD EN SORT\\nSPIL MELODIEN\\nPÅ DE HVIDE",
    "A FRIEND SINGS\\nFIND THE NOTE\\nPLAY HEARS AGAIN": "EN VEN SYNGER\\nFIND TONEN\\nPLAY IGEN",
    "PLAY THE KEY\\nTHAT LIGHTS UP\\nSEQ PICKS A SONG": "SPIL TANGENTEN\\nDER LYSER\\nSEQ SKIFTER SANG",
    "HOLD ALL THE KEYS\\nTHAT LIGHT UP\\nSEQ PICKS LESSONS": "HOLD TANGENTERNE\\nDER LYSER\\nSEQ NY LEKTIE",
    "LISTEN TO THE\\nFRIEND\\nTHEN PLAY IT BACK": "LYT GODT EFTER\\nOG SPIL DET SAMME",
    # the top row's tricks
    "HICCUP": "HIKKE", "BACKWARDS": "BAGLÆNS", "SLEEPY": "SØVNIG", "SQUEAKY": "PIBET", "GIANT": "KÆMPE",
    "FREEZE": "FRYS",
    # the knobs
    "BIG": "STOR", "SMALL": "LILLE", "DAY": "DAG", "SUNSET": "AFTEN", "NIGHT": "NAT", "ECHO": "EKKO",
    "WIGGLE": "VRIKKE", "SLOW": "LANGSOM", "WALK": "GÅTUR", "FAST": "HURTIG", "MEDIUM": "MELLEM",
    # the beats
    "DANCE": "DANS", "MARCH": "MARCH", "SPOOKY": "UHYGGE", "TRAIN": "TOG", "LULLABY": "VUGGEVISE",
    "HOEDOWN": "COUNTRY", "POLKA": "POLKA", "NO BEAT": "INGEN TAKT",
    # games, secrets, the grown-ups' settings
    "YES!": "JA!", "TRY AGAIN": "PRØV IGEN", "LISTEN": "LYT", "YOUR TURN": "DIN TUR", "YAY!": "HURRA!",
    "STAR!": "STJERNE!", "NEW HAT!": "NY HAT!", "NEW FRIEND!": "NY VEN!", "NEW SKY!": "NY HIMMEL!",
    "NEW SONG": "NY SANG", "NO HAT": "INGEN HAT", "STARS": "STJERNER", "LOOK-ALIKES OFF": "KOPIER FRA",
    "STAFF ON": "NODER TIL", "STAFF OFF": "NODER FRA",
    "LOOK-ALIKES ON": "KOPIER TIL", "HI!": "HEJ!", "HI": "HEJ", "YOUR NAME": "DIT NAVN",
    "PRESETS  LETTER": "PRESETS  BOGSTAV", "ALGORITHM  NEXT": "ALGORITHM  NÆSTE", "SAVE  KEEP IT": "SAVE  GEM",
    "HOME  LEAVE IT": "HOME  TILBAGE", "SPARKLE": "GLIMMER", "SPARKLE TUNE": "GLIMMER MELODI", "SPARKLE ALL": "GLIMMER ALT",
    "WRITE": "KOMPONER",
    # chords and lessons
    "MAJOR": "DUR", "MINOR": "MOL", "SEVEN": "SEPTIM", "NINE": "NONE",
    "C_MAJOR=": "C_DUR=", "F_MAJOR=": "F_DUR=", "G_MAJOR=": "G_DUR=", "A_MINOR=": "A_MOL=", "G_SEVEN=": "G_SEPTIM=",
    "FIRST CHORDS": "DE FØRSTE", "POP FOUR": "FIRE POP", "SEVENTHS": "SEPTIMER",
    # the drums' names
    "KICK": "STORTROMME", "SNARE": "LILLETROMME", "CLAP": "KLAP", "HI-HAT": "HI-HAT", "OPEN HAT": "ÅBEN HI-HAT",
    "RIM": "KANT", "COWBELL": "KOKLOKKE", "CYMBAL": "BÆKKEN",
}

NAMES = {   # the friends (and the look-alikes' stand-ins): one line of 13, or two words of 13 and 15 in all
    "DUCKY": "ÆLLING", "PINK DUCKY": "LYSERØD ÆLLING", "COOL DUCKY": "SEJ ÆLLING", "AXOLOTL": "AKSOLOTL",
    "UNICORN": "ENHJØRNING", "GIRAFFE": "GIRAF", "GOO": "SLIM", "GOOBERT": "GOOBERT", "BLUE PUP": "BLÅ HVALP",
    "RED MONSTER": "RØDT MONSTER", "BLUE MONSTER": "BLÅT MONSTER", "APRIL": "APRIL", "SCISSORS": "SAKS",
    "GHOST": "SPØGELSE", "WEB HERO": "NETHELT", "BUTTERFLY": "SOMMERFUGL", "KITTY": "MIS", "FROG": "FRØ",
    "ROBOT": "ROBOT", "RAINBOW": "REGNBUE", "PRINCESS DUCKY": "PRINSESSEAND", "RED PUP": "RØD HVALP",
    "YELLOW BIRD": "GUL FUGL", "SLIMY": "SLIMET", "BUNNY": "KANIN", "PANDA": "PANDA", "PENGUIN": "PINGVIN",
    "OWL": "UGLE", "BEE": "BI", "LADYBUG": "MARIEHØNE", "DINO": "DINO", "WHALE": "HVAL", "OCTOPUS": "BLÆKSPRUTTE",
    "FISH": "FISK", "TURTLE": "SKILDPADDE", "ICE CREAM": "IS", "CUPCAKE": "MUFFIN", "ROCKET": "RAKET",
    "STRAWBERRY": "JORDBÆR", "STAR": "STJERNE", "T-REX": "T-REX", "SKELETON": "SKELET", "RANCHER": "BONDE",
    "RODEO": "COWBOY", "VACUUM": "STØVSUGER", "SPACE HERO": "ASTRONAUT", "BEAT BOT": "TAKTROBOT",
    "TOY DRUM": "LEGETROMME", "BONGO": "BONGO", "MONKEY": "ABE", "ELEPHANT": "ELEFANT", "RACE CAR": "RACERBIL",
    "JELLYFISH": "VANDMAND", "BEAR": "BJØRN", "SNOWMAN": "SNEMAND", "CRAB": "KRABBE", "WOLF": "ULV",
    "CAMEL": "KAMEL", "SCIENTIST": "FORSKER", "FLYTRAP": "FLUEFANGER", "SUNFLOWER": "SOLSIKKE",
    "SPIDER MOM": "EDDERKOPMOR", "DRAGON DUCK": "DRAGEAND", "SPIDER GRANDMA": "EDDERKOPOMA",
    "NIGHT LIGHT": "NATLAMPE", "GREEN QUEEN": "GRØN DRONNING", "KING AXOLOTL": "KONG AKSOLOTL",
    "FAIRY MONSTER": "ALFEMONSTER", "MORNING GLORY": "SNERLE", "GROUCH": "SURMULE", "TIGER CUB": "TIGERUNGE",
    "RACCOON": "VASKEBJØRN", "GOLDENROD": "GYLDENRIS", "PIANO PAL": "KLAVER", "FLUTE BIRD": "FLØJTEFUGL",
    "SAX CAT": "SAXKAT", "COW": "KO", "PIG": "GRIS", "SHEEP": "FÅR", "SHARK": "HAJ",
    "SEAHORSE": "SØHEST", "STARFISH": "SØSTJERNE", "SNAIL": "SNEGL", "CATERPILLAR": "LARVE",
    "FIREFLY": "ILDFLUE", "TRICERATOPS": "TRICERATOPS", "STEGOSAURUS": "STEGOSAURUS", "PIZZA": "PIZZA",
    "DONUT": "DONUT", "BANANA": "BANAN", "TRAIN": "TOG", "FIRE TRUCK": "BRANDBIL", "SCHOOL BUS": "SKOLEBUS",
    "HELICOPTER": "HELIKOPTER", "GOLD DUCKY": "GULDÆLLING",
    "SPOTTY PUP": "PLETTET HVALP", "FOX": "RÆV", "FUZZY": "LODNE", "BIG BLUE": "STORE BLÅ", "SPIDER": "EDDERKOP",
    "PUMPKIN": "GRÆSKAR", "CHICK": "KYLLING", "BAT": "FLAGERMUS", "HORSE": "HEST", "CACTUS": "KAKTUS",
    "ALIEN": "RUMVÆSEN", "RAINBOW MOM": "REGNBUEMOR", "GREEN GRANNY": "GRØN MORMOR", "PIXIE": "NISSE",
    "ALLEY CAT": "GADEKAT", "LION CUB": "LØVEUNGE", "SQUIRREL": "EGERN",
}

HATS = {"PARTY": "FEST", "CROWN": "KRONE", "TOP HAT": "HØJ HAT", "BUCKET": "FISKERHAT", "WIZARD": "TROLDMAND",
        "BEANIE": "HUE", "WESTERN": "COWBOY", "CHEF": "KOK", "PROPELLER": "PROPEL", "FLOWERS": "BLOMSTER",
        "STAR": "STJERNE"}

# FOLLOW's songs: songs Danish children sing, each taken note for note from the score in a Wikipedia article (named above
# it; the article's LilyPond rendered to MIDI and its tune read back, tools: see RAINBOW.md), and moved, where
# it says, to fit the keys at OCT 0 (F3 .. G5) with the fewest black keys. A score that repeats itself whole
# is played once. Then a few known everywhere, the same notes as kid.c's English list.
SOLFA_SONGS = []
SONGS = [
    # Frère Jacques (Mester Jakob) (fr.wikipedia.org, its score)
    ("MESTER JAKOB", "G4 A4 B4 G4 G4 A4 B4 G4 B4 C5 D5 B4 C5 D5 D5 E5 D5 C5 B4 G4 D5 E5 D5 C5 B4 G4 G4 D4 G4 G4 D4 G4"),
    # Den lille Ole med paraplyen (Ole Jacobsen) (da.wikipedia.org, its score, moved -5)
    ("LILLE OLE", "G3 C4 E4 A4 G4 C4 B3 C4 E4 D4 A3 D4 F4 B4 A4 D4 CS4 D4 DS4 E4 G4 A4 B4 D5 C5 E4 F4 G4 A4 A4 B4 A4 A4 G4 G3 A3 B3 C4"),
    # Jeg ved en lærkerede (Carl Nielsen) (da.wikipedia.org, its score)
    ("LÆRKEREDE", "G4 B4 G4 C5 A4 D5 B4 E5 C5 C5 B4 B4 A4 D5 B4 B4 A4 A4 G4 E4 C5 B4 B4 A4 A4 G4"),
    # Solen er så rød, mor (Carl Nielsen) (other.wikipedia.org, its score, moved -5)
    ("SOLEN ER RØD", "E4 E4 E4 D4 C4 C4 D4 E4 D4 E4 F4 G4 C4 A4 A4 A4 G4 E4 D4 E4 C4 B3 A3 C4 B3 D4 D4 D4 E4 F4 E4 D4 E4 F4 E4 F4 G4 A4 A4 F4 E4 D4 C4 B3 C4 D4 G3 C4 A3 D4 B3 C4"),
    ("BLINK STJERNE", "C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4 G4 G4 F4 F4 E4 E4 D4 G4 G4 F4 F4 E4 E4 D4 C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4"),   # known everywhere (as kid.c's English list)
    ("ODE TIL GLÆDEN", "E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4 E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 D4 C4 C4"),   # known everywhere (as kid.c's English list)
    ("BJÆLDEKLANG", "E4 E4 E4 E4 E4 E4 E4 G4 C4 D4 E4 F4 F4 F4 F4 F4 E4 E4 E4 E4 G4 G4 F4 D4 C4"),   # known everywhere (as kid.c's English list)
    # O Tannenbaum (de.wikipedia.org, its score, moved -7)
    ("O JULETRÆ", "G3 C4 C4 C4 D4 E4 E4 E4 E4 D4 E4 F4 B3 D4 C4 G4 G4 E4 A4 G4 G4 F4 F4 F4 F4 D4 G4 F4 F4 E4 E4 G3 C4 C4 C4 D4 E4 E4 E4 E4 D4 E4 F4 B3 D4 C4"),
    # Stille Nacht, heilige Nacht (de.wikipedia.org, its score, moved -2)
    ("GLADE JUL", "G4 A4 G4 E4 G4 A4 G4 E4 D5 CS5 D5 B4 C5 B4 C5 G4 A4 A4 C5 B4 A4 G4 A4 G4 E4 A4 A4 C5 B4 A4 G4 A4 G4 E4 B4 B4 B4 D5 C5 B4 C5 E5 C5 G4 E4 G4 F4 D4 C4"),
]

# Rainbow mode in Norwegian (Bokmål): what the screen says, the friends' and hats' names, and FOLLOW's songs. Same
# rules as pt.py. The notes are C D E F G A H, as Norwegian children learn them (SUBS: kid.c's note names, H for B).
DOREMI = False

SUBS = {'"A", "A#", "B"};': '"A", "A#", "H"};'}

PAGE = {   # its page on the site (web/make_lang_page.py)
    'lang': 'nb',
    'title': 'Rainbow mode på norsk',
    'lede': 'En musikkleke for små hender, nå på norsk. Gratis fastvare som gjør M-VAVE FM-1-synthen til noe et lite barn kan spille på.',
    'install': 'Legg den på FM-1',
    'note': 'Ingen FM-1? Du kan spille likevel, med tangentene på skjermen eller tastaturet på datamaskinen. Installasjonen og nettleserversjonen er fortsatt på engelsk, men leken snakker norsk.',
    'inside': 'Hva som er inni',
    'facts': ['Alt på skjermen er på norsk, og tonene heter C D E F G A H, som på skolen. Hver tangent viser tonen sin, stort og i sin egen farge.', '94 venner, hver med egen tegning, egen lyd, egen himmel og favorittrytme, alle med norske navn: ENHJØRNING, SNØMANN, SJØHEST.', 'FØLG lyser opp neste tangent i 7 sanger, som Fader Jakob, Hurra for deg som fyller ditt år og Glade jul.', 'For voksne: hold HOME et sekund, og så OCT- eller OCT+ for volumet, eller vri KNOB 1 mot venstre for å skjule notelinjene. HOME og SAVE sammen i 3 sekunder går tilbake til Felucca-synthen.'],
    'songs': 'Sangene',
    'source': 'Tonene i hver sang kommer fra notene i Wikipedia-artikkelen om den.',
    'footer': 'Gratis og åpen kildekode (GPL-3.0), bygget på Felucca av Leo Kuroshita og Hügelton Instruments. Et fanprosjekt: M-VAVE har ikke laget den og står ikke bak den.',
    'try': 'Prøv i nettleseren',
}

WORDS = {
    # ALGORITHM
    "1 FRIEND": "1 VENN", "3 FRIENDS": "3 VENNER", "STRUM": "HARPE", "ACCORDION": "TREKKSPILL", "GUESS": "GJETT",
    "FOLLOW": "FØLG", "CHORDS": "AKKORDER", "COPY ME": "HERM ETTER",
    # the cards (ALGORITHM turned): up to 3 lines of 17
    "EVERY KEY PLAYS\\nONE NOTE\\nTRY THE KNOBS TOO": "HVER TANGENT\\nSPILLER EN TONE\\nVRI PÅ KNAPPENE",
    "EVERY KEY PLAYS\\nA BIG CHORD\\nFIND MAGIC ONES": "HVER TANGENT\\nSPILLER AKKORD\\nFINN DE MAGISKE",
    "BLACK KEY CHORDS\\nSWEEP THE WHITE\\nKEYS TO STRUM": "SVART VELGER\\nAKKORDEN DRA\\nOVER DE HVITE",
    "HOLD A BLACK KEY\\nPLAY A TUNE ON\\nTHE WHITE KEYS": "HOLD EN SVART\\nSPILL MELODIEN\\nPÅ DE HVITE",
    "A FRIEND SINGS\\nFIND THE NOTE\\nPLAY HEARS AGAIN": "EN VENN SYNGER\\nFINN TONEN\\nPLAY IGJEN",
    "PLAY THE KEY\\nTHAT LIGHTS UP\\nSEQ PICKS A SONG": "SPILL TANGENTEN\\nSOM LYSER\\nSEQ BYTTER SANG",
    "HOLD ALL THE KEYS\\nTHAT LIGHT UP\\nSEQ PICKS LESSONS": "HOLD TANGENTENE\\nSOM LYSER\\nSEQ BYTTER LEKSE",
    "LISTEN TO THE\\nFRIEND\\nTHEN PLAY IT BACK": "LYTT GODT\\nOG SPILL LIKT",
    # the top row's tricks
    "HICCUP": "HIKKE", "BACKWARDS": "BAKLENGS", "SLEEPY": "SØVNIG", "SQUEAKY": "PIPETE", "GIANT": "KJEMPE",
    "FREEZE": "FRYS",
    # the knobs
    "BIG": "STOR", "SMALL": "LITEN", "DAY": "DAG", "SUNSET": "KVELD", "NIGHT": "NATT", "ECHO": "EKKO",
    "WIGGLE": "VRIKKE", "SLOW": "SAKTE", "WALK": "GÅTUR", "FAST": "FORT", "MEDIUM": "MIDDELS",
    # the beats
    "DANCE": "DANS", "MARCH": "MARSJ", "SPOOKY": "SKUMMEL", "TRAIN": "TOG", "LULLABY": "VUGGESANG",
    "HOEDOWN": "COUNTRY", "POLKA": "POLKA", "NO BEAT": "INGEN TAKT",
    # games, secrets, the grown-ups' settings
    "YES!": "JA!", "TRY AGAIN": "PRØV IGJEN", "LISTEN": "LYTT", "YOUR TURN": "DIN TUR", "YAY!": "HURRA!",
    "STAR!": "STJERNE!", "NEW HAT!": "NY HATT!", "NEW FRIEND!": "NY VENN!", "NEW SKY!": "NY HIMMEL!",
    "NEW SONG": "NY SANG", "NO HAT": "INGEN HATT", "STARS": "STJERNER", "LOOK-ALIKES OFF": "KOPIER AV",
    "STAFF ON": "NOTER PÅ", "STAFF OFF": "NOTER AV",
    "LOOK-ALIKES ON": "KOPIER PÅ", "HI!": "HEI!", "HI": "HEI", "YOUR NAME": "DITT NAVN",
    "PRESETS  LETTER": "PRESETS  BOKSTAV", "ALGORITHM  NEXT": "ALGORITHM  NESTE", "SAVE  KEEP IT": "SAVE  LAGRE",
    "HOME  LEAVE IT": "HOME  TILBAKE", "SPARKLE": "GLITTER", "SPARKLE TUNE": "GLITTER MELODI", "SPARKLE ALL": "GLITTER ALT",
    "WRITE": "KOMPONER",
    # chords and lessons
    "MAJOR": "DUR", "MINOR": "MOLL", "SEVEN": "SEPTIM", "NINE": "NONE",
    "C_MAJOR=": "C_DUR=", "F_MAJOR=": "F_DUR=", "G_MAJOR=": "G_DUR=", "A_MINOR=": "A_MOLL=", "G_SEVEN=": "G_SEPTIM=",
    "FIRST CHORDS": "DE FØRSTE", "POP FOUR": "FIRE POP", "SEVENTHS": "SEPTIMER",
    # the drums' names
    "KICK": "STORTROMME", "SNARE": "SKARPTROMME", "CLAP": "KLAPP", "HI-HAT": "HI-HAT", "OPEN HAT": "ÅPEN HI-HAT",
    "RIM": "KANT", "COWBELL": "KUBJELLE", "CYMBAL": "CYMBAL",
}

NAMES = {   # the friends (and the look-alikes' stand-ins): one line of 13, or two words of 13 and 15 in all
    "DUCKY": "ANDUNGE", "PINK DUCKY": "ROSA ANDUNGE", "COOL DUCKY": "KUL ANDUNGE", "AXOLOTL": "AKSOLOTL",
    "UNICORN": "ENHJØRNING", "GIRAFFE": "SJIRAFF", "GOO": "GUFFE", "GOOBERT": "GOOBERT", "BLUE PUP": "BLÅ VALP",
    "RED MONSTER": "RØDT MONSTER", "BLUE MONSTER": "BLÅTT MONSTER", "APRIL": "APRIL", "SCISSORS": "SAKS",
    "GHOST": "SPØKELSE", "WEB HERO": "NETTHELT", "BUTTERFLY": "SOMMERFUGL", "KITTY": "PUSEKATT", "FROG": "FROSK",
    "ROBOT": "ROBOT", "RAINBOW": "REGNBUE", "PRINCESS DUCKY": "PRINSESSEAND", "RED PUP": "RØD VALP",
    "YELLOW BIRD": "GUL FUGL", "SLIMY": "SLIMETE", "BUNNY": "KANIN", "PANDA": "PANDA", "PENGUIN": "PINGVIN",
    "OWL": "UGLE", "BEE": "BIE", "LADYBUG": "MARIHØNE", "DINO": "DINO", "WHALE": "HVAL", "OCTOPUS": "BLEKKSPRUT",
    "FISH": "FISK", "TURTLE": "SKILPADDE", "ICE CREAM": "IS", "CUPCAKE": "MUFFINS", "ROCKET": "RAKETT",
    "STRAWBERRY": "JORDBÆR", "STAR": "STJERNE", "T-REX": "T-REX", "SKELETON": "SKJELETT", "RANCHER": "BONDE",
    "RODEO": "COWBOY", "VACUUM": "STØVSUGER", "SPACE HERO": "ASTRONAUT", "BEAT BOT": "TAKTROBOT",
    "TOY DRUM": "LEKETROMME", "BONGO": "BONGO", "MONKEY": "APE", "ELEPHANT": "ELEFANT", "RACE CAR": "RACERBIL",
    "JELLYFISH": "MANET", "BEAR": "BJØRN", "SNOWMAN": "SNØMANN", "CRAB": "KRABBE", "WOLF": "ULV",
    "CAMEL": "KAMEL", "SCIENTIST": "FORSKER", "FLYTRAP": "FLUEFANGER", "SUNFLOWER": "SOLSIKKE",
    "SPIDER MOM": "EDDERKOPPMOR", "DRAGON DUCK": "DRAGEAND", "SPIDER GRANDMA": "EDDERKOPPOMA",
    "NIGHT LIGHT": "NATTLAMPE", "GREEN QUEEN": "GRØNN DRONNING", "KING AXOLOTL": "KONG AKSOLOTL",
    "FAIRY MONSTER": "FEMONSTER", "MORNING GLORY": "VINDEL", "GROUCH": "GRINEBITER", "TIGER CUB": "TIGERUNGE",
    "RACCOON": "VASKEBJØRN", "GOLDENROD": "GULLRIS", "PIANO PAL": "PIANO", "FLUTE BIRD": "FLØYTEFUGL",
    "SAX CAT": "SAKSOKATT", "COW": "KU", "PIG": "GRIS", "SHEEP": "SAU", "SHARK": "HAI",
    "SEAHORSE": "SJØHEST", "STARFISH": "SJØSTJERNE", "SNAIL": "SNEGLE", "CATERPILLAR": "LARVE",
    "FIREFLY": "ILDFLUE", "TRICERATOPS": "TRICERATOPS", "STEGOSAURUS": "STEGOSAURUS", "PIZZA": "PIZZA",
    "DONUT": "SMULTRING", "BANANA": "BANAN", "TRAIN": "TOG", "FIRE TRUCK": "BRANNBIL", "SCHOOL BUS": "SKOLEBUSS",
    "HELICOPTER": "HELIKOPTER", "GOLD DUCKY": "GULLANDUNGE",
    "SPOTTY PUP": "PRIKKETE VALP", "FOX": "REV", "FUZZY": "LODDEN", "BIG BLUE": "STORE BLÅ", "SPIDER": "EDDERKOPP",
    "PUMPKIN": "GRESSKAR", "CHICK": "KYLLING", "BAT": "FLAGGERMUS", "HORSE": "HEST", "CACTUS": "KAKTUS",
    "ALIEN": "ROMVESEN", "RAINBOW MOM": "REGNBUEMAMMA", "GREEN GRANNY": "GRØNN MORMOR", "PIXIE": "NISSE",
    "ALLEY CAT": "GATEKATT", "LION CUB": "LØVEUNGE", "SQUIRREL": "EKORN",
}

HATS = {"PARTY": "FEST", "CROWN": "KRONE", "TOP HAT": "FLOSSHATT", "BUCKET": "FISKEHATT", "WIZARD": "TROLLMANN",
        "BEANIE": "LUE", "WESTERN": "COWBOY", "CHEF": "KOKK", "PROPELLER": "PROPELL", "FLOWERS": "BLOMSTER",
        "STAR": "STJERNE"}

# FOLLOW's songs: songs Norwegian children sing, each taken note for note from the score in a Wikipedia article (named above
# it; the article's LilyPond rendered to MIDI and its tune read back, tools: see RAINBOW.md), and moved, where
# it says, to fit the keys at OCT 0 (F3 .. G5) with the fewest black keys. A score that repeats itself whole
# is played once. Then a few known everywhere, the same notes as kid.c's English list.
SOLFA_SONGS = []
SONGS = [
    # Fader Jakob (other.wikipedia.org, its score, moved -2)
    ("FADER JAKOB", "C4 D4 E4 C4 C4 D4 E4 C4 E4 F4 G4 E4 F4 G4 G4 A4 G4 F4 E4 C4 G4 A4 G4 F4 E4 C4 C4 G3 C4 C4 G3 C4"),
    # Hurra for deg som fyller ditt år (other.wikipedia.org, its score, moved -5)
    ("HURRA FOR DEG", "C4 E4 G4 E4 C4 B3 D4 B3 G3 G3 C4 E4 G4 E4 C4 B3 C4 C4 E4 G4 E4 C4 B3 D4 B3 G3 G3 C4 E4 G4 E4 C4 B3 C4 F4 F4 F4 F4 F4 F4 E4 E4 E4 E4 D4 D4 D4 D4 D4 C4 D4 E4 F4 G4 F4 A4 A4 A4 A4 F4 E4 G4 G4 G4 G4 E4 D4 D4 D4 E4 F4 B3 D4 C4 E4 B3 D4 C4"),
    ("BLINKE BLINKE", "C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4 G4 G4 F4 F4 E4 E4 D4 G4 G4 F4 F4 E4 E4 D4 C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4"),   # known everywhere (as kid.c's English list)
    ("ODE TIL GLEDEN", "E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4 E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 D4 C4 C4"),   # known everywhere (as kid.c's English list)
    ("BJELLEKLANG", "E4 E4 E4 E4 E4 E4 E4 G4 C4 D4 E4 F4 F4 F4 F4 F4 E4 E4 E4 E4 G4 G4 F4 D4 C4"),   # known everywhere (as kid.c's English list)
    # O Tannenbaum (de.wikipedia.org, its score, moved -7)
    ("O JULETRE", "G3 C4 C4 C4 D4 E4 E4 E4 E4 D4 E4 F4 B3 D4 C4 G4 G4 E4 A4 G4 G4 F4 F4 F4 F4 D4 G4 F4 F4 E4 E4 G3 C4 C4 C4 D4 E4 E4 E4 E4 D4 E4 F4 B3 D4 C4"),
    # Stille Nacht, heilige Nacht (de.wikipedia.org, its score, moved -2)
    ("GLADE JUL", "G4 A4 G4 E4 G4 A4 G4 E4 D5 CS5 D5 B4 C5 B4 C5 G4 A4 A4 C5 B4 A4 G4 A4 G4 E4 A4 A4 C5 B4 A4 G4 A4 G4 E4 B4 B4 B4 D5 C5 B4 C5 E5 C5 G4 E4 G4 F4 D4 C4"),
]

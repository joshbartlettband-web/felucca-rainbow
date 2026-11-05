# Rainbow mode in Swedish: what the screen says, the friends' and hats' names, and FOLLOW's songs. Same rules as pt.py.
# The notes are C D E F G A H, as Swedish children learn them (SUBS: kid.c's note names with H for B).
DOREMI = False

SUBS = {'"A", "A#", "B"};': '"A", "A#", "H"};'}

PAGE = {   # its page on the site (web/make_lang_page.py)
    'lang': 'sv',
    'title': 'Rainbow mode på svenska',
    'lede': 'En musikleksak för små händer, nu på svenska. Gratis firmware som gör M-VAVE FM-1-synten till något som ett litet barn kan spela på.',
    'install': 'Lägg den på FM-1',
    'note': 'Ingen FM-1? Det går att spela ändå, med tangenterna på skärmen eller datorns tangentbord. Installationen och webbläsarsidan är fortfarande på engelska, men leksaken pratar svenska.',
    'inside': 'Vad som finns i den',
    'facts': ['Allt på skärmen är på svenska, och tonerna heter C D E F G A H, som i skolan. Varje tangent visar sin ton, stort och i sin egen färg.', '94 kompisar, var och en med egen bild, eget ljud, egen himmel och favorittakt, alla med svenska namn: ENHÖRNING, SNÖGUBBE, SJÖHÄST.', 'FÖLJ tänder nästa tangent i 7 sånger, som Broder Jakob, Blinka lilla stjärna och Stilla natt.', 'För vuxna: håll HOME en sekund och sedan OCT- eller OCT+ för volymen, eller vrid KNOB 1 åt vänster för att gömma notraderna. HOME och SAVE tillsammans i 3 sekunder går tillbaka till Felucca-synten.'],
    'songs': 'Sångerna',
    'source': 'Tonerna i varje sång kommer från noterna i Wikipedias artikel om den.',
    'footer': 'Gratis och öppen källkod (GPL-3.0), byggd på Felucca av Leo Kuroshita och Hügelton Instruments. Ett fanprojekt: M-VAVE har inte gjort den och står inte bakom den.',
    'try': 'Prova i webbläsaren',
}

WORDS = {
    # ALGORITHM
    "1 FRIEND": "1 KOMPIS", "3 FRIENDS": "3 KOMPISAR", "STRUM": "HARPA", "ACCORDION": "DRAGSPEL", "GUESS": "GISSA",
    "FOLLOW": "FÖLJ", "CHORDS": "ACKORD", "COPY ME": "HÄRMA",
    # the cards (ALGORITHM turned): up to 3 lines of 17
    "EVERY KEY PLAYS\\nONE NOTE\\nTRY THE KNOBS TOO": "VARJE TANGENT\\nSPELAR EN TON\\nVRID PÅ RATTARNA",
    "EVERY KEY PLAYS\\nA BIG CHORD\\nFIND MAGIC ONES": "VARJE TANGENT\\nSPELAR ETT ACKORD\\nHITTA MAGISKA",
    "BLACK KEY CHORDS\\nSWEEP THE WHITE\\nKEYS TO STRUM": "SVART VÄLJER\\nACKORDET DRA\\nÖVER DE VITA",
    "HOLD A BLACK KEY\\nPLAY A TUNE ON\\nTHE WHITE KEYS": "HÅLL EN SVART\\nSPELA MELODIN\\nPÅ DE VITA",
    "A FRIEND SINGS\\nFIND THE NOTE\\nPLAY HEARS AGAIN": "EN KOMPIS SJUNGER\\nHITTA TONEN\\nPLAY IGEN",
    "PLAY THE KEY\\nTHAT LIGHTS UP\\nSEQ PICKS A SONG": "SPELA TANGENTEN\\nSOM LYSER\\nSEQ BYTER SÅNG",
    "HOLD ALL THE KEYS\\nTHAT LIGHT UP\\nSEQ PICKS LESSONS": "HÅLL TANGENTERNA\\nSOM LYSER\\nSEQ BYTER LEKTION",
    "LISTEN TO THE\\nFRIEND\\nTHEN PLAY IT BACK": "LYSSNA NOGA\\nOCH SPELA SAMMA",
    # the top row's tricks
    "HICCUP": "HICKA", "BACKWARDS": "BAKLÄNGES", "SLEEPY": "SÖMNIG", "SQUEAKY": "PIPIG", "GIANT": "JÄTTE",
    "FREEZE": "FRYS",
    # the knobs
    "BIG": "STOR", "SMALL": "LITEN", "DAY": "DAG", "SUNSET": "KVÄLL", "NIGHT": "NATT", "ECHO": "EKO",
    "WIGGLE": "VICKA", "SLOW": "LÅNGSAM", "WALK": "PROMENAD", "FAST": "SNABB", "MEDIUM": "MELLAN",
    # the beats
    "DANCE": "DANS", "MARCH": "MARSCH", "SPOOKY": "SPÖKE", "TRAIN": "TÅG", "LULLABY": "VAGGVISA",
    "HOEDOWN": "COUNTRY", "POLKA": "POLKA", "NO BEAT": "INGEN TAKT",
    # games, secrets, the grown-ups' settings
    "YES!": "JA!", "TRY AGAIN": "FÖRSÖK IGEN", "LISTEN": "LYSSNA", "YOUR TURN": "DIN TUR", "YAY!": "HURRA!",
    "STAR!": "STJÄRNA!", "NEW HAT!": "NY HATT!", "NEW FRIEND!": "NY KOMPIS!", "NEW SKY!": "NY HIMMEL!",
    "NEW SONG": "NY SÅNG", "NO HAT": "INGEN HATT", "STARS": "STJÄRNOR", "LOOK-ALIKES OFF": "KOPIOR AV",
    "STAFF ON": "NOTER PÅ", "STAFF OFF": "NOTER AV",
    "LOOK-ALIKES ON": "KOPIOR PÅ", "HI!": "HEJ!", "HI": "HEJ", "YOUR NAME": "DITT NAMN",
    "PRESETS  LETTER": "PRESETS  BOKSTAV", "ALGORITHM  NEXT": "ALGORITHM  NÄSTA", "SAVE  KEEP IT": "SAVE  SPARA",
    "HOME  LEAVE IT": "HOME  TILLBAKA", "SPARKLE": "GLITTER", "SPARKLE TUNE": "GLITTER MELODI", "SPARKLE ALL": "GLITTER ALLT",
    "WRITE": "KOMPONERA",
    # chords and lessons
    "MAJOR": "DUR", "MINOR": "MOLL", "SEVEN": "SEPTIMA", "NINE": "NONA",
    "C_MAJOR=": "C_DUR=", "F_MAJOR=": "F_DUR=", "G_MAJOR=": "G_DUR=", "A_MINOR=": "A_MOLL=", "G_SEVEN=": "G_SEPTIMA=",
    "FIRST CHORDS": "DE FÖRSTA", "POP FOUR": "FYRA POP", "SEVENTHS": "SEPTIMOR",
    # the drums' names
    "KICK": "BASTRUMMA", "SNARE": "VIRVEL", "CLAP": "KLAPP", "HI-HAT": "HI-HAT", "OPEN HAT": "ÖPPEN HI-HAT", "RIM": "KANT",
    "COWBELL": "KOSKÄLLA", "CYMBAL": "CYMBAL",
}

NAMES = {   # the friends (and the look-alikes' stand-ins): one line of 13, or two words of 13 and 15 in all
    "DUCKY": "ANKAN", "PINK DUCKY": "ROSA ANKAN", "COOL DUCKY": "COOLA ANKAN", "AXOLOTL": "AXOLOTL",
    "UNICORN": "ENHÖRNING", "GIRAFFE": "GIRAFF", "GOO": "KLADD", "GOOBERT": "GOOBERT", "BLUE PUP": "BLÅ VALP",
    "RED MONSTER": "RÖTT MONSTER", "BLUE MONSTER": "BLÅTT MONSTER", "APRIL": "APRIL", "SCISSORS": "SAX",
    "GHOST": "SPÖKE", "WEB HERO": "NÄTHJÄLTE", "BUTTERFLY": "FJÄRIL", "KITTY": "KISSE", "FROG": "GRODA",
    "ROBOT": "ROBOT", "RAINBOW": "REGNBÅGE", "PRINCESS DUCKY": "PRINSESSANKA", "RED PUP": "RÖD VALP",
    "YELLOW BIRD": "GUL FÅGEL", "SLIMY": "SLEMMIG", "BUNNY": "KANIN", "PANDA": "PANDA", "PENGUIN": "PINGVIN",
    "OWL": "UGGLA", "BEE": "BI", "LADYBUG": "NYCKELPIGA", "DINO": "DINO", "WHALE": "VAL", "OCTOPUS": "BLÄCKFISK",
    "FISH": "FISK", "TURTLE": "SKÖLDPADDA", "ICE CREAM": "GLASS", "CUPCAKE": "MUFFINS", "ROCKET": "RAKET",
    "STRAWBERRY": "JORDGUBBE", "STAR": "STJÄRNA", "T-REX": "T-REX", "SKELETON": "SKELETT", "RANCHER": "BONDE",
    "RODEO": "COWBOY", "VACUUM": "DAMMSUGARE", "SPACE HERO": "ASTRONAUT", "BEAT BOT": "TAKTROBOT",
    "TOY DRUM": "LEKSAKSTRUMMA", "BONGO": "BONGO", "MONKEY": "APA", "ELEPHANT": "ELEFANT", "RACE CAR": "RACERBIL",
    "JELLYFISH": "MANET", "BEAR": "BJÖRN", "SNOWMAN": "SNÖGUBBE", "CRAB": "KRABBA", "WOLF": "VARG",
    "CAMEL": "KAMEL", "SCIENTIST": "FORSKARE", "FLYTRAP": "FLUGFÄLLA", "SUNFLOWER": "SOLROS",
    "SPIDER MOM": "SPINDELMAMMA", "DRAGON DUCK": "DRAKANKA", "SPIDER GRANDMA": "SPINDELMORMOR",
    "NIGHT LIGHT": "NATTLAMPA", "GREEN QUEEN": "GRÖN DROTTNING", "KING AXOLOTL": "KUNG AXOLOTL",
    "FAIRY MONSTER": "ÄLVMONSTER", "MORNING GLORY": "VINDA", "GROUCH": "SURPUTTE", "TIGER CUB": "TIGERUNGE",
    "RACCOON": "TVÄTTBJÖRN", "GOLDENROD": "GULLRIS", "PIANO PAL": "PIANO", "FLUTE BIRD": "FLÖJTFÅGEL",
    "SAX CAT": "SAXKATT", "COW": "KO", "PIG": "GRIS", "SHEEP": "FÅR", "SHARK": "HAJ",
    "SEAHORSE": "SJÖHÄST", "STARFISH": "SJÖSTJÄRNA", "SNAIL": "SNIGEL", "CATERPILLAR": "LARV",
    "FIREFLY": "LYSMASK", "TRICERATOPS": "TRICERATOPS", "STEGOSAURUS": "STEGOSAURUS", "PIZZA": "PIZZA",
    "DONUT": "MUNK", "BANANA": "BANAN", "TRAIN": "TÅG", "FIRE TRUCK": "BRANDBIL", "SCHOOL BUS": "SKOLBUSS",
    "HELICOPTER": "HELIKOPTER", "GOLD DUCKY": "GULDANKAN",
    "SPOTTY PUP": "PRICKIG VALP", "FOX": "RÄV", "FUZZY": "LUDDIS", "BIG BLUE": "STORA BLÅ", "SPIDER": "SPINDEL",
    "PUMPKIN": "PUMPA", "CHICK": "KYCKLING", "BAT": "FLADDERMUS", "HORSE": "HÄST", "CACTUS": "KAKTUS",
    "ALIEN": "RYMDVARELSE", "RAINBOW MOM": "REGNBÅGSMAMMA", "GREEN GRANNY": "GRÖN MORMOR", "PIXIE": "TOMTE",
    "ALLEY CAT": "GATUKATT", "LION CUB": "LEJONUNGE", "SQUIRREL": "EKORRE",
}

HATS = {"PARTY": "KALAS", "CROWN": "KRONA", "TOP HAT": "HÖG HATT", "BUCKET": "FISKEHATT", "WIZARD": "TROLLKARL",
        "BEANIE": "MÖSSA", "WESTERN": "COWBOY", "CHEF": "KOCK", "PROPELLER": "PROPELLER", "FLOWERS": "BLOMMOR",
        "STAR": "STJÄRNA"}

# FOLLOW's songs: songs Swedish children sing, each taken note for note from the score in a Wikipedia article (named above
# it; the article's LilyPond rendered to MIDI and its tune read back, tools: see RAINBOW.md), and moved, where
# it says, to fit the keys at OCT 0 (F3 .. G5) with the fewest black keys. A score that repeats itself whole
# is played once. Then a few known everywhere, the same notes as kid.c's English list.
SOLFA_SONGS = []
SONGS = [
    # Frère Jacques (Broder Jakob) (fr.wikipedia.org, its score)
    ("BRODER JAKOB", "G4 A4 B4 G4 G4 A4 B4 G4 B4 C5 D5 B4 C5 D5 D5 E5 D5 C5 B4 G4 D5 E5 D5 C5 B4 G4 G4 D4 G4 G4 D4 G4"),
    ("BLINKA LILLA", "C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4 G4 G4 F4 F4 E4 E4 D4 G4 G4 F4 F4 E4 E4 D4 C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4"),   # known everywhere (as kid.c's English list)
    ("GRATTIS", "G3 G3 A3 G3 C4 B3 G3 G3 A3 G3 D4 C4 G3 G3 G4 E4 C4 B3 A3 F4 F4 E4 C4 D4 C4"),   # known everywhere (as kid.c's English list)
    ("ODE GLÄDJEN", "E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4 E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 D4 C4 C4"),   # known everywhere (as kid.c's English list)
    ("BJÄLLERKLANG", "E4 E4 E4 E4 E4 E4 E4 G4 C4 D4 E4 F4 F4 F4 F4 F4 E4 E4 E4 E4 G4 G4 F4 D4 C4"),   # known everywhere (as kid.c's English list)
    # O Tannenbaum (de.wikipedia.org, its score, moved -7)
    ("O GRANNA TRÄD", "G3 C4 C4 C4 D4 E4 E4 E4 E4 D4 E4 F4 B3 D4 C4 G4 G4 E4 A4 G4 G4 F4 F4 F4 F4 D4 G4 F4 F4 E4 E4 G3 C4 C4 C4 D4 E4 E4 E4 E4 D4 E4 F4 B3 D4 C4"),
    # Stille Nacht, heilige Nacht (de.wikipedia.org, its score, moved -2)
    ("STILLA NATT", "G4 A4 G4 E4 G4 A4 G4 E4 D5 CS5 D5 B4 C5 B4 C5 G4 A4 A4 C5 B4 A4 G4 A4 G4 E4 A4 A4 C5 B4 A4 G4 A4 G4 E4 B4 B4 B4 D5 C5 B4 C5 E5 C5 G4 E4 G4 F4 D4 C4"),
]

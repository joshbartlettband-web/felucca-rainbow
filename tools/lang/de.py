# Rainbow mode in German: what the screen says, the friends' and hats' names, and FOLLOW's songs. Same rules as pt.py.
# The notes are C D E F G A H, as German children learn them (SUBS: kid.c's note names with H for B).
DOREMI = False

SUBS = {'"A", "A#", "B"};': '"A", "A#", "H"};'}

PAGE = {   # its page on the site (web/make_lang_page.py)
    'lang': 'de',
    'title': 'Rainbow mode auf Deutsch',
    'lede': 'Ein Musikspielzeug für kleine Hände, jetzt auf Deutsch. Eine kostenlose Firmware, die den M-VAVE FM-1 Synthesizer in etwas verwandelt, das schon kleine Kinder spielen können.',
    'install': 'Auf den FM-1 spielen',
    'note': 'Kein FM-1? Man kann trotzdem spielen, mit den Tasten auf dem Bildschirm oder der Computertastatur. Der Installer und die Browserseite sind noch auf Englisch, aber das Spielzeug spricht Deutsch.',
    'inside': 'Was drin ist',
    'facts': ['Alles auf dem Bildschirm ist auf Deutsch, und die Noten heißen C D E F G A H, wie in der Schule. Jede Taste zeigt ihren Ton groß und in seiner Farbe.', '94 Freunde, jeder mit eigenem Bild, Klang, Himmel und Lieblingsbeat, alle mit deutschen Namen: EINHORN, SCHNEEMANN, SEEPFERDCHEN.', 'FOLGEN lässt die nächste Taste von 21 Liedern leuchten, von Alle meine Entchen und Hänschen klein bis Kuckuck, Kuckuck und Stille Nacht.', 'Für Erwachsene: HOME eine Sekunde halten, dann OCT- oder OCT+ für die Lautstärke, oder KNOB 1 nach links, um die Notenlinien auszublenden. HOME und SAVE 3 Sekunden zusammen halten führt zurück zum Felucca-Synth.'],
    'songs': 'Die Lieder',
    'source': 'Die Noten jedes Liedes stammen aus der Partitur im Wikipedia-Artikel darüber.',
    'footer': 'Kostenlos und quelloffen (GPL-3.0), gebaut auf Felucca von Leo Kuroshita und Hügelton Instruments. Ein Fanprojekt: M-VAVE hat es nicht gemacht und unterstützt es nicht.',
    'try': 'Im Browser ausprobieren',
}

WORDS = {
    # ALGORITHM
    "1 FRIEND": "1 FREUND", "3 FRIENDS": "3 FREUNDE", "STRUM": "HARFE", "ACCORDION": "AKKORDEON", "GUESS": "RATEN",
    "FOLLOW": "FOLGEN", "CHORDS": "AKKORDE", "COPY ME": "MACH NACH",
    # the cards (ALGORITHM turned): up to 3 lines of 17
    "EVERY KEY PLAYS\\nONE NOTE\\nTRY THE KNOBS TOO": "JEDE TASTE\\nSPIELT EINEN TON\\nDREH DIE KNÖPFE",
    "EVERY KEY PLAYS\\nA BIG CHORD\\nFIND MAGIC ONES": "JEDE TASTE\\nSPIELT AKKORDE\\nSUCH DIE ZAUBER",
    "BLACK KEY CHORDS\\nSWEEP THE WHITE\\nKEYS TO STRUM": "SCHWARZ GIBT DEN\\nAKKORD WEISS\\nSTREICHT IHN",
    "HOLD A BLACK KEY\\nPLAY A TUNE ON\\nTHE WHITE KEYS": "HALT SCHWARZ\\nSPIEL DIE MELODIE\\nAUF WEISS",
    "A FRIEND SINGS\\nFIND THE NOTE\\nPLAY HEARS AGAIN": "EIN FREUND SINGT\\nFINDE DEN TON\\nPLAY NOCHMAL",
    "PLAY THE KEY\\nTHAT LIGHTS UP\\nSEQ PICKS A SONG": "DRÜCK DIE TASTE\\nDIE LEUCHTET\\nSEQ NEUES LIED",
    "HOLD ALL THE KEYS\\nTHAT LIGHT UP\\nSEQ PICKS LESSONS": "HALT DIE TASTEN\\nDIE LEUCHTEN\\nSEQ WÄHLT ÜBUNG",
    "LISTEN TO THE\\nFRIEND\\nTHEN PLAY IT BACK": "HÖR GUT ZU\\nUND SPIEL ES NACH",
    # the top row's tricks
    "HICCUP": "SCHLUCKAUF", "BACKWARDS": "RÜCKWÄRTS", "SLEEPY": "MÜDE", "SQUEAKY": "PIEPSIG", "GIANT": "RIESE",
    "FREEZE": "EINFRIEREN",
    # the knobs
    "BIG": "GROSS", "SMALL": "KLEIN", "DAY": "TAG", "SUNSET": "ABEND", "NIGHT": "NACHT", "ECHO": "ECHO",
    "WIGGLE": "WACKELN", "SLOW": "LANGSAM", "WALK": "GEHEN", "FAST": "SCHNELL", "MEDIUM": "MITTEL",
    # the beats
    "DANCE": "TANZ", "MARCH": "MARSCH", "SPOOKY": "GRUSELIG", "TRAIN": "ZUG", "LULLABY": "SCHLAFLIED",
    "HOEDOWN": "COUNTRY", "POLKA": "POLKA", "NO BEAT": "KEIN BEAT",
    # games, secrets, the grown-ups' settings
    "YES!": "JA!", "TRY AGAIN": "NOCHMAL", "LISTEN": "HÖR ZU", "YOUR TURN": "DU BIST DRAN", "YAY!": "JUHU!",
    "STAR!": "STERN!", "NEW HAT!": "NEUER HUT!", "NEW FRIEND!": "NEUER FREUND!", "NEW SKY!": "NEUER HIMMEL!",
    "NEW SONG": "NEUES LIED", "NO HAT": "KEIN HUT", "STARS": "STERNE", "LOOK-ALIKES OFF": "DOUBLES AUS",
    "STAFF ON": "NOTEN AN", "STAFF OFF": "NOTEN AUS",
    "LOOK-ALIKES ON": "DOUBLES AN", "HI!": "HALLO!", "HI": "HALLO", "YOUR NAME": "DEIN NAME",
    "PRESETS  LETTER": "PRESETS  ABC", "ALGORITHM  NEXT": "ALGORITHM  WEITER", "SAVE  KEEP IT": "SAVE  BEHALTEN",
    "HOME  LEAVE IT": "HOME  ZURÜCK", "SPARKLE": "GLITZER", "SPARKLE TUNE": "GLITZER MELODIE", "SPARKLE ALL": "GLITZER ALLES",
    "WRITE": "KOMPONIEREN",
    # chords and lessons
    "MAJOR": "DUR", "MINOR": "MOLL", "SEVEN": "SEPTIME", "NINE": "NONE",
    "C_MAJOR=": "C_DUR=", "F_MAJOR=": "F_DUR=", "G_MAJOR=": "G_DUR=", "A_MINOR=": "A_MOLL=", "G_SEVEN=": "G_SEPTIME=",
    "FIRST CHORDS": "DIE ERSTEN", "POP FOUR": "VIER POP", "SEVENTHS": "SEPTIMEN",
    # the drums' names
    "KICK": "BASSDRUM", "SNARE": "SNARE", "CLAP": "KLATSCHEN", "HI-HAT": "HI-HAT", "OPEN HAT": "HI-HAT OFFEN",
    "RIM": "RAND", "COWBELL": "KUHGLOCKE", "CYMBAL": "BECKEN",
}

NAMES = {   # the friends (and the look-alikes' stand-ins): one line of 13, or two words of 13 and 15 in all
    "DUCKY": "ENTCHEN", "PINK DUCKY": "ROSA ENTCHEN", "COOL DUCKY": "COOLE ENTE", "AXOLOTL": "AXOLOTL",
    "UNICORN": "EINHORN", "GIRAFFE": "GIRAFFE", "GOO": "GLIBBER", "GOOBERT": "GOOBERT", "BLUE PUP": "BLAUER WELPE",
    "RED MONSTER": "ROTES MONSTER", "BLUE MONSTER": "BLAUES MONSTER", "APRIL": "APRIL", "SCISSORS": "SCHERE",
    "GHOST": "GESPENST", "WEB HERO": "NETZHELD", "BUTTERFLY": "SCHMETTERLING", "KITTY": "KÄTZCHEN", "FROG": "FROSCH",
    "ROBOT": "ROBOTER", "RAINBOW": "REGENBOGEN", "PRINCESS DUCKY": "PRINZESSIN", "RED PUP": "ROTER WELPE",
    "YELLOW BIRD": "GELBER VOGEL", "SLIMY": "SCHLEIMI", "BUNNY": "HÄSCHEN", "PANDA": "PANDA", "PENGUIN": "PINGUIN",
    "OWL": "EULE", "BEE": "BIENE", "LADYBUG": "MARIENKÄFER", "DINO": "DINO", "WHALE": "WAL", "OCTOPUS": "KRAKE",
    "FISH": "FISCH", "TURTLE": "SCHILDKRÖTE", "ICE CREAM": "EIS", "CUPCAKE": "TÖRTCHEN", "ROCKET": "RAKETE",
    "STRAWBERRY": "ERDBEERE", "STAR": "STERN", "T-REX": "T-REX", "SKELETON": "SKELETT", "RANCHER": "FARMER",
    "RODEO": "COWBOY", "VACUUM": "STAUBSAUGER", "SPACE HERO": "ASTRONAUT", "BEAT BOT": "BEAT-ROBOTER",
    "TOY DRUM": "TROMMEL", "BONGO": "BONGO", "MONKEY": "AFFE", "ELEPHANT": "ELEFANT", "RACE CAR": "RENNAUTO",
    "JELLYFISH": "QUALLE", "BEAR": "BÄR", "SNOWMAN": "SCHNEEMANN", "CRAB": "KRABBE", "WOLF": "WOLF",
    "CAMEL": "KAMEL", "SCIENTIST": "FORSCHERIN", "FLYTRAP": "FLIEGENFALLE", "SUNFLOWER": "SONNENBLUME",
    "SPIDER MOM": "SPINNENMAMA", "DRAGON DUCK": "DRACHENENTE", "SPIDER GRANDMA": "SPINNENOMA",
    "NIGHT LIGHT": "NACHTLICHT", "GREEN QUEEN": "GRÜNE KÖNIGIN", "KING AXOLOTL": "KÖNIG AXOLOTL",
    "FAIRY MONSTER": "FEENMONSTER", "MORNING GLORY": "WINDE", "GROUCH": "GRIESGRAM", "TIGER CUB": "TIGERBABY",
    "RACCOON": "WASCHBÄR", "GOLDENROD": "GOLDRUTE", "PIANO PAL": "KLAVIER", "FLUTE BIRD": "FLÖTENVOGEL",
    "SAX CAT": "SAXOKATZE", "COW": "KUH", "PIG": "SCHWEINCHEN", "SHEEP": "SCHAF", "SHARK": "HAI",
    "SEAHORSE": "SEEPFERDCHEN", "STARFISH": "SEESTERN", "SNAIL": "SCHNECKE", "CATERPILLAR": "RAUPE",
    "FIREFLY": "GLÜHWÜRMCHEN", "TRICERATOPS": "TRICERATOPS", "STEGOSAURUS": "STEGOSAURUS", "PIZZA": "PIZZA",
    "DONUT": "DONUT", "BANANA": "BANANE", "TRAIN": "ZUG", "FIRE TRUCK": "FEUERWEHR", "SCHOOL BUS": "SCHULBUS",
    "HELICOPTER": "HUBSCHRAUBER", "GOLD DUCKY": "GOLDENTCHEN",
    "SPOTTY PUP": "FLECKENWELPE", "FOX": "FUCHS", "FUZZY": "FLAUSCHI", "BIG BLUE": "BLAUER RIESE", "SPIDER": "SPINNE",
    "PUMPKIN": "KÜRBIS", "CHICK": "KÜKEN", "BAT": "FLEDERMAUS", "HORSE": "PFERD", "CACTUS": "KAKTUS",
    "ALIEN": "MARSMENSCH", "RAINBOW MOM": "BUNTE MAMA", "GREEN GRANNY": "GRÜNE OMA", "PIXIE": "KOBOLD",
    "ALLEY CAT": "STRASSENKATZE", "LION CUB": "LÖWENBABY", "SQUIRREL": "EICHHÖRNCHEN",
}

HATS = {"PARTY": "PARTY", "CROWN": "KRONE", "TOP HAT": "ZYLINDER", "BUCKET": "FISCHERHUT", "WIZARD": "ZAUBERER",
        "BEANIE": "MÜTZE", "WESTERN": "COWBOY", "CHEF": "KOCH", "PROPELLER": "PROPELLER", "FLOWERS": "BLUMEN",
        "STAR": "STERN"}

# FOLLOW's songs: German children's songs, each taken note for note from the score in a Wikipedia article (named above
# it; the article's LilyPond rendered to MIDI and its tune read back, tools: see RAINBOW.md), and moved, where
# it says, to fit the keys at OCT 0 (F3 .. G5) with the fewest black keys. A score that repeats itself whole
# is played once. Then a few known everywhere, the same notes as kid.c's English list.
SOLFA_SONGS = []
SONGS = [
    # Alle meine Entchen (de.wikipedia.org, its score)
    ("ALLE ENTCHEN", "C4 D4 E4 F4 G4 G4 A4 A4 A4 A4 G4 A4 A4 A4 A4 G4 F4 F4 F4 F4 E4 E4 D4 D4 D4 D4 C4"),
    # Hänschen klein (de.wikipedia.org, its score, moved +2)
    ("HÄNSCHEN KLEIN", "D5 B4 B4 C5 A4 A4 G4 A4 B4 C5 D5 D5 D5 D5 B4 B4 C5 A4 A4 G4 B4 D5 D5 G4 A4 A4 A4 A4 A4 B4 C5 B4 B4 B4 B4 B4 C5 D5 D5 B4 B4 C5 A4 A4 G4 B4 D5 D5 G4"),
    # Alle Vögel sind schon da (de.wikipedia.org, its score, moved -2)
    ("ALLE VÖGEL", "C4 E4 G4 C5 A4 C5 A4 G4 F4 G4 E4 C4 D4 C4 G4 G4 F4 F4 E4 G4 E4 D4 G4 G4 F4 F4 E4 G4 E4 D4 C4 E4 G4 C5 A4 C5 A4 G4 F4 G4 E4 C4 D4 C4"),
    # Kuckuck, Kuckuck, ruft's aus dem Wald (de.wikipedia.org, its score)
    ("KUCKUCK", "D5 B4 D5 B4 A4 G4 A4 G4 A4 A4 B4 C5 A4 B4 B4 C5 D5 B4 D5 B4 D5 B4 C5 B4 A4 G4"),
    # Summ, summ, summ (de.wikipedia.org, its score)
    ("SUMM SUMM SUMM", "D5 C5 B4 A4 B4 C5 A4 G4 B4 C5 D5 B4 A4 B4 C5 A4 B4 C5 D5 B4 A4 B4 C5 A4 D5 C5 B4 A4 B4 C5 A4 G4"),
    # Fuchs, du hast die Gans gestohlen (de2.wikipedia.org, its score, moved -2)
    ("FUCHS", "C4 D4 E4 F4 G4 G4 G4 G4 A4 F4 C5 A4 G4 A4 F4 C5 A4 G4 G4 F4 F4 F4 F4 E4 E4 E4 E4 D4 E4 D4 C4 E4 G4 G4 F4 F4 F4 F4 E4 E4 E4 E4 D4 E4 D4 C4"),
    # Häschen in der Grube (de.wikipedia.org, its score, moved -2)
    ("HÄSCHEN", "C4 D4 E4 F4 G4 G4 A4 F4 C5 A4 G4 A4 F4 C5 A4 G4 G4 F4 F4 F4 F4 E4 E4 E4 D4 E4 D4 C4 E4 G4 G4 G4 C5 G4 G4 C5 G4 G4 C4"),
    # Die Vogelhochzeit (de.wikipedia.org, its score, moved +5)
    ("VOGELHOCHZEIT", "E5 G5 E5 G5 E5 F5 D5 F5 D5 E5 C5 G5 E5 D5 G5 G5 G5 E5 C5 C5 C5 G5 E5 D5 D5 D5 G5 F5 E5 C5 D5 B4 C5"),
    # Backe, backe Kuchen (de.wikipedia.org, its score, moved -2)
    ("BACKE BACKE", "G4 G4 A4 A4 G4 E4 C4 G4 G4 A4 A4 G4 E4 G4 G4 A4 A4 G4 G4 E4 C4 G4 G4 A4 A4 G4 G4 E4 E4 G4 G4 G4 E4 G4 G4 G4 E4 G4 G4 E4 G4 G4 A4 A4 G4 G4 E4 C5 G4 F4 E4 D4 C4"),
    # Brüderchen, komm tanz mit mir (de.wikipedia.org, its score, moved +5)
    ("BRÜDERCHEN", "G4 C5 C5 C5 B4 D5 G4 G4 B4 D5 F5 E5 G5 C5 E5 E5 F5 D5 D5 E5 C5 C5 D5 D5 B4 B4 C5"),
    # Hänsel und Gretel verliefen sich im Wald (de.wikipedia.org, its score, moved -2)
    ("HÄNSEL GRETEL", "G4 E4 F4 G4 E4 C4 D4 D4 D4 E4 C4 G4 E4 F4 G4 E4 C4 D4 D4 D4 E4 C4 C4 D4 D4 D4 E4 F4 D4 D4 E4 E4 E4 F4 G4 G4 E4 F4 G4 E4 C4 D4 D4 D4 E4 C4"),
    # Grün, grün, grün sind alle meine Kleider (de.wikipedia.org, its score, moved +5)
    ("GRÜN GRÜN GRÜN", "C5 C5 D5 D5 B4 B4 A4 B4 C5 G4 C5 C5 D5 D5 B4 B4 A4 B4 C5 E5 E5 G5 F5 F5 D5 D5 D5 F5 E5 E5 C5 C5 D5 D5 B4 A4 B4 C5"),
    # Ich geh' mit meiner Laterne (de.wikipedia.org, its score)
    ("LATERNE", "D4 G4 G4 B4 G4 B4 D5 B4 G4 A4 A4 A4 A4 B4 A4 G4 D4 G4 G4 B4 G4 B4 D5 B4 G4 A4 A4 A4 B4 A4 G4 B4 D5 B4 G4 B4 D5 B4 G4 G4 A4 A4 A4 A4 B4 A4 G4 B4 D5 B4 G4 B4 D5 B4 G4 G4 A4 A4 A4 A4 B4 A4 G4"),
    # Hopp, hopp, hopp, Pferdchen, lauf Galopp (de2.wikipedia.org, its score, moved +5)
    ("HOPP HOPP HOPP", "C5 E5 G5 G5 F5 E5 D5 C5 D5 D5 B4 G4 G5 G5 E5 C5 D5 D5 B4 G4 G5 G5 E5 C5 C5 D5 E5 F5 G5 G5 F5 E5 D5 C5"),
    # Weißt du, wie viel Sternlein stehen (de.wikipedia.org, its score, moved +2)
    ("STERNLEIN", "G4 A4 B4 B4 C5 A4 E5 D5 D5 B4 D5 D5 C5 C5 D5 C5 B4 G4 A4 B4 B4 C5 A4 E5 D5 D5 B4 D5 D5 C5 C5 D5 C5 B4 D5 B4 B4 A4 A4 E5 C5 C5 B4 B4 D5 B4 B4 A4 A4 E5 C5 C5 B4 B4 G4 A4 B4 B4 C5 A4 E5 D5 B4 D5 D5 C5 C5 D5 C5 B4"),
    # Guten Abend, gut' Nacht (Brahms) (de.wikipedia.org, its score, moved -3)
    ("GUTEN ABEND", "E4 E4 G4 E4 E4 G4 E4 G4 C5 B4 A4 A4 G4 D4 E4 F4 D4 D4 E4 F4 D4 F4 B4 A4 G4 B4 C5 C4 C4 C5 A4 F4 G4 E4 C4 F4 G4 A4 E4 G4 C4 C4 C5 A4 F4 G4 E4 C4 F4 G4 F4 E4 D4 C4"),
    # Frère Jacques (de.wikipedia.org, its score, moved -2)
    ("BRUDER JAKOB", "C4 D4 E4 C4 C4 D4 E4 C4 E4 F4 G4 E4 F4 G4 G4 A4 G4 F4 E4 C4 G4 A4 G4 F4 E4 C4 C4 G3 C4 C4 G3 C4"),
    ("ZUM GEBURTSTAG", "G3 G3 A3 G3 C4 B3 G3 G3 A3 G3 D4 C4 G3 G3 G4 E4 C4 B3 A3 F4 F4 E4 C4 D4 C4"),   # known everywhere (as kid.c's English list)
    ("FREUDE", "E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4 E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 D4 C4 C4"),   # known everywhere (as kid.c's English list)
    # O Tannenbaum (de.wikipedia.org, its score, moved -7)
    ("O TANNENBAUM", "G3 C4 C4 C4 D4 E4 E4 E4 E4 D4 E4 F4 B3 D4 C4 G4 G4 E4 A4 G4 G4 F4 F4 F4 F4 D4 G4 F4 F4 E4 E4 G3 C4 C4 C4 D4 E4 E4 E4 E4 D4 E4 F4 B3 D4 C4"),
    # Stille Nacht, heilige Nacht (de.wikipedia.org, its score, moved -2)
    ("STILLE NACHT", "G4 A4 G4 E4 G4 A4 G4 E4 D5 CS5 D5 B4 C5 B4 C5 G4 A4 A4 C5 B4 A4 G4 A4 G4 E4 A4 A4 C5 B4 A4 G4 A4 G4 E4 B4 B4 B4 D5 C5 B4 C5 E5 C5 G4 E4 G4 F4 D4 C4"),
]

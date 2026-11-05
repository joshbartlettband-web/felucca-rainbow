# Rainbow mode in Italian: what the screen says, the friends' and hats' names, and FOLLOW's songs. Same rules as pt.py.
DOREMI = True                          # the note names start as DO RE MI (HOME held 1 s, then KNOB 2: C D E)

PAGE = {   # its page on the site (web/make_lang_page.py)
    'lang': 'it',
    'title': 'Rainbow mode in italiano',
    'lede': 'Un giocattolo musicale per mani piccole, ora in italiano. Un firmware gratuito che trasforma il sintetizzatore M-VAVE FM-1 in qualcosa che anche un bambino piccolo può suonare.',
    'install': 'Mettilo sul FM-1',
    'note': "Niente FM-1? Si può suonare lo stesso, con i tasti sullo schermo o la tastiera del computer. L'installer e la pagina del browser sono ancora in inglese, ma il giocattolo parla italiano.",
    'inside': "Cosa c'è dentro",
    'facts': ['Tutto sullo schermo è in italiano, e le note si chiamano DO RE MI. Ogni tasto mostra la sua nota, grande e nel suo colore.', '94 amici, ognuno con il suo disegno, il suo suono, il suo cielo e il suo ritmo preferito, tutti con un nome italiano: UNICORNO, PUPAZZO, CAVALLUCCIO.', 'SEGUI accende il prossimo tasto di 10 canzoni, come Fra Martino, Funiculì funiculà e Tu scendi dalle stelle.', 'Per i grandi: tieni premuto HOME un secondo, poi OCT- o OCT+ per il volume, oppure KNOB 1 a sinistra per togliere il pentagramma. HOME e SAVE insieme per 3 secondi riportano al synth Felucca.'],
    'songs': 'Le canzoni',
    'source': 'Le note di ogni canzone vengono dalla partitura nella sua voce su Wikipedia.',
    'footer': "Gratuito e open source (GPL-3.0), costruito su Felucca di Leo Kuroshita e Hügelton Instruments. Un progetto di fan: M-VAVE non l'ha fatto e non lo sostiene.",
    'try': 'Provalo nel browser',
}

WORDS = {
    # ALGORITHM
    "1 FRIEND": "1 AMICO", "3 FRIENDS": "3 AMICI", "STRUM": "ARPA", "ACCORDION": "FISARMONICA", "GUESS": "INDOVINA",
    "FOLLOW": "SEGUI", "CHORDS": "ACCORDI", "COPY ME": "IMITAMI",
    # the cards (ALGORITHM turned): up to 3 lines of 17
    "EVERY KEY PLAYS\\nONE NOTE\\nTRY THE KNOBS TOO": "OGNI TASTO\\nSUONA UNA NOTA\\nGIRA LE MANOPOLE",
    "EVERY KEY PLAYS\\nA BIG CHORD\\nFIND MAGIC ONES": "OGNI TASTO\\nSUONA UN ACCORDO\\nCERCA LA MAGIA",
    "BLACK KEY CHORDS\\nSWEEP THE WHITE\\nKEYS TO STRUM": "TIENI UN NERO\\nE SFIORA\\nI TASTI BIANCHI",
    "HOLD A BLACK KEY\\nPLAY A TUNE ON\\nTHE WHITE KEYS": "TIENI UN NERO\\nSUONA LA MELODIA\\nSUI BIANCHI",
    "A FRIEND SINGS\\nFIND THE NOTE\\nPLAY HEARS AGAIN": "UN AMICO CANTA\\nTROVA LA NOTA\\nPLAY LA RIPETE",
    "PLAY THE KEY\\nTHAT LIGHTS UP\\nSEQ PICKS A SONG": "SUONA IL TASTO\\nCHE SI ACCENDE\\nSEQ CAMBIA BRANO",
    "HOLD ALL THE KEYS\\nTHAT LIGHT UP\\nSEQ PICKS LESSONS": "TIENI I TASTI\\nCHE SI ACCENDONO\\nSEQ PER CAMBIARE",
    "LISTEN TO THE\\nFRIEND\\nTHEN PLAY IT BACK": "ASCOLTA BENE\\nE SUONA UGUALE",
    # the top row's tricks
    "HICCUP": "SINGHIOZZO", "BACKWARDS": "AL CONTRARIO", "SLEEPY": "NANNA", "SQUEAKY": "VOCINA", "GIANT": "GIGANTE",
    "FREEZE": "CONGELA",
    # the knobs
    "BIG": "GRANDE", "SMALL": "PICCOLO", "DAY": "GIORNO", "SUNSET": "TRAMONTO", "NIGHT": "NOTTE", "ECHO": "ECO",
    "WIGGLE": "TREMOLIO", "SLOW": "LENTO", "WALK": "PASSEGGIO", "FAST": "VELOCE", "MEDIUM": "MEDIO",
    # the beats
    "DANCE": "BALLO", "MARCH": "MARCIA", "SPOOKY": "PAURA", "TRAIN": "TRENINO", "LULLABY": "NINNA NANNA",
    "HOEDOWN": "COUNTRY", "POLKA": "POLKA", "NO BEAT": "SENZA RITMO",
    # games, secrets, the grown-ups' settings
    "YES!": "SÌ!", "TRY AGAIN": "RIPROVA", "LISTEN": "ASCOLTA", "YOUR TURN": "TOCCA A TE", "YAY!": "EVVIVA!",
    "STAR!": "STELLA!", "NEW HAT!": "CAPPELLO NUOVO!", "NEW FRIEND!": "NUOVO AMICO!", "NEW SKY!": "CIELO NUOVO!",
    "NEW SONG": "NUOVA CANZONE", "NO HAT": "SENZA CAPPELLO", "STARS": "STELLE", "LOOK-ALIKES OFF": "SOSIA NO",
    "STAFF ON": "PENTAGRAMMA SÌ", "STAFF OFF": "PENTAGRAMMA NO",
    "LOOK-ALIKES ON": "SOSIA SÌ", "HI!": "CIAO!", "HI": "CIAO", "YOUR NAME": "IL TUO NOME",
    "PRESETS  LETTER": "PRESETS  LETTERA", "ALGORITHM  NEXT": "ALGORITHM  AVANTI", "SAVE  KEEP IT": "SAVE  TIENI",
    "HOME  LEAVE IT": "HOME  ESCI", "SPARKLE": "SCINTILLA", "SPARKLE TUNE": "BRILLA MELODIA", "SPARKLE ALL": "BRILLA TUTTO",
    "WRITE": "COMPONI",
    # chords and lessons
    "MAJOR": "MAGGIORE", "MINOR": "MINORE", "SEVEN": "SETTIMA", "NINE": "NONA",
    "C_MAJOR=": "C_MAGGIORE=", "F_MAJOR=": "F_MAGGIORE=", "G_MAJOR=": "G_MAGGIORE=", "A_MINOR=": "A_MINORE=",
    "G_SEVEN=": "G_SETTIMA=", "FIRST CHORDS": "PRIMI", "POP FOUR": "QUATTRO POP", "SEVENTHS": "SETTIME",
    # the drums' names
    "KICK": "CASSA", "SNARE": "RULLANTE", "CLAP": "BATTIMANI", "HI-HAT": "HI-HAT", "OPEN HAT": "HI-HAT APERTO",
    "RIM": "CERCHIO", "COWBELL": "CAMPANACCIO", "CYMBAL": "PIATTO",
}

NAMES = {   # the friends (and the look-alikes' stand-ins): one line of 13, or two words of 13 and 15 in all
    "DUCKY": "PAPERELLA", "PINK DUCKY": "PAPERA ROSA", "COOL DUCKY": "PAPERA COOL", "AXOLOTL": "AXOLOTL",
    "UNICORN": "UNICORNO", "GIRAFFE": "GIRAFFA", "GOO": "MELMA", "GOOBERT": "GOOBERT", "BLUE PUP": "CUCCIOLO BLU",
    "RED MONSTER": "MOSTRO ROSSO", "BLUE MONSTER": "MOSTRO BLU", "APRIL": "APRIL", "SCISSORS": "FORBICI",
    "GHOST": "FANTASMA", "WEB HERO": "EROE RAGNO", "BUTTERFLY": "FARFALLA", "KITTY": "GATTINO", "FROG": "RANA",
    "ROBOT": "ROBOT", "RAINBOW": "ARCOBALENO", "PRINCESS DUCKY": "PAPERA REGINA", "RED PUP": "CUCCIOLO ROSSO",
    "YELLOW BIRD": "UCCELLINO", "SLIMY": "VISCIDO", "BUNNY": "CONIGLIETTO", "PANDA": "PANDA", "PENGUIN": "PINGUINO",
    "OWL": "GUFO", "BEE": "APE", "LADYBUG": "COCCINELLA", "DINO": "DINO", "WHALE": "BALENA", "OCTOPUS": "POLPO",
    "FISH": "PESCE", "TURTLE": "TARTARUGA", "ICE CREAM": "GELATO", "CUPCAKE": "TORTINA", "ROCKET": "RAZZO",
    "STRAWBERRY": "FRAGOLA", "STAR": "STELLA", "T-REX": "T-REX", "SKELETON": "SCHELETRO", "RANCHER": "ALLEVATORE",
    "RODEO": "COWBOY", "VACUUM": "ASPIRATORE", "SPACE HERO": "ASTRONAUTA", "BEAT BOT": "ROBOT RITMO",
    "TOY DRUM": "TAMBURELLO", "BONGO": "BONGO", "MONKEY": "SCIMMIA", "ELEPHANT": "ELEFANTE", "RACE CAR": "BOLIDE",
    "JELLYFISH": "MEDUSA", "BEAR": "ORSO", "SNOWMAN": "PUPAZZO", "CRAB": "GRANCHIO", "WOLF": "LUPO",
    "CAMEL": "CAMMELLO", "SCIENTIST": "SCIENZIATA", "FLYTRAP": "DIONEA", "SUNFLOWER": "GIRASOLE",
    "SPIDER MOM": "MAMMA RAGNO", "DRAGON DUCK": "PAPERA DRAGO", "SPIDER GRANDMA": "NONNA RAGNO",
    "NIGHT LIGHT": "LUCINA", "GREEN QUEEN": "REGINA VERDE", "KING AXOLOTL": "RE AXOLOTL",
    "FAIRY MONSTER": "MOSTRO FATA", "MORNING GLORY": "CAMPANULA", "GROUCH": "BRONTOLONE", "TIGER CUB": "TIGROTTO",
    "RACCOON": "PROCIONE", "GOLDENROD": "FIORE DORATO", "PIANO PAL": "PIANOFORTE", "FLUTE BIRD": "UCCELLO FLAUTO",
    "SAX CAT": "GATTO SAX", "COW": "MUCCA", "PIG": "MAIALINO", "SHEEP": "PECORA", "SHARK": "SQUALO",
    "SEAHORSE": "CAVALLUCCIO", "STARFISH": "STELLA MARINA", "SNAIL": "LUMACA", "CATERPILLAR": "BRUCO",
    "FIREFLY": "LUCCIOLA", "TRICERATOPS": "TRICERATOPO", "STEGOSAURUS": "STEGOSAURO", "PIZZA": "PIZZA",
    "DONUT": "CIAMBELLA", "BANANA": "BANANA", "TRAIN": "TRENINO", "FIRE TRUCK": "POMPIERI", "SCHOOL BUS": "SCUOLABUS",
    "HELICOPTER": "ELICOTTERO", "GOLD DUCKY": "PAPERA DORATA",
    "SPOTTY PUP": "CANE A MACCHIE", "FOX": "VOLPE", "FUZZY": "PELOSETTO", "BIG BLUE": "BLU GIGANTE", "SPIDER": "RAGNO",
    "PUMPKIN": "ZUCCA", "CHICK": "PULCINO", "BAT": "PIPISTRELLO", "HORSE": "CAVALLO", "CACTUS": "CACTUS",
    "ALIEN": "ALIENO", "RAINBOW MOM": "MAMMA COLORI", "GREEN GRANNY": "NONNA VERDE", "PIXIE": "FOLLETTO",
    "ALLEY CAT": "GATTO RANDAGIO", "LION CUB": "LEONCINO", "SQUIRREL": "SCOIATTOLO",
}

HATS = {"PARTY": "FESTA", "CROWN": "CORONA", "TOP HAT": "CILINDRO", "BUCKET": "PESCATORE", "WIZARD": "MAGO",
        "BEANIE": "BERRETTO", "WESTERN": "COWBOY", "CHEF": "CUOCO", "PROPELLER": "ELICA", "FLOWERS": "FIORI",
        "STAR": "STELLA"}

# FOLLOW's songs: songs Italian children sing, each taken note for note from the score in a Wikipedia article (named above
# it; the article's LilyPond rendered to MIDI and its tune read back, tools: see RAINBOW.md), and moved, where
# it says, to fit the keys at OCT 0 (F3 .. G5) with the fewest black keys. A score that repeats itself whole
# is played once. Then a few known everywhere, the same notes as kid.c's English list.
SOLFA_SONGS = []
SONGS = [
    # Frère Jacques (Fra Martino) (fr.wikipedia.org, its score)
    ("FRA MARTINO", "G4 A4 B4 G4 G4 A4 B4 G4 B4 C5 D5 B4 C5 D5 D5 E5 D5 C5 B4 G4 D5 E5 D5 C5 B4 G4 G4 D4 G4 G4 D4 G4"),
    # Funiculì funiculà (Luigi Denza, 1880) (other.wikipedia.org, its score, moved -3)
    ("FUNICULÌ", "B4 A4 B4 A4 C5 B4 A4 C5 B4 B4 A4 B4 A4 C5 B4 A4 C5 G4 E4 E4 E4 E4 E4 E4 E4 E4 E4 E4 E4 E4 E4 E4 E4 C5 D5 C5 A4 C5 G4 E4 E4 F4 G4 F4 E4 D4 C4"),
    # Tu scendi dalle stelle (other.wikipedia.org, its score, moved -3)
    ("TU SCENDI", "G4 G4 D4 A4 G4 F4 F4 E4 D4 E4 F4 G4 G4 F4 E4 D4 E4 D4 E4 F4 E4 D4 A4 G4 A4 G4 F4 E4 D4 E4 E4 D4 E4 F4 E4 D4 A4 G4 A4 G4 F4 E4 D4 C4 E4 F4 G4 F4 F4 D4 E4 F4 E4 E4 E4 F4 G4 F4 F4 D4 E4 F4 E4 D4 E4 F4 G4 G4 F4 E4 D4 E4 D4 E4 F4 E4 D4 A4 G4 A4 G4 F4 E4 D4 E4 E4 D4 E4 F4 E4 D4 A4 G4 A4 G4 F4 E4 D4 C4"),
    # Guten Abend, gut' Nacht (Brahms) (de.wikipedia.org, its score, moved -3)
    ("NINNA NANNA", "E4 E4 G4 E4 E4 G4 E4 G4 C5 B4 A4 A4 G4 D4 E4 F4 D4 D4 E4 F4 D4 F4 B4 A4 G4 B4 C5 C4 C4 C5 A4 F4 G4 E4 C4 F4 G4 A4 E4 G4 C4 C4 C5 A4 F4 G4 E4 C4 F4 G4 F4 E4 D4 C4"),
    # Sur le pont d'Avignon (Sul ponte di Avignone) (fr.wikipedia.org, its score, moved -5)
    ("SUL PONTE", "C4 C4 C4 D4 D4 D4 E4 F4 G4 C4 B3 C4 D4 G3 C4 C4 C4 D4 D4 D4 E4 F4 G4 C4 D4 B3 C4 C4 C4 C4 C4 D4 C4 C4 C4 C4 C4 D4 C4 C4 C4 C4 D4 D4 D4 E4 F4 G4 C4 B3 C4 D4 G3 C4 C4 C4 D4 D4 D4 E4 F4 G4 C4 D4 B3 C4"),
    ("BRILLA BRILLA", "C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4 G4 G4 F4 F4 E4 E4 D4 G4 G4 F4 F4 E4 E4 D4 C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4"),   # known everywhere (as kid.c's English list)
    ("TANTI AUGURI", "G3 G3 A3 G3 C4 B3 G3 G3 A3 G3 D4 C4 G3 G3 G4 E4 C4 B3 A3 F4 F4 E4 C4 D4 C4"),   # known everywhere (as kid.c's English list)
    ("INNO GIOIA", "E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4 E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 D4 C4 C4"),   # known everywhere (as kid.c's English list)
    ("JINGLE BELLS", "E4 E4 E4 E4 E4 E4 E4 G4 C4 D4 E4 F4 F4 F4 F4 F4 E4 E4 E4 E4 G4 G4 F4 D4 C4"),   # known everywhere (as kid.c's English list)
    # Stille Nacht, heilige Nacht (de.wikipedia.org, its score, moved -2)
    ("ASTRO DEL CIEL", "G4 A4 G4 E4 G4 A4 G4 E4 D5 CS5 D5 B4 C5 B4 C5 G4 A4 A4 C5 B4 A4 G4 A4 G4 E4 A4 A4 C5 B4 A4 G4 A4 G4 E4 B4 B4 B4 D5 C5 B4 C5 E5 C5 G4 E4 G4 F4 D4 C4"),
]

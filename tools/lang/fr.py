# Rainbow mode in French: what the screen says, the friends' and hats' names, and FOLLOW's songs. Same rules as pt.py.
DOREMI = True                          # the note names start as DO RE MI (HOME held 1 s, then KNOB 2: C D E)

PAGE = {   # its page on the site (web/make_lang_page.py)
    'lang': 'fr',
    'title': 'Rainbow mode en français',
    'lede': "Un jouet musical pour les petites mains, maintenant en français. Un firmware gratuit qui transforme le synthé M-VAVE FM-1 en quelque chose qu'un petit enfant peut jouer.",
    'install': 'Installer sur le FM-1',
    'note': "Pas de FM-1 ? On peut jouer quand même, avec les touches à l'écran ou le clavier de l'ordinateur. L'installeur et la page du navigateur sont encore en anglais, mais le jouet parle français.",
    'inside': "Ce qu'il y a dedans",
    'facts': ["Tout ce qui s'affiche est en français, et les notes s'appellent DO RÉ MI. Chaque touche montre sa note, en grand et dans sa couleur.", '94 amis, chacun avec son dessin, son son, son ciel et son rythme préféré, tous avec un nom français : LICORNE, BONHOMME, HIPPOCAMPE.', "SUIS allume la prochaine touche de 20 chansons, d'Au clair de la lune et Frère Jacques à Une souris verte et Douce nuit.", 'Pour les grands : tenez HOME une seconde, puis OCT- ou OCT+ pour le volume, ou KNOB 1 vers la gauche pour cacher la portée. HOME et SAVE ensemble pendant 3 secondes ramènent au synthé Felucca.'],
    'songs': 'Les chansons',
    'source': 'Les notes de chaque chanson viennent de la partition de son article sur Wikipédia.',
    'footer': "Gratuit et libre (GPL-3.0), construit sur Felucca de Leo Kuroshita et Hügelton Instruments. Un projet de fan : M-VAVE ne l'a pas fait et ne le soutient pas.",
    'try': 'Essayer dans le navigateur',
}

WORDS = {
    # ALGORITHM
    "1 FRIEND": "1 AMI", "3 FRIENDS": "3 AMIS", "STRUM": "HARPE", "ACCORDION": "ACCORDÉON", "GUESS": "DEVINE",
    "FOLLOW": "SUIS", "CHORDS": "ACCORDS", "COPY ME": "IMITE-MOI",
    # the cards (ALGORITHM turned): up to 3 lines of 17
    "EVERY KEY PLAYS\\nONE NOTE\\nTRY THE KNOBS TOO": "CHAQUE TOUCHE\\nJOUE UNE NOTE\\nJOUE AUX BOUTONS",
    "EVERY KEY PLAYS\\nA BIG CHORD\\nFIND MAGIC ONES": "CHAQUE TOUCHE\\nJOUE UN ACCORD\\nCHERCHE LA MAGIE",
    "BLACK KEY CHORDS\\nSWEEP THE WHITE\\nKEYS TO STRUM": "TIENS UNE NOIRE\\nET BALAIE\\nLES BLANCHES",
    "HOLD A BLACK KEY\\nPLAY A TUNE ON\\nTHE WHITE KEYS": "TIENS UNE NOIRE\\nJOUE UN AIR\\nSUR LES BLANCHES",
    "A FRIEND SINGS\\nFIND THE NOTE\\nPLAY HEARS AGAIN": "UN AMI CHANTE\\nTROUVE LA NOTE\\nPLAY LA REJOUE",
    "PLAY THE KEY\\nTHAT LIGHTS UP\\nSEQ PICKS A SONG": "JOUE LA TOUCHE\\nQUI BRILLE\\nSEQ POUR CHANGER",
    "HOLD ALL THE KEYS\\nTHAT LIGHT UP\\nSEQ PICKS LESSONS": "TIENS LES TOUCHES\\nQUI BRILLENT\\nSEQ CHANGE LEÇON",
    "LISTEN TO THE\\nFRIEND\\nTHEN PLAY IT BACK": "ÉCOUTE TON AMI\\nPUIS REJOUE",
    # the top row's tricks
    "HICCUP": "HOQUET", "BACKWARDS": "À REBOURS", "SLEEPY": "DODO", "SQUEAKY": "SOURIS", "GIANT": "GÉANT",
    "FREEZE": "STOP",
    # the knobs
    "BIG": "GRAND", "SMALL": "PETIT", "DAY": "JOUR", "SUNSET": "SOIR", "NIGHT": "NUIT", "ECHO": "ÉCHO",
    "WIGGLE": "TREMBLE", "SLOW": "LENT", "WALK": "MARCHE", "FAST": "VITE", "MEDIUM": "MOYEN",
    # the beats
    "DANCE": "DANSE", "MARCH": "FANFARE", "SPOOKY": "FANTÔME", "TRAIN": "TRAIN", "LULLABY": "BERCEUSE",
    "HOEDOWN": "COUNTRY", "POLKA": "POLKA", "NO BEAT": "SANS RYTHME",
    # games, secrets, the grown-ups' settings
    "YES!": "OUI!", "TRY AGAIN": "ENCORE", "LISTEN": "ÉCOUTE", "YOUR TURN": "À TOI", "YAY!": "BRAVO!",
    "STAR!": "ÉTOILE!", "NEW HAT!": "NOUVEAU CHAPEAU!", "NEW FRIEND!": "NOUVEL AMI!", "NEW SKY!": "NOUVEAU CIEL!",
    "NEW SONG": "NOUVEL AIR", "NO HAT": "SANS CHAPEAU", "STARS": "ÉTOILES", "LOOK-ALIKES OFF": "SOSIES NON",
    "STAFF ON": "PORTÉE OUI", "STAFF OFF": "PORTÉE NON",
    "LOOK-ALIKES ON": "SOSIES OUI", "HI!": "SALUT!", "HI": "SALUT", "YOUR NAME": "TON NOM",
    "PRESETS  LETTER": "PRESETS  LETTRE", "ALGORITHM  NEXT": "ALGORITHM  APRÈS", "SAVE  KEEP IT": "SAVE  GARDER",
    "HOME  LEAVE IT": "HOME  SORTIR", "SPARKLE": "ÉCLAT", "SPARKLE TUNE": "ÉCLAT MÉLODIE", "SPARKLE ALL": "ÉCLAT TOUT",
    "WRITE": "COMPOSER",
    # chords and lessons
    "MAJOR": "MAJEUR", "MINOR": "MINEUR", "SEVEN": "SEPTIÈME", "NINE": "NEUVIÈME",
    "C_MAJOR=": "C_MAJEUR=", "F_MAJOR=": "F_MAJEUR=", "G_MAJOR=": "G_MAJEUR=", "A_MINOR=": "A_MINEUR=",
    "G_SEVEN=": "G_SEPTIÈME=", "FIRST CHORDS": "PREMIERS", "POP FOUR": "QUATRE POP", "SEVENTHS": "SEPTIÈMES",
    # the drums' names
    "KICK": "GROSSE CAISSE", "SNARE": "CAISSE CLAIRE", "CLAP": "CLAP", "HI-HAT": "HI-HAT",
    "OPEN HAT": "HI-HAT OUVERT", "RIM": "CERCLE", "COWBELL": "CLOCHE", "CYMBAL": "CYMBALE",
}

NAMES = {   # the friends (and the look-alikes' stand-ins): one line of 13, or two words of 13 and 15 in all
    "DUCKY": "CANETON", "PINK DUCKY": "CANETON ROSE", "COOL DUCKY": "CANARD COOL", "AXOLOTL": "AXOLOTL",
    "UNICORN": "LICORNE", "GIRAFFE": "GIRAFE", "GOO": "GLU", "GOOBERT": "GOOBERT", "BLUE PUP": "CHIOT BLEU",
    "RED MONSTER": "MONSTRE ROUGE", "BLUE MONSTER": "MONSTRE BLEU", "APRIL": "APRIL", "SCISSORS": "CISEAUX",
    "GHOST": "FANTÔME", "WEB HERO": "HÉROS TOILE", "BUTTERFLY": "PAPILLON", "KITTY": "MINOU", "FROG": "GRENOUILLE",
    "ROBOT": "ROBOT", "RAINBOW": "ARC-EN-CIEL", "PRINCESS DUCKY": "CANE PRINCESSE", "RED PUP": "CHIOT ROUGE",
    "YELLOW BIRD": "OISEAU JAUNE", "SLIMY": "GLUANT", "BUNNY": "LAPINOU", "PANDA": "PANDA", "PENGUIN": "PINGOUIN",
    "OWL": "HIBOU", "BEE": "ABEILLE", "LADYBUG": "COCCINELLE", "DINO": "DINO", "WHALE": "BALEINE", "OCTOPUS": "PIEUVRE",
    "FISH": "POISSON", "TURTLE": "TORTUE", "ICE CREAM": "GLACE", "CUPCAKE": "PETIT GÂTEAU", "ROCKET": "FUSÉE",
    "STRAWBERRY": "FRAISE", "STAR": "ÉTOILE", "T-REX": "T-REX", "SKELETON": "SQUELETTE", "RANCHER": "FERMIER",
    "RODEO": "COW-BOY", "VACUUM": "ASPIRATEUR", "SPACE HERO": "ASTRONAUTE", "BEAT BOT": "ROBOT RYTHME",
    "TOY DRUM": "TAMBOURIN", "BONGO": "BONGO", "MONKEY": "SINGE", "ELEPHANT": "ÉLÉPHANT", "RACE CAR": "BOLIDE",
    "JELLYFISH": "MÉDUSE", "BEAR": "OURS", "SNOWMAN": "BONHOMME", "CRAB": "CRABE", "WOLF": "LOUP",
    "CAMEL": "CHAMEAU", "SCIENTIST": "SAVANTE", "FLYTRAP": "DIONÉE", "SUNFLOWER": "TOURNESOL",
    "SPIDER MOM": "MAMAN ARAIGNÉE", "DRAGON DUCK": "CANARD DRAGON", "SPIDER GRANDMA": "MAMIE ARAIGNÉE",
    "NIGHT LIGHT": "VEILLEUSE", "GREEN QUEEN": "REINE VERTE", "KING AXOLOTL": "ROI AXOLOTL",
    "FAIRY MONSTER": "MONSTRE FÉE", "MORNING GLORY": "LISERON", "GROUCH": "GROGNON", "TIGER CUB": "BÉBÉ TIGRE",
    "RACCOON": "RATON LAVEUR", "GOLDENROD": "FLEUR DORÉE", "PIANO PAL": "PIANO", "FLUTE BIRD": "OISEAU FLÛTE",
    "SAX CAT": "CHAT SAXO", "COW": "VACHE", "PIG": "COCHON", "SHEEP": "MOUTON", "SHARK": "REQUIN",
    "SEAHORSE": "HIPPOCAMPE", "STARFISH": "ÉTOILE DE MER", "SNAIL": "ESCARGOT", "CATERPILLAR": "CHENILLE",
    "FIREFLY": "LUCIOLE", "TRICERATOPS": "TRICÉRATOPS", "STEGOSAURUS": "STÉGOSAURE", "PIZZA": "PIZZA",
    "DONUT": "BEIGNET", "BANANA": "BANANE", "TRAIN": "TRAIN", "FIRE TRUCK": "POMPIERS", "SCHOOL BUS": "CAR SCOLAIRE",
    "HELICOPTER": "HÉLICOPTÈRE", "GOLD DUCKY": "CANETON DORÉ",
    "SPOTTY PUP": "CHIOT TACHETÉ", "FOX": "RENARD", "FUZZY": "TOUT DOUX", "BIG BLUE": "GRAND BLEU", "SPIDER": "ARAIGNÉE",
    "PUMPKIN": "CITROUILLE", "CHICK": "POUSSIN", "BAT": "CHAUVE-SOURIS", "HORSE": "CHEVAL", "CACTUS": "CACTUS",
    "ALIEN": "MARTIEN", "RAINBOW MOM": "MAMAN COULEURS", "GREEN GRANNY": "MAMIE VERTE", "PIXIE": "LUTIN",
    "ALLEY CAT": "CHAT DES RUES", "LION CUB": "LIONCEAU", "SQUIRREL": "ÉCUREUIL",
}

HATS = {"PARTY": "FÊTE", "CROWN": "COURONNE", "TOP HAT": "HAUT-DE-FORME", "BUCKET": "BOB", "WIZARD": "MAGICIEN",
        "BEANIE": "BONNET", "WESTERN": "COW-BOY", "CHEF": "TOQUE", "PROPELLER": "HÉLICE", "FLOWERS": "FLEURS",
        "STAR": "ÉTOILE"}

# FOLLOW's songs: French children's songs, each taken note for note from the score in a Wikipedia article (named above
# it; the article's LilyPond rendered to MIDI and its tune read back, tools: see RAINBOW.md), and moved, where
# it says, to fit the keys at OCT 0 (F3 .. G5) with the fewest black keys. A score that repeats itself whole
# is played once. Then a few known everywhere, the same notes as kid.c's English list.
SOLFA_SONGS = []
SONGS = [
    # Au clair de la lune (fr.wikipedia.org, its score)
    ("AU CLAIR", "C5 C5 C5 D5 E5 D5 C5 E5 D5 D5 C5 C5 C5 C5 D5 E5 D5 C5 E5 D5 D5 C5 D5 D5 D5 D5 A4 A4 D5 C5 B4 A4 G4 C5 C5 C5 D5 E5 D5 C5 E5 D5 D5 C5"),
    # Frère Jacques (fr.wikipedia.org, its score)
    ("FRÈRE JACQUES", "G4 A4 B4 G4 G4 A4 B4 G4 B4 C5 D5 B4 C5 D5 D5 E5 D5 C5 B4 G4 D5 E5 D5 C5 B4 G4 G4 D4 G4 G4 D4 G4"),
    # Ah ! vous dirai-je, maman (fr.wikipedia.org, its score)
    ("VOUS DIRAI-JE", "C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4 G4 G4 F4 F4 E4 E4 E4 D4 G4 G4 F4 F4 E4 E4 E4 D4"),
    # Sur le pont d'Avignon (fr.wikipedia.org, its score, moved -5)
    ("SUR LE PONT", "C4 C4 C4 D4 D4 D4 E4 F4 G4 C4 B3 C4 D4 G3 C4 C4 C4 D4 D4 D4 E4 F4 G4 C4 D4 B3 C4 C4 C4 C4 C4 D4 C4 C4 C4 C4 C4 D4 C4 C4 C4 C4 D4 D4 D4 E4 F4 G4 C4 B3 C4 D4 G3 C4 C4 C4 D4 D4 D4 E4 F4 G4 C4 D4 B3 C4"),
    # Il était une bergère (fr.wikipedia.org, its score)
    ("UNE BERGÈRE", "G4 C5 D5 E5 D5 C5 G4 G4 A4 A4 G4 G4 G4 A4 A4 G4 G4 C5 D5 E5 D5 C5 G4 G5 E5 C5 D5 B4 C5 C5 C5 G5 E5 C5 D5 B4 C5"),
    # Une souris verte (fr.wikipedia.org, its score)
    ("SOURIS VERTE", "G4 G4 G4 A4 G4 D4 G4 G4 G4 A4 G4 D4 C5 B4 A4 B4 C5 B4 A4 C5 B4 A4 B4 C5 B4 A4 G4 G4 G4 A4 G4 D4 G4 G4 G4 A4 G4 D4 G4 G4 G4 G4 A4 G4 G4 A4 G4 A4 D5 G4 D5 G4 G4 G4 G4 G4 G4 G4 A4 G4 G4 G4 G4 G4 G4 A4 G4 G4 G4 G4 G4 G4 A4 G4 G4 G4 G4 A4 D5 G4"),
    # Dodo, l'enfant do (fr.wikipedia.org, its score)
    ("DODO", "E4 C4 E4 E4 C4 D4 E4 F4 E4 D4 G4 E4 C4 E4 C4 E4 E4 C4 D4 E4 F4 E4 D4 G4 C4"),
    # Le Bon Roi Dagobert (fr.wikipedia.org, its score)
    ("DAGOBERT", "B4 B4 A4 A4 G4 G4 A4 B4 C5 B4 B4 A4 G4 A4 G4 G4 A4 B4 B4 B4 C5 D5 A4 A4 A4 G4 A4 B4 B4 B4 C5 D5 A4 A4 A4 B4 B4 A4 A4 G4 G4 A4 B4 C5 B4 A4 G4 A4 G4"),
    # Meunier tu dors (fr.wikipedia.org, its score, moved +2)
    ("MEUNIER", "D4 G4 B4 G4 A4 A4 A4 A4 A4 A4 G4 A4 B4 G4 D5 B4 D5 B4 C5 C5 C5 C5 C5 C5 D5 C5 B4 B4 B4 B4 B4 B4 B4 B4 B4 B4 B4 B4 D5 A4 A4 A4 A4 A4 A4 A4 A4 A4 D5 D5 B4 B4 B4 B4 B4 B4 B4 B4 B4 B4 B4 B4 D5 A4 A4 A4 A4 A4 A4 A4 A4 A4 D5 D5 G4"),
    # Une poule sur un mur (fr.wikipedia.org, its score)
    ("UNE POULE", "F4 F4 F4 F4 G4 G4 C4 F4 F4 F4 F4 G4 G4 C4 F4 F4 F4 F4 F4 G4 F4 F4 G4 F4 G4 C5 F4"),
    # Il court, il court, le furet (fr.wikipedia.org, its score, moved +2)
    ("LE FURET", "G4 C5 D5 E5 D5 D5 A4 C5 B4 A4 G4 A4 B4 C5 G4 C5 D5 E5 D5 D5 A4 C5 B4 A4 G4 A4 B4 C5 C5 B4 A4 G4 A4 B4 C5 E5 C5 B4 A4 G4 A4 B4 C5 G5 C5 B4 A4 G4 A4 B4 C5 E5 C5 B4 A4 G4 A4 B4 C5 G4 C5 D5 E5 D5 D5 A4 C5 B4 A4 G4 A4 B4 C5 G4 C5 D5 E5 D5 D5 A4 C5 B4 A4 G4 A4 B4 C5"),
    # Trois Petits Chats (fr.wikipedia.org, its score, moved -5)
    ("3 PETITS CHATS", "A3 B3 C4 B3 C4 A3 C4 D4 E4 E4 E4 E4 F4 E4 D4 D4 E4 D4 C4 C4 D4 C4 B3 A3"),
    # Il pleut, il pleut, bergère (fr.wikipedia.org, its score, moved -5)
    ("IL PLEUT", "E4 G4 E4 G4 E4 C4 G3 C4 B3 C4 D4 D4 E4 E4 D4 E4 F4 F4 G4 E4 G4 A4 G4 F4 E4 E4 D4 D4 E4 D4 F4 F4 E4 G4 F4 E4 D4 E4 C4 E4 D4 E4 G4 E4 G4 E4 F4 A4 G4 A4 G4 D4 E4 C4"),
    # Alouette (de.wikipedia.org, its score)
    ("ALOUETTE", "G4 A4 B4 B4 A4 G4 A4 B4 G4 D4 G4 A4 B4 B4 A4 G4 A4 B4 G4 G4 G4 G4 G4 G4 B4 D5 D5 E5 D5 C5 B4 A4 G4 D5 D5 D5 D4 D4 D4 D5 D5 D5 D4 D4 D4 D5 C5 B4 A4 G4 A4 B4 B4 A4 G4 A4 B4 G4 D4 G4 A4 B4 B4 A4 G4 A4 B4 G4"),
    # À la claire fontaine (de.wikipedia.org, its score)
    ("LA FONTAINE", "F4 F4 A4 A4 G4 A4 G4 F4 F4 A4 A4 G4 A4 A4 A4 G4 F4 A4 C5 A4 C5 C5 A4 F4 A4 G4 F4 F4 A4 A4 G4 F4 A4 F4 A4 A4 G4 F4 A4 G4 F4"),
    # Maman les p'tits bateaux (fr.wikipedia.org, its score, moved +5)
    ("PETITS BATEAUX", "G4 G4 F5 E5 D5 C5 G4 A4 C5 B4 G4 A4 B4 C5 C5 G4 G4 F5 E5 D5 C5 G4 G4 A4 C5 B4 G4 A4 B4 C5 G5 G5 E5 E5 C5 C5 E5 G5 G5 G5 G5 E5 C5 G5 G5 E5 E5 C5 C5 C5 E5 G5 G5 G5 G5 C5"),
    ("ANNIVERSAIRE", "G3 G3 A3 G3 C4 B3 G3 G3 A3 G3 D4 C4 G3 G3 G4 E4 C4 B3 A3 F4 F4 E4 C4 D4 C4"),   # known everywhere (as kid.c's English list)
    ("À LA JOIE", "E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4 E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 D4 C4 C4"),   # known everywhere (as kid.c's English list)
    ("VIVE LE VENT", "E4 E4 E4 E4 E4 E4 E4 G4 C4 D4 E4 F4 F4 F4 F4 F4 E4 E4 E4 E4 G4 G4 F4 D4 C4"),   # known everywhere (as kid.c's English list)
    # Stille Nacht, heilige Nacht (de.wikipedia.org, its score, moved -2)
    ("DOUCE NUIT", "G4 A4 G4 E4 G4 A4 G4 E4 D5 CS5 D5 B4 C5 B4 C5 G4 A4 A4 C5 B4 A4 G4 A4 G4 E4 A4 A4 C5 B4 A4 G4 A4 G4 E4 B4 B4 B4 D5 C5 B4 C5 E5 C5 G4 E4 G4 F4 D4 C4"),
]

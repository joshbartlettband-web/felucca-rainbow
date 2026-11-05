# Rainbow mode in Portuguese (Brazil): what the screen says, the friends' and hats' names, and FOLLOW's songs.
# tools/gen_kid_lang.py applies it to kid.c (WORDS: each English string literal, exactly as kid.c has it, and only ones
# the screen shows; never a preset's or a kit's name, which look the sounds up) and gen_kid_art.py to the names.
# Capitals only, in the band's font: A-Z, digits, # ! ? - and the accented capitals kid.c has (Á À Â Ã Ç É Ê Í Ó Ô Õ Ú).
DOREMI = True                          # the note names start as DO RE MI (HOME held 1 s, then KNOB 2: C D E)

WORDS = {
    # ALGORITHM
    "1 FRIEND": "1 AMIGO", "3 FRIENDS": "3 AMIGOS", "STRUM": "HARPA", "ACCORDION": "SANFONA", "GUESS": "ADIVINHE",
    "FOLLOW": "SIGA", "CHORDS": "ACORDES", "COPY ME": "ME IMITE",
    # the cards (ALGORITHM turned): up to 3 lines of 17
    "EVERY KEY PLAYS\\nONE NOTE\\nTRY THE KNOBS TOO": "CADA TECLA TOCA\\nUMA NOTA\\nGIRE OS BOTÕES",
    "EVERY KEY PLAYS\\nA BIG CHORD\\nFIND MAGIC ONES": "CADA TECLA TOCA\\nUM ACORDE\\nACHE OS MÁGICOS",
    "BLACK KEY CHORDS\\nSWEEP THE WHITE\\nKEYS TO STRUM": "A TECLA PRETA\\nESCOLHE O ACORDE\\nPASSE NAS BRANCAS",
    "HOLD A BLACK KEY\\nPLAY A TUNE ON\\nTHE WHITE KEYS": "SEGURE UMA PRETA\\nTOQUE A MELODIA\\nNAS BRANCAS",
    "A FRIEND SINGS\\nFIND THE NOTE\\nPLAY HEARS AGAIN": "UM AMIGO CANTA\\nACHE A NOTA\\nPLAY OUVE DE NOVO",
    "PLAY THE KEY\\nTHAT LIGHTS UP\\nSEQ PICKS A SONG": "TOQUE A TECLA\\nQUE ACENDE\\nSEQ MUDA A MÚSICA",
    "HOLD ALL THE KEYS\\nTHAT LIGHT UP\\nSEQ PICKS LESSONS": "SEGURE AS TECLAS\\nQUE ACENDEM\\nSEQ TROCA A LIÇÃO",
    "LISTEN TO THE\\nFRIEND\\nTHEN PLAY IT BACK": "ESCUTE O AMIGO\\nE TOQUE IGUAL",
    # the top row's tricks
    "HICCUP": "SOLUÇO", "BACKWARDS": "AO CONTRÁRIO", "SLEEPY": "SONINHO", "SQUEAKY": "FININHO", "GIANT": "GIGANTE",
    "FREEZE": "CONGELA",
    # the knobs
    "BIG": "GRANDE", "SMALL": "PEQUENO", "DAY": "DIA", "SUNSET": "PÔR DO SOL", "NIGHT": "NOITE", "ECHO": "ECO", "WIGGLE": "TREMIDO",
    "SLOW": "DEVAGAR", "WALK": "ANDANDO", "FAST": "RÁPIDO", "MEDIUM": "MÉDIO",
    # the beats
    "DANCE": "DANÇA", "MARCH": "MARCHA", "SPOOKY": "ASSOMBRADO", "TRAIN": "TREM", "LULLABY": "NINAR",
    "HOEDOWN": "QUADRILHA", "POLKA": "POLCA", "NO BEAT": "SEM BATIDA",
    # games, secrets, the grown-ups' settings
    "YES!": "ISSO!", "TRY AGAIN": "DE NOVO", "LISTEN": "OUÇA", "YOUR TURN": "SUA VEZ", "YAY!": "EBA!",
    "STAR!": "ESTRELA!", "NEW HAT!": "CHAPÉU NOVO!", "NEW FRIEND!": "AMIGO NOVO!", "NEW SKY!": "CÉU NOVO!",
    "NEW SONG": "MÚSICA NOVA", "NO HAT": "SEM CHAPÉU", "STARS": "ESTRELAS", "LOOK-ALIKES OFF": "SÓSIAS NÃO",
    "STAFF ON": "PAUTA SIM", "STAFF OFF": "PAUTA NÃO",
    "LOOK-ALIKES ON": "SÓSIAS SIM", "HI!": "OI!", "HI": "OI", "YOUR NAME": "SEU NOME", "PRESETS  LETTER": "PRESETS  LETRA",
    "ALGORITHM  NEXT": "ALGORITHM  SEGUE", "SAVE  KEEP IT": "SAVE  GUARDA", "HOME  LEAVE IT": "HOME  SAIR",
    "SPARKLE": "BRILHO", "SPARKLE TUNE": "BRILHA MELODIA", "SPARKLE ALL": "BRILHA TUDO", "WRITE": "COMPOR",
    # chords and lessons
    "MAJOR": "MAIOR", "MINOR": "MENOR", "SEVEN": "SÉTIMA", "NINE": "NONA",
    "C_MAJOR=": "C_MAIOR=", "F_MAJOR=": "F_MAIOR=", "G_MAJOR=": "G_MAIOR=", "A_MINOR=": "A_MENOR=", "G_SEVEN=": "G_SÉTIMA=",
    "FIRST CHORDS": "PRIMEIROS", "POP FOUR": "QUATRO POP", "SEVENTHS": "SÉTIMAS",
    # the drums' names
    "KICK": "BUMBO", "SNARE": "CAIXA", "CLAP": "PALMA", "HI-HAT": "CHIMBAL", "OPEN HAT": "CHIMBAL SOLTO", "RIM": "ARO",
    "COWBELL": "SINO", "CYMBAL": "PRATO",
}

NAMES = {   # the friends (and the look-alikes' stand-ins): one line of 13, or two words of 13 and 15 in all
    "DUCKY": "PATINHO", "PINK DUCKY": "PATINHO ROSA", "COOL DUCKY": "PATO LEGAL", "AXOLOTL": "AXOLOTE",
    "UNICORN": "UNICÓRNIO", "GIRAFFE": "GIRAFA", "GOO": "GOSMA", "GOOBERT": "GOOBERT", "BLUE PUP": "CÃO AZUL",
    "RED MONSTER": "MONSTRO RUBRO", "BLUE MONSTER": "MONSTRO AZUL", "APRIL": "APRIL", "SCISSORS": "TESOURA",
    "GHOST": "FANTASMA", "WEB HERO": "HERÓI DA TEIA", "BUTTERFLY": "BORBOLETA", "KITTY": "GATINHO", "FROG": "SAPO",
    "ROBOT": "ROBÔ", "RAINBOW": "ARCO-ÍRIS", "PRINCESS DUCKY": "PATA PRINCESA", "RED PUP": "CÃO VERMELHO",
    "YELLOW BIRD": "PÁSSARO", "SLIMY": "MELECA", "BUNNY": "COELHINHO", "PANDA": "PANDA", "PENGUIN": "PINGUIM",
    "OWL": "CORUJA", "BEE": "ABELHA", "LADYBUG": "JOANINHA", "DINO": "DINO", "WHALE": "BALEIA", "OCTOPUS": "POLVO",
    "FISH": "PEIXE", "TURTLE": "TARTARUGA", "ICE CREAM": "SORVETE", "CUPCAKE": "BOLINHO", "ROCKET": "FOGUETE",
    "STRAWBERRY": "MORANGO", "STAR": "ESTRELA", "T-REX": "T-REX", "SKELETON": "ESQUELETO", "RANCHER": "FAZENDEIRO",
    "RODEO": "PEÃO", "VACUUM": "ASPIRADOR", "SPACE HERO": "ASTRONAUTA", "BEAT BOT": "ROBÔ BATIDA",
    "TOY DRUM": "TAMBORZINHO", "BONGO": "BONGÔ", "MONKEY": "MACACO", "ELEPHANT": "ELEFANTE", "RACE CAR": "CARRO",
    "JELLYFISH": "ÁGUA-VIVA", "BEAR": "URSO", "SNOWMAN": "BONECO DE NEVE", "CRAB": "CARANGUEJO", "WOLF": "LOBO",
    "CAMEL": "CAMELO", "SCIENTIST": "CIENTISTA", "FLYTRAP": "PAPA-MOSCAS", "SUNFLOWER": "GIRASSOL",
    "SPIDER MOM": "MÃE ARANHA", "DRAGON DUCK": "PATO DRAGÃO", "SPIDER GRANDMA": "VOVÓ ARANHA",
    "NIGHT LIGHT": "LUZINHA", "GREEN QUEEN": "RAINHA VERDE", "KING AXOLOTL": "REI AXOLOTE",
    "FAIRY MONSTER": "MONSTRO FADA", "MORNING GLORY": "CAMPAINHA", "GROUCH": "RABUGENTO", "TIGER CUB": "TIGRINHO",
    "RACCOON": "GUAXINIM", "GOLDENROD": "FLOR DOURADA", "PIANO PAL": "PIANINHO", "FLUTE BIRD": "PÁSSARO FLAUTA",
    "SAX CAT": "GATO SAX", "COW": "VACA", "PIG": "PORQUINHO", "SHEEP": "OVELHA", "SHARK": "TUBARÃO",
    "SEAHORSE": "CAVALO MARINHO", "STARFISH": "ESTRELA DO MAR", "SNAIL": "CARACOL", "CATERPILLAR": "LAGARTA",
    "FIREFLY": "VAGA-LUME", "TRICERATOPS": "TRICERÁTOPO", "STEGOSAURUS": "ESTEGOSSAURO", "PIZZA": "PIZZA",
    "DONUT": "ROSQUINHA", "BANANA": "BANANA", "TRAIN": "TREM", "FIRE TRUCK": "BOMBEIROS", "SCHOOL BUS": "ÔNIBUS",
    "HELICOPTER": "HELICÓPTERO", "GOLD DUCKY": "PATINHO DE OURO",
    "SPOTTY PUP": "CÃO PINTADO", "FOX": "RAPOSA", "FUZZY": "PELUDINHO", "BIG BLUE": "AZULÃO", "SPIDER": "ARANHA",
    "PUMPKIN": "ABÓBORA", "CHICK": "PINTINHO", "BAT": "MORCEGO", "HORSE": "CAVALO", "CACTUS": "CACTO",
    "ALIEN": "ALIENÍGENA", "RAINBOW MOM": "MÃE ARCO-ÍRIS", "GREEN GRANNY": "VOVÓ VERDE", "PIXIE": "DUENDE",
    "ALLEY CAT": "GATO DE RUA", "LION CUB": "LEÃOZINHO", "SQUIRREL": "ESQUILO",
}

HATS = {"PARTY": "FESTA", "CROWN": "COROA", "TOP HAT": "CARTOLA", "BUCKET": "PESCADOR", "WIZARD": "MAGO",
        "BEANIE": "GORRO", "WESTERN": "CAUBÓI", "CHEF": "CHEF", "PROPELLER": "HÉLICE", "FLOWERS": "FLORES",
        "STAR": "ESTRELA"}

# FOLLOW's songs: Brazilian children's songs (traditional, public domain), as published note by note for recorder by
# Cifra Visual (cifravisual.com.br/flauta-doce, "Domínio público", checked there against their sources: lower case the
# low octave, capitals the high one), then a few known everywhere. Octave 4 = the middle (C4 is key 7). Each has to fit
# the keys at OCT 0 (F3 .. G5); Ciranda is moved from F down to C, so it stays on the white keys.
# FOLLOW's songs. First the Brazilian children's songs (traditional, public domain), copied exactly as Cifra Visual
# publishes them note by note for recorder (cifravisual.com.br/flauta-doce/<song>, each marked "Domínio público" and
# checked there against its sources): do re mi .. si, # and b, lower case the low octave (C4 = do), capitals the high
# one (DO = C5), " / " between phrases. tools/gen_kid_lang.py turns them into keys, moved by the number of semitones
# given (Ciranda from F to C, Boi da Cara Preta from G to C, so they stay on the white keys). Then a few known
# everywhere, written as notes. Each has to fit the keys at OCT 0 (F3 .. G5).
SOLFA_SONGS = [
    ("CIRANDA", -5, "Ciranda Cirandinha",
     "do fa fa la la DO DO / sib la sol DO la sol fa / la DO sib la sol fa mi do / sib sol la fa sol mi fa"),
    ("ATIREI O PAU", 0, "Atirei o Pau no Gato",
     "sol fa mi re mi fa sol sol sol / la sol fa fa fa / sol fa mi mi mi / do do la la la / si la sol sol sol / mi fa sol mi fa sol fa mi re do / DO"),
    ("MARCHA SOLDADO", 0, "Marcha Soldado",
     "sol sol mi do do / mi sol sol sol mi re / mi fa fa fa re sol sol / la sol fa mi re do / do mi sol sol mi do do / do mi sol sol sol mi re / mi fa# fa# fa# fa# re re sol sol / sol la sol fa mi re do"),
    ("CAI CAI BALÃO", 0, "Cai Cai Balão",
     "sol sol fa mi sol sol fa mi / sol la sol fa mi re / re mi fa re mi fa re mi fa / sol la sol fa mi re do"),
    ("ESCRAVOS DE JÓ", 0, "Escravos de Jó",
     "sol DO si la sol la sol la sol fa mi / sol mi sol mi sol mi sol do mi mi re do / sol la sol mi sol la sol mi sol la sol la si DO / sol la sol mi sol la sol mi sol la sol la si DO"),
    ("PEIXE VIVO", 0, "Peixe Vivo",
     "mi sol sol fa fa la la sol / mi sol sol fa re fa fa mi / mi sol sol fa fa la la sol / mi sol sol fa re fa fa mi / DO DO la si DO si la sol / DO DO la si DO si la sol / mi sol sol fa fa la la sol / mi sol sol fa re fa fa mi / mi sol sol fa fa la la sol / mi sol sol fa re mi do do"),
    ("BORBOLETINHA", 0, "Borboletinha",
     "sol la sol DO DO / sol la sol si si / sol la la sol sol si si / sol la si DO DO / sol la sol DO / sol la sol si / sol la sol si si / sol sol la la si si DO"),
    ("CRAVO E ROSA", 0, "O Cravo Brigou com a Rosa",
     "sol sol mi DO si la sol fa / la la fa DO si la sol / sol DO DO DO RE DO si la / la sol si sol fa re do"),
    ("PIRULITO", 0, "Pirulito Que Bate Bate",
     "mi fa sol sol sol fa mi la la / re mi fa fa fa mi re sol / mi sol sol sol fa mi la DO / si la sol fa mi re do"),
    ("A CANOA VIROU", 0, "A Canoa Virou (Se Eu Fosse um Peixinho)",
     "do la la la sol fa / fa fa fa mi fa sol / fa fa la DO DO DO DO la / fa sol sol fa sol la / do la la la sol fa / fa fa fa mi fa sol / fa fa la DO DO DO DO la / fa sol sol fa sol la"),
    ("O SAPO", 0, "O Sapo Não Lava o Pé",
     "sol DO DO sol la sol mi / sol DO DO sol la sol fa / sol la sol si si sol la sol / si si sol la sol si si / sol la si DO"),
    ("ALECRIM", 0, "Alecrim Dourado",
     "sol fa mi mi re mi sol fa / fa mi fa sol fa fa mi fa sol mi / DO DO DO la la la si la sol / sol sol la sol fa fa la sol fa mi"),
    ("MEU LIMÃO", 0, "Meu Limão, Meu Limoeiro",
     "mi fa sol mi la la sol mi / la sol mi mi sol sol fa / re mi fa re sol sol fa / re mi fa re fa fa mi"),
    ("TEREZINHA", 0, "Terezinha de Jesus",
     "sol si mi mi sol si mi / si si DO si la sol# la / la si RE DO DO si la DO si / si DO si la sol fa# mi / sol si mi mi sol si mi / si si DO si la sol# la / la si RE DO DO si la DO si / si DO si la sol fa# mi / sol si mi mi sol si mi / si si DO si la sol# la / la si RE DO DO si la DO si / si DO si la sol fa# mi"),
    ("BOI BOI BOI", -7, "Boi da Cara Preta",
     "sol sol sol / DO si la sol la la / re re fa# sol la la / la DO si la sol fa# sol sol"),
]
SONGS = [
    # known everywhere (from the English list)
    ("BRILHA BRILHA", "C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4 G4 G4 F4 F4 E4 E4 D4 G4 G4 F4 F4 E4 E4 D4 "
                      "C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4"),
    ("PARABÉNS", "G3 G3 A3 G3 C4 B3 G3 G3 A3 G3 D4 C4 G3 G3 G4 E4 C4 B3 A3 F4 F4 E4 C4 D4 C4"),
    ("ODE À ALEGRIA", "E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4 E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 D4 C4 C4"),
    ("BATE O SINO", "E4 E4 E4 E4 E4 E4 E4 G4 C4 D4 E4 F4 F4 F4 F4 F4 E4 E4 E4 E4 G4 G4 F4 D4 C4"),
    ("NOITE FELIZ", "G4 A4 G4 E4 G4 A4 G4 E4 D5 D5 B4 C5 C5 G4 A4 A4 C5 B4 A4 G4 A4 G4 E4 A4 A4 C5 B4 A4 G4 A4 G4 E4 "
                    "D5 D5 F5 D5 B4 C5 E5 C5 G4 E4 G4 F4 D4 C4"),
]

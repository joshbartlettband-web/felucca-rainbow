# Rainbow mode in Japanese: what the screen says, the friends' and hats' names, and FOLLOW's songs. Same rules as pt.py.
# Written as a picture book for small children writes it: hiragana, katakana for words from other languages, no kanji,
# a space between words (so a long name can go on two lines). SCRIPT = "kana": 7 px letters on an 8 px step, from
# tools/fonts/misaki_kana.bdf, so a line holds fewer of them (9 in the band, 13 on a card).
SCRIPT = "kana"
DOREMI = True                          # the note names start as ド レ ミ (HOME held 1 s, then KNOB 2: C D E)

SUBS = {'{"DO", "DO#", "RE", "RE#", "MI", "FA", "FA#", "SOL", "SOL#", "LA", "LA#", "SI"}':
        '{"ド", "ド#", "レ", "レ#", "ミ", "ファ", "ファ#", "ソ", "ソ#", "ラ", "ラ#", "シ"}'}

PAGE = {   # its page on the site (web/make_lang_page.py)
    'lang': 'ja',
    'sep': '、',
    'title': 'Rainbow mode 日本語版',
    'lede': '小さな手のための音楽のおもちゃ、日本語版です。M-VAVE FM-1 シンセサイザーを、小さな子どもでも遊べるものに変える無料のファームウェアです。',
    'try': 'ブラウザで試す',
    'install': 'FM-1 に入れる',
    'note': 'FM-1 がなくても、画面の鍵盤やパソコンのキーボードで遊べます。インストーラーとブラウザ版のページはまだ英語ですが、おもちゃは日本語を話します。',
    'inside': '中身',
    'facts': ['画面の文字はすべて、ひらがなとカタカナです。音の名前はドレミで、鍵盤ごとに大きく、色つきで出ます。', '94 人のともだちには、それぞれ絵と音と空と好きなリズムがあって、名前も日本語です。ユニコーン、ゆきだるま、たつのおとしご。', 'まねっこモードでは、次に弾く鍵盤が光ります。曲は 22 曲。きらきらぼし、ちょうちょう、あかとんぼ、ゆうやけこやけ、かごめかごめ、とおりゃんせなど。', '大人の方へ：HOME を 1 秒押してから OCT- か OCT+ で音量、KNOB 1 を左に回すと五線譜を隠せます。HOME と SAVE を 3 秒いっしょに押すと Felucca シンセに戻ります。'],
    'songs': '曲',
    'source': 'どの曲の音も、Wikipedia の記事にある楽譜から一音ずつ写しています。文字は Num Kadoma さんの美咲フォントです。',
    'footer': '無料のオープンソース（GPL-3.0）です。Leo Kuroshita さんと Hügelton Instruments の Felucca をもとに作っています。ファンのプロジェクトで、M-VAVE が作ったものでも、推奨しているものでもありません。',
}

WORDS = {
    # ALGORITHM
    "1 FRIEND": "1 ともだち", "3 FRIENDS": "3 ともだち", "STRUM": "ハープ", "ACCORDION": "アコーディオン",
    "GUESS": "あてっこ", "FOLLOW": "まねっこ", "CHORDS": "わおん", "COPY ME": "まねして",
    # the cards (ALGORITHM turned): up to 3 lines of 13
    "EVERY KEY PLAYS\\nONE NOTE\\nTRY THE KNOBS TOO": "けんばんを おすと\\nおとが でるよ\\nつまみも まわしてね",
    "EVERY KEY PLAYS\\nA BIG CHORD\\nFIND MAGIC ONES": "けんばん ひとつで\\nわおんが なるよ\\nまほうを さがそう",
    "BLACK KEY CHORDS\\nSWEEP THE WHITE\\nKEYS TO STRUM": "くろで わおんを\\nえらんで しろを\\nなでてね",
    "HOLD A BLACK KEY\\nPLAY A TUNE ON\\nTHE WHITE KEYS": "くろを おさえて\\nしろで メロディー\\nを ひこう",
    "A FRIEND SINGS\\nFIND THE NOTE\\nPLAY HEARS AGAIN": "ともだちが うたう\\nおとを さがそう\\nPLAY もういちど",
    "PLAY THE KEY\\nTHAT LIGHTS UP\\nSEQ PICKS A SONG": "ひかった けんばん\\nを おしてね\\nSEQ で うたを",
    "HOLD ALL THE KEYS\\nTHAT LIGHT UP\\nSEQ PICKS LESSONS": "ひかった けんばん\\nを ぜんぶ おさえて\\nSEQ で つぎ",
    "LISTEN TO THE\\nFRIEND\\nTHEN PLAY IT BACK": "よく きいて\\nおなじに ひこう",
    # the top row's tricks
    "HICCUP": "しゃっくり", "BACKWARDS": "さかさま", "SLEEPY": "ねむねむ", "SQUEAKY": "ちゅうちゅう",
    "GIANT": "きょじん", "FREEZE": "ストップ",
    # the knobs
    "BIG": "おおきい", "SMALL": "ちいさい", "DAY": "ひる", "SUNSET": "ゆうがた", "NIGHT": "よる", "ECHO": "エコー",
    "WIGGLE": "ゆらゆら", "SLOW": "ゆっくり", "WALK": "てくてく", "FAST": "はやい", "MEDIUM": "ふつう",
    # the beats
    "DANCE": "ダンス", "MARCH": "こうしん", "SPOOKY": "おばけ", "TRAIN": "きしゃ", "LULLABY": "こもりうた",
    "HOEDOWN": "カントリー", "POLKA": "ポルカ", "NO BEAT": "リズムなし",
    # games, secrets, the grown-ups' settings
    "YES!": "せいかい!", "TRY AGAIN": "もういちど", "LISTEN": "きいてね", "YOUR TURN": "どうぞ", "YAY!": "やったー!",
    "STAR!": "ほし!", "NEW HAT!": "あたらしい ぼうし!", "NEW FRIEND!": "あたらしい ともだち!", "NEW SKY!": "あたらしい そら!",
    "NEW SONG": "あたらしい うた", "NO HAT": "ぼうし なし", "STARS": "ほし", "STAFF ON": "ごせんふ あり",
    "STAFF OFF": "ごせんふ なし", "LOOK-ALIKES ON": "そっくり あり", "LOOK-ALIKES OFF": "そっくり なし",
    "HI!": "こんにちは", "HI": "やあ", "YOUR NAME": "おなまえ", "PRESETS  LETTER": "PRESETS  もじ",
    "ALGORITHM  NEXT": "ALGORITHM  つぎ", "SAVE  KEEP IT": "SAVE  きめる", "HOME  LEAVE IT": "HOME  やめる",
    "SPARKLE": "キラキラ", "SPARKLE TUNE": "キラキラ メロディー", "SPARKLE ALL": "キラキラ ぜんぶ", "WRITE": "さっきょく",
    "DO RE MI": "ドレミ",
    # chords and lessons
    "MAJOR": "メジャー", "MINOR": "マイナー", "SEVEN": "セブンス", "NINE": "ナインス",
    "C_MAJOR=": "C_メジャー=", "F_MAJOR=": "F_メジャー=", "G_MAJOR=": "G_メジャー=", "A_MINOR=": "A_マイナー=",
    "G_SEVEN=": "G_セブンス=", "FIRST CHORDS": "はじめて", "POP FOUR": "ポップ", "SEVENTHS": "セブンス",
    # the drums' names
    "KICK": "キック", "SNARE": "こだいこ", "CLAP": "はくしゅ", "HI-HAT": "ハイハット", "OPEN HAT": "オープン",
    "RIM": "リム", "COWBELL": "かね", "CYMBAL": "シンバル",
}

NAMES = {   # the friends (and the look-alikes' stand-ins): one line of 9, or two words of 9 and 15 in all
    "DUCKY": "あひる", "PINK DUCKY": "ピンクの あひる", "COOL DUCKY": "クールな あひる", "AXOLOTL": "ウーパールーパー",
    "UNICORN": "ユニコーン", "GIRAFFE": "きりん", "GOO": "ドロドロ", "GOOBERT": "ぐーばーと", "BLUE PUP": "あおい こいぬ",
    "RED MONSTER": "あかい かいじゅう", "BLUE MONSTER": "あおい かいじゅう", "APRIL": "エイプリル", "SCISSORS": "はさみ",
    "GHOST": "おばけ", "WEB HERO": "クモの ヒーロー", "BUTTERFLY": "ちょうちょ", "KITTY": "こねこ", "FROG": "かえる",
    "ROBOT": "ロボット", "RAINBOW": "にじ", "PRINCESS DUCKY": "おひめさま あひる", "RED PUP": "あかい こいぬ",
    "YELLOW BIRD": "きいろい とり", "SLIMY": "ヌルヌル", "BUNNY": "うさぎ", "PANDA": "パンダ", "PENGUIN": "ペンギン",
    "OWL": "ふくろう", "BEE": "みつばち", "LADYBUG": "てんとうむし", "DINO": "きょうりゅう", "WHALE": "くじら",
    "OCTOPUS": "たこ", "FISH": "さかな", "TURTLE": "かめ", "ICE CREAM": "アイス", "CUPCAKE": "カップケーキ",
    "ROCKET": "ロケット", "STRAWBERRY": "いちご", "STAR": "ほし", "T-REX": "ティラノ", "SKELETON": "がいこつ",
    "RANCHER": "ぼくじょう", "RODEO": "カウボーイ", "VACUUM": "そうじき", "SPACE HERO": "うちゅう ヒーロー",
    "BEAT BOT": "リズム ロボ", "TOY DRUM": "たいこ", "BONGO": "ボンゴ", "MONKEY": "さる", "ELEPHANT": "ぞう",
    "RACE CAR": "レースカー", "JELLYFISH": "くらげ", "BEAR": "くま", "SNOWMAN": "ゆきだるま", "CRAB": "かに",
    "WOLF": "おおかみ", "CAMEL": "らくだ", "SCIENTIST": "はかせ", "FLYTRAP": "ハエトリソウ", "SUNFLOWER": "ひまわり",
    "SPIDER MOM": "クモの ママ", "DRAGON DUCK": "ドラゴン あひる", "SPIDER GRANDMA": "クモの おばあちゃん",
    "NIGHT LIGHT": "ほたる", "GREEN QUEEN": "みどりの じょおう", "KING AXOLOTL": "ウーパー おうさま",
    "FAIRY MONSTER": "ようせい かいじゅう", "MORNING GLORY": "あさがお", "GROUCH": "ぷんぷん", "TIGER CUB": "とらの こ",
    "RACCOON": "あらいぐま", "GOLDENROD": "きんいろの はな", "PIANO PAL": "ピアノ", "FLUTE BIRD": "ふえの とり",
    "SAX CAT": "サックス ねこ", "COW": "うし", "PIG": "ぶた", "SHEEP": "ひつじ", "SHARK": "さめ",
    "SEAHORSE": "たつのおとしご", "STARFISH": "ひとで", "SNAIL": "かたつむり", "CATERPILLAR": "いもむし",
    "FIREFLY": "ほたる", "TRICERATOPS": "トリケラ", "STEGOSAURUS": "ステゴ", "PIZZA": "ピザ", "DONUT": "ドーナツ",
    "BANANA": "バナナ", "TRAIN": "きしゃ", "FIRE TRUCK": "しょうぼうしゃ", "SCHOOL BUS": "バス", "HELICOPTER": "ヘリコプター",
    "GOLD DUCKY": "きんの あひる",
    "SPOTTY PUP": "ぶちの こいぬ", "FOX": "きつね", "FUZZY": "もこもこ", "BIG BLUE": "おおきな あお", "SPIDER": "クモ",
    "PUMPKIN": "かぼちゃ", "CHICK": "ひよこ", "BAT": "こうもり", "HORSE": "うま", "CACTUS": "サボテン",
    "ALIEN": "うちゅうじん", "RAINBOW MOM": "にじの ママ", "GREEN GRANNY": "みどりの おばあちゃん", "PIXIE": "ようせい",
    "ALLEY CAT": "のらねこ", "LION CUB": "ライオンの こ", "SQUIRREL": "りす",
}

HATS = {"PARTY": "パーティー", "CROWN": "おうかん", "TOP HAT": "シルクハット", "BUCKET": "ぼうし", "WIZARD": "まほうつかい",
        "BEANIE": "ニット", "WESTERN": "カウボーイ", "CHEF": "コック", "PROPELLER": "プロペラ", "FLOWERS": "おはな",
        "STAR": "ほし"}

# FOLLOW's songs: Japanese children's songs, each taken note for note from the score in a Wikipedia article (named
# above it, tools/wiki_song.py), moved where it says to fit the keys at OCT 0 (F3 .. G5) with the fewest black keys; all
# traditional or out of copyright (the newest, Yamada Kosaku's, since 2016). Then a few known everywhere.
SOLFA_SONGS = []
SONGS = [
    # きらきら星 (probe_ja.wikipedia.org, its score)
    ("きらきらぼし", "C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4 G4 G4 F4 F4 E4 E4 D4 G4 G4 F4 F4 E4 E4 D4 C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4"),
    # Hänschen klein (ちょうちょう) (de.wikipedia.org, its score, moved +2)
    ("ちょうちょう", "D5 B4 B4 C5 A4 A4 G4 A4 B4 C5 D5 D5 D5 D5 B4 B4 C5 A4 A4 G4 B4 D5 D5 G4 A4 A4 A4 A4 A4 B4 C5 B4 B4 B4 B4 B4 C5 D5 D5 B4 B4 C5 A4 A4 G4 B4 D5 D5 G4"),
    # ぶんぶんぶん (probe_ja.wikipedia.org, its score)
    ("ぶんぶんぶん", "D5 C5 B4 A4 B4 C5 A4 G4 B4 C5 D5 B4 A4 B4 C5 A4 B4 C5 D5 B4 A4 B4 C5 A4 D5 C5 B4 A4 B4 C5 A4 G4"),
    # Kuckuck, Kuckuck, ruft's aus dem Wald (かっこう) (de.wikipedia.org, its score)
    ("かっこう", "D5 B4 D5 B4 A4 G4 A4 G4 A4 A4 B4 C5 A4 B4 B4 C5 D5 B4 D5 B4 D5 B4 C5 B4 A4 G4"),
    # むすんでひらいて (probe_ja.wikipedia.org, its score)
    ("むすんで ひらいて", "E4 E4 D4 C4 C4 D4 D4 E4 D4 C4 G4 G4 F4 E4 E4 D4 C4 D4 E4 C4 E4 E4 F4 G4 G4 A4 A4 G4 F4 E4 E4 E4 F4 G4 G4 A4 A4 G4 E4 E4 D4 C4 C4 D4 D4 E4 D4 C4 G4 G4 F4 E4 E4 D4 C4 D4 E4 C4"),
    # メリーさんのひつじ (probe_ja.wikipedia.org, its score)
    ("メリーさん", "E4 D4 C4 D4 E4 E4 E4 D4 D4 D4 E4 G4 G4 E4 D4 C4 D4 E4 E4 E4 D4 D4 E4 D4 C4"),
    # 大きな栗の木の下で (probe_ja.wikipedia.org, its score)
    ("おおきな くりのき", "C4 C4 D4 E4 E4 G4 E4 E4 D4 D4 C4 E4 E4 F4 G4 C5 A4 C5 G4 C5 C5 B4 G4 A4 A4 A4 A4 G4 C4 C4 D4 E4 E4 G4 E4 E4 D4 D4 C4"),
    # 春が来た (岡野貞一) (probe_ja.wikipedia.org, its score)
    ("はるが きた", "G4 E4 F4 G4 A4 G4 E4 F4 G4 C5 A4 G4 E4 C4 D4 G4 A4 G4 E4 G4 C5 D5 C5 A4 C5 G4 E5 D5 G4 C5"),
    # かたつむり (童謡) (probe_ja.wikipedia.org, its score)
    ("かたつむり", "G4 G4 G4 E4 C4 C4 C4 D4 E4 E4 D4 C4 D4 E4 F4 G4 A4 G4 G4 G4 E4 D4 D4 C4 D4 E4 G4 C5 C5 G4 E4 G4 G4 E4 C4 E4 E4 D4 C4"),
    # 通りゃんせ (probe_ja.wikipedia.org, its score, moved -5)
    ("とおりゃんせ", "E4 E4 D4 E4 E4 D4 B3 F4 F4 F4 A4 F4 E4 F4 E4 D4 D4 E4 F4 F4 A4 F4 E4 F4 E4 D4 D4 E4 C4 C4 E4 C4 B3 C4 B3 A3 A3 B3 C4 C4 C4 E4 E4 C4 B3 C4 B3 A3 A3 B3 F4 F4 F4 F4 A4 A4 F4 E4 F4 E4 D4 D4 E4 C4 C4 C4 C4 C4 E4 C4 B3 C4 B3 A3 A3 B3 E4 E4 E4 E4 E4 E4 D4 E4 E4 E4 D4 A3 A3 B3 A3 B3 C4 D4 E4 F4 E4 F4 A4 B4 A4 F4 E4 E4 D4 E4"),
    # 江戸子守唄 (probe_ja.wikipedia.org, its score)
    ("こもりうた", "F4 F4 F4 E4 F4 A4 F4 E4 C4 E4 F4 A4 F4 A4 E4 A3 A3 B3 A3 B3 C4 E4 F4 E4 A3 B3 C4 A3 B3"),
    # 七つの子 (本居長世) (probe_ja.wikipedia.org, its score)
    ("ななつのこ", "B4 A4 G4 A4 B4 G4 E4 G4 D4 E4 D4 B3 D4 E4 G4 A4 B4 C5 D5 B4 D5 E5 D5 B4 G4 A4 A4 B4 G4 E4 D4 G4 A4 A4 A4 A4 A4 A4 B4 C5 B4 A4 A4 A4 B4 E4 D4 D4 D4 G4 G4 G4 A4 B4 C5 E4 G4 A4 B4 A4 G4 A4 B4 G4 E4 G4 D4 E4 D4 B3 D4 E4 G4 A4 B4 C5 D5 B4 D5 E5 D5 B4 G4 A4 B4 G4 E4 D4 G4"),
    # 赤とんぼ (山田耕筰) (probe_ja.wikipedia.org, its score)
    ("あかとんぼ", "C4 F4 F4 G4 A4 C5 F5 D5 C5 D5 F4 F4 G4 A4 A4 D5 C5 D5 F5 D5 C5 D5 C5 A4 C5 A4 F4 A4 G4 F4 F4"),
    # 雪 (童謡) (probe_ja.wikipedia.org, its score, moved +2)
    ("ゆき", "D5 E5 D5 E5 D5 B4 B4 C5 B4 C5 B4 G4 B4 G4 A4 B4 G4 A4 B4 C5 D5 D5 A4 B4 A4 D5 E5 D5 E5 D5 D5 B4 B4 B4 C5 B4 C5 B4 B4 G4 E5 D5 B4 D5 D5 B4 G4 B4 B4 A4 A4 G4"),
    # 夕焼小焼 (草川信) (probe_ja.wikipedia.org, its score)
    ("ゆうやけ こやけ", "G4 G4 A4 G4 G4 G4 E4 C4 C4 D4 E4 D4 E4 E4 G4 A4 C5 C5 A4 G4 G4 A4 G4 C5 C5 D5 C5 A4 C5 C5 G4 G4 A4 G4 A4 G4 E4 G4 E4 D4 C4 D4 D4 C4 D4 E4 G4 A4 G4 C5"),
    # ずいずいずっころばし (probe_ja.wikipedia.org, its score, moved +5)
    ("ずいずい", "D5 E5 F5 F5 E5 E5 E5 D5 D5 D5 E5 F5 F5 E5 D5 D5 AS4 A4 D5 D5 E5 E5 A4 F5 E5 D5 D5 E5 D5 E5 D5 B4 B4 B4 E5 E5 E5 E5 E5 E5 FS5 FS5 E5 E5 D5 D5 E5 E5 D5 E5 D5 E5 D5 E5 D5 D5 D5 D5 D5 D5 D5 E5 D5 D5 D5 D5 D5 D5 D5 E5 F5 F5 E5 F5 E5 D5 E5 E5 D5 D5 D5 D5 D5 D5 D5 E5 D5 D5 D5 D5 D5 D5 E5 D5 E5"),
    # かごめかごめ (probe_ja.wikipedia.org, its score)
    ("かごめ かごめ", "A4 A4 B4 A4 A4 A4 A4 A4 A4 A4 G4 G4 A4 A4 G4 E4 A4 G4 A4 G4 A4 A4 G4 E4 A4 A4 A4 B4 A4 A4 A4 A4 G4 G4 A4 G4 G4 A4 A4 G4 E4 A4 A4 A4 A4 A4 B4 A4 G4 A4"),
    # あめふり (中山晋平) (probe_ja.wikipedia.org, its score)
    ("あめふり", "C4 C4 C4 D4 E4 D4 G4 E4 C5 A4 G4 E4 G4 C4 C4 C4 D4 E4 G4 A4 A4 E4 E4 E4 D4 C4 C5 A4 C5 A4 G4 E4 G4 E4 G4 C5 C5"),
    ("たんじょうび", "G3 G3 A3 G3 C4 B3 G3 G3 A3 G3 D4 C4 G3 G3 G4 E4 C4 B3 A3 F4 F4 E4 C4 D4 C4"),   # known everywhere (as kid.c's English list)
    ("よろこびの うた", "E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4 E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 D4 C4 C4"),   # known everywhere (as kid.c's English list)
    ("ジングルベル", "E4 E4 E4 E4 E4 E4 E4 G4 C4 D4 E4 F4 F4 F4 F4 F4 E4 E4 E4 E4 G4 G4 F4 D4 C4"),   # known everywhere (as kid.c's English list)
    # Stille Nacht, heilige Nacht (きよしこの夜) (de.wikipedia.org, its score, moved -2)
    ("きよしこのよる", "G4 A4 G4 E4 G4 A4 G4 E4 D5 CS5 D5 B4 C5 B4 C5 G4 A4 A4 C5 B4 A4 G4 A4 G4 E4 A4 A4 C5 B4 A4 G4 A4 G4 E4 B4 B4 B4 D5 C5 B4 C5 E5 C5 G4 E4 G4 F4 D4 C4"),
]

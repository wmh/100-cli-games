"""
Game 009: Wordle
Guess the 5-letter word in 6 attempts with color-coded feedback.
"""

import curses
import random

# Common 5-letter words for the game
WORD_LIST = [
    "ABOUT", "ABOVE", "ABUSE", "ACTOR", "ACUTE", "ADMIT", "ADOPT", "ADULT", "AFTER", "AGAIN",
    "AGENT", "AGREE", "AHEAD", "ALARM", "ALBUM", "ALERT", "ALIEN", "ALIGN", "ALIKE", "ALIVE",
    "ALLOW", "ALONE", "ALONG", "ALTER", "ANGEL", "ANGER", "ANGLE", "ANGRY", "APART", "APPLE",
    "APPLY", "ARENA", "ARGUE", "ARISE", "ARRAY", "ASIDE", "ASSET", "AUDIO", "AVOID", "AWAKE",
    "AWARD", "AWARE", "BADLY", "BAKER", "BASIC", "BEACH", "BEGAN", "BEGIN", "BEING", "BELOW",
    "BENCH", "BILLY", "BIRTH", "BLACK", "BLAME", "BLIND", "BLOCK", "BLOOD", "BOARD", "BOOST",
    "BOOTH", "BOUND", "BRAIN", "BRAND", "BREAD", "BREAK", "BREED", "BRIEF", "BRING", "BROAD",
    "BROKE", "BROWN", "BUILD", "BUILT", "BUYER", "CABLE", "CALIF", "CARRY", "CATCH", "CAUSE",
    "CHAIN", "CHAIR", "CHART", "CHASE", "CHEAP", "CHECK", "CHEST", "CHIEF", "CHILD", "CHINA",
    "CHOSE", "CIVIC", "CIVIL", "CLAIM", "CLASS", "CLEAN", "CLEAR", "CLICK", "CLOCK", "CLOSE",
    "COACH", "COAST", "COULD", "COUNT", "COURT", "COVER", "CRAFT", "CRASH", "CRAZY", "CREAM",
    "CRIME", "CROSS", "CROWD", "CROWN", "CRUDE", "CURVE", "CYCLE", "DAILY", "DANCE", "DATED",
    "DEALT", "DEATH", "DEBUT", "DELAY", "DEPTH", "DOING", "DOUBT", "DOZEN", "DRAFT", "DRAMA",
    "DRANK", "DRAWN", "DREAM", "DRESS", "DRILL", "DRINK", "DRIVE", "DROVE", "DYING", "EAGER",
    "EARLY", "EARTH", "EIGHT", "ELITE", "EMPTY", "ENEMY", "ENJOY", "ENTER", "ENTRY", "EQUAL",
    "ERROR", "EVENT", "EVERY", "EXACT", "EXIST", "EXTRA", "FAITH", "FALSE", "FAULT", "FIBER",
    "FIELD", "FIFTH", "FIFTY", "FIGHT", "FINAL", "FIRST", "FIXED", "FLASH", "FLEET", "FLOOR",
    "FLUID", "FOCUS", "FORCE", "FORTH", "FORTY", "FORUM", "FOUND", "FRAME", "FRANK", "FRAUD",
    "FRESH", "FRONT", "FRUIT", "FULLY", "FUNNY", "GIANT", "GIVEN", "GLASS", "GLOBE", "GOING",
    "GRACE", "GRADE", "GRAND", "GRANT", "GRASS", "GREAT", "GREEN", "GROSS", "GROUP", "GROWN",
    "GUARD", "GUESS", "GUEST", "GUIDE", "HAPPY", "HARRY", "HEART", "HEAVY", "HENCE", "HENRY",
    "HORSE", "HOTEL", "HOUSE", "HUMAN", "IDEAL", "IMAGE", "INDEX", "INNER", "INPUT", "ISSUE",
    "JAPAN", "JIMMY", "JOINT", "JONES", "JUDGE", "KNOWN", "LABEL", "LARGE", "LASER", "LATER",
    "LAUGH", "LAYER", "LEARN", "LEASE", "LEAST", "LEAVE", "LEGAL", "LEMON", "LEVEL", "LEWIS",
    "LIGHT", "LIMIT", "LINKS", "LIVED", "LIVES", "LOCAL", "LOGIC", "LOOSE", "LOWER", "LUCKY",
    "LUNCH", "LYING", "MAGIC", "MAJOR", "MAKER", "MARCH", "MARIA", "MATCH", "MAYBE", "MAYOR",
    "MEANT", "MEDIA", "METAL", "MIGHT", "MINOR", "MINUS", "MIXED", "MODEL", "MONEY", "MONTH",
    "MORAL", "MOTOR", "MOUNT", "MOUSE", "MOUTH", "MOVED", "MOVIE", "MUSIC", "NEEDS", "NEVER",
    "NEWLY", "NIGHT", "NOISE", "NORTH", "NOTED", "NOVEL", "NURSE", "OCCUR", "OCEAN", "OFFER",
    "OFTEN", "ORDER", "OTHER", "OUGHT", "PAINT", "PANEL", "PAPER", "PARTY", "PEACE", "PETER",
    "PHASE", "PHONE", "PHOTO", "PIECE", "PILOT", "PITCH", "PLACE", "PLAIN", "PLANE", "PLANT",
    "PLATE", "POINT", "POUND", "POWER", "PRESS", "PRICE", "PRIDE", "PRIME", "PRINT", "PRIOR",
    "PRIZE", "PROOF", "PROUD", "PROVE", "QUEEN", "QUICK", "QUIET", "QUITE", "RADIO", "RAISE",
    "RANGE", "RAPID", "RATIO", "REACH", "READY", "REFER", "RIGHT", "RIVAL", "RIVER", "ROBIN",
    "ROCKY", "ROMAN", "ROUGH", "ROUND", "ROUTE", "ROYAL", "RURAL", "SCALE", "SCENE", "SCOPE",
    "SCORE", "SENSE", "SERVE", "SEVEN", "SHALL", "SHAPE", "SHARE", "SHARP", "SHEET", "SHELF",
    "SHELL", "SHIFT", "SHINE", "SHIRT", "SHOCK", "SHOOT", "SHORT", "SHOWN", "SIGHT", "SINCE",
    "SIXTH", "SIXTY", "SIZED", "SKILL", "SLEEP", "SLIDE", "SMALL", "SMART", "SMILE", "SMITH",
    "SMOKE", "SOLID", "SOLVE", "SORRY", "SOUND", "SOUTH", "SPACE", "SPARE", "SPEAK", "SPEED",
    "SPEND", "SPENT", "SPLIT", "SPOKE", "SPORT", "STAFF", "STAGE", "STAKE", "STAND", "START",
    "STATE", "STEAM", "STEEL", "STICK", "STILL", "STOCK", "STONE", "STOOD", "STORE", "STORM",
    "STORY", "STRIP", "STUCK", "STUDY", "STUFF", "STYLE", "SUGAR", "SUITE", "SUPER", "SWEET",
    "TABLE", "TAKEN", "TASTE", "TAXES", "TEACH", "TEETH", "TEXAS", "THANK", "THEFT", "THEIR",
    "THEME", "THERE", "THESE", "THICK", "THING", "THINK", "THIRD", "THOSE", "THREE", "THREW",
    "THROW", "TIGHT", "TIMES", "TITLE", "TODAY", "TOPIC", "TOTAL", "TOUCH", "TOUGH", "TOWER",
    "TRACK", "TRADE", "TRAIN", "TREAT", "TREND", "TRIAL", "TRIBE", "TRICK", "TRIED", "TRIES",
    "TROOP", "TRUCK", "TRULY", "TRUNK", "TRUST", "TRUTH", "TWICE", "UNDER", "UNDUE", "UNION",
    "UNITY", "UNTIL", "UPPER", "UPSET", "URBAN", "USAGE", "USUAL", "VALID", "VALUE", "VIDEO",
    "VIRUS", "VISIT", "VITAL", "VOCAL", "VOICE", "WASTE", "WATCH", "WATER", "WHEEL", "WHERE",
    "WHICH", "WHILE", "WHITE", "WHOLE", "WHOSE", "WOMAN", "WOMEN", "WORLD", "WORRY", "WORSE",
    "WORST", "WORTH", "WOULD", "WOUND", "WRITE", "WRONG", "WROTE", "YOUNG", "YOUTH",
    "ABACK", "ABASE", "ABATE", "ABBEY", "ABBOT", "ABHOR", "ABIDE", "ABLED", "ABODE", "ABORT",
    "ABOVE", "ABUSE", "ABYSS", "ACHED", "ACIDS", "ACING", "ACRES", "ACTED", "ACTOR", "ACUTE",
    "ADAGE", "ADAPT", "ADDED", "ADDER", "ADEPT", "ADMIN", "ADMIT", "ADOBE", "ADOPT", "ADORE",
    "ADORN", "ADULT", "AEGIS", "AFIRE", "AFOOT", "AFOUL", "AFTER", "AGAIN", "AGENT", "AGILE",
    "AGING", "AGLOW", "AGONY", "AGREE", "AHEAD", "AIDED", "AIDER", "AIMED", "AIRER", "AISLE",
    "ALARM", "ALBUM", "ALERT", "ALGAE", "ALIBI", "ALIEN", "ALIGN", "ALIKE", "ALIVE", "ALLAY",
    "ALLEY", "ALLOT", "ALLOW", "ALLOY", "ALOFT", "ALONE", "ALONG", "ALOOF", "ALOUD", "ALPHA",
    "ALTAR", "ALTER", "AMBER", "AMBLE", "AMEND", "AMIGO", "AMISS", "AMONG", "AMPLE", "AMPLY",
    "AMUSE", "ANGEL", "ANGER", "ANGLE", "ANGRY", "ANGST", "ANKLE", "ANNEX", "ANNOY", "ANNUL",
    "ANTIC", "ANVIL", "AORTA", "APART", "APHID", "APPLE", "APPLY", "APRON", "ARBOR", "ARDOR",
    "ARENA", "ARGUE", "ARISE", "ARMOR", "AROMA", "AROSE", "ARRAY", "ARROW", "ARSON", "ARTSY",
    "ASHEN", "ASHES", "ASIDE", "ASKED", "ASPEN", "ASSAY", "ASSET", "ATOLL", "ATONE", "ATTIC",
    "AUDIO", "AUDIT", "AUGUR", "AUNTY", "AVAIL", "AVERT", "AVOID", "AWAIT", "AWAKE", "AWARD",
    "AWARE", "AWASH", "AWFUL", "AWOKE", "AXIAL", "AXIOM", "AZURE", "BADGE", "BADLY", "BAGEL",
    "BALMY", "BANAL", "BANJO", "BARGE", "BARON", "BASAL", "BASIC", "BASIL", "BASIN", "BATCH",
    "BATHE", "BATON", "BATTY", "BAYOU", "BEACH", "BEARD", "BEAST", "BEGAN", "BEGIN", "BEGUN",
    "BEING", "BELCH", "BELLE", "BELLY", "BELOW", "BENCH", "BERRY", "BERTH", "BESET", "BEVEL",
    "BIDDY", "BIGHT", "BIJOU", "BIKINI", "BILLY", "BINGE", "BINGO", "BIOME", "BIRCH", "BIRTH",
    "BISON", "BLACK", "BLADE", "BLAME", "BLAND", "BLANK", "BLARE", "BLAST", "BLAZE", "BLEAK",
    "BLEAT", "BLEED", "BLEND", "BLESS", "BLIMP", "BLIND", "BLINK", "BLISS", "BLITZ", "BLOAT",
    "BLOCK", "BLOKE", "BLOND", "BLOOD", "BLOOM", "BLOWN", "BLUES", "BLUFF", "BLUNT", "BLURB",
    "BLURT", "BLUSH", "BOARD", "BOAST", "BOGEY", "BOGUS", "BOILS", "BOLTS", "BOMBS", "BONDS",
    "BONED", "BONES", "BONUS", "BOOBY", "BOOKS", "BOOST", "BOOTH", "BOOTS", "BOOZE", "BORAX",
    "BORED", "BOUND", "BOWEL", "BOXER", "BRACE", "BRAID", "BRAIN", "BRAKE", "BRAND", "BRASH",
    "BRASS", "BRAVE", "BRAVO", "BRAWL", "BRAWN", "BREAD", "BREAK", "BREED", "BRIAR", "BRIBE",
    "BRICK", "BRIDE", "BRIEF", "BRINE", "BRING", "BRINK", "BRINY", "BRISK", "BROAD", "BROIL",
    "BROKE", "BROOD", "BROOK", "BROOM", "BROTH", "BROWN", "BRUNT", "BRUSH", "BRUTE", "BUDDY",
    "BUDGE", "BUGGY", "BUILD", "BUILT", "BULGE", "BULKY", "BULLY", "BUNCH", "BUNNY", "BURLY",
    "BURNS", "BURNT", "BURST", "BUSHY", "BUTCH", "BUYER", "BYLAW", "CABIN", "CABLE", "CACHE",
    "CADET", "CADRE", "CAMEL", "CAMEO", "CANAL", "CANDY", "CANNY", "CANOE", "CANON", "CAPER",
    "CARAT", "CARGO", "CAROL", "CARRY", "CARVE", "CASTE", "CATCH", "CATER", "CATTY", "CAUSE",
    "CAVIL", "CEASE", "CEDAR", "CHAIN", "CHAIR", "CHALK", "CHAMP", "CHANT", "CHAOS", "CHARD",
    "CHARM", "CHART", "CHASE", "CHASM", "CHEAP", "CHEAT", "CHECK", "CHEEK", "CHEER", "CHESS",
    "CHEST", "CHICK", "CHIEF", "CHILD", "CHILI", "CHILL", "CHIME", "CHIMP", "CHINA", "CHIRP",
    "CHIVE", "CHOCK", "CHOIR", "CHOKE", "CHORD", "CHORE", "CHOSE", "CHUCK", "CHUMP", "CHUNK",
    "CHURN", "CHUTE", "CIDER", "CIGAR", "CINCH", "CIRCA", "CIVIC", "CIVIL", "CLACK", "CLAIM",
    "CLAMP", "CLANG", "CLANK", "CLASH", "CLASP", "CLASS", "CLEAN", "CLEAR", "CLEAT", "CLEFT",
    "CLERK", "CLICK", "CLIFF", "CLIMB", "CLING", "CLOAK", "CLOCK", "CLONE", "CLOSE", "CLOTH",
    "CLOUD", "CLOUT", "CLOVE", "CLOWN", "CLUBS", "CLUCK", "CLUMP", "CLUNG", "COACH", "COAST",
    "COBRA", "COCOA", "COLON", "COLOR", "COMET", "COMIC", "COMMA", "CONCH", "CORAL", "CORNY",
    "COUCH", "COUGH", "COULD", "COUNT", "COUPE", "COURT", "COVEN", "COVER", "COVET", "COWER",
    "COYLY", "CRACK", "CRAFT", "CRAMP", "CRANE", "CRANK", "CRASH", "CRASS", "CRATE", "CRAVE",
    "CRAWL", "CRAZE", "CRAZY", "CREAK", "CREAM", "CREED", "CREEK", "CREEP", "CREME", "CREPE",
    "CREPT", "CRESS", "CREST", "CRICK", "CRIED", "CRIER", "CRIES", "CRIME", "CRIMP", "CRISP",
    "CROAK", "CROCK", "CRONY", "CROOK", "CROSS", "CROUCH", "CROWD", "CROWN", "CRUDE", "CRUEL",
    "CRUMB", "CRUSH", "CRUST", "CRYPT", "CUBIC", "CUMIN", "CUPID", "CURLY", "CURRY", "CURSE",
    "CURVE", "CURVY", "CUTIE", "CYBER", "CYCLE", "CYNIC", "DADDY", "DAILY", "DAIRY", "DAISY",
    "DALLY", "DANCE", "DANDY", "DATUM", "DAUNT", "DEALT", "DEATH", "DEBAR", "DEBIT", "DEBUG",
    "DEBUT", "DECAF", "DECAY", "DECOR", "DECOY", "DECRY", "DEFER", "DEITY", "DELAY", "DELTA",
    "DELVE", "DEMON", "DEMUR", "DENIM", "DENSE", "DEPOT", "DEPTH", "DERBY", "DETER", "DETOX",
    "DEUCE", "DEVIL", "DIARY", "DICEY", "DIGIT", "DIMLY", "DINER", "DINGO", "DINGY", "DIRTY",
    "DISCO", "DITCH", "DITTO", "DITTY", "DIVAN", "DIVER", "DIZZY", "DODGE", "DODGY", "DOGMA",
    "DOING", "DOLLY", "DONOR", "DONUT", "DOPEY", "DOUBT", "DOUGH", "DOWDY", "DOWEL", "DOWNY",
    "DOWRY", "DOYEN", "DOZEN", "DRAFT", "DRAIN", "DRAKE", "DRAMA", "DRANK", "DRAPE", "DRAWL",
    "DRAWN", "DREAD", "DREAM", "DREARY", "DRECK", "DRESS", "DRIED", "DRIER", "DRIFT", "DRILL",
    "DRINK", "DRIVE", "DROIT", "DROLL", "DRONE", "DROOL", "DROOP", "DROSS", "DROVE", "DROWN",
    "DRUGS", "DRUMS", "DRUNK", "DRYER", "DRYLY", "DUCHY", "DUCKY", "DUELS", "DUET", "DUMMY",
    "DUMPS", "DUMPY", "DUNCE", "DUNES", "DUSKY", "DUSTY", "DUTCH", "DUVET", "DWARF", "DWELL",
    "DWELT", "DYING", "EAGER", "EAGLE", "EARLY", "EARTH", "EASEL", "EATEN", "EATER", "EBONY",
    "ECLAT", "EDICT", "EDIFY", "EERIE", "EGGED", "EGRET", "EIGHT", "EJECT", "EKING", "ELATE",
    "ELBOW", "ELDER", "ELECT", "ELEGY", "ELFIN", "ELIDE", "ELITE", "ELOPE", "ELUDE", "ELVES",
    "EMAIL", "EMBED", "EMBER", "EMCEE", "EMOTE", "EMPTY", "ENACT", "ENDOW", "ENEMA", "ENEMY",
    "ENJOY", "ENNUI", "ENSUE", "ENTER", "ENTRY", "ENVOY", "EPOXY", "EQUAL", "EQUIP", "ERASE",
    "ERECT", "ERODE", "ERROR", "ERUPT", "ESSAY", "ESTER", "ETHER", "ETHIC", "ETHOS", "EVADE",
    "EVICT", "EVOKE", "EXACT", "EXALT", "EXCEL", "EXERT", "EXILE", "EXIST", "EXPAT", "EXTOL",
    "EXULT", "EYING", "FABLE", "FACET", "FAINT", "FAIRY", "FAITH", "FAKER", "FALLS", "FALSE",
    "FANCY", "FANNY", "FARCE", "FATAL", "FATTY", "FAULT", "FAUNA", "FAVOR", "FEAST", "FECAL",
    "FEIGN", "FELLA", "FELON", "FEMME", "FEMUR", "FENCE", "FERAL", "FERRY", "FETAL", "FETCH",
    "FETID", "FETUS", "FEVER", "FEWER", "FIBER", "FICUS", "FIEND", "FIERY", "FIFTH", "FIFTY",
    "FIGHT", "FILCH", "FILER", "FILET", "FILLY", "FILMY", "FILTH", "FINAL", "FINCH", "FINER",
    "FIRED", "FIRMS", "FIRST", "FISHY", "FIXER", "FIZZY", "FJORD", "FLACK", "FLAIL", "FLAIR",
    "FLAKE", "FLAKY", "FLAME", "FLANK", "FLARE", "FLASH", "FLASK", "FLATS", "FLECK", "FLEET",
    "FLESH", "FLICK", "FLIER", "FLING", "FLINT", "FLIRT", "FLOAT", "FLOCK", "FLOOD", "FLOOR",
    "FLORA", "FLOSS", "FLOUR", "FLOUT", "FLOWN", "FLUFF", "FLUID", "FLUKE", "FLUNG", "FLUNK",
    "FLUSH", "FLUTE", "FOAMY", "FOCAL", "FOCUS", "FOGGY", "FOILS", "FOIST", "FOLIO", "FOLKS",
    "FOLLY", "FONTS", "FORAY", "FORCE", "FORGE", "FORGO", "FORMS", "FORTE", "FORTH", "FORTY",
    "FORUM", "FOUND", "FOYER", "FRAIL", "FRAME", "FRANK", "FRAUD", "FREAK", "FREED", "FRESH",
    "FRIAR", "FRIED", "FRILL", "FRISK", "FROCK", "FROGS", "FRONT", "FROST", "FROWN", "FROZE",
    "FRUIT", "FULLY", "FUMED", "FUNDS", "FUNGI", "FUNKY", "FUNNY", "FURRY", "FUSSY", "FUZZY",
    "GAILY", "GAINS", "GAMER", "GAMES", "GAMMA", "GAMUT", "GASSY", "GAUGE", "GAUNT", "GAUZE",
    "GAVEL", "GAWKY", "GAZER", "GEARS", "GECKO", "GEESE", "GENES", "GENIE", "GENRE", "GENUS",
    "GHOST", "GHOUL", "GIANT", "GIDDY", "GIFTS", "GILDS", "GIRLS", "GIRTH", "GIVEN", "GIVER",
    "GIVES", "GIZMO", "GLADE", "GLAND", "GLARE", "GLASS", "GLAZE", "GLEAM", "GLEAN", "GLIDE",
    "GLINT", "GLOAT", "GLOBE", "GLOOM", "GLORY", "GLOSS", "GLOVE", "GLOWS", "GLUEY", "GLYPH",
    "GNARL", "GNASH", "GNOME", "GODLY", "GOING", "GOLLY", "GONNA", "GOODS", "GOOEY", "GOOFY",
    "GOOSE", "GORGE", "GOUGE", "GOURD", "GRACE", "GRADE", "GRAIN", "GRAND", "GRANT", "GRAPH",
    "GRASP", "GRASS", "GRATE", "GRAVE", "GRAVY", "GRAZE", "GREAT", "GREED", "GREEK", "GREEN",
    "GREET", "GRIEF", "GRILL", "GRIME", "GRIMY", "GRIND", "GRIPE", "GROAN", "GROIN", "GROOM",
    "GROPE", "GROSS", "GROUP", "GROVE", "GROWL", "GROWN", "GRUEL", "GRUFF", "GRUNT", "GUARD",
    "GUAVA", "GUESS", "GUEST", "GUIDE", "GUILD", "GUILE", "GUILT", "GUISE", "GULCH", "GULLY",
    "GUMBO", "GUMMY", "GUSTY", "HABIT", "HAIRY", "HALVE", "HANDY", "HAPPY", "HARDY", "HASTE",
    "HASTY", "HATCH", "HATER", "HAUNT", "HAVEN", "HAVOC", "HAZEL", "HEADS", "HEADY", "HEARD",
    "HEART", "HEATH", "HEAVE", "HEAVY", "HEDGE", "HEFTY", "HEIRS", "HEIST", "HELIX", "HELLO",
    "HELPS", "HENCE", "HENRY", "HERON", "HILLY", "HINGE", "HINTS", "HIPPO", "HIPPY", "HITCH",
    "HOARD", "HOARY", "HOBBY", "HOIST", "HOLES", "HOLEY", "HOLLY", "HOMER", "HOMES", "HONEY",
    "HONOR", "HOPED", "HOPES", "HORNY", "HORSE", "HOTEL", "HOTLY", "HOUND", "HOUSE", "HOVEL",
    "HOVER", "HOWDY", "HUFFY", "HUMAN", "HUMID", "HUMOR", "HUMPH", "HUMUS", "HUNCH", "HUNKY",
    "HURRY", "HUSKY", "HUSSY", "HUTCH", "HYDRO", "HYENA", "HYMEN", "HYPER", "ICHOR", "ICING",
    "ICONS", "IDEAL", "IDEAS", "IDIOM", "IDIOT", "IDLER", "IDOLS", "IGLOO", "ILEUM", "IMAGE",
    "IMBUE", "IMPEL", "IMPLY", "INBOX", "INCUR", "INEPT", "INERT", "INFER", "INGOT", "INLAY",
    "INLET", "INNER", "INPUT", "INTER", "INTRO", "IONIC", "IRATE", "IRKED", "IRONS", "IRONY",
    "ISLES", "ISLET", "ISSUE", "ITCHY", "ITEMS", "IVORY", "JABOT", "JAUNT", "JAZZY", "JEANS",
    "JELLY", "JENNY", "JERKY", "JETTY", "JEWEL", "JIFFY", "JOINT", "JOKER", "JOLLY", "JOUST",
    "JUDGE", "JUICE", "JUICY", "JUMBO", "JUMPY", "JUNTA", "JUROR", "KAPPA", "KARMA", "KAYAK",
    "KEBAB", "KHAKI", "KIOSK", "KITTY", "KLUTZ", "KNACK", "KNAVE", "KNEAD", "KNEEL", "KNELT",
    "KNIFE", "KNOCK", "KNOLL", "KNOWN", "KNOWS", "KOALA", "KOOKY", "KUDOS", "LABEL", "LABOR",
    "LACED", "LADEN", "LADLE", "LAGER", "LANCE", "LANDS", "LANES", "LANKY", "LAPEL", "LAPSE",
    "LARGE", "LARGO", "LASSO", "LATCH", "LATER", "LATHE", "LATTE", "LAUGH", "LAYER", "LAYUP",
    "LEACH", "LEAFY", "LEAKY", "LEANT", "LEAPT", "LEARN", "LEASE", "LEASH", "LEAST", "LEAVE",
    "LEDGE", "LEECH", "LEEKS", "LEERY", "LEFTY", "LEGAL", "LEGGY", "LEMON", "LEMUR", "LEPER",
    "LETUP", "LEVEE", "LEVER", "LEXIS", "LIBEL", "LIFER", "LIGHT", "LIKEN", "LILAC", "LIMBO",
    "LIMIT", "LINEN", "LINER", "LINGO", "LINKS", "LIONS", "LIPID", "LITER", "LITHE", "LIVER",
    "LIVID", "LLAMA", "LOADS", "LOAMY", "LOANS", "LOATH", "LOBBY", "LOCAL", "LOCKS", "LOCUS",
    "LODGE", "LOFTY", "LOGIC", "LOGIN", "LOGOS", "LOINS", "LONER", "LOOPS", "LOOPY", "LOOSE",
    "LORDY", "LOSER", "LOSES", "LOTTE", "LOTTO", "LOTUS", "LOUGH", "LOUSE", "LOUSY", "LOVED",
    "LOVER", "LOVES", "LOWER", "LOWLY", "LOYAL", "LUCID", "LUCKY", "LUMPY", "LUNAR", "LUNCH",
    "LUNGE", "LURCH", "LURED", "LURKS", "LUSTY", "LYING", "LYMPH", "LYNCH", "LYRIC", "MACHO",
    "MACRO", "MADAM", "MADLY", "MAFIA", "MAGIC", "MAGMA", "MAIZE", "MAJOR", "MAKER", "MAKES",
    "MALES", "MALLS", "MALTY", "MAMAS", "MAMBO", "MAMMA", "MANGO", "MANIA", "MANIC", "MANOR",
    "MAPLE", "MARCH", "MARRY", "MARSH", "MASON", "MATCH", "MATED", "MATER", "MATES", "MATHS",
    "MATTE", "MAUVE", "MAXIM", "MAYBE", "MAYOR", "MAZES", "MEALY", "MEANS", "MEATY", "MECCA",
    "MEDAL", "MEDIA", "MEDIC", "MELEE", "MELON", "MENUS", "MERCY", "MERGE", "MERIT", "MERRY",
    "MESSY", "METAL", "METER", "METRO", "MICRO", "MIDGE", "MIDST", "MIGHT", "MILKY", "MILLS",
    "MIMIC", "MINCE", "MINDS", "MINED", "MINER", "MINES", "MINIM", "MINOR", "MINTY", "MINUS",
    "MIRTH", "MISER", "MISTY", "MITES", "MIXED", "MIXER", "MIXES", "MOANS", "MOATS", "MOBIL",
    "MODEL", "MODEM", "MODES", "MOGUL", "MOIST", "MOLDY", "MOLES", "MONEY", "MONKS", "MONTH",
    "MOODS", "MOODY", "MOONS", "MOOSE", "MORAL", "MORON", "MORPH", "MORSE", "MOSSY", "MOTEL",
    "MOTIF", "MOTOR", "MOTTO", "MOULD", "MOULT", "MOUND", "MOUNT", "MOURN", "MOUSE", "MOUSY",
    "MOUTH", "MOVED", "MOVER", "MOVES", "MOVIE", "MOWER", "MUCKS", "MUCKY", "MUCUS", "MUDDY",
    "MULCH", "MUMMY", "MUNCH", "MURAL", "MURKY", "MUSHY", "MUSIC", "MUSKY", "MUSTY", "MUTED",
    "MUTES", "MYRRH", "MYTHS", "NACHO", "NAIVE", "NAKED", "NAMED", "NAMES", "NANNY", "NAPES",
    "NAPPY", "NASAL", "NASTY", "NATAL", "NAVAL", "NAVEL", "NEARS", "NEATO", "NECKS", "NEEDS",
    "NEEDY", "NEIGH", "NERDS", "NERDY", "NERVE", "NERVY", "NEVER", "NEWER", "NEWLY", "NICHE",
    "NIFTY", "NIGHT", "NINJA", "NINNY", "NINTH", "NOBLE", "NOBLY", "NODES", "NOISE", "NOISY",
    "NOMAD", "NONCE", "NOOKS", "NOONS", "NOOSE", "NORMS", "NORTH", "NOSED", "NOSES", "NOSEY",
    "NOTCH", "NOTED", "NOTES", "NOVEL", "NUDGE", "NUKED", "NUKES", "NULLS", "NUMB", "NURSE",
    "NUTTY", "NYLON", "NYMPH", "OAKEN", "OARED", "OASIS", "OATHS", "OBESE", "OBEYS", "OCCUR",
    "OCEAN", "OCTET", "ODDER", "ODDLY", "ODORS", "OFFAL", "OFFER", "OFTEN", "OGLED", "OGLES",
    "OILED", "OILER", "OKAPI", "OKAYS", "OLDEN", "OLDER", "OLDIE", "OLIVE", "OMEGA", "OMENS",
    "OMITS", "ONION", "ONSET", "OOHED", "OOMPH", "OOZED", "OOZES", "OPALS", "OPENS", "OPERA",
    "OPINE", "OPIUM", "OPTED", "OPTIC", "ORBIT", "ORCAS", "ORDER", "ORGAN", "OTHER", "OTTER",
    "OUGHT", "OUNCE", "OUTDO", "OUTER", "OUTGO", "OVARY", "OVATE", "OVENS", "OVERT", "OVINE",
    "OWING", "OWLET", "OWNED", "OWNER", "OXIDE", "OZONE", "PACED", "PACER", "PACES", "PACKS",
    "PACTS", "PADDY", "PAGAN", "PAGED", "PAGER", "PAGES", "PAILS", "PAINS", "PAINT", "PAIRS",
    "PALMS", "PALSY", "PAMPA", "PANDA", "PANEL", "PANIC", "PANSY", "PANTS", "PAPAL", "PAPAW",
    "PAPER", "PARCH", "PARED", "PARER", "PARES", "PARKA", "PARKS", "PARRY", "PARSE", "PARTS",
    "PARTY", "PASSE", "PASTA", "PASTE", "PASTY", "PATCH", "PATEN", "PATER", "PATHS", "PATIO",
    "PATSY", "PATTY", "PAUSE", "PAVED", "PAVER", "PAVES", "PAWED", "PAWNS", "PAYEE", "PAYER",
    "PEACE", "PEACH", "PEAKS", "PEAKY", "PEARL", "PEARS", "PECAN", "PECKS", "PEDAL", "PEEKS",
    "PEELS", "PEEPS", "PEERS", "PEEVE", "PENAL", "PENCE", "PENIS", "PENNY", "PERCH", "PERKS",
    "PERKY", "PERMS", "PESOS", "PESTS", "PETAL", "PETTY", "PHASE", "PHONE", "PHONY", "PHOTO",
    "PIANO", "PICKS", "PICKY", "PIECE", "PIERS", "PIETY", "PIGGY", "PILES", "PILLS", "PILOT",
    "PINCH", "PINED", "PINES", "PINGS", "PINKO", "PINKS", "PINKY", "PINTO", "PINTS", "PIPER",
    "PIPES", "PIQUE", "PITCH", "PITHY", "PIVOT", "PIXEL", "PIXIE", "PIZZA", "PLACE", "PLAID",
    "PLAIN", "PLAIT", "PLANE", "PLANK", "PLANS", "PLANT", "PLATE", "PLATS", "PLAYS", "PLAZA",
    "PLEAD", "PLEAS", "PLEAT", "PLIED", "PLIES", "PLINK", "PLODS", "PLOPS", "PLOTS", "PLOWS",
    "PLOYS", "PLUCK", "PLUGS", "PLUMB", "PLUME", "PLUMP", "PLUMS", "PLUNG", "PLUNK", "PLUSH",
    "PLUTO", "POACH", "POCKS", "PODGY", "POEMS", "POESY", "POETS", "POINT", "POISE", "POKED",
    "POKER", "POKES", "POLAR", "POLED", "POLES", "POLIO", "POLLS", "POLYP", "PONDS", "PONES",
    "PONIES", "POOCH", "POOLS", "POOPS", "POPES", "POPPY", "POPUP", "PORCH", "PORED", "PORES",
    "PORGY", "PORKS", "PORKY", "PORTS", "POSED", "POSER", "POSES", "POSIT", "POSSE", "POSTS",
    "POTTY", "POUCH", "POUND", "POURS", "POUTS", "POWER", "PRANK", "PRATE", "PRAWN", "PRAYS",
    "PREEN", "PREPS", "PRESS", "PREYS", "PRICE", "PRICK", "PRIDE", "PRIED", "PRIER", "PRIES",
    "PRIMA", "PRIME", "PRIMO", "PRIMP", "PRINT", "PRIOR", "PRISM", "PRIVY", "PRIZE", "PROBE",
    "PRODS", "PROFS", "PROMO", "PRONE", "PRONG", "PROOF", "PROPS", "PROSE", "PROSY", "PROUD",
    "PROVE", "PROWL", "PROXY", "PRUDE", "PRUNE", "PSALM", "PSYCH", "PUBIC", "PUCKA", "PUDGY",
    "PUFFS", "PUFFY", "PULLS", "PULPS", "PULPY", "PULSE", "PUMPS", "PUNCH", "PUNKS", "PUNNY",
    "PUPIL", "PUPPY", "PUREE", "PURER", "PURGE", "PURRS", "PURSE", "PUSHY", "PUSSY", "PUTTY",
    "PYGMY", "PYLON", "QUACK", "QUADS", "QUAFF", "QUAIL", "QUAKE", "QUALM", "QUART", "QUASH",
    "QUASI", "QUEEN", "QUEER", "QUELL", "QUERY", "QUEST", "QUEUE", "QUICK", "QUIET", "QUIFF",
    "QUILT", "QUIPS", "QUIRK", "QUITE", "QUITS", "QUOTA", "QUOTE", "QUOTH", "RABID", "RACED",
    "RACER", "RACES", "RACKS", "RADAR", "RADII", "RADIO", "RADON", "RAFTS", "RAGED", "RAGES",
    "RAGGED", "RAIDS", "RAILS", "RAINS", "RAINY", "RAISE", "RAJAH", "RAKED", "RAKER", "RAKES",
    "RALLY", "RALPH", "RAMPS", "RANCH", "RANDY", "RANGE", "RANGY", "RANKS", "RANTS", "RAPED",
    "RAPER", "RAPES", "RAPID", "RARER", "RASED", "RASES", "RASPS", "RASPY", "RATED", "RATES",
    "RATIO", "RATTY", "RAVED", "RAVEL", "RAVEN", "RAVER", "RAVES", "RAYON", "RAZED", "RAZER",
    "RAZES", "RAZOR", "REACH", "REACT", "READS", "READY", "REALM", "REAMS", "REAPS", "REARS",
    "REBEL", "REBUT", "RECAP", "RECUR", "RECUT", "REEDY", "REEFS", "REEKS", "REELS", "REFER",
    "REFIT", "REGAL", "REHAB", "REIGN", "REINS", "RELAX", "RELAY", "RELIC", "REMIT", "RENAL",
    "RENEW", "RENTS", "REPAY", "REPEL", "REPLY", "REPOS", "RESET", "RESIN", "RESTS", "RETCH",
    "RETRO", "RETRY", "REUSE", "REVED", "REVEL", "REVS", "RHINO", "RHYME", "RICED", "RICES",
    "RICHER", "RICKY", "RIDER", "RIDES", "RIDGE", "RIDGY", "RIFLE", "RIFTS", "RIGHT", "RIGID",
    "RIGOR", "RILED", "RILES", "RILLS", "RINDS", "RINGS", "RINKS", "RINSE", "RIOTS", "RIPEN",
    "RIPER", "RISEN", "RISER", "RISES", "RISKS", "RISKY", "RITES", "RITZY", "RIVAL", "RIVED",
    "RIVEN", "RIVER", "RIVET", "ROACH", "ROADS", "ROAMS", "ROANS", "ROARS", "ROAST", "ROBED",
    "ROBES", "ROBIN", "ROBOT", "ROCKS", "ROCKY", "RODEO", "ROGER", "ROGUE", "ROILS", "ROLES",
    "ROLLS", "ROMAN", "ROMPS", "ROOFS", "ROOKS", "ROOMS", "ROOMY", "ROOST", "ROOTS", "ROPED",
    "ROPER", "ROPES", "ROSES", "ROSIN", "ROTAS", "ROTOR", "ROUGE", "ROUGH", "ROUND", "ROUPS",
    "ROUSE", "ROUST", "ROUTE", "ROUTS", "ROVED", "ROVER", "ROVES", "ROWAN", "ROWDY", "ROWED",
    "ROWER", "ROYAL", "RUBLE", "RUDDY", "RUDER", "RUFFS", "RUGBY", "RUINS", "RULED", "RULER",
    "RULES", "RUMBA", "RUMOR", "RUMPS", "RUNIC", "RUNNY", "RUNTS", "RUPEE", "RURAL", "RUSES",
    "RUSHS", "RUSHY", "RUSTS", "RUSTY", "RUTTY", "SABRE", "SACKS", "SADLY", "SAFER", "SAFES",
    "SAGAS", "SAGER", "SAGES", "SAGGY", "SAHIB", "SAILS", "SAINT", "SAITH", "SAKES", "SALAD",
    "SALEM", "SALES", "SALLY", "SALON", "SALSA", "SALTS", "SALTY", "SALVE", "SALVO", "SAMBA",
    "SANDS", "SANDY", "SANER", "SANGS", "SAPPY", "SARGE", "SARIS", "SASSY", "SATAN", "SATED",
    "SATES", "SATIN", "SATYR", "SAUCE", "SAUCY", "SAUNA", "SAUTE", "SAVED", "SAVER", "SAVES",
    "SAVOR", "SAVOY", "SAVVY", "SAWED", "SAYER", "SAYSO", "SCABS", "SCADS", "SCALD", "SCALE",
    "SCALP", "SCALY", "SCAMP", "SCAMS", "SCANS", "SCANT", "SCARE", "SCARF", "SCARP", "SCARY",
    "SCENE", "SCENT", "SCHMO", "SCHWA", "SCION", "SCOFF", "SCOLD", "SCONE", "SCOOP", "SCOOT",
    "SCOPE", "SCORE", "SCORN", "SCOTS", "SCOUR", "SCOUT", "SCOWL", "SCRAM", "SCRAP", "SCREE",
    "SCREW", "SCRIP", "SCRUB", "SCRUM", "SCUBA", "SCUDS", "SCUFF", "SCULL", "SCUMS", "SEALS",
    "SEAMS", "SEAMY", "SEARS", "SEATS", "SEBUM", "SECTS", "SEDAN", "SEDGE", "SEEDY", "SEEKS",
    "SEEMS", "SEEPS", "SEERS", "SEGUE", "SEIZE", "SELLS", "SEMEN", "SEMIS", "SENDS", "SENOR",
    "SENSE", "SEPAL", "SEPIA", "SEPOY", "SEPTA", "SERF", "SERIF", "SERUM", "SERVE", "SETUP",
    "SEVEN", "SEVER", "SEWED", "SEWER", "SEXED", "SEXES", "SHACK", "SHADE", "SHADY", "SHAFT",
    "SHAKE", "SHAKY", "SHALE", "SHALL", "SHALT", "SHAME", "SHAMS", "SHANK", "SHAPE", "SHARD",
    "SHARE", "SHARK", "SHARP", "SHAVE", "SHAWL", "SHEAF", "SHEAR", "SHEDS", "SHEEN", "SHEEP",
    "SHEER", "SHEET", "SHEIK", "SHELF", "SHELL", "SHERD", "SHIED", "SHIES", "SHIFT", "SHILL",
    "SHIMS", "SHINE", "SHINS", "SHINY", "SHIPS", "SHIRE", "SHIRK", "SHIRT", "SHITS", "SHIVA",
    "SHOAL", "SHOCK", "SHOED", "SHOER", "SHOES", "SHONE", "SHOOK", "SHOOT", "SHOPS", "SHORE",
    "SHORN", "SHORT", "SHOTS", "SHOUT", "SHOVE", "SHOWN", "SHOWS", "SHOWY", "SHRED", "SHREW",
    "SHRUB", "SHRUG", "SHUCK", "SHUNS", "SHUNT", "SHUSH", "SHUTS", "SHYER", "SHYLY", "SICKO",
    "SICKS", "SIDED", "SIDES", "SIDLE", "SIEGE", "SIEVE", "SIFTS", "SIGHS", "SIGHT", "SIGMA",
    "SIGNS", "SILKS", "SILKY", "SILLS", "SILLY", "SILOS", "SILTS", "SILTY", "SINCE", "SINES",
    "SINEW", "SINGE", "SINGS", "SINKS", "SINUS", "SIRED", "SIREN", "SIRES", "SIRUP", "SISAL",
    "SISSY", "SITAR", "SITED", "SITES", "SITUS", "SIXES", "SIXTH", "SIXTY", "SIZED", "SIZER",
    "SIZES", "SKATE", "SKEIN", "SKEWS", "SKIDS", "SKIED", "SKIER", "SKIES", "SKIFF", "SKILL",
    "SKIMP", "SKIMS", "SKINK", "SKINS", "SKIPS", "SKIRT", "SKITS", "SKULK", "SKULL", "SKUNK",
    "SLABS", "SLACK", "SLAGS", "SLAIN", "SLAKE", "SLAMS", "SLANG", "SLANT", "SLAPS", "SLASH",
    "SLATE", "SLATS", "SLAVE", "SLAYS", "SLEDS", "SLEEK", "SLEEP", "SLEET", "SLEPT", "SLEWS",
    "SLICE", "SLICK", "SLIDE", "SLIER", "SLILY", "SLIME", "SLIMS", "SLIMY", "SLING", "SLINK",
    "SLIPS", "SLITS", "SLOBS", "SLOES", "SLOGS", "SLOOP", "SLOPE", "SLOPS", "SLOSH", "SLOTH",
    "SLOTS", "SLOWS", "SLUDGE", "SLUED", "SLUES", "SLUGS", "SLUMP", "SLUMS", "SLUNG", "SLUNK",
    "SLURP", "SLURS", "SLUSH", "SLUTS", "SMALL", "SMART", "SMASH", "SMEAR", "SMELL", "SMELT",
    "SMILE", "SMIRK", "SMITE", "SMITH", "SMOCK", "SMOKE", "SMOKY", "SMOTE", "SNACK", "SNAFU",
    "SNAGS", "SNAIL", "SNAKE", "SNAKY", "SNAPS", "SNARE", "SNARL", "SNEAK", "SNEER", "SNIDE",
    "SNIFF", "SNIPS", "SNITS", "SNOBS", "SNOOP", "SNOOT", "SNORE", "SNORT", "SNOTS", "SNOUT",
    "SNOWS", "SNOWY", "SNUBS", "SNUCK", "SNUFF", "SNUGS", "SOAPS", "SOAPY", "SOARS", "SOBER",
    "SOCKS", "SODAS", "SODDY", "SOFAS", "SOFTY", "SOGGY", "SOILS", "SOLAR", "SOLED", "SOLES",
    "SOLID", "SOLON", "SOLOS", "SOLVE", "SONAR", "SONGS", "SONIC", "SONNY", "SOOTH", "SOOTY",
    "SOPHS", "SOREL", "SORER", "SORES", "SORRY", "SORTS", "SOUGH", "SOULS", "SOUND", "SOUPS",
    "SOUPY", "SOURS", "SOUSE", "SOUTH", "SOWED", "SOWER", "SPACE", "SPADE", "SPANK", "SPARE",
    "SPARK", "SPARS", "SPASM", "SPATE", "SPAWN", "SPEAK", "SPEAR", "SPECS", "SPEED", "SPELL",
    "SPEND", "SPENT", "SPERM", "SPICE", "SPICY", "SPIED", "SPIEL", "SPIES", "SPIKE", "SPIKY",
    "SPILL", "SPILT", "SPINE", "SPINY", "SPIRE", "SPITE", "SPITZ", "SPLAT", "SPLIT", "SPOIL",
    "SPOKE", "SPOOF", "SPOOK", "SPOOL", "SPOON", "SPORE", "SPORT", "SPOTS", "SPOUT", "SPRAY",
    "SPREE", "SPRIG", "SPRIT", "SPROUT", "SPRUE", "SPUDS", "SPUNK", "SPURN", "SPURS", "SPURT",
    "SQUAD", "SQUAT", "SQUIB", "SQUID", "STABS", "STACK", "STAFF", "STAGE", "STAGS", "STAID",
    "STAIN", "STAIR", "STAKE", "STALE", "STALK", "STALL", "STAMP", "STAND", "STANK", "STARE",
    "STARK", "STARS", "START", "STASH", "STATE", "STATS", "STAVE", "STAYS", "STEAD", "STEAK",
    "STEAL", "STEAM", "STEED", "STEEL", "STEEP", "STEER", "STEIN", "STEMS", "STENO", "STEPS",
    "STERN", "STEWS", "STICK", "STIFF", "STILL", "STILT", "STING", "STINK", "STINT", "STOCK",
    "STOIC", "STOKE", "STOLE", "STOMP", "STONE", "STONY", "STOOD", "STOOL", "STOOP", "STOPS",
    "STORE", "STORK", "STORM", "STORY", "STOUT", "STOVE", "STRAP", "STRAW", "STRAY", "STRIP",
    "STROP", "STROVE", "STRUCK", "STRUM", "STRUT", "STUBS", "STUCK", "STUDS", "STUDY", "STUFF",
    "STUMP", "STUNG", "STUNK", "STUNT", "STUPE", "STYLE", "SUAVE", "SUCKS", "SUDSY", "SUEDE",
    "SUGAR", "SUING", "SUITE", "SUITS", "SULKS", "SULKY", "SULLY", "SUMAC", "SUMMON", "SUNNY",
    "SUPER", "SURER", "SURGE", "SURLY", "SUSHI", "SWABS", "SWAGS", "SWAIN", "SWAMP", "SWANK",
    "SWANS", "SWAPS", "SWARM", "SWASH", "SWATH", "SWATS", "SWAYS", "SWEAR", "SWEAT", "SWEDE",
    "SWEEP", "SWEET", "SWELL", "SWEPT", "SWIFT", "SWIGS", "SWILL", "SWIMS", "SWINE", "SWING",
    "SWIPE", "SWIRL", "SWISS", "SWOOP", "SWORD", "SWORE", "SWORN", "SWUNG", "SYNOD", "SYRUP",
    "TABBY", "TABLE", "TABOO", "TACIT", "TACKY", "TACOS", "TAFFY", "TAILS", "TAINT", "TAKEN",
    "TAKER", "TAKES", "TALES", "TALKS", "TALKY", "TALLY", "TALON", "TAMED", "TAMER", "TAMES",
    "TANGO", "TANGY", "TANKS", "TANSY", "TANTO", "TAPED", "TAPER", "TAPES", "TAPIR", "TARDY",
    "TARED", "TARES", "TAROT", "TARPS", "TARRY", "TARTS", "TARTY", "TASKS", "TASTE", "TASTY",
    "TATTY", "TAUNT", "TAUPE", "TAWNY", "TAXED", "TAXES", "TAXIS", "TEACH", "TEAKS", "TEAMS",
    "TEARS", "TEARY", "TEASE", "TEATS", "TEDDY", "TEENS", "TEENY", "TEETH", "TEMPO", "TEMPS",
    "TEMPT", "TENET", "TENOR", "TENSE", "TENTH", "TENTS", "TEPEE", "TERMS", "TERRA", "TERRY",
    "TERSE", "TESTS", "TESTY", "TEXAS", "TEXTS", "THANK", "THAW", "THEFT", "THEIR", "THEME",
    "THENS", "THERE", "THESE", "THETA", "THICK", "THIEF", "THIGH", "THING", "THINK", "THIRD",
    "THORN", "THOSE", "THREE", "THREW", "THROB", "THROE", "THROW", "THUGS", "THUMB", "THUMP",
    "THUNK", "THYME", "TIARA", "TIBIA", "TICKS", "TIDAL", "TIDED", "TIDES", "TIERS", "TIGER",
    "TIGHT", "TILDE", "TILED", "TILES", "TILLS", "TILTS", "TIMED", "TIMER", "TIMES", "TIMID",
    "TINES", "TINGE", "TINTS", "TIPPY", "TIPS", "TIRED", "TIRES", "TITAN", "TITHE", "TITLE",
    "TOAST", "TODAY", "TODDY", "TOGAS", "TOGETHER", "TOILS", "TOKED", "TOKEN", "TOKES", "TOKYO",
    "TOLLS", "TOMBS", "TOMES", "TONAL", "TONED", "TONER", "TONES", "TONGS", "TONIC", "TONNE",
    "TONUS", "TOOLS", "TOONS", "TOOTH", "TOOTS", "TOPAZ", "TOPIC", "TORCH", "TORIC", "TORSO",
    "TORUS", "TOTAL", "TOTEM", "TOUCH", "TOUGH", "TOURS", "TOUTS", "TOWED", "TOWEL", "TOWER",
    "TOWNS", "TOXIC", "TOXIN", "TRACE", "TRACK", "TRACT", "TRADE", "TRAIL", "TRAIN", "TRAIT",
    "TRAMP", "TRAMS", "TRANS", "TRASH", "TRASK", "TRAWL", "TRAYS", "TREAD", "TREAT", "TREED",
    "TREES", "TREKS", "TREND", "TRESS", "TRIAD", "TRIAL", "TRIBE", "TRICK", "TRIED", "TRIER",
    "TRIES", "TRIKE", "TRILL", "TRIMS", "TRINE", "TRIOS", "TRIPE", "TRIPS", "TRITE", "TROD",
    "TROLL", "TROMP", "TROOP", "TROPE", "TROTH", "TROTS", "TROUT", "TROVE", "TRUCE", "TRUCK",
    "TRUED", "TRUER", "TRUES", "TRULY", "TRUMP", "TRUNK", "TRUSS", "TRUST", "TRUTH", "TRYST",
    "TSARS", "TUBAS", "TUBBY", "TUBED", "TUBER", "TUBES", "TUCKS", "TUFTS", "TULIP", "TULLE",
    "TUMBLE", "TUMOR", "TUNAS", "TUNED", "TUNER", "TUNES", "TUNIC", "TUNNY", "TURBO", "TURFS",
    "TURNS", "TURPS", "TUSKS", "TUTOR", "TUTUS", "TUXES", "TWAIN", "TWANG", "TWEAK", "TWEED",
    "TWEET", "TWERP", "TWICE", "TWIGS", "TWILL", "TWINE", "TWINS", "TWIRL", "TWIST", "TWITS",
    "TWIXT", "TYING", "TYKES", "TYPED", "TYPES", "TYPIC", "TYPOS", "UDDER", "ULCER", "ULTRA",
    "UMBRA", "UMIAK", "UMPHS", "UNABLE", "UNCLE", "UNCLES", "UNCUT", "UNDER", "UNDUE", "UNFED",
    "UNFIT", "UNHAPPIUNION", "UNITE", "UNITS", "UNITY", "UNJUST", "UNWED", "UNZIP", "UPEND", "UPPER",
    "UPSET", "URBAN", "URGED", "URGES", "URINE", "USAGE", "USHER", "USING", "USUAL", "USURP",
    "UTTER", "UVULA", "VACUA", "VAGUE", "VAILS", "VALES", "VALET", "VALID", "VALOR", "VALUE",
    "VALVE", "VAMPS", "VANES", "VAPOR", "VAULT", "VAUNT", "VEALS", "VEERS", "VEINS", "VELAR",
    "VENAL", "VENDS", "VENOM", "VENTS", "VENUE", "VERBS", "VERGE", "VERSE", "VERSO", "VERVE",
    "VESTS", "VETCH", "VEXED", "VEXES", "VIALS", "VIBES", "VICAR", "VICES", "VIDEO", "VIEWS",
    "VIGIL", "VIGOR", "VILER", "VILLA", "VINES", "VINYL", "VIOLA", "VIPER", "VIRAL", "VIRUS",
    "VISAS", "VISED", "VISES", "VISIT", "VISOR", "VISTA", "VITAL", "VIVID", "VIXEN", "VIZOR",
    "VOCAL", "VODKA", "VOGUE", "VOICE", "VOIDS", "VOILA", "VOLES", "VOLTS", "VOMIT", "VOTED",
    "VOTER", "VOTES", "VOUCH", "VOWED", "VOWEL", "VOWER", "VYING", "WACKO", "WACKS", "WACKY",
    "WADED", "WADER", "WADES", "WAFER", "WAFTS", "WAGED", "WAGER", "WAGES", "WAGON", "WAIFS",
    "WAILS", "WAIST", "WAITS", "WAIVE", "WAKED", "WAKEN", "WAKES", "WALDO", "WALES", "WALKS",
    "WALLS", "WALTZ", "WANDS", "WANES", "WANNA", "WANTS", "WARDS", "WARES", "WARILY", "WARMS",
    "WARNS", "WARPS", "WARTS", "WARTY", "WASPS", "WASPY", "WASTE", "WATCH", "WATER", "WATTS",
    "WAVED", "WAVER", "WAVES", "WAXED", "WAXEN", "WAXES", "WEARY", "WEAVE", "WEBER", "WEDGE",
    "WEDGY", "WEEDS", "WEEDY", "WEEKS", "WEENY", "WEEPS", "WEEPY", "WEFTS", "WEIGH", "WEIRD",
    "WEIRS", "WELDS", "WELLS", "WELSH", "WELTS", "WENCH", "WENDS", "WHACK", "WHALE", "WHAMS",
    "WHARF", "WHEAT", "WHEEL", "WHELK", "WHELM", "WHELP", "WHERE", "WHICH", "WHIFF", "WHILE",
    "WHIMS", "WHINE", "WHINY", "WHIPS", "WHIRL", "WHIRS", "WHISK", "WHIST", "WHITE", "WHITS",
    "WHOLE", "WHOMP", "WHOOP", "WHOPS", "WHORE", "WHORL", "WHOSE", "WICKS", "WIDEN", "WIDER",
    "WIDOW", "WIDTH", "WIELD", "WIFED", "WIFES", "WIGHT", "WILED", "WILES", "WILLS", "WILLY",
    "WILTS", "WIMPS", "WIMPY", "WINCE", "WINCH", "WINDS", "WINDY", "WINED", "WINES", "WINGS",
    "WINKS", "WINOS", "WIPED", "WIPER", "WIPES", "WIRED", "WIRES", "WIRY", "WISED", "WISER",
    "WISES", "WISPS", "WISPY", "WITCH", "WITEN", "WITHER", "WITTY", "WIVED", "WIVES", "WIZEN",
    "WOKE", "WOLDS", "WOMAN", "WOMEN", "WONKY", "WOODS", "WOODY", "WOOED", "WOOER", "WOOFS",
    "WOOLS", "WOOLY", "WOOZY", "WORDS", "WORDY", "WORKS", "WORLD", "WORMS", "WORMY", "WORRY",
    "WORSE", "WORST", "WORTH", "WOULD", "WOUND", "WOVEN", "WOWED", "WRACK", "WRAPS", "WRATH",
    "WREAK", "WRECK", "WREST", "WRING", "WRIST", "WRITE", "WRONG", "WROTE", "WROTH", "WRUNG",
    "WRYLY", "XEROX", "XYLEM", "YACHT", "YAHOO", "YANKS", "YARDS", "YARNS", "YAWED", "YAWLS",
    "YAWNS", "YEAHS", "YEARS", "YEAST", "YELLS", "YELPS", "YIELD", "YIKES", "YODEL", "YOGAS",
    "YOGIS", "YOKED", "YOKES", "YOLKS", "YOUNG", "YOURS", "YOUTH", "YOWLS", "YUCCA", "YUCKY",
    "YUKON", "YUMMY", "ZAGGED", "ZAPPY", "ZEROS", "ZESTS", "ZESTY", "ZILCH", "ZINCS", "ZINGY",
    "ZIPPY", "ZONED", "ZONES", "ZONKS", "ZOOMS"
]

# Filter out words with duplicate letters for simpler gameplay
WORD_LIST = [word for word in WORD_LIST if len(set(word)) == 5]

class Wordle:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.word_length = 5
        self.max_attempts = 6
        
        # Initialize curses
        curses.curs_set(0)
        self.stdscr.nodelay(0)
        self.stdscr.timeout(-1)
        
        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)   # Correct position
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # Wrong position
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Not in word
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)   # Empty cell
        
        # Initialize game
        self.reset_game()
    
    def reset_game(self):
        """Reset the game state"""
        self.target_word = random.choice(WORD_LIST)
        self.attempts = []
        self.current_guess = ""
        self.keyboard_state = {}
        self.game_over = False
        self.won = False
        self.error_message = ""
    
    def check_guess(self, guess):
        """Check guess and return color codes for each letter"""
        result = ['gray'] * self.word_length
        target_chars = list(self.target_word)
        guess_chars = list(guess)
        
        # First pass: mark correct positions (green)
        for i in range(self.word_length):
            if guess_chars[i] == target_chars[i]:
                result[i] = 'green'
                target_chars[i] = None
                guess_chars[i] = None
        
        # Second pass: mark wrong positions (yellow)
        for i in range(self.word_length):
            if guess_chars[i] is not None and guess_chars[i] in target_chars:
                result[i] = 'yellow'
                target_chars[target_chars.index(guess_chars[i])] = None
        
        return result
    
    def update_keyboard(self, guess, result):
        """Update keyboard state based on guess result"""
        for i, letter in enumerate(guess):
            current = self.keyboard_state.get(letter, 'unused')
            new_state = result[i]
            
            # Priority: green > yellow > gray
            if new_state == 'green':
                self.keyboard_state[letter] = 'green'
            elif new_state == 'yellow' and current != 'green':
                self.keyboard_state[letter] = 'yellow'
            elif current == 'unused':
                self.keyboard_state[letter] = 'gray'
    
    def is_valid_guess(self, guess):
        """Check if guess is valid"""
        return len(guess) == self.word_length and guess.isalpha() and guess.upper() in WORD_LIST
    
    def get_color_pair(self, state):
        """Get color pair for a state"""
        if state == 'green':
            return curses.color_pair(1)
        elif state == 'yellow':
            return curses.color_pair(2)
        elif state == 'gray':
            return curses.color_pair(3)
        else:
            return curses.color_pair(4)
    
    def draw_board(self):
        """Draw the game board"""
        self.stdscr.erase()
        height, width = self.stdscr.getmaxyx()
        
        # Draw title
        title = "WORDLE - 猜單字"
        self.stdscr.addstr(1, (width - len(title)) // 2, title, curses.A_BOLD)
        
        # Draw attempts
        start_y = 3
        cell_width = 4
        
        for attempt_idx in range(self.max_attempts):
            y = start_y + attempt_idx * 2
            x_offset = (width - self.word_length * cell_width) // 2
            
            if attempt_idx < len(self.attempts):
                # Show completed attempt
                guess, result = self.attempts[attempt_idx]
                for i, (letter, state) in enumerate(zip(guess, result)):
                    x = x_offset + i * cell_width
                    color = self.get_color_pair(state)
                    try:
                        self.stdscr.addstr(y, x, f" {letter} ", color | curses.A_BOLD)
                    except:
                        pass
            elif attempt_idx == len(self.attempts) and not self.game_over:
                # Show current input
                for i in range(self.word_length):
                    x = x_offset + i * cell_width
                    if i < len(self.current_guess):
                        letter = self.current_guess[i]
                        try:
                            self.stdscr.addstr(y, x, f" {letter} ", curses.A_REVERSE)
                        except:
                            pass
                    else:
                        try:
                            self.stdscr.addstr(y, x, " _ ", curses.color_pair(4))
                        except:
                            pass
            else:
                # Show empty slots
                for i in range(self.word_length):
                    x = x_offset + i * cell_width
                    try:
                        self.stdscr.addstr(y, x, " _ ", curses.color_pair(4))
                    except:
                        pass
        
        # Draw keyboard
        keyboard_y = start_y + self.max_attempts * 2 + 1
        self.draw_keyboard(keyboard_y, width)
        
        # Draw instructions
        inst_y = keyboard_y + 5
        if self.game_over:
            if self.won:
                msg = f"🎉 YOU WIN! The word was {self.target_word}"
            else:
                msg = f"😢 Game Over! The word was {self.target_word}"
            self.stdscr.addstr(inst_y, (width - len(msg)) // 2, msg, curses.A_BOLD)
            
            inst = "Press N for new game, Q to quit"
            self.stdscr.addstr(inst_y + 1, (width - len(inst)) // 2, inst)
        else:
            inst = "Type your guess and press ENTER"
            self.stdscr.addstr(inst_y, (width - len(inst)) // 2, inst)
            
            inst2 = "BACKSPACE: Delete  Q: Quit"
            self.stdscr.addstr(inst_y + 1, (width - len(inst2)) // 2, inst2)
            
            # Show error message if any
            if self.error_message:
                self.stdscr.addstr(inst_y + 2, (width - len(self.error_message)) // 2, 
                                 self.error_message, curses.color_pair(3))
        
        self.stdscr.refresh()
    
    def draw_keyboard(self, y, width):
        """Draw virtual keyboard with color states"""
        keyboard_rows = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]
        
        for row_idx, row in enumerate(keyboard_rows):
            row_y = y + row_idx
            x_pos = (width - len(row) * 2) // 2 + row_idx * 2
            
            for col_idx, letter in enumerate(row):
                state = self.keyboard_state.get(letter, 'unused')
                x = x_pos + col_idx * 2
                
                # Show letter with color background
                if state == 'green':
                    char = letter
                    color = self.get_color_pair('green') | curses.A_BOLD
                elif state == 'yellow':
                    char = letter
                    color = self.get_color_pair('yellow') | curses.A_BOLD
                elif state == 'gray':
                    # Darker/dimmed x for excluded letters
                    char = 'x'
                    color = curses.A_DIM
                else:
                    # Unused letters
                    char = letter
                    color = curses.A_NORMAL
                
                try:
                    self.stdscr.addstr(row_y, x, char, color)
                except:
                    pass
        
        # Legend
        legend_y = y + 4
        legend = "🟩=Correct pos  🟨=Wrong pos  x=Not in word"
        try:
            self.stdscr.addstr(legend_y, (width - len(legend)) // 2, legend, curses.A_DIM)
        except:
            pass
    
    def run(self):
        """Main game loop"""
        while True:
            self.draw_board()
            
            # Get input
            try:
                key = self.stdscr.getch()
            except:
                continue
            
            # Handle quit
            if key in [ord('q'), ord('Q')]:
                break
            
            # Handle new game
            if self.game_over and key in [ord('n'), ord('N')]:
                self.reset_game()
                continue
            
            # Don't allow input if game is over
            if self.game_over:
                continue
            
            # Handle backspace
            if key in [curses.KEY_BACKSPACE, 127, 8]:
                if self.current_guess:
                    self.current_guess = self.current_guess[:-1]
                    # Clear error when user starts editing
                    self.error_message = ""
            
            # Handle letter input
            elif key >= ord('a') and key <= ord('z'):
                letter = chr(key).upper()
                if len(self.current_guess) < self.word_length:
                    self.current_guess += letter
                    # Clear error when user starts editing
                    self.error_message = ""
            elif key >= ord('A') and key <= ord('Z'):
                letter = chr(key)
                if len(self.current_guess) < self.word_length:
                    self.current_guess += letter
                    # Clear error when user starts editing
                    self.error_message = ""
            
            # Handle enter
            elif key == ord('\n'):
                if len(self.current_guess) == self.word_length:
                    if self.is_valid_guess(self.current_guess):
                        # Clear error message
                        self.error_message = ""
                        
                        # Check guess
                        result = self.check_guess(self.current_guess)
                        self.update_keyboard(self.current_guess, result)
                        self.attempts.append((self.current_guess, result))
                        
                        # Check win
                        if self.current_guess == self.target_word:
                            self.won = True
                            self.game_over = True
                        elif len(self.attempts) >= self.max_attempts:
                            self.game_over = True
                        
                        self.current_guess = ""
                    else:
                        # Invalid word: show error but DON'T consume attempt
                        # Let user fix the word
                        self.error_message = "Not in word list! (use BACKSPACE to fix)"

def main(stdscr=None):
    """Entry point for the game"""
    if stdscr is None:
        from curses import wrapper
        wrapper(main)
    else:
        game = Wordle(stdscr)
        game.run()

if __name__ == "__main__":
    main()

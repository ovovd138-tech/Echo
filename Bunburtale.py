# -*- coding: utf-8 -*-
"""
ЭХО-ЛОКАЦИЯ (Pygame Edition v9)
Музыка, компаньоны, сохранения, эпичный финальный босс.

Управление:
  Карта:  WASD — ходьба, E — войти, I — инвентарь, M — магазин,
          C — компаньоны, F5 — сохранить, F9 — загрузить, Esc — меню
  Бой:    A S D F — ноты, 1/2/3 — зелья, Q — способность компаньона,
          Esc — сдаться
  Головоломки: мышь, стрелки (для "Путь стрелок")
"""

import sys, math, array, random, pygame, json, os, time as _time

# ─────────────────────────── ЦВЕТА ───────────────────────────
BG_DARK=(8,8,15); BG_PANEL=(18,18,31); BG_PANEL_HI=(30,30,53)
NEON_CYAN=(95,251,241); NEON_PINK=(255,95,181); NEON_PURPLE=(181,123,255)
NEON_GOLD=(255,215,95); NEON_GREEN=(123,255,158); NEON_RED=(255,90,90)
NEON_BLUE=(95,180,251); NEON_ORANGE=(255,140,60)
TEXT_MAIN=(200,208,224); TEXT_DIM=(90,100,120); TEXT_WHITE=(255,255,255)
DARK_LINE=(21,21,42); HP_RED=(220,60,70); HP_GREEN=(90,220,120)

WIDTH,HEIGHT = 960,700
FPS = 60
SAMPLE_RATE = 22050
SAVE_FILE = "echo_save.json"

RARITY_COLORS={"common":(180,180,180),"uncommon":(123,255,158),
               "rare":(95,180,251),"epic":(181,123,255),"legendary":(255,215,95)}
RARITY_NAMES={"common":"Обычное","uncommon":"Необычное","rare":"Редкое",
              "epic":"Эпическое","legendary":"Легендарное"}


# ═══════════════════════ ОРУЖИЕ / ЗЕЛЬЯ ═══════════════════════
WEAPONS = {
    "wood_stick":  {"name":"Палка","dmg":6,"price":0,"rarity":"common",
                    "color":(140,100,60),"desc":"Ветка."},
    "rust_dagger": {"name":"Ржавый кинжал","dmg":10,"price":40,"rarity":"common",
                    "color":(160,120,80),"desc":"Старый."},
    "iron_sword":  {"name":"Железный меч","dmg":16,"price":100,"rarity":"uncommon",
                    "color":(200,200,220),"desc":"Надёжный."},
    "runed_blade": {"name":"Рунический клинок","dmg":24,"price":220,"rarity":"rare",
                    "color":NEON_CYAN,"desc":"Светится."},
    "silver_scepter":{"name":"Серебряный посох","dmg":34,"price":450,"rarity":"epic",
                    "color":NEON_PURPLE,"desc":"Гудит."},
    "echo_glaive": {"name":"Глефа Эха","dmg":48,"price":900,"rarity":"legendary",
                    "color":NEON_GOLD,"desc":"Режет тишину."},
}
POTIONS = {
    "small_heal":{"name":"Малое зелье","heal":30,"price":20,"color":HP_GREEN,
                  "desc":"+30 HP","atk_bonus":0,"def_bonus":0,"hp_bonus":0},
    "med_heal":{"name":"Среднее зелье","heal":60,"price":50,"color":NEON_GREEN,
                "desc":"+60 HP","atk_bonus":0,"def_bonus":0,"hp_bonus":0},
    "big_heal":{"name":"Большое зелье","heal":100,"price":120,"color":NEON_CYAN,
                "desc":"+100 HP","atk_bonus":0,"def_bonus":0,"hp_bonus":0},
    "mega_heal":{"name":"Мега-зелье","heal":9999,"price":250,"color":NEON_GOLD,
                 "desc":"Полное HP","atk_bonus":0,"def_bonus":0,"hp_bonus":0},
    "epic_elixir":{"name":"Эликсир Пробуждения","heal":9999,"price":0,
                   "color":NEON_PURPLE,"desc":"Полное HP +5 ATK +3 DEF +20 MAX HP",
                   "atk_bonus":5,"def_bonus":3,"hp_bonus":20},
}


# ═══════════════════════ ПРЕДМЕТЫ (ФИКС) ═══════════════════════
ITEMS = {
    "scarf":{"name":"Детский шарф","slot":"scarf","color":NEON_CYAN,"rarity":"common",
             "desc":"Тёплый, пахнет домом.","memory_bonus":0,"window_bonus":5,"act":1},
    "apron":{"name":"Фартук официантки","slot":"apron","color":(240,230,200),
             "rarity":"common","desc":"Белый, с кружевом.",
             "memory_bonus":5,"window_bonus":0,"act":1},
    "shawl":{"name":"Платок матери","slot":"hat","color":(200,60,90),
             "rarity":"uncommon","desc":"Уютный и тёплый.",
             "memory_bonus":5,"window_bonus":0,"act":1},
    "glasses":{"name":"Очки библиотекаря","slot":"eyes","color":NEON_CYAN,
               "rarity":"uncommon","desc":"Помогают видеть.",
               "memory_bonus":0,"window_bonus":10,"act":1},
    "lantern":{"name":"Фонарь моряка","slot":"lantern","color":(255,180,60),
               "rarity":"rare","desc":"Ярче и надёжнее.",
               "memory_bonus":10,"window_bonus":0,"act":1},
    "cloak":{"name":"Плащ машиниста","slot":"cloak","color":(70,100,150),
             "rarity":"rare","desc":"Плотный, тёплый.",
             "memory_bonus":0,"window_bonus":10,"act":1},
    "crystal":{"name":"Кристалл памяти","slot":"amulet","color":NEON_CYAN,
               "rarity":"rare","desc":"Светится изнутри.",
               "memory_bonus":15,"window_bonus":0,"act":2},
    "moonstone":{"name":"Лунный камень","slot":"ring","color":(170,200,255),
                 "rarity":"rare","desc":"Холодный на ощупь.",
                 "memory_bonus":0,"window_bonus":15,"act":2},
    "quill":{"name":"Чернильное перо","slot":"eyes","color":NEON_PURPLE,
             "rarity":"epic","desc":"Пишет само.",
             "memory_bonus":0,"window_bonus":20,"act":2},
    "compass":{"name":"Компас странника","slot":"lantern","color":(255,130,60),
               "rarity":"epic","desc":"Указывает путь.",
               "memory_bonus":15,"window_bonus":0,"act":2},
    "starmap":{"name":"Карта звёзд","slot":"hat","color":(255,220,130),
               "rarity":"rare","desc":"Мерцает в темноте.",
               "memory_bonus":10,"window_bonus":10,"act":2},
    "silver":{"name":"Серебряный ключ","slot":"cloak","color":(220,220,240),
              "rarity":"epic","desc":"Открывает забытое.",
              "memory_bonus":10,"window_bonus":15,"act":2},
    "theatre_mask":{"name":"Маска актёра","slot":"hat","color":(255,100,120),
                    "rarity":"epic","desc":"Улыбается сама.",
                    "memory_bonus":15,"window_bonus":10,"act":3},
    "chip":{"name":"Старая фишка","slot":"ring","color":(200,180,90),
            "rarity":"rare","desc":"Помнит азарт.",
            "memory_bonus":0,"window_bonus":20,"act":3},
    "key_hotel":{"name":"Ключ от номера","slot":"amulet","color":(200,160,100),
                 "rarity":"rare","desc":"От номера 7.",
                 "memory_bonus":20,"window_bonus":0,"act":3},
    "gavel":{"name":"Судейский молоток","slot":"lantern","color":(170,100,60),
             "rarity":"epic","desc":"Стучит по истине.",
             "memory_bonus":15,"window_bonus":15,"act":3},
    "gear":{"name":"Стальная шестерня","slot":"cloak","color":(160,160,180),
            "rarity":"epic","desc":"Вращается вечно.",
            "memory_bonus":10,"window_bonus":20,"act":3},
    "mask_owl":{"name":"Совиная личина","slot":"eyes","color":(200,180,140),
                "rarity":"epic","desc":"Смотрит в темноте.",
                "memory_bonus":20,"window_bonus":10,"act":3},
    "pearl":{"name":"Жемчужина бездны","slot":"amulet","color":(230,220,240),
             "rarity":"epic","desc":"Светится в воде.",
             "memory_bonus":25,"window_bonus":5,"act":4},
    "coral":{"name":"Коралловый венец","slot":"hat","color":(255,130,160),
             "rarity":"epic","desc":"Живой и тёплый.",
             "memory_bonus":15,"window_bonus":20,"act":4},
    "trident":{"name":"Ржавый трезубец","slot":"lantern","color":(150,200,220),
               "rarity":"legendary","desc":"Помнит бури.",
               "memory_bonus":20,"window_bonus":20,"act":4},
    "abyss_ring":{"name":"Кольцо из тьмы","slot":"ring","color":(90,40,140),
                  "rarity":"legendary","desc":"Поглощает свет.",
                  "memory_bonus":0,"window_bonus":35,"act":4},
    "shell":{"name":"Поющая раковина","slot":"cloak","color":(255,200,150),
             "rarity":"epic","desc":"Шепчет о море.",
             "memory_bonus":20,"window_bonus":15,"act":4},
    "scale":{"name":"Чешуя левиафана","slot":"eyes","color":(120,200,180),
             "rarity":"legendary","desc":"Броня морского змея.",
             "memory_bonus":15,"window_bonus":25,"act":4},
    "echo_heart":{"name":"Сердце Эха","slot":"amulet","color":(255,90,90),
                  "rarity":"legendary","desc":"Бьётся в такт.",
                  "memory_bonus":30,"window_bonus":10,"act":5},
    "crown":{"name":"Венец Эха","slot":"crown","color":NEON_GOLD,
             "rarity":"legendary","desc":"Собран из всех голосов.",
             "memory_bonus":25,"window_bonus":25,"act":6},
    "last_voice":{"name":"Последний голос","slot":"ring","color":(255,240,200),
                  "rarity":"legendary","desc":"Звучит тихо.",
                  "memory_bonus":15,"window_bonus":30,"act":6},
}
SLOT_NAMES={"cloak":"Плащ","hat":"Капюшон","scarf":"Шарф","apron":"Фартук",
            "eyes":"Очи","lantern":"Фонарь","amulet":"Амулет","ring":"Кольцо",
            "crown":"Венец"}
SLOT_ORDER=["cloak","hat","scarf","apron","eyes","lantern","amulet","ring","crown"]


# ═══════════════════════ ВРАГИ ═══════════════════════
ENEMY_TEMPLATES = {
    "guard":{"name":"Страж-Тень","hp":60,"attack":8,"spawn":50,"speed":4,
             "notes":20,"window":95,"color":(120,100,160),"shards":10,"boss":False},
    "crawler":{"name":"Ползун","hp":45,"attack":10,"spawn":40,"speed":5,
               "notes":22,"window":88,"color":(140,90,130),"shards":12,"boss":False},
    "hunter":{"name":"Тень-охотник","hp":80,"attack":12,"spawn":42,"speed":5,
              "notes":24,"window":85,"color":(170,110,180),"shards":16,"boss":False},
    "boss_1":{"name":"Хранитель","hp":150,"attack":18,"spawn":38,"speed":5,
              "notes":28,"window":80,"color":(200,80,130),"shards":45,"boss":True},
    "boss_2":{"name":"Владыка","hp":200,"attack":22,"spawn":34,"speed":6,
              "notes":32,"window":76,"color":(230,70,90),"shards":70,"boss":True},
    "boss_3":{"name":"Молчальник","hp":260,"attack":26,"spawn":30,"speed":6,
              "notes":36,"window":72,"color":(255,60,80),"shards":100,"boss":True},
    "final":{"name":"Первый Голос","hp":400,"attack":32,"spawn":24,"speed":7,
             "notes":44,"window":68,"color":(255,30,60),"shards":250,"boss":True},
}


# ═══════════════════════ МОДИФИКАТОРЫ ═══════════════════════
MODIFIERS = {
    "swift":{"name":"Стремительный","color":NEON_CYAN,"speed":+1,"spawn":-6,
             "hp_mult":1.0,"atk_mult":1.0,"window_mod":0,"note_style":"normal"},
    "armored":{"name":"Бронированный","color":NEON_BLUE,"speed":0,"spawn":0,
               "hp_mult":1.5,"atk_mult":0.85,"window_mod":15,"note_style":"normal"},
    "savage":{"name":"Свирепый","color":NEON_RED,"speed":0,"spawn":0,
              "hp_mult":1.0,"atk_mult":1.5,"window_mod":0,"note_style":"normal"},
    "veiled":{"name":"Скрытный","color":NEON_PURPLE,"speed":0,"spawn":0,
              "hp_mult":1.1,"atk_mult":1.0,"window_mod":-18,"note_style":"normal"},
    "echoing":{"name":"Эхо","color":NEON_GOLD,"speed":0,"spawn":0,
               "hp_mult":1.0,"atk_mult":1.0,"window_mod":0,"note_style":"dual"},
    "rushing":{"name":"Несущийся","color":NEON_PINK,"speed":0,"spawn":0,
               "hp_mult":1.0,"atk_mult":1.0,"window_mod":5,"note_style":"burst"},
    "waving":{"name":"Волнующийся","color":NEON_GREEN,"speed":0,"spawn":0,
              "hp_mult":1.15,"atk_mult":1.05,"window_mod":0,"note_style":"wave"},
    "fragile":{"name":"Хрупкий","color":(180,200,180),"speed":0,"spawn":0,
               "hp_mult":0.65,"atk_mult":1.0,"window_mod":10,"note_style":"normal",
               "reward_mult":1.5},
    "berserk":{"name":"Берсерк","color":(255,60,60),"speed":+1,"spawn":-4,
               "hp_mult":1.0,"atk_mult":1.35,"window_mod":-5,"note_style":"normal"},
    "haunted":{"name":"Проклятый","color":(150,50,200),"speed":0,"spawn":-3,
               "hp_mult":1.2,"atk_mult":1.15,"window_mod":-5,"note_style":"wave",
               "reward_mult":1.3},
}
MODIFIER_POOLS = {
    1:[], 2:["swift","armored","fragile"],
    3:["swift","armored","savage","veiled","fragile","rushing"],
    4:["swift","armored","savage","veiled","echoing","rushing","waving","fragile"],
    5:["swift","armored","savage","veiled","echoing","rushing","waving","berserk","haunted"],
    6:["savage","veiled","echoing","rushing","waving","berserk","haunted"],
}


# ═══════════════════════ КОМПАНЬОНЫ (НОВОЕ) ═══════════════════════
# Разблокируются по мере прохождения акта. Помогают в бою (Q).
COMPANIONS = {
    "lira": {
        "name":"Лира","unlock_act":1,"color":NEON_PINK,
        "desc":"Дух певицы, потерявшей голос.",
        "assist":"heal","assist_name":"Песня-исцеление (+40% HP)",
        "lines":{
            "hello":"Твоя песня звучит громче, чем кажется...",
            "battle":"Пой со мной, странник!",
            "low_hp":"Держись! Я спою тебе!",
            "win":"Ты подарил голос всем. И мне тоже.",
        },
    },
    "guide": {
        "name":"Проводник","unlock_act":2,"color":NEON_GOLD,
        "desc":"Древний дух, указывающий путь.",
        "assist":"window","assist_name":"Прозрение (широкое окно 8 сек)",
        "lines":{
            "hello":"Город помнит тебя, странник. Иди.",
            "battle":"Я подсвечу ноты — смотри внимательно!",
            "low_hp":"Не сдавайся. Ещё не время.",
            "win":"Каждый шаг был к этому. Спасибо.",
        },
    },
    "cat": {
        "name":"Кот-Тень","unlock_act":3,"color":NEON_PURPLE,
        "desc":"Призрачный кот, умеет видеть слабости.",
        "assist":"atk","assist_name":"Ярость кота (+15 ATK на 10 сек)",
        "lines":{
            "hello":"Мурр. Ты не боишься меня? Смело.",
            "battle":"Тсс... Я укажу слабое место!",
            "low_hp":"Не умирай. Кто меня покормит?",
            "win":"Мурр. Ты стоишь своих осколков.",
        },
    },
    "firefly": {
        "name":"Светлячок","unlock_act":4,"color":NEON_CYAN,
        "desc":"Маленькое существо, что-то помнит.",
        "assist":"auto","assist_name":"Рой (авто-5 нот)",
        "lines":{
            "hello":"Пи-пи! Я так долго ждал тебя!",
            "battle":"Держись — я сбиваю сама!",
            "low_hp":"Пи-пи-пи! Ты должен жить!",
            "win":"Мы вместе! Мы всё смогли!",
        },
    },
    "ancestor": {
        "name":"Дух-Предок","unlock_act":5,"color":NEON_GREEN,
        "desc":"Тот, кто начал эхо — но был забыт.",
        "assist":"mega_heal","assist_name":"Дыхание предка (полное HP + DEF)",
        "lines":{
            "hello":"Я слышал тебя сквозь века.",
            "battle":"Возьми мою силу — она твоя по праву.",
            "low_hp":"Я держу твою нить. Восстань!",
            "win":"Ты закончил то, что я не смог.",
        },
    },
}
COMPANION_ORDER = ["lira","guide","cat","firefly","ancestor"]


# ═══════════════════════ ЛОКАЦИИ ═══════════════════════
def LOC(name,desc,artifact,artifact_desc,battle_text,shadow,story,loot,
        puzzle,hint,battle,enemy,scene=None):
    return {"name":name,"desc":desc,"artifact":artifact,
            "artifact_desc":artifact_desc,"battle_text":battle_text,
            "shadow":shadow,"story":story,"loot":loot,"puzzle":puzzle,
            "hint":hint,"battle":battle,"enemy":enemy,
            "scene":scene or name.lower().replace(" ","_")}

ACT1 = {
 "park":LOC("Старый парк",
  "Ржавые качели скрипят на ветру. Деревья застыли\nв безмолвии, а на пыльных дорожках не осталось следов.",
  "Скрип качелей",
  "Ты касаешься холодного металла — и в воздухе\nповисает тонкий скрип. Это эхо детского смеха.",
  "*Скрип качелей разносится по парку...*","Тень Ребёнка",
  "Я помню! Я играл здесь с мамой, и она смеялась...\nСпасибо, что вернул мне этот день.",
  [("scarf",85),(None,15)],None,"Мягкий ритм — все клавиши, неспешно.",
  {"keys":[0,1,2,3],"spawn":55,"speed":3,"notes":18,"window":100,"start":55},
  {**ENEMY_TEMPLATES["guard"],"hp":60,"attack":6}),
 "cafe":LOC("Заброшенное кафе",
  "Пыльные столики и опрокинутые стулья. За стойкой\nзастыло время, а в воздухе висит запах старого кофе.",
  "Звон разбитой чашки",
  "На полу — осколки фарфора. Ты собираешь их\nв ладони, и звон разбитой чашки наполняет пустоту.",
  "*Звон разбитой чашки отражается от стен...*","Тень Официантки",
  "Я помню этот звон... Спасибо, что не дал мне забыть.",
  [("apron",85),(None,15)],None,"Быстрый перезвон — только D и F.",
  {"keys":[2,3],"spawn":45,"speed":4,"notes":16,"window":95,"start":55},
  {**ENEMY_TEMPLATES["crawler"],"hp":50,"attack":7}),
 "house":LOC("Разрушенный дом",
  "Обрушенные стены, обугленные балки. Здесь когда-то\nжила семья, а теперь лишь ветер гуляет по комнатам.",
  "Колыбельная матери",
  "Из-под обломков доносится тихая колыбельная.\nТы записываешь её в аудио-слепок, и мелодия дрожит.",
  "*Колыбельная матери льётся сквозь руины...*","Тень Матери",
  "Мой сын... Я пела ему каждый вечер. Благодарю.",
  [("shawl",75),(None,25)],None,"Медленная колыбельная — A и S, широкое окно.",
  {"keys":[0,1],"spawn":65,"speed":2,"notes":14,"window":120,"start":60},
  ENEMY_TEMPLATES["boss_1"]),
 "library":LOC("Тихая библиотека",
  "Высокие стеллажи уходят во тьму. Книги покрыты пылью\nвеков, и только лёгкий сквозняк перелистывает страницы.",
  "Шелест страниц",
  "Ты проводишь рукой по корешкам — и воздух\nнаполняется тихим шелестом. Это голос читателя.",
  "*Шелест страниц наполняет тишину зала...*","Тень Библиотекаря",
  "Я помню каждую книгу здесь... Спасибо, что вернул мне голос.",
  [("glasses",70),(None,30)],None,"Плотный поток нот — все клавиши, быстро.",
  {"keys":[0,1,2,3],"spawn":42,"speed":4,"notes":22,"window":90,"start":55},
  {**ENEMY_TEMPLATES["hunter"],"hp":85,"attack":10}),
 "lighthouse":LOC("Одинокий маяк",
  "Волны бьются о каменные стены. Маяк давно погас,\nно в его глубине всё ещё живёт эхо давнего сигнала.",
  "Гудок корабля",
  "Из тумана доносится протяжный гудок. Ты\nзаписываешь его в аудио-слепок, и море затихает.",
  "*Гудок корабля плывёт сквозь туман...*","Тень Смотрителя",
  "Я зажигал огонь для моряков каждую ночь... Ты вернул мне свет.",
  [("lantern",55),(None,45)],None,"Редкие гудки — только A и F, широкое окно.",
  {"keys":[0,3],"spawn":80,"speed":3,"notes":10,"window":130,"start":60},
  {**ENEMY_TEMPLATES["boss_1"],"hp":170,"attack":20,"name":"Владыка Маяка"}),
 "station":LOC("Мёртвый вокзал",
  "Пустые платформы, застывшие часы. Поезда больше не\nприходят, но на рельсах дрожит память о последнем пути.",
  "Свисток поезда",
  "Ты прикладываешь руку к рельсам — и слышишь\nдалёкий свисток. Последний поезд уходит в ночь.",
  "*Свисток поезда дрожит в мёртвой тишине...*","Тень Машиниста",
  "Последний рейс... Спасибо, что дал вспомнить путь.",
  [("cloak",55),(None,45)],None,"Ритм колёс — все клавиши, ровный темп.",
  {"keys":[0,1,2,3],"spawn":48,"speed":4,"notes":20,"window":92,"start":55},
  {**ENEMY_TEMPLATES["boss_1"],"hp":190,"attack":21,"name":"Станционный Призрак"}),
}

ACT2 = {
 "mirror_hall":LOC("Зеркальный зал",
  "Стены — сплошные зеркала. Отражения двигаются\nмедленнее, чем ты, и смотрят прямо в душу.",
  "Отражённый шёпот","Ты приближаешься к зеркалу, и оно шепчет\nчужую историю.",
  "*Шёпот отражений дрожит между зеркал...*","Тень Отражения",
  "Я — то, чем был каждый, кто здесь смотрелся. Спасибо.",
  [("crystal",60),(None,40)],"match","Сложный ритм — все клавиши, узкое окно.",
  {"keys":[0,1,2,3],"spawn":38,"speed":5,"notes":26,"window":82,"start":50},
  {**ENEMY_TEMPLATES["hunter"],"hp":100,"attack":12}),
 "clock_tower":LOC("Часовая башня",
  "Огромные шестерни вращаются в пустоте. Часы\nидут назад, и стрелки дрожат, будто боятся времени.",
  "Ход шестерён","Ты прижимаешь ухо к стене — и слышишь мерный\nход шестерён.",
  "*Ход шестерён отбивает старый ритм...*","Тень Часовщика",
  "Я чинил эти часы сотни лет. Спасибо тебе.",
  [("silver",55),(None,45)],"order","Ровный ритм — все клавиши, но быстро.",
  {"keys":[0,1,2,3],"spawn":42,"speed":5,"notes":24,"window":85,"start":50},
  {**ENEMY_TEMPLATES["hunter"],"hp":110,"attack":13}),
 "garden":LOC("Сад теней",
  "Призрачные цветы распускаются и увядают в один\nмиг. Здесь когда-то гуляли влюблённые.",
  "Шелест лепестков","Ты ловишь лепесток в воздухе — и он\nшуршит чей-то смех.",
  "*Шелест лепестков кружится в воздухе...*","Тень Садовника",
  "Каждый цветок — чьё-то воспоминание. Спасибо.",
  [("starmap",55),(None,45)],"math","Плавный ритм — все клавиши, широкое окно.",
  {"keys":[0,1,2,3],"spawn":46,"speed":4,"notes":20,"window":95,"start":55},
  {**ENEMY_TEMPLATES["guard"],"hp":90,"attack":11}),
 "chapel":LOC("Затонувшая часовня",
  "Часовня ушла под воду, но свечи всё ещё горят\nпод водой. Молитвы здесь не слышны, но живы.",
  "Подводный хорал","Ты закрываешь глаза — и слышишь хор голосов.",
  "*Хорал плывёт сквозь толщу воды...*","Тень Служителя",
  "Я хранил эти свечи для тех, кто молился. Спасибо.",
  [("quill",45),(None,55)],"cipher","Медленный хорал — A и F, широкое окно.",
  {"keys":[0,3],"spawn":55,"speed":4,"notes":18,"window":110,"start":55},
  {**ENEMY_TEMPLATES["hunter"],"hp":120,"attack":14}),
 "cellar":LOC("Кристальный погреб",
  "Подземелье полно светящихся кристаллов. Они\nпульсируют в такт чему-то далёкому и тёмному.",
  "Гул кристаллов","Ты касаешься кристалла — и он гудит\nна одной ноте с твоим сердцем.",
  "*Гул кристаллов дрожит в темноте...*","Тень Рудокопа",
  "Я искал свет всю жизнь в этой тьме. Спасибо тебе.",
  [("compass",45),(None,55)],"lights","Рваный ритм — все клавиши, узкое окно.",
  {"keys":[0,1,2,3],"spawn":40,"speed":5,"notes":26,"window":80,"start":50},
  {**ENEMY_TEMPLATES["hunter"],"hp":130,"attack":15}),
 "observatory":LOC("Обсерватория",
  "Купол открыт звёздам, но телескоп смотрит в пол.\nЗдесь кто-то искал ответы в небе — и не нашёл.",
  "Песня звёзд","Ты смотришь в окуляр — и звёзды поют.",
  "*Песня звёзд льётся сквозь купол...*","Тень Астронома",
  "Я искал во вселенной хоть кого-то. Благодарю.",
  [("moonstone",50),(None,50)],"memory","Финальный сложный ритм акта.",
  {"keys":[0,1,2,3],"spawn":36,"speed":5,"notes":28,"window":78,"start":48},
  {**ENEMY_TEMPLATES["boss_2"],"hp":220,"attack":22,"name":"Хранитель Обсерватории"}),
}

ACT3 = {
 "theatre":LOC("Старый театр",
  "Кресла затянуты бархатом, но пыль покрывает сцену.\nЗанавес застыл в полупоклоне, будто ждёт актёра.",
  "Аплодисменты","Ты хлопаешь в ладоши — и зал наполняется эхом\nчужих аплодисментов.",
  "*Аплодисменты гремят в пустом зале...*","Тень Актёра",
  "Я играл здесь сотни ролей... Спасибо, что дал мне сцену.",
  [("theatre_mask",45),("chip",20),(None,35)],"simon","Сложный ритм, длинная последовательность.",
  {"keys":[0,1,2,3],"spawn":34,"speed":6,"notes":30,"window":78,"start":48},
  {**ENEMY_TEMPLATES["hunter"],"hp":140,"attack":16}),
 "casino":LOC("Игорный дом",
  "Рулетка всё ещё крутится. Карты лежат открытыми,\nно игроков давно нет.",
  "Звон фишек","Ты сжимаешь фишки в ладони — и слышишь звон\nудачи.",
  "*Звон фишек дрожит над рулеткой...*","Тень Игрока",
  "Последняя ставка... Спасибо, что напомнил имя.",
  [("chip",55),(None,45)],"lights","Рваный ритм — очень узкое окно.",
  {"keys":[0,1,2,3],"spawn":32,"speed":6,"notes":32,"window":75,"start":45},
  {**ENEMY_TEMPLATES["hunter"],"hp":150,"attack":17}),
 "hotel":LOC("Заброшенный отель",
  "Коридоры уходят в бесконечность. Двери открыты,\nно за ними — только темнота и старые ключи.",
  "Скрип половиц","Ты идёшь по коридору — и половицы стонут\nпод ногами.",
  "*Скрип половиц плывёт по коридору...*","Тень Постояльца",
  "Я жил здесь, когда был никем... Спасибо, что вспомнил.",
  [("key_hotel",50),(None,50)],"memory","Медленный ритм.",
  {"keys":[0,1,2,3],"spawn":40,"speed":5,"notes":24,"window":85,"start":50},
  {**ENEMY_TEMPLATES["boss_2"],"hp":240,"attack":24,"name":"Хозяин Отеля"}),
 "court":LOC("Старый суд",
  "Скамьи присяжных пусты, но вердикт всё ещё висит\nв воздухе. Здесь кто-то был признан невиновным.",
  "Удар молотка","Ты берёшь молоток — и тишина взрывается\nударом.",
  "*Удар молотка раскалывает тишину...*","Тень Судьи",
  "Я вынес вердикт, но сам не был прощён. Спасибо.",
  [("gavel",40),(None,60)],"order","Точный ритм — A и F.",
  {"keys":[0,3],"spawn":50,"speed":5,"notes":20,"window":100,"start":50},
  {**ENEMY_TEMPLATES["hunter"],"hp":160,"attack":18}),
 "factory":LOC("Мёртвая фабрика",
  "Станки застыли на полпути. Что-то так и не было\nсобрано до конца.",
  "Лязг металла","Ты прикасаешься к шестерне — и она ворочается\nсо скрипом.",
  "*Лязг металла дрожит в цехах...*","Тень Мастера",
  "Я собирал механизмы всю жизнь... Спасибо.",
  [("gear",40),(None,60)],"slider","Тяжёлый ритм.",
  {"keys":[0,1,2,3],"spawn":44,"speed":5,"notes":26,"window":88,"start":50},
  {**ENEMY_TEMPLATES["boss_2"],"hp":250,"attack":25,"name":"Главный Мастер"}),
 "alley":LOC("Тёмный переулок",
  "Фонари здесь давно не горят. Только тени шныряют\nпо стенам, и кажется, будто за тобой следят.",
  "Шёпот в темноте","Ты замираешь — и слышишь чужие голоса,\nшепчущие имена. Одно из них — твоё.",
  "*Шёпот в темноте становится громче...*","Тень Прохожего",
  "Я шёл мимо сотню раз... Спасибо, что остановился.",
  [("mask_owl",35),(None,65)],"arrows","Тихий ритм — длинная последовательность.",
  {"keys":[0,1,2,3],"spawn":30,"speed":6,"notes":34,"window":75,"start":45},
  {**ENEMY_TEMPLATES["boss_3"],"hp":280,"attack":27,"name":"Первый Шёпот"}),
}

ACT4 = {
 "reef":LOC("Коралловый риф",
  "Тысячи кораллов пульсируют в такт океану.\nРыбы застыли, будто их поймали в стекло.",
  "Шёпот рифа","Ты касаешься коралла — и он отвечает песней\nбез слов.",
  "*Шёпот рифа плывёт в толще воды...*","Тень Ныряльщика",
  "Я искал жемчуг всю жизнь. Спасибо, что вернул голос.",
  [("coral",40),(None,60)],"math","Долгая последовательность.",
  {"keys":[0,1,2,3],"spawn":30,"speed":6,"notes":32,"window":76,"start":46},
  {**ENEMY_TEMPLATES["hunter"],"hp":170,"attack":18}),
 "wreck":LOC("Затонувший корабль",
  "Огромный парусник лежит на дне, мачты покрыты\nракушками. Трюм полон чьих-то снов.",
  "Скрип трюма","Ты спускаешься в трюм — и слышишь скрип дерева.",
  "*Скрип трюма дрожит под водой...*","Тень Капитана",
  "Я вёл этот корабль сквозь шторма. Спасибо за экипаж.",
  [("trident",20),("shell",30),(None,50)],"slider","Сложная сетка огней.",
  {"keys":[0,1,2,3],"spawn":28,"speed":6,"notes":34,"window":74,"start":45},
  {**ENEMY_TEMPLATES["boss_3"],"hp":300,"attack":28,"name":"Капитан Затонувших"}),
 "grotto":LOC("Грот сирен",
  "Свет пробивается сквозь воду, отражаясь от стен.\nТы слышишь пение — но не можешь понять слова.",
  "Пение сирен","Ты закрываешь глаза — и голоса становятся\nяснее.",
  "*Пение сирен дрожит в гроте...*","Тень Сирены",
  "Я пела морякам, но не знала, о чём. Спасибо, что научил.",
  [("pearl",35),(None,65)],"cipher","Запомни числа — их много.",
  {"keys":[0,1,2,3],"spawn":32,"speed":6,"notes":28,"window":80,"start":48},
  {**ENEMY_TEMPLATES["hunter"],"hp":180,"attack":19}),
 "abyss":LOC("Бездна",
  "Свет сюда не доходит. Только ты и пустота,\nи чей-то взгляд из глубины.",
  "Вздох бездны","Ты задерживаешь дыхание — и слышишь\nчужой вздох.",
  "*Вздох бездны дрожит в пустоте...*","Тень Утонувшего",
  "Я ушёл на дно, но не умер... Спасибо, что напомнил.",
  [("abyss_ring",15),(None,85)],"arrows","Очень сложная сетка огней.",
  {"keys":[0,1,2,3],"spawn":26,"speed":7,"notes":36,"window":72,"start":44},
  {**ENEMY_TEMPLATES["boss_3"],"hp":320,"attack":30,"name":"Владыка Бездны"}),
 "sunken_town":LOC("Подводный город",
  "Дома тянутся вверх, будто пытаются всплыть.\nОкна светятся изнутри — но там давно никого.",
  "Городской гул","Ты прижимаешься к стене — и слышишь далёкий\nгул.",
  "*Городской гул плывёт в глубине...*","Тень Горожанина",
  "Мы жили здесь, пока вода не пришла. Спасибо.",
  [("scale",15),(None,85)],"slider","Самый длинный эхо-повтор.",
  {"keys":[0,1,2,3],"spawn":26,"speed":7,"notes":38,"window":72,"start":42},
  {**ENEMY_TEMPLATES["hunter"],"hp":190,"attack":20}),
 "trench":LOC("Морская впадина",
  "Дно уходит в бесконечность. Здесь время\nне имеет значения, и смерть — не конец.",
  "Тишина бездны","Ты стоишь на самом дне — и слышишь полную\nтишину.",
  "*Тишина бездны поглощает всё...*","Тень Забытого",
  "Я — тот, кого не помнит никто. Спасибо, что пришёл.",
  [("last_voice",15),(None,85)],"cipher","Запомни как можно больше чисел.",
  {"keys":[0,1,2,3],"spawn":28,"speed":7,"notes":32,"window":78,"start":46},
  {**ENEMY_TEMPLATES["boss_3"],"hp":340,"attack":31,"name":"Тот, кого Забыли"}),
}

ACT5 = {
 "echo_hall":LOC("Зал Эха",
  "Ты стоишь в зале, где каждое слово звучит вечно.\nЗдесь собраны все голоса, что были потеряны.",
  "Хор голосов","Все, кого ты спас, звучат здесь одновременно.",
  "*Хор голосов наполняет Зал Эха...*","Тень Хранителя",
  "Я хранил эти голоса вечность. Спасибо тебе, странник.",
  [("echo_heart",100)],"chain","Три головоломки подряд. Готов?",
  {"keys":[0,1,2,3],"spawn":28,"speed":6,"notes":30,"window":80,"start":50},
  {**ENEMY_TEMPLATES["boss_3"],"hp":350,"attack":30,"name":"Хранитель Голосов"}),
 "memory_vault":LOC("Хранилище Памяти",
  "Полки уходят в бесконечность. На каждой —\nчья-то жизнь, застывшая в стекле.",
  "Шёпот хранилища","Ты берёшь одну из сфер — и она рассказывает\nисторию.",
  "*Шёпот хранилища дрожит в тишине...*","Тень Архивариуса",
  "Я подписывал каждую жизнь. Благодарю.",
  [("last_voice",60),(None,40)],"chain","Три головоломки подряд.",
  {"keys":[0,1,2,3],"spawn":26,"speed":7,"notes":32,"window":78,"start":48},
  {**ENEMY_TEMPLATES["boss_3"],"hp":380,"attack":32,"name":"Хранитель Имён"}),
}

ACT6 = {
 "heart":LOC("Сердце города",
  "Ты стоишь в самом центре Забытого Города. Здесь\nбьётся его сердце — и оно почти остановилось.",
  "Первый звук","Ты собираешь эхо всех голосов города\nв единый аудио-слепок.",
  "*Все голоса города звучат в унисон...*","Первый Голос",
  "Я — каждый, кто жил здесь. И я снова целый. Спасибо.",
  [("crown",100)],None,"Финальная битва. Ты готов?",
  {"keys":[0,1,2,3],"spawn":22,"speed":8,"notes":42,"window":70,"start":45},
  ENEMY_TEMPLATES["final"]),
 "echo_throne":LOC("Трон Эха",
  "Пустой трон парит в воздухе. Вокруг — только\nтишина и ожидание последнего слова.",
  "Последнее слово","Ты слышишь его — самое последнее слово\nв этом мире.",
  "*Последнее слово рождает целый мир...*","Хозяин Тишины",
  "Я создал тишину. И только ты смог её разбить. Спасибо.",
  [("last_voice",100)],None,"Финальный босс — Хозяин Тишины.",
  {"keys":[0,1,2,3],"spawn":20,"speed":8,"notes":46,"window":68,"start":42},
  {**ENEMY_TEMPLATES["final"],"hp":500,"attack":35,"name":"Хозяин Тишины"}),
}

ALL_LOCATIONS = {}
for d in (ACT1,ACT2,ACT3,ACT4,ACT5,ACT6): ALL_LOCATIONS.update(d)

ACTS = {
 1:{"name":"Акт I — Пробуждение","sub":"Первые голоса","locs":list(ACT1.keys()),"color":NEON_CYAN},
 2:{"name":"Акт II — Глубина","sub":"Город раскрывает тайны","locs":list(ACT2.keys()),"color":NEON_PURPLE},
 3:{"name":"Акт III — Городские тайны","sub":"Тени прошлого","locs":list(ACT3.keys()),"color":NEON_GOLD},
 4:{"name":"Акт IV — Затонувший мир","sub":"Скрытое водой","locs":list(ACT4.keys()),"color":NEON_BLUE},
 5:{"name":"Акт V — Последнее эхо","sub":"Возвращение к истоку","locs":list(ACT5.keys()),"color":NEON_RED},
 6:{"name":"Акт VI — Финал","sub":"Последний бой","locs":list(ACT6.keys()),"color":NEON_ORANGE},
}

def _b(x,y,r): return {"x":x,"y":y,"r":r}
ACT_BUILDINGS = {
 1:{"park":_b(160,175,78),"cafe":_b(480,140,74),"house":_b(800,175,78),
    "library":_b(160,545,78),"lighthouse":_b(480,565,74),"station":_b(800,545,78)},
 2:{k:_b(int(WIDTH//2+math.cos(math.pi*2*i/6-math.pi/2)*320),
          int(HEIGHT//2+20+math.sin(math.pi*2*i/6-math.pi/2)*220),76)
    for i,k in enumerate(ACT2.keys())},
 3:{k:_b(int(WIDTH//2+math.cos(math.pi*2*i/6+0.3)*320),
          int(HEIGHT//2+20+math.sin(math.pi*2*i/6+0.3)*220),78)
    for i,k in enumerate(ACT3.keys())},
 4:{k:_b(int(WIDTH//2+math.cos(math.pi*2*i/6-0.4)*320),
          int(HEIGHT//2+20+math.sin(math.pi*2*i/6-0.4)*220),78)
    for i,k in enumerate(ACT4.keys())},
 5:{"echo_hall":_b(240,260,85),"memory_vault":_b(720,260,85)},
 6:{"heart":_b(300,350,90),"echo_throne":_b(660,350,90)},
}
for a in (2,3,4):
    for k,b in ACT_BUILDINGS[a].items():
        b["x"]=max(90,min(WIDTH-90,b["x"]))
        b["y"]=max(80,min(HEIGHT-90,b["y"]))

UP_KEYS={pygame.K_w,pygame.K_UP}; DOWN_KEYS={pygame.K_s,pygame.K_DOWN}
LEFT_KEYS={pygame.K_a,pygame.K_LEFT}; RIGHT_KEYS={pygame.K_d,pygame.K_RIGHT}


# ═══════════════════════ ГЕНЕРАЦИЯ ЗВУКОВ ═══════════════════════
def make_tone(freq,ms,vol=0.3,wave="sine",fade_in=0.005,fade_out=0.1):
    n=int(SAMPLE_RATE*ms/1000); buf=array.array('h')
    attack=max(1,int(SAMPLE_RATE*fade_in)); release=max(1,int(SAMPLE_RATE*fade_out))
    for i in range(n):
        t=i/SAMPLE_RATE
        if wave=="square": v=1.0 if math.sin(2*math.pi*freq*t)>0 else -1.0
        elif wave=="saw": v=2.0*((freq*t)%1.0)-1.0
        else: v=math.sin(2*math.pi*freq*t)
        env=1.0
        if i<attack: env=i/attack
        elif i>n-release: env=max(0.0,(n-i)/release)
        s=int(32767*vol*env*v); buf.append(s); buf.append(s)
    return pygame.mixer.Sound(buffer=buf.tobytes())


def make_chord(freqs,ms,vol=0.3):
    n=int(SAMPLE_RATE*ms/1000); buf=array.array('h')
    attack=max(1,int(SAMPLE_RATE*0.01)); release=max(1,int(SAMPLE_RATE*0.4))
    for i in range(n):
        t=i/SAMPLE_RATE
        v=sum(math.sin(2*math.pi*f*t) for f in freqs)/len(freqs)
        env=1.0
        if i<attack: env=i/attack
        elif i>n-release: env=max(0.0,(n-i)/release)
        s=int(32767*vol*env*v); buf.append(s); buf.append(s)
    return pygame.mixer.Sound(buffer=buf.tobytes())


def make_sweep(f1,f2,ms,vol=0.3):
    n=int(SAMPLE_RATE*ms/1000); buf=array.array('h'); phase=0.0
    for i in range(n):
        t=i/n; freq=f1+(f2-f1)*t
        phase+=2*math.pi*freq/SAMPLE_RATE
        env=1.0-t
        s=int(32767*vol*env*math.sin(phase)); buf.append(s); buf.append(s)
    return pygame.mixer.Sound(buffer=buf.tobytes())


def make_drone(freq=80.0,ms=2000,vol=0.06):
    n=int(SAMPLE_RATE*ms/1000); buf=array.array('h')
    for i in range(n):
        t=i/SAMPLE_RATE
        v=math.sin(2*math.pi*freq*t)
        v*=0.7+0.3*math.sin(2*math.pi*0.5*t)
        s=int(32767*vol*v); buf.append(s); buf.append(s)
    return pygame.mixer.Sound(buffer=buf.tobytes())


# ─── Музыка: бесшовный цикл длиной ~4 сек ───
def make_music_track(notes, ms=4000, vol=0.08, tempo_ms=500,
                      bass_freq=None, wave="sine", style="pad"):
    """
    notes: список частот — проигрываются по кругу в tempo_ms
    Если длина цикла кратна длине notes*tempo_ms, стык бесшовный.
    """
    total = int(SAMPLE_RATE * ms / 1000)
    per_note = int(SAMPLE_RATE * tempo_ms / 1000)
    if bass_freq is None: bass_freq = notes[0] / 2
    buf = array.array('h')
    # Делаем длину кратной одной ноте
    if total % per_note != 0:
        total = (total // per_note) * per_note
    if total == 0: total = per_note
    for i in range(total):
        note_idx = (i // per_note) % len(notes)
        freq = notes[note_idx]
        t = i / SAMPLE_RATE
        pos = (i % per_note) / per_note
        # мягкая огибающая внутри ноты
        env = math.sin(math.pi * pos) if style == "bell" else (1.0 - pos * 0.3)
        if wave == "square": v = 1.0 if math.sin(2*math.pi*freq*t) > 0 else -1.0
        elif wave == "saw": v = 2.0 * ((freq*t) % 1.0) - 1.0
        else: v = math.sin(2 * math.pi * freq * t)
        bass = math.sin(2 * math.pi * bass_freq * t) * 0.4
        s = int(32767 * vol * env * (v + bass))
        buf.append(s); buf.append(s)
    return pygame.mixer.Sound(buffer=buf.tobytes())


def make_drum_loop(ms=4000, vol=0.12, kick_ms=100, bpm=120):
    """Простой басовый барабан + щелчок для боевых тем."""
    total = int(SAMPLE_RATE * ms / 1000)
    beat = int(SAMPLE_RATE * 60 / bpm)
    if total % beat != 0: total = (total // beat) * beat
    buf = array.array('h')
    for i in range(total):
        t = i / SAMPLE_RATE
        pos_in_beat = (i % beat) / beat
        # Kick в начале каждой доли
        kick_env = math.exp(-pos_in_beat * 12)
        kick = math.sin(2 * math.pi * 60 * t) * kick_env
        # Хай-хэт каждые полдоли
        half = (i % (beat // 2)) / (beat // 2)
        hat_env = math.exp(-half * 40)
        hat = (random.random() * 2 - 1) * hat_env * 0.15
        s = int(32767 * vol * (kick + hat))
        buf.append(s); buf.append(s)
    return pygame.mixer.Sound(buffer=buf.tobytes())


# ═══════════════════════════ ИГРА ═══════════════════════════
class EchoLocationGame:
    KEYS=["a","s","d","f"]; KEY_LETTERS=["A","S","D","F"]
    KEY_COLORS=[NEON_CYAN,NEON_PINK,NEON_PURPLE,NEON_GOLD]
    KEY_FREQS=[440,554,659,784]

    ST_MENU="menu"; ST_MAP="map"; ST_LOCATION="location"; ST_COLLECT="collect"
    ST_BATTLE="battle"; ST_WIN="win"; ST_LOSE="lose"; ST_END="end"
    ST_INV="inventory"; ST_PUZZLE="puzzle"; ST_ACT_INTRO="act_intro"
    ST_SHOP="shop"; ST_COMPANIONS="companions"

    def __init__(self):
        pygame.mixer.pre_init(SAMPLE_RATE, -16, 2, 512)
        pygame.init()
        try:
            pygame.mixer.init(SAMPLE_RATE, -16, 2, 512); self.audio_ok=True
        except pygame.error:
            self.audio_ok=False
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Эхо-Локация")
        self.clock=pygame.time.Clock()

        # Шрифты
        self.f_title=pygame.font.SysFont("georgia",56,bold=True)
        self.f_big=pygame.font.SysFont("georgia",32,bold=True)
        self.f_head=pygame.font.SysFont("georgia",22,bold=True)
        self.f_sub=pygame.font.SysFont("georgia",18,italic=True)
        self.f_body=pygame.font.SysFont("georgia",17)
        self.f_small=pygame.font.SysFont("georgia",14)
        self.f_tiny=pygame.font.SysFont("georgia",12,bold=True)
        self.f_btn=pygame.font.SysFont("georgia",17,bold=True)
        self.f_note=pygame.font.SysFont("consolas",30,bold=True)
        self.f_key=pygame.font.SysFont("consolas",24,bold=True)
        self.f_bar=pygame.font.SysFont("georgia",15,bold=True)
        self.f_mono=pygame.font.SysFont("consolas",16,bold=True)
        self.f_arrow=pygame.font.SysFont("consolas",48,bold=True)

        # Состояние
        self.state=self.ST_MENU; self.act=1
        self.buildings=ACT_BUILDINGS[self.act]
        self.sounds_found=set(); self.done=set(); self.puzzles_done=set()
        self.current_loc=None; self.nearby_building=None; self.visited=set()

        self.inventory=set(); self.equipped={}
        self.reward_popup=None; self.drops_this_fight=[]

        self.shards=0; self.potions={}
        self.weapons_owned={"wood_stick"}; self.weapon="wood_stick"

        self.base_max_hp=100; self.base_atk=0; self.base_def=0
        self.max_hp=self.base_max_hp; self.player_hp=self.max_hp
        self.epic_elixir_received=False

        # Компаньоны (НОВОЕ)
        self.companions=set()           # разблокированные
        self.active_companion=None      # выбранный для боя
        self.companion_message=""
        self.companion_msg_timer=0
        self.companion_assist_used=False
        self.companion_atk_bonus=0
        self.companion_window_bonus=0
        self.companion_buff_timer=0

        # Игрок
        self.player={"x":WIDTH//2,"y":HEIGHT-100,"anim":0,
                     "moving":False,"facing":"up"}
        self.keys_held=set()

        # Бой
        self.notes=[]; self.spawn_timer=0; self.total_spawned=0
        self.col_x=[200,380,560,740]; self.active_keys=[0,1,2,3]
        self.target_y=400; self.spawn_interval=50; self.speed=3
        self.max_notes=20; self.hit_window=90
        self.feedback_text=""; self.feedback_color=NEON_CYAN
        self.feedback_timer=0
        self.battle_flash=0; self.hit_flash=0; self.hurt_flash=0
        self.key_cd=[0,0,0,0]; self.enemy=None
        self.enemy_mods=[]; self.note_style="normal"
        self.boss_phase2=False; self.safe_window=0
        self.player_invuln=0; self.player_combo=0; self.combo_dmg_bonus=0
        self.enemy_combo=0
        # VFX финального босса
        self.shake_timer=0; self.shake_mag=0
        self.lightning_timer=0
        self.particles=[]

        # Головоломка
        self.puzzle_kind=None; self.puzzle={}
        self.puzzle_message=""; self.puzzle_msg_timer=0
        self.puzzle_chain=[]; self.chain_index=0

        # Таймер
        self.game_start_time=None; self.elapsed=0.0; self.final_time=0.0

        # UI
        self.buttons=[]; self.hover_index=-1; self.time_accum=0
        self.msg_toast=""; self.msg_toast_timer=0  # всплывающие сообщения

        # Звуки
        self.sfx={}; self._create_sfx()
        self._start_ambient()

        # МУЗЫКА
        self.music={}; self.music_channel=None
        self.current_music=""
        if self.audio_ok:
            try:
                self.music_channel=pygame.mixer.Channel(1)
                self.music_channel.set_volume(0.6)
            except Exception:
                self.music_channel=None
        self._create_music()

        # Предрендер
        self.map_surfaces={a:self._build_map_surface(a) for a in [1,2,3,4,5,6]}
        self.building_surfaces={k:self._render_building(k) for k in ALL_LOCATIONS}
        self.aura_pink=self._make_aura_surface(130,NEON_PINK)
        self.aura_gold=self._make_aura_surface(130,NEON_GOLD)
        self.aura_puzzle=self._make_aura_surface(130,NEON_PURPLE)
        self.aura_boss=self._make_aura_surface(150,NEON_RED)

        self.running=True

    # ─── ЗВУКИ ───
    def _create_sfx(self):
        if not self.audio_ok: return
        try:
            self.sfx["click"]=make_tone(1200,40,0.12)
            self.sfx["hit"]=[make_tone(f,180,0.25) for f in self.KEY_FREQS]
            self.sfx["miss"]=make_tone(140,200,0.18,wave="square")
            self.sfx["collect"]=make_chord([659,880],500,0.25)
            self.sfx["win"]=make_chord([523,659,784,1046],900,0.28)
            self.sfx["lose"]=make_sweep(300,80,700,0.22)
            self.sfx["equip"]=make_chord([660,990],260,0.2)
            self.sfx["puzzle"]=make_chord([520,660,880],300,0.22)
            self.sfx["solve"]=make_chord([660,880,1100,1320],700,0.28)
            self.sfx["error"]=make_tone(220,200,0.25,wave="square")
            self.sfx["tile"]=[make_tone(f,90,0.18) for f in [523,659,784,1046]]
            self.sfx["drop"]=make_chord([880,1320,1760],500,0.22)
            self.sfx["legendary"]=make_chord([523,659,784,1046,1318],1200,0.3)
            self.sfx["purchase"]=make_chord([880,1320],500,0.28)
            self.sfx["heal"]=make_chord([440,660,880,1100],600,0.3)
            self.sfx["boss"]=make_chord([110,220,330],1500,0.25)
            self.sfx["combo"]=make_chord([880,1100,1320],250,0.22)
            self.sfx["shield"]=make_chord([660,990,1320],300,0.22)
            self.sfx["companion"]=make_chord([550,825,1100],600,0.26)
            self.sfx["thunder"]=make_sweep(200,60,900,0.25)
            self.sfx["drone"]=make_drone(80.0,2000,0.06)
        except Exception:
            self.audio_ok=False

    def _start_ambient(self):
        if not self.audio_ok or "drone" not in self.sfx: return
        try:
            self.ambient=pygame.mixer.Channel(0)
            self.ambient.set_volume(0.35)
            self.ambient.play(self.sfx["drone"],loops=-1)
        except Exception: pass

    def _play(self,name):
        if not self.audio_ok or name not in self.sfx: return
        try:
            s=self.sfx[name]
            if isinstance(s,list): random.choice(s).play()
            else: s.play()
        except Exception: pass

    def _play_index(self,name,idx):
        if not self.audio_ok or name not in self.sfx: return
        try: self.sfx[name][idx].play()
        except Exception: pass

    # ─── МУЗЫКА ───
    def _create_music(self):
        if not self.audio_ok: return
        try:
            # Меню — минорный гул, медленный
            self.music["menu"]=make_music_track(
                [220, 261.6, 329.6, 261.6], ms=4000, vol=0.08, tempo_ms=1000,
                style="pad")
            # Карта — нейтральная атмосфера
            self.music["map"]=make_music_track(
                [196, 246.9, 293.7, 246.9], ms=4000, vol=0.07, tempo_ms=1000,
                style="pad")
            # Бой — ритмичная, выше
            battle=make_music_track(
                [329.6, 392, 440, 392], ms=2000, vol=0.07, tempo_ms=250,
                style="pad")
            self.music["battle"]=battle
            # Босс — тяжелее
            self.music["boss"]=make_music_track(
                [220, 261.6, 293.7, 261.6], ms=2000, vol=0.09, tempo_ms=200,
                bass_freq=55, style="pad")
            # Финальный босс — быстрая и мощная
            self.music["final"]=make_music_track(
                [440, 523, 587, 659, 587, 523], ms=3000, vol=0.10, tempo_ms=150,
                bass_freq=82, style="pad")
            # Грустная — нисходящая
            self.music["sad"]=make_music_track(
                [329.6, 293.7, 261.6, 220], ms=4000, vol=0.08, tempo_ms=1000,
                style="pad")
            # Весёлая — восходящая мажорная
            self.music["happy"]=make_music_track(
                [261.6, 329.6, 392, 523.3], ms=4000, vol=0.08, tempo_ms=1000,
                style="bell")
            # Магазин — лёгкая, звонкая
            self.music["shop"]=make_music_track(
                [523, 659, 784, 659], ms=3000, vol=0.07, tempo_ms=500,
                style="bell")
        except Exception:
            self.music={}

    def set_music(self, name):
        if not self.audio_ok or not self.music_channel: return
        if name == self.current_music: return
        if name not in self.music:
            # Мягкий стоп
            try: self.music_channel.stop()
            except Exception: pass
            self.current_music=""
            return
        try:
            self.music_channel.stop()
            self.music_channel.play(self.music[name], loops=-1)
            self.current_music=name
        except Exception: pass

    # ─── УТИЛИТЫ ───
    def recalc_stats(self):
        mem=0; win=0
        for slot,iid in self.equipped.items():
            item=ITEMS.get(iid)
            if not item: continue
            mem+=item.get("memory_bonus",0); win+=item.get("window_bonus",0)
        self.bonus_memory=mem; self.bonus_window=win
        self.max_hp=self.base_max_hp
        self.player_hp=min(self.player_hp,self.max_hp)

    def get_attack_power(self):
        w=WEAPONS.get(self.weapon,WEAPONS["wood_stick"])
        return w["dmg"]+self.base_atk+self.base_def+self.combo_dmg_bonus+self.companion_atk_bonus

    def total_bonus(self):
        return getattr(self,"bonus_memory",0), getattr(self,"bonus_window",0)

    def get_battle_config(self):
        base=dict(ALL_LOCATIONS[self.current_loc]["battle"])
        mem_b,win_b=self.total_bonus()
        base["start"]=min(85,base["start"]+mem_b)
        base["window"]=base["window"]+win_b+self.companion_window_bonus
        return base

    def get_column_positions(self):
        n=len(self.active_keys)
        if n==4: return [200,380,560,740]
        if n==3: return [240,480,720]
        if n==2: return [320,640]
        return [WIDTH//2]

    def act_all_done(self,act):
        return all(loc in self.done for loc in ACTS[act]["locs"])

    def format_time(self,sec):
        return f"{int(sec)//60:02d}:{int(sec)%60:02d}"

    def update_timer(self):
        if self.game_start_time is not None:
            self.elapsed=_time.time()-self.game_start_time

    def toast(self,text,color=TEXT_WHITE,dur=120):
        self.msg_toast=text; self.msg_color=color; self.msg_toast_timer=dur

    def roll_loot(self,loc_key):
        loot=ALL_LOCATIONS[loc_key].get("loot",[])
        if not loot: return []
        total=sum(w for _,w in loot); r=random.random()*total; acc=0
        for item_id,w in loot:
            acc+=w
            if r<=acc: return [item_id] if item_id else []
        return []

    # ─── КОМПАНЬОНЫ ───
    def unlock_companion(self, cid):
        if cid not in self.companions:
            self.companions.add(cid)
            c=COMPANIONS[cid]
            self.toast(f"◈ Новый компаньон: {c['name']}", c["color"])
            self.companion_message=f"{c['name']}: «{c['lines']['hello']}»"
            self.companion_msg_timer=180
            # Первый становится активным
            if self.active_companion is None:
                self.active_companion=cid
            self._play("companion")
            return True
        return False

    def use_companion_assist(self):
        if self.companion_assist_used: return
        if not self.active_companion: return
        cid=self.active_companion
        c=COMPANIONS[cid]
        self.companion_assist_used=True
        self._play("companion")
        self.companion_message=f"{c['name']}: «{c['lines']['battle']}»"
        self.companion_msg_timer=120

        ability=c["assist"]
        if ability=="heal":
            heal=int(self.max_hp*0.4)
            self.player_hp=min(self.max_hp,self.player_hp+heal)
            self.show_feedback(f"Лира исцеляет +{heal} HP!", NEON_PINK)
        elif ability=="window":
            self.companion_window_bonus=40
            self.companion_buff_timer=480  # 8 сек
            self.show_feedback("Прозрение! Окно расширено!", NEON_GOLD)
        elif ability=="atk":
            self.companion_atk_bonus=15
            self.companion_buff_timer=600  # 10 сек
            self.show_feedback("Ярость кота! +15 ATK!", NEON_PURPLE)
        elif ability=="auto":
            # Автоматически сбить 5 нот
            count=0
            for note in self.notes:
                if not note["hit"] and not note["missed"]:
                    note["hit"]=True; count+=1
                    self.enemy["hp"]=max(0,self.enemy["hp"]-self.get_attack_power())
                    if count>=5: break
            self.show_feedback(f"Рой сбил {count} нот!", NEON_CYAN)
        elif ability=="mega_heal":
            self.player_hp=self.max_hp
            self.base_def+=2
            self.show_feedback("Дыхание предка! Полное HP +2 DEF!", NEON_GREEN)

    # ─── СОХРАНЕНИЕ / ЗАГРУЗКА ───
    def save_game(self):
        data={
            "act":self.act,
            "sounds_found":list(self.sounds_found),
            "done":list(self.done),
            "puzzles_done":list(self.puzzles_done),
            "inventory":list(self.inventory),
            "equipped":self.equipped,
            "shards":self.shards,
            "potions":self.potions,
            "weapons_owned":list(self.weapons_owned),
            "weapon":self.weapon,
            "base_max_hp":self.base_max_hp,
            "base_atk":self.base_atk,
            "base_def":self.base_def,
            "player_hp":self.player_hp,
            "epic_elixir_received":self.epic_elixir_received,
            "companions":list(self.companions),
            "active_companion":self.active_companion,
            "player_x":self.player["x"],
            "player_y":self.player["y"],
            "elapsed":self.elapsed,
            "game_start_time":self.game_start_time,
        }
        try:
            with open(SAVE_FILE,"w",encoding="utf-8") as f:
                json.dump(data,f,ensure_ascii=False,indent=2)
            self.toast("✓ Игра сохранена",NEON_GREEN)
            self._play("collect")
        except Exception as e:
            self.toast(f"Ошибка сохранения: {e}",NEON_RED)

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            self.toast("Сохранение не найдено",NEON_RED); return
        try:
            with open(SAVE_FILE,"r",encoding="utf-8") as f:
                data=json.load(f)
            self.act=data["act"]
            self.buildings=ACT_BUILDINGS[self.act]
            self.sounds_found=set(data["sounds_found"])
            self.done=set(data["done"])
            self.puzzles_done=set(data["puzzles_done"])
            self.inventory=set(data["inventory"])
            self.equipped=dict(data["equipped"])
            self.shards=data["shards"]
            self.potions=dict(data["potions"])
            self.weapons_owned=set(data["weapons_owned"])
            self.weapon=data["weapon"]
            self.base_max_hp=data["base_max_hp"]
            self.base_atk=data["base_atk"]
            self.base_def=data["base_def"]
            self.player_hp=data["player_hp"]
            self.epic_elixir_received=data["epic_elixir_received"]
            self.companions=set(data.get("companions",[]))
            self.active_companion=data.get("active_companion")
            self.player["x"]=data["player_x"]; self.player["y"]=data["player_y"]
            self.elapsed=data["elapsed"]
            self.game_start_time=data.get("game_start_time")
            self.recalc_stats()
            self.state=self.ST_MAP
            self.toast("✓ Игра загружена",NEON_CYAN)
            self._play("collect")
        except Exception as e:
            self.toast(f"Ошибка загрузки: {e}",NEON_RED)

    # ─── КАРТА ───
    def _build_map_surface(self,act):
        random.seed(3000+act); surf=pygame.Surface((WIDTH,HEIGHT))
        base={1:(14,18,20),2:(12,12,24),3:(18,14,22),4:(10,16,26),
              5:(22,10,12),6:(28,8,14)}
        surf.fill(base[act])
        for _ in range(1200):
            x=random.randint(0,WIDTH); y=random.randint(0,HEIGHT)
            if act==1: c=random.choice([(16,22,18),(14,20,16),(18,24,20)])
            elif act==2: c=random.choice([(16,16,32),(18,14,36),(14,18,30)])
            elif act==3: c=random.choice([(24,18,28),(26,20,30),(22,16,26)])
            elif act==4: c=random.choice([(12,22,36),(14,24,38),(10,20,32)])
            elif act==5: c=random.choice([(28,12,14),(30,14,16),(24,10,12)])
            else: c=random.choice([(36,10,14),(38,12,16),(32,8,12)])
            pygame.draw.circle(surf,c,(x,y),random.choice([1,1,2]))
        if act==1:
            pr=pygame.Rect(WIDTH-260,HEIGHT-170,240,150)
            pygame.draw.ellipse(surf,(18,30,55),pr)
            pygame.draw.ellipse(surf,(40,60,90),pr,2)
        elif act==2:
            for _ in range(120):
                x=random.randint(0,WIDTH); y=random.randint(0,HEIGHT)
                a=random.randint(80,200); gs=pygame.Surface((6,6),pygame.SRCALPHA)
                pygame.draw.circle(gs,(220,230,255,a),(3,3),2); surf.blit(gs,(x-3,y-3))
            for r in (120,240,380):
                pygame.draw.circle(surf,(40,36,70),(WIDTH//2,HEIGHT//2),r,1)
        elif act==3:
            for _ in range(20):
                x=random.randint(50,WIDTH-50); y=random.randint(50,HEIGHT-50)
                pygame.draw.line(surf,(60,50,60),(x,y),(x,y-20),2)
                pygame.draw.circle(surf,(180,140,90),(x,y-22),4)
        elif act==4:
            for y0 in range(0,HEIGHT,30):
                for x0 in range(0,WIDTH,40):
                    yy=y0+int(math.sin(x0/50+y0/30)*3)
                    pygame.draw.arc(surf,(30,50,80),(x0-10,yy-3,20,8),0,math.pi,1)
        elif act==5:
            for _ in range(15):
                x=random.randint(50,WIDTH-50); y=random.randint(50,HEIGHT-50)
                pts=[(x,y)]
                for _ in range(5):
                    x+=random.randint(-50,50); y+=random.randint(-40,40); pts.append((x,y))
                pygame.draw.lines(surf,(80,30,30),False,pts,1)
        else:
            for r in (100,200,320):
                pygame.draw.circle(surf,(120,30,40),(WIDTH//2,HEIGHT//2+20),r,1)

        ps={1:((46,42,52),(68,62,76),(28,26,34)),
            2:((60,50,90),(120,90,180),(28,24,45)),
            3:((70,60,80),(140,110,160),(35,30,45)),
            4:((40,60,90),(80,140,200),(20,30,50)),
            5:((80,40,40),(160,70,70),(45,20,20)),
            6:((90,30,50),(200,60,90),(45,15,25))}
        pc,ph,po=ps[act]; bd=ACT_BUILDINGS[act]; locs=ACTS[act]["locs"]
        if len(locs)==6: conns=[(locs[i],locs[(i+1)%6]) for i in range(6)]
        else: conns=[(locs[0],locs[1])] if len(locs)>1 else []
        for a,b in conns:
            if a not in bd or b not in bd: continue
            ax,ay=bd[a]["x"],bd[a]["y"]; bx,by=bd[b]["x"],bd[b]["y"]
            dx,dy=bx-ax,by-ay; d=math.hypot(dx,dy)
            if d==0: continue
            ux,uy=dx/d,dy/d
            sa=bd[a]["r"]+14; sb=bd[b]["r"]+14
            sx,sy=ax+ux*sa,ay+uy*sa; ex,ey=bx-ux*sb,by-uy*sb
            pygame.draw.line(surf,po,(sx,sy),(ex,ey),26)
            pygame.draw.line(surf,pc,(sx,sy),(ex,ey),20)
            pygame.draw.line(surf,ph,(sx,sy),(ex,ey),3)
        vign=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        for i in range(70):
            a=int(170*(1-i/70))
            pygame.draw.rect(vign,(0,0,0,a),(i,i,WIDTH-2*i,HEIGHT-2*i),1)
        surf.blit(vign,(0,0)); random.seed(); return surf

    # ─── ЗДАНИЯ ───
    def _render_building(self,key):
        size=220; surf=pygame.Surface((size,size),pygame.SRCALPHA)
        cx=cy=size//2
        act=None
        for a,d in ((1,ACT1),(2,ACT2),(3,ACT3),(4,ACT4),(5,ACT5),(6,ACT6)):
            if key in d: act=a; break
        drawer=getattr(self,f"_draw_b_{act}",None)
        if drawer: drawer(surf,cx,cy,key)
        return surf

    def _tree(self,s,x,y,scale=1.0,leaf=(28,58,34)):
        pygame.draw.rect(s,(45,32,20),(x-3,y+4,6,int(14*scale)))
        pygame.draw.circle(s,leaf,(x,y-4),int(20*scale))
        pygame.draw.circle(s,(leaf[0]+6,leaf[1]+12,leaf[2]+6),(x,y-8),int(16*scale))
        pygame.draw.circle(s,(leaf[0]+12,leaf[1]+24,leaf[2]+12),(x-4,y-12),int(11*scale))

    def _lamp(self,s,x,y,h=25,col=NEON_GOLD):
        pygame.draw.line(s,(60,55,55),(x,y),(x,y-h),3)
        pygame.draw.circle(s,col,(x,y-h-3),5)
        pygame.draw.circle(s,(255,250,200),(x,y-h-3),2)

    def _house_body(self,s,cx,cy,w,h,roof_col,wall_col,door_col):
        pygame.draw.rect(s,wall_col,(cx-w//2,cy-h//2,w,h))
        pygame.draw.rect(s,(0,0,0),(cx-w//2,cy-h//2,w,h),2)
        pygame.draw.polygon(s,roof_col,[(cx-w//2-8,cy-h//2),
                                          (cx+w//2+8,cy-h//2),(cx,cy-h//2-20)])
        pygame.draw.polygon(s,(0,0,0),[(cx-w//2-8,cy-h//2),
                                          (cx+w//2+8,cy-h//2),(cx,cy-h//2-20)],2)
        pygame.draw.rect(s,door_col,(cx-9,cy-4,18,h//2))

    def _draw_b_1(self,s,cx,cy,key):
        if key=="park":
            pygame.draw.circle(s,(18,34,20),(cx,cy),78)
            pygame.draw.circle(s,(24,44,26),(cx,cy),78,2)
            for dx,dy,sc in [(-52,-35,1.1),(-42,30,.9),(55,-28,1),(48,40,1.1)]:
                self._tree(s,cx+dx,cy+dy,sc)
            pygame.draw.line(s,(110,85,60),(cx-26,cy+2),(cx-26,cy+22),3)
            pygame.draw.line(s,(110,85,60),(cx+26,cy+2),(cx+26,cy+22),3)
            pygame.draw.line(s,(130,100,70),(cx-26,cy+2),(cx+26,cy+2),3)
            self._lamp(s,cx+60,cy+5,30)
        elif key=="cafe":
            rect=pygame.Rect(cx-60,cy-40,120,90)
            pygame.draw.rect(s,(55,40,42),rect)
            awning=[(cx-70,cy-40),(cx+70,cy-40),(cx+60,cy-55),(cx-60,cy-55)]
            pygame.draw.polygon(s,(90,30,45),awning)
            for i in range(5):
                x=cx-60+i*30
                pygame.draw.line(s,(170,80,90),(x,cy-55),(x-10,cy-40),2)
            pygame.draw.rect(s,(25,18,22),(cx-12,cy-5,24,55))
            pygame.draw.rect(s,(40,55,65),(cx-50,cy-25,30,30))
        elif key=="house":
            pygame.draw.rect(s,(60,45,40),(cx-55,cy-45,110,25))
            pygame.draw.rect(s,(55,42,38),(cx-55,cy-45,20,100))
            pygame.draw.rect(s,(55,42,38),(cx+35,cy-25,20,80))
            pygame.draw.line(s,(30,20,15),(cx-55,cy-45),(cx+10,cy-20),4)
            pygame.draw.line(s,(30,20,15),(cx+55,cy-25),(cx-10,cy-20),4)
            for dx,dy,w in [(-30,20,20),(5,30,15),(20,10,12),(-15,45,18)]:
                pygame.draw.polygon(s,(45,35,30),[(cx+dx,cy+dy),
                    (cx+dx+w,cy+dy+4),(cx+dx+w-3,cy+dy+10),(cx+dx-3,cy+dy+8)])
        elif key=="library":
            self._house_body(s,cx,cy,110,95,(55,48,72),(45,40,60),(25,20,35))
            for dx in (-45,-25,25,45):
                pygame.draw.rect(s,(100,92,120),(cx+dx-3,cy-30,6,80))
            pygame.draw.circle(s,(60,80,120),(cx,cy-52),8)
        elif key=="lighthouse":
            for y_off in (40,46):
                for i in range(-70,71,14):
                    wy=cy+y_off+int(math.sin(i/10)*3)
                    pygame.draw.arc(s,(30,50,80),(cx+i-8,wy-3,16,8),0,math.pi,2)
            pygame.draw.polygon(s,(55,50,55),[(cx-22,cy+45),(cx+22,cy+45),
                                                 (cx+14,cy-45),(cx-14,cy-45)])
            for y in (cy+20,cy-5,cy-30):
                w1=20-(y-cy+45)*8//90
                pygame.draw.polygon(s,(140,40,50),[(cx-w1,y),(cx+w1,y),
                                                     (cx+w1-8,y-10),(cx-w1+8,y-10)])
            pygame.draw.circle(s,NEON_GOLD,(cx,cy-49),6)
        elif key=="station":
            pygame.draw.rect(s,(40,35,40),(cx-90,cy+40,180,8))
            for i in range(-85,86,12):
                pygame.draw.rect(s,(55,48,55),(cx+i,cy+38,4,12))
            self._house_body(s,cx,cy,130,55,(75,55,50),(55,45,42),(25,20,18))
            pygame.draw.circle(s,(240,230,210),(cx,cy-15),10)
            self._lamp(s,cx-70,cy+20,25)

    def _draw_b_2(self,s,cx,cy,key):
        if key=="mirror_hall":
            pygame.draw.circle(s,(30,28,60),(cx,cy),80)
            pygame.draw.circle(s,(60,60,110),(cx,cy),80,2)
            for i in range(6):
                a=math.pi*i/6
                x1=cx+math.cos(a)*70; y1=cy-30-math.sin(a)*40
                pygame.draw.line(s,(90,90,160),(x1,y1),(cx-math.cos(a)*70,y1),1)
            pygame.draw.polygon(s,(60,55,100),[(cx,cy+30),(cx-15,cy-10),(cx+15,cy-10)])
            pygame.draw.circle(s,NEON_CYAN,(cx,cy-18),5)
        elif key=="clock_tower":
            pygame.draw.polygon(s,(55,50,65),[(cx-22,cy+50),(cx+22,cy+50),
                                                 (cx+16,cy-50),(cx-16,cy-50)])
            pygame.draw.circle(s,(230,220,200),(cx,cy-15),15)
            pygame.draw.circle(s,(50,45,55),(cx,cy-15),15,2)
            pygame.draw.line(s,(40,40,40),(cx,cy-15),(cx,cy-25),2)
            pygame.draw.line(s,(40,40,40),(cx,cy-15),(cx+7,cy-12),2)
            pygame.draw.polygon(s,(80,50,100),[(cx-20,cy-50),(cx+20,cy-50),(cx,cy-70)])
        elif key=="garden":
            pygame.draw.circle(s,(25,20,40),(cx,cy),78)
            for dx,dy in [(-40,-30),(20,-40),(45,20),(-30,40),(0,10)]:
                px,py=cx+dx,cy+dy
                pygame.draw.line(s,(80,90,60),(px,py+10),(px,py),1)
                for a in range(5):
                    angle=math.pi*2*a/5
                    fx=px+math.cos(angle)*6; fy=py+math.sin(angle)*6
                    col=random.choice([NEON_PURPLE,NEON_PINK,NEON_CYAN])
                    pygame.draw.circle(s,col,(int(fx),int(fy)),4)
                pygame.draw.circle(s,NEON_GOLD,(px,py),3)
        elif key=="chapel":
            pygame.draw.rect(s,(35,55,75),(cx-60,cy-30,120,80))
            pygame.draw.polygon(s,(30,45,65),[(cx-65,cy-30),(cx+65,cy-30),(cx,cy-60)])
            pygame.draw.line(s,NEON_GOLD,(cx,cy-60),(cx,cy-75),3)
            pygame.draw.line(s,NEON_GOLD,(cx-7,cy-68),(cx+7,cy-68),3)
            for dx in (-35,5):
                pygame.draw.rect(s,(150,100,180),(cx+dx,cy-15,20,40))
        elif key=="cellar":
            pygame.draw.circle(s,(20,18,35),(cx,cy),78)
            for dx,dy,h,col in [(-30,-30,20,NEON_CYAN),(25,-35,25,NEON_PURPLE),
                                 (45,10,18,NEON_PINK),(-40,15,22,NEON_CYAN),
                                 (0,25,20,NEON_PURPLE)]:
                px,py=cx+dx,cy+dy
                pts=[(px,py),(px-5,py+h//2),(px,py+h),(px+5,py+h//2)]
                pygame.draw.polygon(s,col,pts)
                pygame.draw.polygon(s,(255,255,255),pts,1)
        elif key=="observatory":
            pygame.draw.circle(s,(30,30,55),(cx,cy),78)
            pygame.draw.arc(s,(90,80,140),(cx-60,cy-60,120,120),0,math.pi,3)
            pygame.draw.line(s,(150,140,180),(cx-10,cy+10),(cx+20,cy-20),8)
            pygame.draw.circle(s,(200,190,220),(cx+20,cy-20),6)

    def _draw_b_3(self,s,cx,cy,key):
        if key=="theatre":
            pygame.draw.rect(s,(60,30,40),(cx-70,cy-40,140,90))
            for i in range(8):
                x=cx-65+i*18
                pygame.draw.polygon(s,(90,20,40),[(x,cy-40),(x+18,cy-40),(x+10,cy-5)])
            pygame.draw.circle(s,(255,100,120),(cx-30,cy-10),8)
            pygame.draw.circle(s,(100,180,220),(cx+30,cy-10),8)
        elif key=="casino":
            pygame.draw.circle(s,(60,20,30),(cx,cy),50)
            pygame.draw.circle(s,(150,50,70),(cx,cy),50,2)
            for i in range(12):
                a=math.pi*2*i/12
                x1=cx+math.cos(a)*15; y1=cy+math.sin(a)*15
                x2=cx+math.cos(a)*45; y2=cy+math.sin(a)*45
                col=NEON_RED if i%2 else (30,30,30)
                pygame.draw.line(s,col,(x1,y1),(x2,y2),5)
        elif key=="hotel":
            self._house_body(s,cx,cy,130,100,(50,40,60),(60,50,70),(30,20,30))
            for r in range(3):
                for c in range(3):
                    x=cx-45+c*35; y=cy-30+r*25
                    col=NEON_GOLD if random.random()<.4 else (20,20,30)
                    pygame.draw.rect(s,col,(x,y,18,16))
        elif key=="court":
            self._house_body(s,cx,cy,140,90,(70,60,50),(100,90,80),(40,30,25))
            for dx in (-50,-30,30,50):
                pygame.draw.rect(s,(150,140,120),(cx+dx-3,cy-20,6,50))
            pygame.draw.line(s,(60,40,20),(cx,cy+10),(cx+20,cy-10),3)
        elif key=="factory":
            pygame.draw.rect(s,(50,50,55),(cx-70,cy-40,140,90))
            for dx in (-50,-25,25,50):
                pygame.draw.rect(s,(70,60,60),(cx+dx-4,cy-70,8,30))
            for (dx,dy,r) in [(-40,10,12),(40,20,14)]:
                pygame.draw.circle(s,(120,110,120),(cx+dx,cy+dy),r,3)
        elif key=="alley":
            pygame.draw.rect(s,(25,22,30),(cx-80,cy-70,40,140))
            pygame.draw.rect(s,(25,22,30),(cx+40,cy-70,40,140))
            pygame.draw.rect(s,(15,12,18),(cx-40,cy-70,80,140))
            self._lamp(s,cx,cy+30,25,(150,100,60))
            pygame.draw.polygon(s,(5,5,10),[(cx,cy-10),(cx-8,cy+20),(cx+8,cy+20)])

    def _draw_b_4(self,s,cx,cy,key):
        for r in range(90,0,-8):
            a=max(0,int(40*(1-r/90)))
            if a<=0: continue
            gs=pygame.Surface((180,180),pygame.SRCALPHA)
            pygame.draw.circle(gs,(30,80,140,a),(90,90),r)
            s.blit(gs,(cx-90,cy-90))
        if key=="reef":
            for dx,dy,col,sz in [(-40,20,(255,130,160),18),(-20,30,(255,80,120),15),
                                   (10,35,(200,100,180),20),(35,25,(255,150,180),16)]:
                px,py=cx+dx,cy+dy
                for i in range(5):
                    a=math.pi*2*i/5-math.pi/2
                    ex=px+math.cos(a)*sz; ey=py+math.sin(a)*sz
                    pygame.draw.line(s,col,(px,py),(ex,ey),3)
                    pygame.draw.circle(s,col,(int(ex),int(ey)),4)
        elif key=="wreck":
            pygame.draw.polygon(s,(60,45,35),[(cx-60,cy+20),(cx+60,cy+20),
                                                 (cx+40,cy-10),(cx-40,cy-10)])
            pygame.draw.line(s,(80,60,45),(cx-20,cy-10),(cx-20,cy-70),4)
            pygame.draw.line(s,(80,60,45),(cx+20,cy-10),(cx+20,cy-70),4)
        elif key=="grotto":
            pygame.draw.arc(s,(80,120,160),(cx-70,cy-50,140,120),math.pi,math.pi*2,3)
            pygame.draw.polygon(s,(150,200,220),[(cx,cy-30),(cx-15,cy+10),(cx+15,cy+10)])
            pygame.draw.circle(s,(150,200,220),(cx,cy-40),10)
        elif key=="abyss":
            for r in range(90,0,-6):
                a=max(0,int(180*(1-r/90)))
                gs=pygame.Surface((180,180),pygame.SRCALPHA)
                pygame.draw.circle(gs,(5,5,15,a),(90,90),r)
                s.blit(gs,(cx-90,cy-90))
            pygame.draw.ellipse(s,(200,60,60),(cx-30,cy-15,60,30))
            pygame.draw.circle(s,(0,0,0),(cx,cy),10)
            pygame.draw.circle(s,NEON_RED,(cx,cy),5)
        elif key=="sunken_town":
            for dx,dy,w,h in [(-50,10,30,40),(-15,-10,40,60),(30,5,35,50),(65,-5,25,35)]:
                pygame.draw.rect(s,(60,80,100),(cx+dx,cy+dy,w,h))
                for r in range(2):
                    for c in range(2):
                        wx=cx+dx+5+c*(w//2-3); wy=cy+dy+5+r*(h//2-3)
                        col=(150,200,220) if random.random()<.5 else (30,50,70)
                        pygame.draw.rect(s,col,(wx,wy,8,8))
        elif key=="trench":
            pygame.draw.polygon(s,(10,15,25),[(0,220),(60,cy),(160,cy),(220,220)])
            for i in range(8):
                pygame.draw.line(s,(60,100,140,20-i*2),(cx-20+i*5,0),(cx-10+i*3,cy),4)
            pygame.draw.circle(s,(150,200,240),(cx,cy-20),4)

    def _draw_b_5(self,s,cx,cy,key):
        if key=="echo_hall":
            for r in (30,55,80):
                pygame.draw.arc(s,NEON_PURPLE,(cx-r,cy-r,r*2,r*2),math.pi,math.pi*2,3)
            for i in range(6):
                rr=20+i*12; a=max(0,200-i*30)
                gs=pygame.Surface((rr*2,rr*2),pygame.SRCALPHA)
                pygame.draw.circle(gs,(*NEON_CYAN,a),(rr,rr),rr,2)
                s.blit(gs,(cx-rr,cy-rr))
            pygame.draw.circle(s,NEON_GOLD,(cx,cy),10)
        elif key=="memory_vault":
            for r in range(3):
                y=cy-50+r*40
                pygame.draw.rect(s,(60,50,80),(cx-80,y,160,4))
                for c in range(4):
                    x=cx-60+c*40
                    col=random.choice([NEON_CYAN,NEON_PURPLE,NEON_PINK,
                                        NEON_GOLD,NEON_GREEN])
                    pygame.draw.circle(s,col,(x,y-8),8)
                    pygame.draw.circle(s,(255,255,255),(x,y-8),8,1)

    def _draw_b_6(self,s,cx,cy,key):
        if key=="heart":
            for r in range(90,0,-4):
                a=max(0,int(120*(1-r/90)))
                gs=pygame.Surface((180,180),pygame.SRCALPHA)
                pygame.draw.circle(gs,(180,40,60,a),(90,90),r)
                s.blit(gs,(cx-90,cy-90))
            pygame.draw.circle(s,(140,30,50),(cx,cy),45)
            pygame.draw.circle(s,(200,50,80),(cx,cy),45,2)
            pygame.draw.circle(s,(255,130,130),(cx-10,cy-10),15)
            for i in range(12):
                a=math.pi*2*i/12
                x1=cx+math.cos(a)*50; y1=cy+math.sin(a)*50
                x2=cx+math.cos(a)*75; y2=cy+math.sin(a)*75
                pygame.draw.line(s,(255,100,100),(x1,y1),(x2,y2),2)
        elif key=="echo_throne":
            pygame.draw.rect(s,(60,20,40),(cx-45,cy-40,90,110))
            pygame.draw.rect(s,(120,40,70),(cx-45,cy-40,90,110),2)
            pygame.draw.rect(s,(90,20,50),(cx-55,cy-20,20,80))
            pygame.draw.rect(s,(90,20,50),(cx+35,cy-20,20,80))
            pygame.draw.polygon(s,(140,30,60),[(cx-40,cy-40),(cx+40,cy-40),
                                                 (cx+20,cy-80),(cx-20,cy-80)])
            for r in range(35,0,-3):
                a=int(200*(1-r/35))
                gs=pygame.Surface((70,70),pygame.SRCALPHA)
                pygame.draw.circle(gs,(0,0,0,a),(35,35),r)
                s.blit(gs,(cx-35,cy-120+r//2))
            pygame.draw.circle(s,(10,10,15),(cx,cy-105),15)
            pygame.draw.circle(s,(200,40,60),(cx,cy-105),15,2)

    def _make_aura_surface(self,radius,color):
        size=radius*2; surf=pygame.Surface((size,size),pygame.SRCALPHA)
        for rad in range(radius,0,-2):
            a=int(70*(1-rad/radius))
            if a<=0: continue
            pygame.draw.circle(surf,(*color,a),(radius,radius),rad)
        return surf

    # ─── РИСОВАЛКИ ───
    def draw_text_center(self,text,font,color,y,x=None):
        if x is None: x=WIDTH//2
        surf=font.render(text,True,color); rect=surf.get_rect(center=(x,y))
        self.screen.blit(surf,rect); return rect

    def draw_text_lines(self,lines,font,color,cx,cy):
        lh=font.get_linesize(); total=lh*len(lines)
        y0=cy-total//2+lh//2
        for i,ln in enumerate(lines):
            self.draw_text_center(ln,font,color,y0+i*lh,cx)

    def draw_button(self,text,cx,cy,w,h,color,idx):
        rect=pygame.Rect(cx-w//2,cy-h//2,w,h)
        hover=self.hover_index==idx
        bg=BG_PANEL_HI if hover else BG_PANEL
        pygame.draw.rect(self.screen,bg,rect,border_radius=6)
        pygame.draw.rect(self.screen,color,rect,width=2,border_radius=6)
        surf=self.f_btn.render(text,True,color)
        self.screen.blit(surf,surf.get_rect(center=rect.center))
        self.buttons.append((rect,idx))

    # ─── ПЕРСОНАЖ ───
    def _get_hero_colors(self):
        cloak=(40,34,62); hat=(25,22,45)
        scarf=None; apron=None; eyes=NEON_CYAN; lantern=NEON_GOLD
        ring=None; amulet=None; crown=None
        for slot,iid in self.equipped.items():
            item=ITEMS.get(iid)
            if not item: continue
            col=item["color"]
            if slot=="cloak": cloak=col
            elif slot=="hat": hat=col
            elif slot=="scarf": scarf=col
            elif slot=="apron": apron=col
            elif slot=="eyes": eyes=col
            elif slot=="lantern": lantern=col
            elif slot=="ring": ring=col
            elif slot=="amulet": amulet=col
            elif slot=="crown": crown=col
        return cloak,hat,scarf,apron,eyes,lantern,ring,amulet,crown

    def _draw_glow(self,cx,cy,radius,color):
        size=radius*2; surf=pygame.Surface((size,size),pygame.SRCALPHA)
        steps=max(3,radius//3)
        for i in range(steps):
            r=radius-int(i*radius/steps)
            if r<=0: continue
            a=int(90*(1-i/steps))
            if a<=0: continue
            pygame.draw.circle(surf,(*color,a),(radius,radius),r)
        self.screen.blit(surf,(cx-radius,cy-radius))

    def draw_hero_front(self,x,y,scale=1.0):
        s=scale
        cc,hc,sc_,ac,ec,lc,rc,amc,cwc=self._get_hero_colors()
        sh=pygame.Surface((int(80*s),int(18*s)),pygame.SRCALPHA)
        pygame.draw.ellipse(sh,(0,0,0,160),sh.get_rect())
        self.screen.blit(sh,(x-int(40*s),y+int(30*s)))
        pygame.draw.ellipse(self.screen,(18,16,32),
                             (x-int(16*s),y+int(22*s),int(14*s),int(9*s)))
        pygame.draw.ellipse(self.screen,(18,16,32),
                             (x+int(2*s),y+int(22*s),int(14*s),int(9*s)))
        pygame.draw.line(self.screen,(45,40,60),(x-int(7*s),y+int(4*s)),
                         (x-int(7*s),y+int(23*s)),int(6*s))
        pygame.draw.line(self.screen,(45,40,60),(x+int(7*s),y+int(4*s)),
                         (x+int(7*s),y+int(23*s)),int(6*s))
        cloak=[(x,y-int(28*s)),(x-int(30*s),y+int(28*s)),(x+int(30*s),y+int(28*s))]
        pygame.draw.polygon(self.screen,cc,cloak)
        pygame.draw.polygon(self.screen,NEON_PURPLE,cloak,1)
        pygame.draw.line(self.screen,(200,180,120),
                         (x-int(28*s),y+int(26*s)),(x+int(28*s),y+int(26*s)),1)
        body=[(x,y-int(22*s)),(x-int(17*s),y+int(11*s)),(x+int(17*s),y+int(11*s))]
        pygame.draw.polygon(self.screen,(72,62,100),body)
        if ac:
            rect=pygame.Rect(x-int(11*s),y-int(5*s),int(22*s),int(21*s))
            pygame.draw.rect(self.screen,ac,rect)
            pygame.draw.rect(self.screen,(200,190,170),rect,1)
        pygame.draw.line(self.screen,(35,25,18),(x-int(16*s),y+int(9*s)),
                         (x+int(16*s),y+int(9*s)),2)
        pygame.draw.rect(self.screen,NEON_GOLD,
                         (x-int(4*s),y+int(6*s),int(8*s),int(6*s)))
        pygame.draw.line(self.screen,(60,52,88),(x-int(17*s),y-int(11*s)),
                         (x-int(21*s),y+int(7*s)),int(5*s))
        pygame.draw.line(self.screen,(60,52,88),(x+int(17*s),y-int(11*s)),
                         (x+int(21*s),y+int(7*s)),int(5*s))
        pygame.draw.circle(self.screen,(90,80,110),
                           (x-int(21*s),y+int(7*s)),int(3*s))
        pygame.draw.circle(self.screen,(90,80,110),
                           (x+int(21*s),y+int(7*s)),int(3*s))
        if rc:
            pygame.draw.circle(self.screen,rc,
                               (int(x-int(21*s)),int(y+int(7*s))),
                               max(2,int(3*s)),1)
        if amc:
            pygame.draw.circle(self.screen,amc,(x,y-int(4*s)),int(5*s))
            pygame.draw.circle(self.screen,(255,255,255),(x,y-int(4*s)),int(5*s),1)
        if sc_:
            pygame.draw.line(self.screen,sc_,(x-int(14*s),y-int(17*s)),
                             (x+int(14*s),y-int(17*s)),int(6*s))
            pygame.draw.line(self.screen,sc_,(x+int(10*s),y-int(16*s)),
                             (x+int(15*s),y-int(1*s)),int(4*s))
            pygame.draw.line(self.screen,sc_,(x-int(10*s),y-int(16*s)),
                             (x-int(15*s),y-int(1*s)),int(4*s))
        pygame.draw.circle(self.screen,(85,75,110),(x,y-int(36*s)),int(12*s))
        pygame.draw.circle(self.screen,(55,48,82),(x,y-int(33*s)),int(9*s))
        pygame.draw.circle(self.screen,ec,(x-int(4*s),y-int(36*s)),2)
        pygame.draw.circle(self.screen,ec,(x+int(4*s),y-int(36*s)),2)
        pygame.draw.circle(self.screen,(20,15,30),(x-int(4*s),y-int(36*s)),1)
        pygame.draw.circle(self.screen,(20,15,30),(x+int(4*s),y-int(36*s)),1)
        hood=[(x-int(15*s),y-int(29*s)),(x-int(11*s),y-int(49*s)),
              (x+int(11*s),y-int(49*s)),(x+int(15*s),y-int(29*s))]
        pygame.draw.polygon(self.screen,hc,hood)
        pygame.draw.polygon(self.screen,(max(0,hc[0]-40),max(0,hc[1]-40),
                                           max(0,hc[2]-40)),hood,1)
        if cwc:
            for dx in [-9,-4,0,4,9]:
                hh=8 if dx==0 else 5
                pygame.draw.polygon(self.screen,cwc,
                                     [(x+int(dx*s),y-int(49*s)),
                                      (x+int((dx-2)*s),y-int((49+hh)*s)),
                                      (x+int((dx+2)*s),y-int((49+hh)*s))])
            for dx in (-6,0,6):
                pygame.draw.circle(self.screen,NEON_CYAN,
                                   (x+int(dx*s),y-int(50*s)),1)
        if self.equipped.get("eyes"):
            for gx in (-4,4):
                pygame.draw.circle(self.screen,NEON_CYAN,
                                   (x+int(gx*s),y-int(36*s)),int(5*s),1)
        weapon_data=WEAPONS.get(self.weapon,WEAPONS["wood_stick"])
        wx=x+int(23*s); wy=y+int(5*s)
        pygame.draw.line(self.screen,(60,40,20),(wx,wy+int(10*s)),(wx,wy-int(3*s)),3)
        bl=int(28*s) if self.weapon!="wood_stick" else int(18*s)
        pygame.draw.polygon(self.screen,weapon_data["color"],
                             [(wx-int(2*s),wy-int(3*s)),(wx+int(2*s),wy-int(3*s)),
                              (wx+int(2*s),wy-int(3*s)-bl),
                              (wx,wy-int(3*s)-bl-int(4*s)),
                              (wx-int(2*s),wy-int(3*s)-bl)])
        if self.weapon in ("runed_blade","silver_scepter","echo_glaive"):
            glow=pygame.Surface((int(40*s),int(40*s)),pygame.SRCALPHA)
            pygame.draw.circle(glow,(*weapon_data["color"],60),
                                (int(20*s),int(20*s)),int(15*s))
            self.screen.blit(glow,(wx-int(20*s),wy-int(20*s)))
        lx=x-int(26*s); ly=y+int(6*s)
        pygame.draw.line(self.screen,(50,40,30),(x-int(22*s),y+int(6*s)),
                         (lx,ly-int(6*s)),2)
        pygame.draw.rect(self.screen,(60,55,55),
                         (lx-int(5*s),ly-int(4*s),int(10*s),int(10*s)))
        pygame.draw.rect(self.screen,(90,85,85),
                         (lx-int(5*s),ly-int(4*s),int(10*s),int(10*s)),1)
        self._draw_glow(lx,ly,int(55*s),lc)
        pygame.draw.circle(self.screen,lc,(lx,ly),int(4*s))
        pygame.draw.circle(self.screen,(255,250,220),(lx,ly),int(2*s))

    def draw_hero_map(self,cx,cy,facing="down",anim=0,moving=False):
        cc,hc,sc_,ac,ec,lc,rc,amc,cwc=self._get_hero_colors()
        sh=pygame.Surface((40,14),pygame.SRCALPHA)
        pygame.draw.ellipse(sh,(0,0,0,160),sh.get_rect())
        self.screen.blit(sh,(cx-20,cy+12))
        if moving:
            phase=(anim//4)%4
            offs=[(-4,4,4,-4),(-6,0,6,0),(-4,-4,4,6),(-6,0,6,0)][phase]
            lo,lo2,ro,ro2=offs
            pygame.draw.line(self.screen,(45,40,60),(cx-5,cy+4),(cx+lo,cy+20+lo2),5)
            pygame.draw.line(self.screen,(45,40,60),(cx+5,cy+4),(cx+ro,cy+20+ro2),5)
        else:
            pygame.draw.line(self.screen,(45,40,60),(cx-5,cy+4),(cx-5,cy+20),5)
            pygame.draw.line(self.screen,(45,40,60),(cx+5,cy+4),(cx+5,cy+20),5)
        pygame.draw.ellipse(self.screen,(18,16,32),(cx-10,cy+18,10,6))
        pygame.draw.ellipse(self.screen,(18,16,32),(cx,cy+18,10,6))
        cloak=[(cx,cy-20),(cx-17,cy+8),(cx+17,cy+8)]
        pygame.draw.polygon(self.screen,cc,cloak)
        pygame.draw.polygon(self.screen,NEON_PURPLE,cloak,1)
        body=[(cx,cy-14),(cx-9,cy+2),(cx+9,cy+2)]
        pygame.draw.polygon(self.screen,(72,62,100),body)
        if ac: pygame.draw.rect(self.screen,ac,(cx-6,cy-8,12,12))
        pygame.draw.line(self.screen,(35,25,18),(cx-12,cy+2),(cx+12,cy+2),2)
        pygame.draw.line(self.screen,(60,52,88),(cx-12,cy-10),(cx-15,cy+2),4)
        pygame.draw.line(self.screen,(60,52,88),(cx+12,cy-10),(cx+15,cy+2),4)
        if sc_: pygame.draw.circle(self.screen,sc_,(cx,cy-16),6)
        pygame.draw.circle(self.screen,(85,75,110),(cx,cy-22),10)
        pygame.draw.circle(self.screen,hc,(cx,cy-22),10,3)
        pygame.draw.circle(self.screen,(20,16,30),(cx,cy-24),6)
        if facing=="down":
            pygame.draw.circle(self.screen,ec,(cx-3,cy-22),2)
            pygame.draw.circle(self.screen,ec,(cx+3,cy-22),2)
        elif facing=="left": pygame.draw.circle(self.screen,ec,(cx-5,cy-22),2)
        elif facing=="right": pygame.draw.circle(self.screen,ec,(cx+5,cy-22),2)
        if self.equipped.get("eyes"):
            pygame.draw.circle(self.screen,NEON_CYAN,(cx-3,cy-22),4,1)
            pygame.draw.circle(self.screen,NEON_CYAN,(cx+3,cy-22),4,1)
        if cwc:
            for dx in (-5,0,5):
                pygame.draw.polygon(self.screen,cwc,
                                     [(cx+dx-2,cy-30),(cx+dx,cy-36),(cx+dx+2,cy-30)])
        if amc: pygame.draw.circle(self.screen,amc,(cx,cy-8),3)
        weapon_data=WEAPONS.get(self.weapon,WEAPONS["wood_stick"])
        wl=14 if self.weapon!="wood_stick" else 10
        pygame.draw.line(self.screen,(60,40,20),(cx+13,cy-2),(cx+13,cy-10),2)
        pygame.draw.line(self.screen,weapon_data["color"],
                         (cx+13,cy-10),(cx+13,cy-10-wl),2)
        lx,ly=cx-18,cy+2
        self._draw_glow(lx,ly,36,lc)
        pygame.draw.rect(self.screen,(60,55,55),(lx-3,ly-3,6,8))
        pygame.draw.circle(self.screen,lc,(lx,ly),3)
        pygame.draw.circle(self.screen,(255,250,220),(lx,ly),1)
        # Компаньон летит рядом
        if self.active_companion:
            cx2=cx+math.cos(self.time_accum*0.05)*35
            cy2=cy-45+math.sin(self.time_accum*0.07)*8
            col=COMPANIONS[self.active_companion]["color"]
            self._draw_glow(int(cx2),int(cy2),20,col)
            pygame.draw.circle(self.screen,col,(int(cx2),int(cy2)),5)

    def draw_shadow_figure(self,x,y,t,custom_color=None,is_boss=False):
        if custom_color: color=custom_color
        else:
            r=int(30+t*(181-30)); g=int(30+t*(123-30)); b=int(40+t*(255-40))
            color=(r,g,b)
        size=200 if is_boss else 170
        surf=pygame.Surface((size,size),pygame.SRCALPHA)
        max_a=int(30+t*130) if not is_boss else int(60+t*160)
        for rad in range(size//2,0,-2):
            a=int(max_a*(1-rad/(size/2)))
            if a<=0: continue
            pygame.draw.circle(surf,(*color,a),(size//2,size//2),rad)
        self.screen.blit(surf,(x-size//2,y-size//2))
        body=[(x,y-45),(x-30,y+30),(x+30,y+30)]
        pygame.draw.polygon(self.screen,color,body)
        pygame.draw.circle(self.screen,color,(x,y-55),18)
        if t>0.7:
            pygame.draw.circle(self.screen,NEON_GOLD,(x-6,y-57),3)
            pygame.draw.circle(self.screen,NEON_GOLD,(x+6,y-57),3)
        if is_boss:
            for i in range(2):
                pygame.draw.circle(self.screen,NEON_RED,(x,y-20),60+i*8,2)

    # ═══════════════ МЕНЮ ═══════════════
    def draw_menu(self):
        self.buttons=[]
        self.set_music("menu")
        self.draw_text_center("ЭХО-ЛОКАЦИЯ",self.f_title,NEON_CYAN,70)
        self.draw_text_center("мистический детектив о забытых голосах",
                              self.f_sub,NEON_PURPLE,125)
        pygame.draw.line(self.screen,NEON_PURPLE,
                         (WIDTH//2-240,155),(WIDTH//2+240,155),1)
        desc=["Забытый Город погружён в тишину. Жители — серые тени,",
              "потерявшие воспоминания. Пройди шесть актов, найди звуки,",
              "разгадай головоломки и победи боссов.",
              "Каждая встреча уникальна, а рядом — верные компаньоны."]
        self.draw_text_lines(desc,self.f_body,TEXT_MAIN,WIDTH//2,205)
        self.draw_hero_front(WIDTH//2,395,scale=1.4)
        self.draw_button("НАЧАТЬ ИССЛЕДОВАНИЕ",WIDTH//2,530,360,55,NEON_CYAN,0)
        self.draw_button("ЗАГРУЗИТЬ ИГРУ",WIDTH//2,600,260,42,NEON_GOLD,1)
        self.draw_text_center(
            "WASD — ходьба • E — войти • I — инвентарь • M — магазин "
            "• C — компаньоны",
            self.f_tiny,TEXT_DIM,660)
        self.draw_text_center("F5 — сохранить • F9 — загрузить",
                              self.f_tiny,TEXT_DIM,680)

    # ═══════════════ ИНТРО ═══════════════
    def draw_act_intro(self):
        self.buttons=[]
        act=ACTS[self.act]; color=act["color"]
        self.set_music("map")
        pulse=int(20+15*math.sin(self.time_accum*0.05))
        self.screen.fill((8+pulse//2,8,15+pulse//2))
        self.draw_text_center("НОВЫЙ АКТ",self.f_sub,TEXT_DIM,120)
        self.draw_text_center(act["name"],self.f_title,color,185)
        self.draw_text_center(act["sub"],self.f_sub,TEXT_MAIN,250)
        pygame.draw.line(self.screen,color,
                         (WIDTH//2-260,290),(WIDTH//2+260,290),1)
        txt={1:["Начни свой путь. Найди шесть первых звуков.",
                "Лира, дух певицы, уже рядом с тобой."],
             2:["Город раскрывает тайны.",
                "Проводник укажет путь. Головоломки разнообразнее."],
             3:["Городские секреты. Три новых босса.",
                "Кот-Тень появился — он видит слабости."],
             4:["Затонувший мир. Древние тайны.",
                "Светлячок спешит на помощь."],
             5:["Сердце города близко.",
                "Дух-Предок вернулся. Цепочки головоломок."],
             6:["Финал. Хозяин Тишины ждёт.",
                "Покажи, чего ты стоишь."]}
        self.draw_text_lines(txt[self.act],self.f_body,TEXT_MAIN,WIDTH//2,380)
        self.draw_hero_front(WIDTH//2,525,scale=1.2)
        self.draw_button("Продолжить",WIDTH//2,645,260,44,color,0)

    # ═══════════════ КАРТА ═══════════════
    def update_map(self):
        p=self.player; dx=dy=0
        if "up" in self.keys_held: dy-=1
        if "down" in self.keys_held: dy+=1
        if "left" in self.keys_held: dx-=1
        if "right" in self.keys_held: dx+=1
        if dx or dy:
            d=math.hypot(dx,dy); dx/=d; dy/=d
            p["anim"]+=1; p["moving"]=True
            if abs(dx)>abs(dy): p["facing"]="right" if dx>0 else "left"
            else: p["facing"]="down" if dy>0 else "up"
        else: p["moving"]=False; p["anim"]=0
        speed=3.2
        nx=p["x"]+dx*speed; ny=p["y"]+dy*speed
        for b in self.buildings.values():
            bx,by,br=b["x"],b["y"],b["r"]
            ddx,ddy=nx-bx,ny-by; d=math.hypot(ddx,ddy)
            if d<br:
                if d<0.01: nx=bx+br; ny=by
                else:
                    ux,uy=ddx/d,ddy/d; nx=bx+ux*br; ny=by+uy*br
        nx=max(30,min(WIDTH-30,nx)); ny=max(30,min(HEIGHT-30,ny))
        p["x"],p["y"]=nx,ny
        self.nearby_building=None; best_d=99999
        for k,b in self.buildings.items():
            d=math.hypot(p["x"]-b["x"],p["y"]-b["y"])
            if d<b["r"]+45 and d<best_d: self.nearby_building=k; best_d=d

    def draw_map(self):
        self.buttons=[]
        self.set_music("map")
        act=ACTS[self.act]; act_color=act["color"]
        self.screen.blit(self.map_surfaces[self.act],(0,0))
        pulse=0.85+0.15*math.sin(self.time_accum*0.08)
        for k,b in self.buildings.items():
            loc_data=ALL_LOCATIONS[k]; enemy=loc_data.get("enemy",{})
            is_boss=enemy.get("boss",False)
            if k in self.done: aura=self.aura_gold
            elif is_boss and k in self.sounds_found: aura=self.aura_boss
            elif k in self.sounds_found and loc_data.get("puzzle") \
                    and k not in self.puzzles_done: aura=self.aura_puzzle
            elif k in self.sounds_found: aura=self.aura_pink
            else: continue
            ac=aura.copy(); ac.set_alpha(int(180*pulse))
            self.screen.blit(ac,(b["x"]-ac.get_width()//2,b["y"]-ac.get_height()//2))
        for k,b in self.buildings.items():
            surf=self.building_surfaces.get(k)
            if surf: self.screen.blit(surf,(b["x"]-surf.get_width()//2,
                                             b["y"]-surf.get_height()//2))
        for k,b in self.buildings.items():
            by=b["y"]-b["r"]-18
            is_boss=ALL_LOCATIONS[k].get("enemy",{}).get("boss",False)
            if k in self.done: self._draw_status_badge(b["x"],by,NEON_GOLD,"✓")
            elif is_boss and k in self.sounds_found:
                self._draw_status_badge(b["x"],by,NEON_RED,"☠")
            elif k in self.sounds_found and ALL_LOCATIONS[k].get("puzzle") \
                    and k not in self.puzzles_done:
                self._draw_status_badge(b["x"],by,NEON_PURPLE,"?")
            elif k in self.sounds_found:
                self._draw_status_badge(b["x"],by,NEON_PINK,"♪")
        for i in range(4):
            t=self.time_accum*0.03+i*2.1
            fx=self.player["x"]+math.cos(t)*65+math.sin(t*1.7)*22
            fy=self.player["y"]+math.sin(t*1.1)*45
            a=int(120+60*math.sin(t*3))
            gs=pygame.Surface((10,10),pygame.SRCALPHA)
            pygame.draw.circle(gs,(*NEON_GOLD,max(30,a)),(5,5),5)
            self.screen.blit(gs,(fx-5,fy-5))
        p=self.player
        self.draw_hero_map(p["x"],p["y"],p["facing"],p["anim"],p["moving"])
        if self.nearby_building:
            b=self.buildings[self.nearby_building]
            loc=ALL_LOCATIONS[self.nearby_building]
            bx,by=b["x"],b["y"]-b["r"]-55
            text=f"E — войти в «{loc['name']}»"
            w=self.f_small.size(text)[0]+30
            rect=pygame.Rect(bx-w//2,by-14,w,28)
            pygame.draw.rect(self.screen,BG_PANEL,rect,border_radius=6)
            pygame.draw.rect(self.screen,NEON_CYAN,rect,width=2,border_radius=6)
            s=self.f_small.render(text,True,NEON_CYAN)
            self.screen.blit(s,s.get_rect(center=rect.center))
        panel=pygame.Rect(0,0,WIDTH,46)
        pygame.draw.rect(self.screen,(8,8,16),panel)
        pygame.draw.line(self.screen,act_color,(0,46),(WIDTH,46),1)
        self.screen.blit(self.f_head.render(act["name"],True,act_color),(20,12))
        time_str=self.format_time(self.elapsed)
        ts=self.f_mono.render(f"⏱ {time_str}",True,NEON_GOLD)
        self.screen.blit(ts,(WIDTH-ts.get_width()-20,14))
        mid=pygame.Rect(0,46,WIDTH,30)
        pygame.draw.rect(self.screen,(10,10,20),mid)
        pygame.draw.line(self.screen,act_color,(0,76),(WIDTH,76),1)
        hp_frac=self.player_hp/max(1,self.max_hp)
        hr=pygame.Rect(20,53,200,16)
        pygame.draw.rect(self.screen,(30,15,20),hr,border_radius=3)
        fw=int(hr.w*hp_frac)
        if fw>0:
            pygame.draw.rect(self.screen,HP_RED,(hr.x,hr.y,fw,hr.h),border_radius=3)
        pygame.draw.rect(self.screen,HP_RED,hr,width=1,border_radius=3)
        ht=self.f_tiny.render(f"HP {self.player_hp}/{self.max_hp}",True,TEXT_WHITE)
        self.screen.blit(ht,ht.get_rect(center=hr.center))
        self.screen.blit(self.f_tiny.render(f"ATK {self.get_attack_power()}",
                                              True,NEON_ORANGE),(240,55))
        self.screen.blit(self.f_tiny.render(f"DEF {self.base_def}",
                                              True,NEON_BLUE),(320,55))
        self.screen.blit(self.f_tiny.render(f"◈ {self.shards}",
                                              True,NEON_GOLD),(400,55))
        self.screen.blit(self.f_tiny.render(
            f"🧪 {sum(self.potions.values())}",True,NEON_GREEN),(480,55))
        self.screen.blit(self.f_tiny.render(
            f"⚔ {WEAPONS[self.weapon]['name'][:16]}",True,NEON_CYAN),(540,55))
        if self.active_companion:
            cn=COMPANIONS[self.active_companion]
            self.screen.blit(self.f_tiny.render(
                f"◆ {cn['name']}",True,cn["color"]),(730,55))
        act_locs=ACTS[self.act]["locs"]
        done_act=sum(1 for l in act_locs if l in self.done)
        prog=f"Тени: {done_act}/{len(act_locs)}"
        psurf=self.f_tiny.render(prog,True,TEXT_MAIN)
        self.screen.blit(psurf,(WIDTH-psurf.get_width()-20,55))
        hint="WASD — ходьба • E — войти • I — инвентарь • M — магазин • C — компаньоны"
        hs=self.f_tiny.render(hint,True,TEXT_DIM)
        self.screen.blit(hs,(WIDTH//2-hs.get_width()//2,HEIGHT-20))
        if self.act_all_done(self.act):
            if self.act<6:
                self.draw_button("→ СЛЕДУЮЩИЙ АКТ",WIDTH//2,HEIGHT-60,
                                 280,42,act_color,2)
            else:
                self.draw_button("✦ ЗАВЕРШИТЬ ПУТЬ ✦",WIDTH//2,HEIGHT-60,
                                 320,42,act_color,2)
        self.draw_button("I — Инвентарь",WIDTH-110,130,180,30,NEON_PURPLE,3)
        self.draw_button("M — Магазин",WIDTH-110,168,180,30,NEON_GOLD,4)
        self.draw_button("C — Компаньоны",WIDTH-110,206,180,30,NEON_PINK,5)

    def _draw_status_badge(self,x,y,color,symbol):
        pygame.draw.circle(self.screen,BG_PANEL,(x,y),14)
        pygame.draw.circle(self.screen,color,(x,y),14,2)
        s=self.f_small.render(symbol,True,color)
        self.screen.blit(s,s.get_rect(center=(x,y)))

    # ═══════════════ КОМПАНЬОНЫ (ЭКРАН) ═══════════════
    def draw_companions(self):
        self.buttons=[]
        pygame.draw.rect(self.screen,(10,10,20),(0,0,WIDTH,HEIGHT))
        self.draw_text_center("КОМПАНЬОНЫ",self.f_big,NEON_PINK,35)
        self.draw_text_center("Те, кто помогает тебе в пути",
                              self.f_sub,TEXT_DIM,72)
        self.draw_button("← Выйти",WIDTH-90,35,140,40,TEXT_DIM,0)
        if self.companion_message:
            self.draw_text_center(self.companion_message,self.f_sub,
                                  NEON_CYAN,110)
        for i,cid in enumerate(COMPANION_ORDER):
            c=COMPANIONS[cid]
            unlocked=cid in self.companions
            is_active=self.active_companion==cid
            rect=pygame.Rect(80,140+i*100,800,85)
            hover=self.hover_index==10+i
            bg=BG_PANEL_HI if (hover or is_active) else BG_PANEL
            pygame.draw.rect(self.screen,bg,rect,border_radius=10)
            border=c["color"] if unlocked else TEXT_DIM
            pygame.draw.rect(self.screen,border,rect,width=2,border_radius=10)
            # Портрет
            px=rect.x+50; py=rect.centery
            self._draw_glow(px,py,40,c["color"] if unlocked else TEXT_DIM)
            pygame.draw.circle(self.screen,border,(px,py),20)
            pygame.draw.circle(self.screen,(20,20,30),(px,py),18)
            # Текст
            name_col=c["color"] if unlocked else TEXT_DIM
            self.screen.blit(self.f_head.render(c["name"],True,name_col),
                              (rect.x+90,rect.y+10))
            if unlocked:
                self.screen.blit(self.f_small.render(c["desc"],True,TEXT_MAIN),
                                  (rect.x+90,rect.y+38))
                self.screen.blit(self.f_tiny.render(
                    f"Q в бою: {c['assist_name']}",True,NEON_CYAN),
                    (rect.x+90,rect.y+58))
            else:
                self.screen.blit(self.f_small.render(
                    f"Откроется в акте {c['unlock_act']}",True,TEXT_DIM),
                    (rect.x+90,rect.y+38))
            if is_active:
                self.screen.blit(self.f_small.render("★ АКТИВЕН",
                                                       True,NEON_GOLD),
                                  (rect.right-140,rect.y+15))
            if unlocked:
                self.buttons.append((rect,10+i))
        self.draw_text_center(
            "Клик по компаньону — выбрать активного (помогает в бою)",
            self.f_small,TEXT_DIM,HEIGHT-40)

    # ═══════════════ ИНВЕНТАРЬ / МАГАЗИН ═══════════════
    def draw_inventory(self):
        self.buttons=[]
        pygame.draw.rect(self.screen,(10,10,20),(0,0,WIDTH,HEIGHT))
        self.draw_text_center("ИНВЕНТАРЬ",self.f_big,NEON_CYAN,26)
        pygame.draw.rect(self.screen,BG_PANEL,(40,60,320,570),border_radius=10)
        pygame.draw.rect(self.screen,NEON_PURPLE,(40,60,320,570),
                          width=1,border_radius=10)
        self.draw_hero_front(200,310,scale=1.6)
        ys=440
        self.screen.blit(self.f_small.render(
            f"HP: {self.player_hp} / {self.max_hp}",True,HP_RED),(70,ys))
        self.screen.blit(self.f_small.render(
            f"ATK: {self.get_attack_power()}",True,NEON_ORANGE),(70,ys+20))
        self.screen.blit(self.f_small.render(
            f"DEF: {self.base_def}",True,NEON_BLUE),(70,ys+40))
        self.screen.blit(self.f_small.render(
            f"◈ Осколки: {self.shards}",True,NEON_GOLD),(70,ys+60))
        slot_y0=505
        for i,slot in enumerate(SLOT_ORDER):
            sx=60+(i%3)*100; sy=slot_y0+(i//3)*40
            rect=pygame.Rect(sx,sy,90,32)
            iid=self.equipped.get(slot)
            if iid:
                item=ITEMS[iid]
                pygame.draw.rect(self.screen,BG_PANEL_HI,rect,border_radius=6)
                pygame.draw.rect(self.screen,item["color"],rect,width=2,border_radius=6)
                ns=self.f_tiny.render(item["name"][:14],True,item["color"])
                self.screen.blit(ns,ns.get_rect(center=(rect.centerx,rect.y+16)))
            else:
                pygame.draw.rect(self.screen,BG_PANEL,rect,border_radius=6)
                pygame.draw.rect(self.screen,TEXT_DIM,rect,width=1,border_radius=6)
                s=self.f_tiny.render(SLOT_NAMES[slot],True,TEXT_DIM)
                self.screen.blit(s,s.get_rect(center=rect.center))
            self.buttons.append((rect,100+i))
        pygame.draw.rect(self.screen,BG_PANEL,(400,60,530,570),border_radius=10)
        pygame.draw.rect(self.screen,NEON_PURPLE,(400,60,530,570),
                          width=1,border_radius=10)
        self.draw_text_center("ПРЕДМЕТЫ",self.f_head,NEON_GOLD,82,x=665)
        if not self.inventory:
            self.draw_text_center("Пока пусто.",self.f_small,TEXT_DIM,300,x=665)
        items=sorted([i for i in ITEMS if i in self.inventory],
                     key=lambda x:(ITEMS[x].get("act",1),x))
        for i,iid in enumerate(items[:14]):
            item=ITEMS[iid]; col=i//7; row=i%7
            rect=pygame.Rect(415+col*260,105+row*68,245,60)
            is_eq=self.equipped.get(item["slot"])==iid
            hover=self.hover_index==50+i
            bg=BG_PANEL_HI if (hover or is_eq) else BG_PANEL
            pygame.draw.rect(self.screen,bg,rect,border_radius=6)
            pygame.draw.rect(self.screen,item["color"],rect,width=2,border_radius=6)
            pygame.draw.circle(self.screen,item["color"],
                                (rect.x+24,rect.centery),12)
            pygame.draw.circle(self.screen,BG_DARK,
                                (rect.x+24,rect.centery),7)
            self.screen.blit(self.f_small.render(item["name"],True,item["color"]),
                              (rect.x+44,rect.y+6))
            rar=item.get("rarity","common")
            self.screen.blit(self.f_tiny.render(RARITY_NAMES[rar],True,
                                                  RARITY_COLORS[rar]),
                              (rect.x+44,rect.y+26))
            bp=[]
            if item["memory_bonus"]: bp.append(f"+{item['memory_bonus']}%")
            if item["window_bonus"]: bp.append(f"+{item['window_bonus']}px")
            info=f"{SLOT_NAMES[item['slot']]} "+" ".join(bp)
            self.screen.blit(self.f_tiny.render(info,True,TEXT_DIM),
                              (rect.x+44,rect.y+42))
            if is_eq:
                self.screen.blit(self.f_tiny.render("✓",True,NEON_GOLD),
                                  (rect.right-16,rect.y+6))
            self.buttons.append((rect,50+i))
        self.draw_button("← Вернуться на карту",WIDTH//2,660,300,36,TEXT_DIM,0)

    def on_inventory_button(self,idx):
        if idx==0: self.state=self.ST_MAP; return
        if 50<=idx<64:
            items=sorted([i for i in ITEMS if i in self.inventory],
                         key=lambda x:(ITEMS[x].get("act",1),x))
            k=idx-50
            if k<len(items):
                iid=items[k]; slot=ITEMS[iid]["slot"]
                if self.equipped.get(slot)==iid: del self.equipped[slot]
                else: self.equipped[slot]=iid
                self.recalc_stats(); self._play("equip")
        elif 100<=idx<100+len(SLOT_ORDER):
            k=idx-100
            if k<len(SLOT_ORDER):
                slot=SLOT_ORDER[k]
                if slot in self.equipped:
                    del self.equipped[slot]; self.recalc_stats(); self._play("equip")

    def draw_shop(self):
        self.buttons=[]
        self.set_music("shop")
        pygame.draw.rect(self.screen,(10,10,20),(0,0,WIDTH,HEIGHT))
        self.draw_text_center("ЛАВКА ЭХО",self.f_big,NEON_GOLD,32)
        self.draw_text_center(f"Осколки: ◈ {self.shards}",self.f_head,NEON_CYAN,72)
        self.draw_button("← Выйти",WIDTH-90,35,140,40,TEXT_DIM,0)
        wx0,wy0=60,110
        pygame.draw.rect(self.screen,BG_PANEL,(wx0,wy0,430,520),border_radius=10)
        pygame.draw.rect(self.screen,NEON_ORANGE,(wx0,wy0,430,520),
                          width=2,border_radius=10)
        self.draw_text_center("⚔ ОРУЖИЕ",self.f_head,NEON_ORANGE,wy0+22,x=wx0+215)
        wlist=list(WEAPONS.items())
        for i,(wid,w) in enumerate(wlist):
            y=wy0+52+i*72
            rect=pygame.Rect(wx0+15,y,400,64)
            owned=wid in self.weapons_owned
            eq=self.weapon==wid
            hover=self.hover_index==200+i
            bg=BG_PANEL_HI if (hover or eq) else BG_PANEL
            pygame.draw.rect(self.screen,bg,rect,border_radius=6)
            pygame.draw.rect(self.screen,RARITY_COLORS.get(w["rarity"],TEXT_DIM),
                              rect,width=2,border_radius=6)
            pygame.draw.line(self.screen,(60,40,20),
                             (rect.x+30,rect.centery+8),
                             (rect.x+30,rect.centery-2),3)
            pygame.draw.line(self.screen,w["color"],
                             (rect.x+30,rect.centery-2),
                             (rect.x+30,rect.centery-18),3)
            self.screen.blit(self.f_small.render(w["name"],True,w["color"]),
                              (rect.x+55,rect.y+6))
            self.screen.blit(self.f_tiny.render(
                f"Урон: {w['dmg']}  •  {w['desc']}",True,TEXT_DIM),
                (rect.x+55,rect.y+28))
            if eq:
                self.screen.blit(self.f_tiny.render("★ НАДЕТО",True,NEON_GOLD),
                                  (rect.right-90,rect.y+8))
            elif owned:
                self.screen.blit(self.f_tiny.render("Надеть →",True,NEON_CYAN),
                                  (rect.right-90,rect.y+8))
            else:
                pc=NEON_GREEN if self.shards>=w["price"] else NEON_RED
                self.screen.blit(self.f_small.render(f"◈ {w['price']}",True,pc),
                                  (rect.right-80,rect.y+8))
            if not eq: self.buttons.append((rect,200+i))
        px0,py0=510,110
        pygame.draw.rect(self.screen,BG_PANEL,(px0,py0,400,520),border_radius=10)
        pygame.draw.rect(self.screen,NEON_GREEN,(px0,py0,400,520),
                          width=2,border_radius=10)
        self.draw_text_center("🧪 ЗЕЛЬЯ",self.f_head,NEON_GREEN,py0+22,x=px0+200)
        plist=list(POTIONS.items())
        for i,(pid,p) in enumerate(plist):
            y=py0+52+i*82
            rect=pygame.Rect(px0+15,y,370,74)
            cnt=self.potions.get(pid,0)
            hover=self.hover_index==300+i
            bg=BG_PANEL_HI if hover else BG_PANEL
            pygame.draw.rect(self.screen,bg,rect,border_radius=6)
            pygame.draw.rect(self.screen,p["color"],rect,width=2,border_radius=6)
            pygame.draw.circle(self.screen,p["color"],(rect.x+35,rect.centery),14)
            pygame.draw.circle(self.screen,(255,255,255),
                                (rect.x+35,rect.centery),14,1)
            self.screen.blit(self.f_small.render(p["name"],True,p["color"]),
                              (rect.x+60,rect.y+8))
            self.screen.blit(self.f_tiny.render(p["desc"],True,TEXT_DIM),
                              (rect.x+60,rect.y+30))
            pc=NEON_GREEN if self.shards>=p["price"] else NEON_RED
            self.screen.blit(self.f_small.render(f"◈ {p['price']}",True,pc),
                              (rect.right-80,rect.y+8))
            self.screen.blit(self.f_tiny.render(f"в сумке: {cnt}",True,TEXT_MAIN),
                              (rect.right-100,rect.y+42))
            self.buttons.append((rect,300+i))

    def on_shop_button(self,idx):
        if idx==0: self.state=self.ST_MAP; return
        if 200<=idx<210:
            k=idx-200; wl=list(WEAPONS.items())
            if k<len(wl):
                wid,w=wl[k]
                if wid in self.weapons_owned: self.weapon=wid; self._play("equip")
                elif self.shards>=w["price"]:
                    self.shards-=w["price"]; self.weapons_owned.add(wid)
                    self.weapon=wid; self._play("purchase")
                else: self._play("error")
        elif 300<=idx<310:
            k=idx-300; pl=list(POTIONS.items())
            if k<len(pl):
                pid,p=pl[k]
                if self.shards>=p["price"]:
                    self.shards-=p["price"]
                    self.potions[pid]=self.potions.get(pid,0)+1
                    self._play("purchase")
                else: self._play("error")

    # ═══════════════ ЛОКАЦИЯ ═══════════════
    def draw_location_scene(self,key,cx,cy,w=320,h=140):
        rect=pygame.Rect(cx-w//2,cy-h//2,w,h)
        pygame.draw.rect(self.screen,(12,14,22),rect,border_radius=8)
        pygame.draw.rect(self.screen,NEON_PURPLE,rect,width=1,border_radius=8)
        sub=pygame.Surface((w,h),pygame.SRCALPHA)
        sx=w//2; sy=h//2
        act=None
        for a,d in ((1,ACT1),(2,ACT2),(3,ACT3),(4,ACT4),(5,ACT5),(6,ACT6)):
            if key in d: act=a; break
        drawer=getattr(self,f"_scene_{act}",None)
        if drawer: drawer(sub,sx,sy,w,h,key)
        self.screen.blit(sub,rect.topleft)

    def _scene_1(self,sub,sx,sy,w,h,key):
        if key=="park":
            for i in range(h):
                t=i/h; c=(int(15+20*(1-t)),int(20+30*(1-t)),int(40+60*(1-t)))
                pygame.draw.line(sub,c,(0,i),(w,i))
            pygame.draw.circle(sub,(230,220,180),(w-60,35),15)
            for dx in (-120,-80,40,100,130):
                pygame.draw.rect(sub,(10,15,12),(sx+dx-3,sy+10,6,40))
                pygame.draw.circle(sub,(12,22,15),(sx+dx,sy+5),22)
        elif key=="cafe":
            sub.fill((25,18,20))
            pygame.draw.rect(sub,(55,38,30),(0,sy+30,w,40))
            for i in range(6):
                px=20+i*50
                pygame.draw.rect(sub,(200,190,170),(px,12,14,8))
        elif key=="house":
            sub.fill((15,12,15))
            pygame.draw.polygon(sub,(45,35,30),[(0,h),(0,30),(50,30),(50,60),
                (100,60),(100,20),(160,20),(160,50),(220,50),(220,25),
                (280,25),(280,55),(w,55),(w,h)])
        elif key=="library":
            sub.fill((20,18,30))
            for side in (-1,1):
                base=sx+side*100
                pygame.draw.rect(sub,(45,35,25),(base-55,10,110,h-20))
                for row in range(4):
                    ry=20+row*30
                    for i in range(11):
                        bx=base-52+i*10
                        c=random.choice([(120,40,50),(60,100,80),(110,90,40)])
                        pygame.draw.rect(sub,c,(bx,ry,8,24))
        elif key=="lighthouse":
            sub.fill((15,25,45))
            for yo in (h-30,h-20):
                for i in range(-w//2,w//2,20):
                    wy=yo+int(math.sin(i/15)*3)
                    pygame.draw.arc(sub,(60,100,160),(sx+i-10,wy-4,20,10),0,math.pi,2)
            pygame.draw.polygon(sub,(170,165,170),[(sx-30,h-40),(sx+30,h-40),
                                                     (sx+15,30),(sx-15,30)])
        elif key=="station":
            sub.fill((18,18,25))
            pygame.draw.rect(sub,(60,55,62),(0,sy+30,w,30))
            for x in range(20,w,60):
                pygame.draw.rect(sub,(60,50,45),(x,25,6,sy+5))

    def _scene_2(self,sub,sx,sy,w,h,key):
        sub.fill((15,15,30))
        pygame.draw.rect(sub,(45,40,60),(sx-80,30,160,h-40))
        pygame.draw.rect(sub,(100,90,130),(sx-80,30,160,h-40),2)

    def _scene_3(self,sub,sx,sy,w,h,key):
        sub.fill((25,18,30))
        pygame.draw.rect(sub,(60,30,45),(sx-100,sy+10,200,h//2-15))
        pygame.draw.rect(sub,(120,50,80),(sx-100,sy+10,200,h//2-15),2)

    def _scene_4(self,sub,sx,sy,w,h,key):
        for i in range(h):
            t=i/h; c=(int(10+20*(1-t)),int(20+40*(1-t)),int(40+60*(1-t)))
            pygame.draw.line(sub,c,(0,i),(w,i))
        for _ in range(20):
            x=random.randint(0,w); y=random.randint(0,h)
            pygame.draw.circle(sub,(80,140,200),(x,y),random.randint(1,3),1)
        pygame.draw.polygon(sub,(100,180,220),[(sx-40,sy+30),(sx-20,sy-30),
                                                 (sx+20,sy-30),(sx+40,sy+30)])

    def _scene_5(self,sub,sx,sy,w,h,key):
        sub.fill((15,12,28))
        for r in (30,55):
            pygame.draw.arc(sub,NEON_PURPLE,(sx-r,sy-r,r*2,r*2),math.pi,math.pi*2,3)
        for i in range(5):
            rr=20+i*12; a=max(0,180-i*40)
            gs=pygame.Surface((rr*2,rr*2),pygame.SRCALPHA)
            pygame.draw.circle(gs,(*NEON_CYAN,a),(rr,rr),rr,2)
            sub.blit(gs,(sx-rr,sy-rr))

    def _scene_6(self,sub,sx,sy,w,h,key):
        if key=="heart":
            sub.fill((25,12,15))
            for r in range(80,0,-4):
                a=max(0,int(120*(1-r/80)))
                gs=pygame.Surface((160,160),pygame.SRCALPHA)
                pygame.draw.circle(gs,(180,40,60,a),(80,80),r)
                sub.blit(gs,(sx-80,sy-80))
            pygame.draw.circle(sub,(140,30,50),(sx,sy),40)
        else:
            sub.fill((20,8,15))
            pygame.draw.rect(sub,(60,20,40),(sx-35,sy-30,70,80))
            pygame.draw.circle(sub,(10,10,15),(sx,sy-75),12)

    def draw_location(self):
        self.buttons=[]
        loc=ALL_LOCATIONS[self.current_loc]
        self.draw_text_center(loc["name"],self.f_big,NEON_CYAN,40)
        self.draw_location_scene(self.current_loc,WIDTH//2,145)
        self.draw_text_lines(loc["desc"].split("\n"),self.f_body,
                             TEXT_MAIN,WIDTH//2,245)
        key=self.current_loc
        enemy=loc.get("enemy",{}); is_boss=enemy.get("boss",False)
        ename=enemy.get("name","Тень")
        if key in self.done:
            self.draw_text_center("Тень вновь обрела свой цвет:",
                                  self.f_small,TEXT_DIM,310)
            self.draw_text_center(loc["shadow"],self.f_head,NEON_PURPLE,338)
            sl=[f'«{l}»' for l in loc["story"].split("\n")]
            self.draw_text_lines(sl,self.f_sub,NEON_GOLD,WIDTH//2,405)
            self.draw_hero_front(WIDTH//2,525,scale=1.1)
        elif key in self.sounds_found:
            self.draw_text_center("Ты слышишь этот звук вновь:",
                                  self.f_small,TEXT_DIM,300)
            self.draw_text_center(f"«{loc['artifact']}»",self.f_head,NEON_CYAN,325)
            if loc.get("puzzle") and key not in self.puzzles_done:
                self.draw_text_center("Тень ждёт, пока ты разгадаешь тайну.",
                                      self.f_small,NEON_PURPLE,355)
                self.draw_hero_front(WIDTH//2,460,scale=1.0)
                self.draw_button("✦ РАЗГАДАТЬ ТАЙНУ ✦",WIDTH//2,545,
                                 340,50,NEON_PURPLE,2)
            else:
                if is_boss:
                    self.draw_text_center(f"⚠ БОСС: {ename}",self.f_head,NEON_RED,355)
                    self.draw_text_center(
                        f"HP: {enemy.get('hp','?')} • Атака: {enemy.get('attack','?')}",
                        self.f_small,NEON_ORANGE,382)
                else:
                    self.draw_text_center(
                        f"Враг: {ename}   HP: {enemy.get('hp','?')}",
                        self.f_small,NEON_PURPLE,355)
                hs=self.f_small.render(loc["hint"],True,NEON_PURPLE)
                self.screen.blit(hs,hs.get_rect(center=(WIDTH//2,405)))
                self.draw_hero_front(WIDTH//2,490,scale=1.0)
                self.draw_button("ВСТРЕТИТЬ ТЕНЬ",WIDTH//2,565,300,50,
                                 NEON_RED if is_boss else NEON_PINK,0)
        else:
            self.draw_hero_front(WIDTH//2,395,scale=1.0)
            self.draw_button("ПРИСЛУШАТЬСЯ К ТИШИНЕ",WIDTH//2,495,
                             360,52,NEON_CYAN,0)
        self.draw_button("← Вернуться к карте",WIDTH//2,645,260,40,TEXT_DIM,1)

    def draw_collect(self):
        self.buttons=[]
        loc=ALL_LOCATIONS[self.current_loc]
        self.draw_text_center("✧ АУДИО-СЛЕПОК ПОЛУЧЕН ✧",self.f_head,NEON_GOLD,80)
        self.draw_text_center(f"«{loc['artifact']}»",self.f_big,NEON_CYAN,145)
        self.draw_location_scene(self.current_loc,WIDTH//2,260,w=380,h=160)
        self.draw_text_lines(loc["artifact_desc"].split("\n"),
                             self.f_body,TEXT_MAIN,WIDTH//2,395)
        self.draw_hero_front(WIDTH//2,520,scale=1.1)
        self.draw_button("Продолжить",WIDTH//2,640,240,44,NEON_CYAN,0)

    # ═══════════════ ГОЛОВОЛОМКИ ═══════════════
    def pick_puzzle_for_act(self,act):
        simple=["simon","match","order"]
        medium=simple+["lights","memory","math"]
        hard=medium+["cipher"]
        extreme=hard+["slider","arrows"]
        if act<=1: return random.choice(simple)
        if act==2: return random.choice(medium)
        if act==3: return random.choice(hard)
        if act==4: return random.choice(extreme)
        return random.choice(extreme)

    def start_puzzle(self,kind):
        self.state=self.ST_PUZZLE; self.puzzle_kind=kind; self.puzzle={}
        self.puzzle_message=""; self.puzzle_msg_timer=0
        self.puzzle_chain=[]; self.chain_index=0
        act=self.act
        if kind=="chain":
            first=self.pick_puzzle_for_act(act)
            pool=[first]
            for _ in range(2):
                nxt=self.pick_puzzle_for_act(act)
                for _t in range(5):
                    if nxt not in pool: break
                    nxt=self.pick_puzzle_for_act(act)
                pool.append(nxt)
            self.puzzle_chain=pool; self.chain_index=0
            kind=self.puzzle_chain[0]; self.puzzle_kind=kind
        if kind=="simon":
            length=3+act+(1 if act>=4 else 0)
            self.puzzle={"sequence":[random.randint(0,3) for _ in range(length)],
                         "phase":"show","show_timer":0,"input_idx":0,
                         "mistakes":0,"max_mistakes":2,
                         "highlight":-1,"flash_wrong":0,"flash_ok":0}
        elif kind=="match":
            npairs=min(6+act-1,12); nc=npairs*2
            cols=4 if nc<=16 else 6; rows=(nc+cols-1)//cols
            vals=list(range(npairs))*2; random.shuffle(vals)
            self.puzzle={"cols":cols,"rows":rows,
                         "cards":[{"val":v,"flipped":False,"matched":False}
                                  for v in vals],
                         "flipped_idx":[],"flash_timer":0,"moves":0}
        elif kind=="order":
            n=4+act; positions=[]
            for _ in range(n):
                for _t in range(40):
                    x=random.randint(80,WIDTH-80); y=random.randint(200,560)
                    if all(math.hypot(x-px,y-py)>80 for px,py in positions):
                        positions.append((x,y)); break
            while len(positions)<n:
                positions.append((random.randint(80,WIDTH-80),random.randint(200,560)))
            self.puzzle={"n":n,"positions":positions,"clicked":[],
                         "mistakes":0,"max_mistakes":2,"flash_wrong":0}
        elif kind=="lights":
            n=3 if act<=3 else 4; size=n*n; grid=[0]*size
            moves=3+act+(2 if act>=5 else 0)
            for _ in range(moves):
                i=random.randint(0,size-1); self._lights_toggle(grid,i,n)
            self.puzzle={"n":n,"grid":grid,"moves":0}
        elif kind=="memory":
            n=4+min(act,5); positions=[]
            for _ in range(n):
                for _t in range(40):
                    x=random.randint(120,WIDTH-120); y=random.randint(200,560)
                    if all(math.hypot(x-px,y-py)>90 for px,py in positions):
                        positions.append((x,y)); break
            while len(positions)<n:
                positions.append((random.randint(120,WIDTH-120),random.randint(200,560)))
            self.puzzle={"n":n,"positions":positions,"clicked":[],
                         "show_phase":"show","show_timer":0,
                         "show_duration":100+15*n,"mistakes":0,
                         "max_mistakes":2,"flash_wrong":0,"flash_ok":0}
        elif kind=="math":
            nq=3+act; qs=[]
            for _ in range(nq):
                mx=10+act*8
                a=random.randint(1,mx); b=random.randint(1,mx)
                op=random.choice(["+","-","*"]) if act>=3 else random.choice(["+","-"])
                if op=="+": ans=a+b; text=f"{a} + {b}"
                elif op=="-":
                    if b>a: a,b=b,a
                    ans=a-b; text=f"{a} - {b}"
                else: ans=a*b; text=f"{a} × {b}"
                opts={ans}
                while len(opts)<4:
                    delta=random.choice([-3,-2,-1,1,2,3,5,10])
                    c=ans+delta
                    if c>=0: opts.add(c)
                opts=list(opts); random.shuffle(opts)
                qs.append({"text":text,"answer":ans,"options":opts})
            self.puzzle={"questions":qs,"idx":0,"mistakes":0,"max_mistakes":2,
                         "flash_wrong":0,"time_per_q":300+(10-act)*30,"timer":0}
        elif kind=="cipher":
            syms=["◆","●","▲","★","⬢","■","♦","◈"]
            ns=min(3+act,len(syms)); chosen=random.sample(syms,ns)
            letters="АБВГДЕЖЗ"; pairs={chosen[i]:letters[i] for i in range(ns)}
            length=3+act; seq=[random.choice(chosen) for _ in range(length)]
            correct="".join(pairs[s] for s in seq); opts={correct}
            all_l=letters[:ns]
            while len(opts)<4:
                w="".join(random.choice(all_l) for _ in range(length))
                opts.add(w)
            opts=list(opts); random.shuffle(opts)
            self.puzzle={"pairs":pairs,"seq":seq,"correct":correct,
                         "options":opts,"mistakes":0,"max_mistakes":2,
                         "flash_wrong":0}
        elif kind=="slider":
            n=3 if act<=3 else 4; size=n*n
            board=list(range(1,size))+[0]; blank=size-1
            for _ in range(80+act*15):
                r,c=divmod(blank,n); moves=[]
                if r>0: moves.append(blank-n)
                if r<n-1: moves.append(blank+n)
                if c>0: moves.append(blank-1)
                if c<n-1: moves.append(blank+1)
                t=random.choice(moves)
                board[blank],board[t]=board[t],board[blank]; blank=t
            self.puzzle={"n":n,"board":board,"blank":blank,"moves":0}
        elif kind=="arrows":
            length=3+act; ar=["U","D","L","R"]
            self.puzzle={"sequence":[random.choice(ar) for _ in range(length)],
                         "phase":"show","show_timer":0,"input_idx":0,
                         "mistakes":0,"max_mistakes":2,
                         "highlight":-1,"flash_wrong":0,"flash_ok":0}
        self._play("puzzle")

    def _lights_toggle(self,grid,i,n):
        r,c=divmod(i,n)
        for dr,dc in [(0,0),(-1,0),(1,0),(0,-1),(0,1)]:
            nr,nc=r+dr,c+dc
            if 0<=nr<n and 0<=nc<n: grid[nr*n+nc]^=1

    def update_puzzle(self):
        if self.puzzle_msg_timer>0: self.puzzle_msg_timer-=1
        k=self.puzzle_kind
        if k=="simon":
            p=self.puzzle
            if p["flash_wrong"]>0: p["flash_wrong"]-=1
            if p["flash_ok"]>0: p["flash_ok"]-=1
            if p["phase"]=="show":
                p["show_timer"]+=1
                step=p["show_timer"]//35; sub=p["show_timer"]%35
                if step<len(p["sequence"]):
                    p["highlight"]=p["sequence"][step] if sub<22 else -1
                else:
                    p["phase"]="input"; p["highlight"]=-1; p["input_idx"]=0
        elif k=="match":
            p=self.puzzle
            if p["flash_timer"]>0:
                p["flash_timer"]-=1
                if p["flash_timer"]==0:
                    for idx in p["flipped_idx"]: p["cards"][idx]["flipped"]=False
                    p["flipped_idx"]=[]
        elif k=="order":
            if self.puzzle["flash_wrong"]>0: self.puzzle["flash_wrong"]-=1
        elif k=="memory":
            p=self.puzzle
            if p["flash_wrong"]>0: p["flash_wrong"]-=1
            if p["flash_ok"]>0: p["flash_ok"]-=1
            if p["show_phase"]=="show":
                p["show_timer"]+=1
                if p["show_timer"]>=p["show_duration"]: p["show_phase"]="input"
        elif k=="math":
            p=self.puzzle
            if p["flash_wrong"]>0: p["flash_wrong"]-=1
            p["timer"]+=1
            if p["timer"]>=p["time_per_q"]:
                p["timer"]=0; self._math_wrong()
        elif k=="cipher":
            if self.puzzle["flash_wrong"]>0: self.puzzle["flash_wrong"]-=1
        elif k=="arrows":
            p=self.puzzle
            if p["flash_wrong"]>0: p["flash_wrong"]-=1
            if p["flash_ok"]>0: p["flash_ok"]-=1
            if p["phase"]=="show":
                p["show_timer"]+=1
                step=p["show_timer"]//30; sub=p["show_timer"]%30
                if step<len(p["sequence"]):
                    p["highlight"]=step if sub<18 else -1
                else:
                    p["phase"]="input"; p["highlight"]=-1; p["input_idx"]=0

    def draw_puzzle(self):
        self.buttons=[]
        kind=self.puzzle_kind
        titles={"simon":"ЭХО-ПОВТОР","match":"ПАРНЫЕ ОСКОЛКИ","order":"ПОРЯДОК",
                "lights":"ОГНИ СУДЬБЫ","memory":"ПАМЯТЬ ЧИСЕЛ","math":"СЧЁТ ЭХА",
                "cipher":"ДРЕВНИЙ ШИФР","slider":"ПЯТНАШКИ","arrows":"ПУТЬ СТРЕЛОК"}
        subs={"simon":"Повтори свечения","match":"Найди пары","order":"Нажимай 1→N",
              "lights":"Погаси все огни","memory":"Запомни и нажми по порядку",
              "math":"Реши примеры","cipher":"Расшифруй последовательность",
              "slider":"Собери 1..N","arrows":"Повтори стрелки"}
        if self.puzzle_chain:
            prog=(f"Головоломка {self.chain_index+1}/{len(self.puzzle_chain)}: "
                  f"{titles[kind]}")
            self.draw_text_center("✦ ИСПЫТАНИЕ ✦",self.f_small,NEON_GOLD,25)
            self.draw_text_center(prog,self.f_big,NEON_CYAN,65)
        else:
            self.draw_text_center("✦ ГОЛОВОЛОМКА ✦",self.f_small,NEON_PURPLE,25)
            self.draw_text_center(titles[kind],self.f_big,NEON_CYAN,65)
        self.draw_text_center(subs[kind],self.f_sub,TEXT_MAIN,105)
        area=pygame.Rect(60,130,WIDTH-120,HEIGHT-255)
        pygame.draw.rect(self.screen,BG_PANEL,area,border_radius=10)
        pygame.draw.rect(self.screen,NEON_PURPLE,area,width=2,border_radius=10)
        drawer={"simon":self._draw_simon,"match":self._draw_match,
                "order":self._draw_order,"lights":self._draw_lights,
                "memory":self._draw_memory,"math":self._draw_math,
                "cipher":self._draw_cipher,"slider":self._draw_slider,
                "arrows":self._draw_arrows}.get(kind)
        if drawer: drawer()
        if self.puzzle_message:
            col=NEON_GREEN if ("решен" in self.puzzle_message.lower()
                                or "решены" in self.puzzle_message.lower()
                                or "шаг" in self.puzzle_message.lower()) else NEON_PINK
            self.draw_text_center(self.puzzle_message,self.f_sub,col,HEIGHT-100)
        pt=self._puzzle_progress_text()
        if pt: self.draw_text_center(pt,self.f_small,TEXT_DIM,HEIGHT-65)
        self.draw_button("Сдаться",WIDTH-90,65,140,36,TEXT_DIM,0)

    def _puzzle_progress_text(self):
        k=self.puzzle_kind; p=self.puzzle
        if k=="simon":
            return (f"Шаг {p['input_idx']}/{len(p['sequence'])}   "
                    f"Ошибки: {p['mistakes']}/{p['max_mistakes']}")
        if k=="match":
            m=sum(1 for c in p["cards"] if c["matched"])
            return f"Пары: {m//2}/{len(p['cards'])//2}   Ходы: {p['moves']}"
        if k=="order":
            return (f"Отмечено: {len(p['clicked'])}/{p['n']}   "
                    f"Ошибки: {p['mistakes']}/{p['max_mistakes']}")
        if k=="lights": return f"Огней: {sum(p['grid'])}   Ходы: {p['moves']}"
        if k=="memory":
            if p["show_phase"]=="show":
                left=max(0,(p["show_duration"]-p["show_timer"])//60)
                return f"Запоминай... {left} сек"
            return (f"Отмечено: {len(p['clicked'])}/{p['n']}   "
                    f"Ошибки: {p['mistakes']}/{p['max_mistakes']}")
        if k=="math":
            left=max(0,(p["time_per_q"]-p["timer"])//60)
            return (f"Вопрос {p['idx']+1}/{len(p['questions'])}   ⏱ {left} сек   "
                    f"Ошибки: {p['mistakes']}/{p['max_mistakes']}")
        if k=="cipher": return f"Ошибки: {p['mistakes']}/{p['max_mistakes']}"
        if k=="slider": return f"Ходы: {p['moves']}"
        if k=="arrows":
            return (f"Шаг {p['input_idx']}/{len(p['sequence'])}   "
                    f"Ошибки: {p['mistakes']}/{p['max_mistakes']}")
        return ""

    def _draw_simon(self):
        p=self.puzzle; cx,cy=WIDTH//2,(HEIGHT+100)//2
        offset=100; size=150
        pos=[(cx-offset,cy-offset),(cx+offset,cy-offset),
             (cx-offset,cy+offset),(cx+offset,cy+offset)]
        for i,(px,py) in enumerate(pos):
            rect=pygame.Rect(px-size//2,py-size//2,size,size)
            bc=self.KEY_COLORS[i]
            bright=(p["highlight"]==i) or \
                    (p["flash_ok"]>0 and p["input_idx"]>0 and
                     p["input_idx"]-1<len(p["sequence"]) and
                     i==p["sequence"][p["input_idx"]-1])
            if bright:
                fill=bc; border=TEXT_WHITE
                glow=pygame.Surface((size+40,size+40),pygame.SRCALPHA)
                for r in range(size//2+20,0,-4):
                    a=int(60*(1-r/(size/2+20)))
                    if a<=0: continue
                    pygame.draw.circle(glow,(*bc,a),(size//2+20,size//2+20),r)
                self.screen.blit(glow,(rect.x-20,rect.y-20))
            else:
                fill=tuple(max(15,c//5) for c in bc); border=bc
            pygame.draw.rect(self.screen,fill,rect,border_radius=14)
            pygame.draw.rect(self.screen,border,rect,width=3,border_radius=14)
            sym=self.f_key.render(self.KEY_LETTERS[i],True,border)
            self.screen.blit(sym,sym.get_rect(center=rect.center))
            self.buttons.append((rect,200+i))

    def _draw_match(self):
        p=self.puzzle; cols,rows=p["cols"],p["rows"]
        aw=min(720,cols*90); ah=min(400,rows*90)
        cx=WIDTH//2; cy=(HEIGHT+90)//2
        cw=aw//cols-8; ch=ah//rows-8
        x0=cx-(cols*(cw+8))//2; y0=cy-(rows*(ch+8))//2
        syms=[NEON_CYAN,NEON_PINK,NEON_PURPLE,NEON_GOLD,NEON_GREEN,(255,130,80),
              (180,180,255),NEON_RED,(140,220,180),(255,200,220),(200,150,255),
              (150,255,200)]
        for i,card in enumerate(p["cards"]):
            r=i//cols; c=i%cols
            x=x0+c*(cw+8); y=y0+r*(ch+8); rect=pygame.Rect(x,y,cw,ch)
            col=syms[card["val"]%len(syms)]
            if card["matched"]:
                pygame.draw.rect(self.screen,(30,30,50),rect,border_radius=8)
                pygame.draw.rect(self.screen,col,rect,width=2,border_radius=8)
                sx,sy=rect.centerx,rect.centery
                pygame.draw.polygon(self.screen,col,
                                     [(sx,sy-12),(sx+12,sy),(sx,sy+12),(sx-12,sy)])
            elif card["flipped"]:
                pygame.draw.rect(self.screen,BG_PANEL_HI,rect,border_radius=8)
                pygame.draw.rect(self.screen,col,rect,width=3,border_radius=8)
                sx,sy=rect.centerx,rect.centery
                pygame.draw.polygon(self.screen,col,
                                     [(sx,sy-14),(sx+14,sy),(sx,sy+14),(sx-14,sy)])
            else:
                pygame.draw.rect(self.screen,BG_PANEL_HI,rect,border_radius=8)
                pygame.draw.rect(self.screen,NEON_PURPLE,rect,width=2,border_radius=8)
                pygame.draw.line(self.screen,(80,60,120),(rect.x+10,rect.y+10),
                                  (rect.right-10,rect.bottom-10),1)
                pygame.draw.line(self.screen,(80,60,120),(rect.right-10,rect.y+10),
                                  (rect.x+10,rect.bottom-10),1)
            self.buttons.append((rect,200+i))

    def _draw_order(self):
        p=self.puzzle
        for i,(x,y) in enumerate(p["positions"]):
            n=i+1; already=n in p["clicked"]
            col=NEON_GREEN if already else NEON_CYAN
            fill=(20,50,30) if already else BG_PANEL_HI
            if p["flash_wrong"]>0: col=NEON_RED
            pygame.draw.circle(self.screen,fill,(x,y),28)
            pygame.draw.circle(self.screen,col,(x,y),28,3)
            s=self.f_big.render(str(n),True,col)
            self.screen.blit(s,s.get_rect(center=(x,y)))
            self.buttons.append((pygame.Rect(x-28,y-28,56,56),300+i))

    def _draw_lights(self):
        p=self.puzzle; n=p["n"]; cell=80; gap=12
        total=n*cell+(n-1)*gap
        x0=WIDTH//2-total//2; y0=(HEIGHT+60)//2-total//2+30
        for r in range(n):
            for c in range(n):
                i=r*n+c
                x=x0+c*(cell+gap); y=y0+r*(cell+gap)
                rect=pygame.Rect(x,y,cell,cell)
                if p["grid"][i]:
                    for rad in range(cell//2+15,0,-4):
                        a=int(80*(1-rad/(cell/2+15)))
                        if a<=0: continue
                        gs=pygame.Surface((cell+30,cell+30),pygame.SRCALPHA)
                        pygame.draw.circle(gs,(*NEON_GOLD,a),
                                            (cell//2+15,cell//2+15),rad)
                        self.screen.blit(gs,(x-15,y-15))
                    pygame.draw.rect(self.screen,NEON_GOLD,rect,border_radius=10)
                    pygame.draw.rect(self.screen,(255,240,180),rect,
                                      width=3,border_radius=10)
                else:
                    pygame.draw.rect(self.screen,BG_PANEL,rect,border_radius=10)
                    pygame.draw.rect(self.screen,TEXT_DIM,rect,width=2,border_radius=10)
                self.buttons.append((rect,200+i))

    def _draw_memory(self):
        p=self.puzzle; show=p["show_phase"]=="show"
        for i,(x,y) in enumerate(p["positions"]):
            n=i+1; cl=n in p["clicked"]
            if show: col=NEON_CYAN; fill=BG_PANEL_HI
            elif cl: col=NEON_GREEN; fill=(20,50,30)
            else: col=TEXT_DIM; fill=(25,25,35)
            if p["flash_wrong"]>0: col=NEON_RED
            pygame.draw.circle(self.screen,fill,(x,y),32)
            pygame.draw.circle(self.screen,col,(x,y),32,3)
            s=self.f_big.render(str(n) if (show or cl) else "?",True,col)
            self.screen.blit(s,s.get_rect(center=(x,y)))
            if not show:
                self.buttons.append((pygame.Rect(x-32,y-32,64,64),300+i))

    def _draw_math(self):
        p=self.puzzle
        if p["idx"]>=len(p["questions"]): return
        q=p["questions"][p["idx"]]
        self.draw_text_center(f"{q['text']} = ?",self.f_big,NEON_CYAN,260)
        bw=400; bx=WIDTH//2-bw//2
        frac=1.0-p["timer"]/p["time_per_q"]
        pygame.draw.rect(self.screen,(30,20,20),(bx,320,bw,12),border_radius=4)
        if frac>0:
            col=NEON_GREEN if frac>0.4 else (NEON_GOLD if frac>0.15 else NEON_RED)
            pygame.draw.rect(self.screen,col,(bx,320,int(bw*frac),12),border_radius=4)
        pygame.draw.rect(self.screen,NEON_PURPLE,(bx,320,bw,12),
                          width=2,border_radius=4)
        bw2,bh2=140,60; gap=20
        tot=4*bw2+3*gap; x0=WIDTH//2-tot//2; y0=400
        for i,opt in enumerate(q["options"]):
            rect=pygame.Rect(x0+i*(bw2+gap),y0,bw2,bh2)
            hover=self.hover_index==400+i
            bg=BG_PANEL_HI if hover else BG_PANEL
            border=NEON_RED if p["flash_wrong"]>0 else NEON_CYAN
            pygame.draw.rect(self.screen,bg,rect,border_radius=8)
            pygame.draw.rect(self.screen,border,rect,width=2,border_radius=8)
            s=self.f_big.render(str(opt),True,NEON_CYAN)
            self.screen.blit(s,s.get_rect(center=rect.center))
            self.buttons.append((rect,400+i))

    def _draw_cipher(self):
        p=self.puzzle
        self.draw_text_center("Легенда:",self.f_small,TEXT_DIM,180)
        pairs=list(p["pairs"].items()); n=len(pairs)
        x0=WIDTH//2-(n-1)*60//2
        for i,(sym,letter) in enumerate(pairs):
            x=x0+i*60
            self.draw_text_center(sym,self.f_big,NEON_PURPLE,220,x=x)
            self.draw_text_center("=",self.f_small,TEXT_DIM,250,x=x)
            self.draw_text_center(letter,self.f_big,NEON_CYAN,285,x=x)
        self.draw_text_center("Расшифруй:",self.f_small,TEXT_DIM,330)
        seq=p["seq"]; sx0=WIDTH//2-(len(seq)-1)*55//2
        for i,sym in enumerate(seq):
            self.draw_text_center(sym,self.f_big,NEON_GOLD,375,x=sx0+i*55)
        bw,bh=180,55; gap=12; tot=2*bw+gap
        for i,opt in enumerate(p["options"]):
            col=i%2; row=i//2
            rect=pygame.Rect(WIDTH//2-tot//2+col*(bw+gap),
                              430+row*(bh+gap),bw,bh)
            hover=self.hover_index==400+i
            bg=BG_PANEL_HI if hover else BG_PANEL
            border=NEON_RED if p["flash_wrong"]>0 else NEON_CYAN
            pygame.draw.rect(self.screen,bg,rect,border_radius=8)
            pygame.draw.rect(self.screen,border,rect,width=2,border_radius=8)
            s=self.f_head.render(opt,True,NEON_CYAN)
            self.screen.blit(s,s.get_rect(center=rect.center))
            self.buttons.append((rect,400+i))

    def _draw_slider(self):
        p=self.puzzle; n=p["n"]; cell=80; gap=8
        total=n*cell+(n-1)*gap
        x0=WIDTH//2-total//2; y0=(HEIGHT+60)//2-total//2+20
        for r in range(n):
            for c in range(n):
                idx=r*n+c; val=p["board"][idx]
                rect=pygame.Rect(x0+c*(cell+gap),y0+r*(cell+gap),cell,cell)
                if val==0:
                    pygame.draw.rect(self.screen,(10,10,20),rect,border_radius=8)
                    pygame.draw.rect(self.screen,TEXT_DIM,rect,width=2,border_radius=8)
                else:
                    ip=(val==idx+1)
                    col=NEON_GREEN if ip else NEON_CYAN
                    bg=(20,50,30) if ip else BG_PANEL_HI
                    pygame.draw.rect(self.screen,bg,rect,border_radius=8)
                    pygame.draw.rect(self.screen,col,rect,width=2,border_radius=8)
                    s=self.f_big.render(str(val),True,col)
                    self.screen.blit(s,s.get_rect(center=rect.center))
                    self.buttons.append((rect,400+idx))

    def _draw_arrows(self):
        p=self.puzzle
        cx,cy=WIDTH//2,(HEIGHT+100)//2
        arrows={"U":"↑","D":"↓","L":"←","R":"→"}
        if p["phase"]=="show":
            idx=p["highlight"]
            if 0<=idx<len(p["sequence"]):
                a=p["sequence"][idx]
                self.draw_text_center(arrows[a],self.f_arrow,NEON_GOLD,cy,x=cx)
            else:
                self.draw_text_center("• • •",self.f_arrow,TEXT_DIM,cy,x=cx)
        else:
            for i in range(len(p["sequence"])):
                x=cx-(len(p["sequence"])-1)*45//2+i*45
                if i<p["input_idx"]:
                    col=NEON_GREEN; txt=arrows[p["sequence"][i]]
                else:
                    col=TEXT_DIM; txt="?"
                self.draw_text_center(txt,self.f_arrow,col,cy,x=x)
        self.draw_text_center("Нажимай ↑ ↓ ← → на клавиатуре",
                              self.f_sub,TEXT_DIM,560)

    def handle_puzzle_click(self,pos,idx):
        if idx==0: self.state=self.ST_LOCATION; return
        k=self.puzzle_kind
        if k=="simon" and 200<=idx<300: self._simon_click(idx-200)
        elif k=="match" and 200<=idx<300: self._match_click(idx-200)
        elif k=="order" and 300<=idx<400: self._order_click(idx-300+1)
        elif k=="lights" and 200<=idx<300: self._lights_click(idx-200)
        elif k=="memory" and 300<=idx<400: self._memory_click(idx-300+1)
        elif k=="math" and 400<=idx<500: self._math_click(idx-400)
        elif k=="cipher" and 400<=idx<500: self._cipher_click(idx-400)
        elif k=="slider" and 400<=idx<500: self._slider_click(idx-400)

    def _simon_click(self,i):
        p=self.puzzle
        if p["phase"]!="input": return
        if i==p["sequence"][p["input_idx"]]:
            p["highlight"]=i; p["flash_ok"]=15
            self._play_index("tile",i); p["input_idx"]+=1
            if p["input_idx"]>=len(p["sequence"]): self._puzzle_solved()
        else:
            p["mistakes"]+=1; p["flash_wrong"]=20; self._play("error")
            if p["mistakes"]>=p["max_mistakes"]:
                self.puzzle_message="Слишком много ошибок. Заново."
                self.puzzle_msg_timer=90; self.start_puzzle("simon")
            else:
                p["phase"]="show"; p["show_timer"]=0; p["input_idx"]=0

    def _match_click(self,ci):
        p=self.puzzle; card=p["cards"][ci]
        if card["matched"] or card["flipped"] or p["flash_timer"]>0: return
        card["flipped"]=True; p["flipped_idx"].append(ci); self._play("click")
        if len(p["flipped_idx"])==2:
            p["moves"]+=1
            a=p["cards"][p["flipped_idx"][0]]; b=p["cards"][p["flipped_idx"][1]]
            if a["val"]==b["val"]:
                a["matched"]=True; b["matched"]=True
                p["flipped_idx"]=[]; self._play("solve")
                if all(c["matched"] for c in p["cards"]): self._puzzle_solved()
            else: p["flash_timer"]=40

    def _order_click(self,n):
        p=self.puzzle
        if n==len(p["clicked"])+1:
            p["clicked"].append(n); self._play("click")
            if len(p["clicked"])>=p["n"]: self._puzzle_solved()
        else:
            p["mistakes"]+=1; p["flash_wrong"]=15; p["clicked"]=[]
            self._play("error")
            if p["mistakes"]>=p["max_mistakes"]:
                self.puzzle_message="Слишком много ошибок. Заново."
                self.puzzle_msg_timer=90; self.start_puzzle("order")

    def _lights_click(self,i):
        p=self.puzzle; self._lights_toggle(p["grid"],i,p["n"]); p["moves"]+=1
        self._play("click")
        if all(v==0 for v in p["grid"]): self._play("solve"); self._puzzle_solved()

    def _memory_click(self,n):
        p=self.puzzle
        if p["show_phase"]!="input": return
        if n==len(p["clicked"])+1:
            p["clicked"].append(n); p["flash_ok"]=10; self._play("click")
            if len(p["clicked"])>=p["n"]: self._puzzle_solved()
        else:
            p["mistakes"]+=1; p["flash_wrong"]=15; p["clicked"]=[]
            self._play("error")
            if p["mistakes"]>=p["max_mistakes"]:
                self.puzzle_message="Слишком много ошибок. Заново."
                self.puzzle_msg_timer=90; self.start_puzzle("memory")

    def _math_click(self,oi):
        p=self.puzzle
        if p["idx"]>=len(p["questions"]): return
        q=p["questions"][p["idx"]]
        if oi>=len(q["options"]): return
        if q["options"][oi]==q["answer"]:
            p["idx"]+=1; p["timer"]=0; self._play("click")
            if p["idx"]>=len(p["questions"]):
                self._play("solve"); self._puzzle_solved()
        else: self._math_wrong()

    def _math_wrong(self):
        p=self.puzzle
        p["mistakes"]+=1; p["flash_wrong"]=20; p["timer"]=0
        self._play("error")
        if p["mistakes"]>=p["max_mistakes"]:
            self.puzzle_message="Слишком много ошибок. Заново."
            self.puzzle_msg_timer=90; self.start_puzzle("math")

    def _cipher_click(self,oi):
        p=self.puzzle
        if oi>=len(p["options"]): return
        if p["options"][oi]==p["correct"]:
            self._play("solve"); self._puzzle_solved()
        else:
            p["mistakes"]+=1; p["flash_wrong"]=15; self._play("error")
            if p["mistakes"]>=p["max_mistakes"]:
                self.puzzle_message="Слишком много ошибок. Заново."
                self.puzzle_msg_timer=90; self.start_puzzle("cipher")

    def _slider_click(self,idx):
        p=self.puzzle; n=p["n"]; blank=p["blank"]
        br,bc=divmod(blank,n); r,c=divmod(idx,n)
        if abs(br-r)+abs(bc-c)!=1: return
        p["board"][blank],p["board"][idx]=p["board"][idx],p["board"][blank]
        p["blank"]=idx; p["moves"]+=1; self._play("click")
        solved=(all(p["board"][i]==i+1 for i in range(n*n-1))
                and p["board"][-1]==0)
        if solved: self._play("solve"); self._puzzle_solved()

    def handle_arrow_key(self,key):
        p=self.puzzle
        if p["phase"]!="input": return
        amap={pygame.K_UP:"U",pygame.K_DOWN:"D",pygame.K_LEFT:"L",pygame.K_RIGHT:"R"}
        if key not in amap: return
        ch=amap[key]
        if ch==p["sequence"][p["input_idx"]]:
            p["highlight"]=p["input_idx"]; p["flash_ok"]=12
            self._play_index("tile",p["input_idx"]%4); p["input_idx"]+=1
            if p["input_idx"]>=len(p["sequence"]):
                self._play("solve"); self._puzzle_solved()
        else:
            p["mistakes"]+=1; p["flash_wrong"]=20; self._play("error")
            if p["mistakes"]>=p["max_mistakes"]:
                self.puzzle_message="Слишком много ошибок. Заново."
                self.puzzle_msg_timer=90; self.start_puzzle("arrows")
            else:
                p["phase"]="show"; p["show_timer"]=0; p["input_idx"]=0

    def _puzzle_solved(self):
        self._play("solve")
        if self.puzzle_chain and self.chain_index<len(self.puzzle_chain)-1:
            self.chain_index+=1
            nk=self.puzzle_chain[self.chain_index]
            sc=self.puzzle_chain; si=self.chain_index
            self.start_puzzle(nk)
            self.puzzle_chain=sc; self.chain_index=si
            self.puzzle_kind=nk
            self.puzzle_message=f"Шаг {si}/{len(sc)} решён!"
            self.puzzle_msg_timer=60
            return
        self.puzzles_done.add(self.current_loc)
        self.puzzle_message="Все тайны раскрыты!"
        self.puzzle_msg_timer=90
        self.state=self.ST_LOCATION

    # ═══════════════ БОЙ ═══════════════
    def start_battle(self):
        self.state=self.ST_BATTLE; self.notes=[]
        cfg=self.get_battle_config()
        le=ALL_LOCATIONS[self.current_loc].get("enemy",{})
        self.enemy={"name":le.get("name","Тень"),
                    "max_hp":le.get("hp",60),"hp":le.get("hp",60),
                    "attack":le.get("attack",8),
                    "color":le.get("color",(140,100,160)),
                    "shards":le.get("shards",10),
                    "boss":le.get("boss",False)}
        self.spawn_timer=0; self.total_spawned=0
        self.active_keys=list(cfg["keys"])
        self.col_x=self.get_column_positions()
        self.spawn_interval=cfg["spawn"]; self.speed=cfg["speed"]
        self.max_notes=cfg["notes"]; self.hit_window=cfg["window"]
        self.feedback_text=""; self.feedback_timer=0
        self.battle_flash=0; self.hit_flash=0; self.hurt_flash=0
        self.key_cd=[0,0,0,0]
        self.boss_phase2=False; self.safe_window=0
        self.player_invuln=0; self.player_combo=0; self.combo_dmg_bonus=0
        self.enemy_combo=0
        self.shake_timer=0; self.shake_mag=0; self.lightning_timer=0
        self.particles=[]
        self.companion_assist_used=False
        self.companion_atk_bonus=0; self.companion_window_bonus=0
        self.companion_buff_timer=0
        self.note_style="normal"
        self.keys_held.clear()
        self.battle_start_time=_time.time()
        self.apply_battle_modifiers()
        # Музыка
        if self.act==6:
            self.set_music("final")
        elif self.enemy["boss"]:
            self.set_music("boss")
        else:
            self.set_music("battle")
        if self.enemy["boss"]: self._play("boss")
        if self.active_companion and self.companion_msg_timer<=0:
            c=COMPANIONS[self.active_companion]
            self.companion_message=f"{c['name']}: «{c['lines']['battle']}»"
            self.companion_msg_timer=120

    def apply_battle_modifiers(self):
        pool=MODIFIER_POOLS.get(self.act,[])
        if not pool: self.enemy_mods=[]; return
        if self.enemy["boss"]: n=random.randint(1,2)
        else: n=0 if random.random()<0.6 else 1
        picked=random.sample(pool,min(n,len(pool)))
        self.enemy_mods=picked
        hm=1.0; am=1.0; sd=0; spd=0; wd=0; rm=1.0
        for mid in picked:
            m=MODIFIERS[mid]
            hm*=m.get("hp_mult",1.0); am*=m.get("atk_mult",1.0)
            sd+=m.get("speed",0); spd+=m.get("spawn",0)
            wd+=m.get("window_mod",0); rm*=m.get("reward_mult",1.0)
            if m.get("note_style") and m["note_style"]!="normal":
                self.note_style=m["note_style"]
        self.enemy["max_hp"]=int(self.enemy["max_hp"]*hm)
        self.enemy["hp"]=self.enemy["max_hp"]
        self.enemy["attack"]=max(1,int(self.enemy["attack"]*am))
        self.enemy["shards"]=int(self.enemy["shards"]*rm)
        self.spawn_interval=max(14,self.spawn_interval+spd)
        self.speed=max(2,min(11,self.speed+sd))
        self.hit_window=max(50,min(160,self.hit_window+wd))

    def update_battle(self):
        for i in range(4):
            if self.key_cd[i]>0: self.key_cd[i]-=1
        if self.player_invuln>0: self.player_invuln-=1
        if self.companion_buff_timer>0:
            self.companion_buff_timer-=1
            if self.companion_buff_timer==0:
                self.companion_atk_bonus=0
                self.companion_window_bonus=0
        if self.shake_timer>0:
            self.shake_timer-=1
        if self.lightning_timer>0:
            self.lightning_timer-=1

        # Обновление частиц
        self.particles=[p for p in self.particles
                        if p["life"]>0]
        for p in self.particles:
            p["x"]+=p["vx"]; p["y"]+=p["vy"]; p["life"]-=1

        # Фаза босса
        if self.enemy and self.enemy["boss"] and not self.boss_phase2:
            if self.enemy["hp"]<=self.enemy["max_hp"]//2:
                self.boss_phase2=True
                self.spawn_interval=max(15,int(self.spawn_interval*0.7))
                self.speed=min(9,self.speed+1)
                self.safe_window=60
                self.show_feedback("Яростный шёпот! Тень ускоряется!",NEON_RED)
                self.battle_flash=20
                # Финал-босс: тряска и молнии
                if self.act==6:
                    self.shake_timer=30; self.shake_mag=12
                    self._spawn_lightning_burst()
                    self._play("thunder")

        if self.safe_window>0: self.safe_window-=1

        if self.safe_window<=0:
            self.spawn_timer+=1
            if (self.spawn_timer>=self.spawn_interval
                    and self.total_spawned<self.max_notes):
                self.spawn_timer=0; self.spawn_note()
        if self.total_spawned>=self.max_notes and not self.notes:
            if self.enemy["hp"]>0:
                self.total_spawned=0
                self.max_notes=max(self.max_notes,15)

        # Финальный босс — случайные молнии и частицы
        if self.act==6 and self.enemy["boss"]:
            if random.random()<0.02:
                self.lightning_timer=8
                self._play("thunder")
                self._spawn_lightning_burst()
            if random.random()<0.3:
                px=random.randint(WIDTH//2-200,WIDTH//2+200)
                py=random.randint(50,200)
                self.particles.append({
                    "x":px,"y":py,
                    "vx":random.uniform(-2,2),"vy":random.uniform(-3,-1),
                    "life":random.randint(20,50),
                    "color":random.choice([NEON_RED,NEON_ORANGE,NEON_GOLD])})

        for note in self.notes:
            note["y"]+=self.speed
            if (not note["hit"] and not note["missed"]
                    and note["y"]>self.target_y+self.hit_window):
                note["missed"]=True; self.enemy_combo+=1
                if self.player_invuln>0:
                    self.show_feedback("Щит держит удар!",NEON_CYAN)
                    self._play("shield")
                else:
                    dmg=max(1,self.enemy["attack"]-self.base_def)
                    self.player_hp=max(0,self.player_hp-dmg)
                    self.hurt_flash=15
                    self.player_invuln=40
                    self.show_feedback(f"Тень бьёт! -{dmg} HP",NEON_RED)
                    self._play("miss")
                    self.player_combo=0; self.combo_dmg_bonus=0
                    if self.act==6 and self.enemy["boss"]:
                        self.shake_timer=15; self.shake_mag=8
                    if self.enemy_combo>=3:
                        self.safe_window=40; self.enemy_combo=0
                        self.show_feedback("Тень переводит дух...",NEON_GOLD)
                    # Компаньон беспокоится
                    if self.active_companion and self.player_hp < self.max_hp*0.3:
                        if self.companion_msg_timer<=0:
                            c=COMPANIONS[self.active_companion]
                            self.companion_message=f"{c['name']}: «{c['lines']['low_hp']}»"
                            self.companion_msg_timer=120

        self.notes=[n for n in self.notes if n["y"]<=HEIGHT+60]

        if self.feedback_timer>0:
            self.feedback_timer-=1
            if self.feedback_timer==0: self.feedback_text=""
        if self.battle_flash>0: self.battle_flash-=1
        if self.hit_flash>0: self.hit_flash-=1
        if self.hurt_flash>0: self.hurt_flash-=1
        if self.companion_msg_timer>0: self.companion_msg_timer-=1

        if self.enemy["hp"]<=0:
            self.win_battle(); return
        if self.player_hp<=0:
            self.state=self.ST_LOSE; self._play("lose"); return

    def _spawn_lightning_burst(self):
        """Молнии для финального босса."""
        for _ in range(3):
            x=random.randint(100,WIDTH-100)
            self.particles.append({
                "x":x,"y":0,
                "vx":random.uniform(-1,1),"vy":random.uniform(8,15),
                "life":random.randint(15,30),
                "color":(255,255,255),"lightning":True})

    def win_battle(self):
        self.state=self.ST_WIN
        self.shards+=self.enemy["shards"]
        self.drops_this_fight=self.roll_loot(self.current_loc)
        self.reward_popup=None
        for iid in self.drops_this_fight: self.inventory.add(iid)
        if self.drops_this_fight:
            self.reward_popup=self.drops_this_fight[0]
            rar=ITEMS[self.drops_this_fight[0]].get("rarity","common")
            self._play("legendary" if rar=="legendary" else "drop")
        self.done.add(self.current_loc)
        # Компаньон радуется
        if self.active_companion:
            c=COMPANIONS[self.active_companion]
            self.companion_message=f"{c['name']}: «{c['lines']['win']}»"
            self.companion_msg_timer=180
        self.set_music("happy")
        if self.act==1 and self.act_all_done(1) and not self.epic_elixir_received:
            self.potions["epic_elixir"]=self.potions.get("epic_elixir",0)+1
            self.epic_elixir_received=True
            self.show_feedback("Получен Эликсир Пробуждения!",NEON_PURPLE)
        # Разблокировка компаньонов по актам
        for cid in COMPANION_ORDER:
            if COMPANIONS[cid]["unlock_act"]<=self.act and cid not in self.companions:
                self.unlock_companion(cid)
                break
        self._play("win")
        self.save_game()  # автосохранение после победы

    def use_potion(self,pid):
        if pid not in self.potions or self.potions[pid]<=0: return
        p=POTIONS[pid]; self.potions[pid]-=1
        if self.potions[pid]<=0: del self.potions[pid]
        if p["heal"]>=9999: self.player_hp=self.max_hp
        else: self.player_hp=min(self.max_hp,self.player_hp+p["heal"])
        if p.get("atk_bonus"): self.base_atk+=p["atk_bonus"]
        if p.get("def_bonus"): self.base_def+=p["def_bonus"]
        if p.get("hp_bonus"):
            self.base_max_hp+=p["hp_bonus"]
            self.player_hp=min(self.base_max_hp,self.player_hp+p["hp_bonus"])
        self.recalc_stats(); self._play("heal")
        self.show_feedback(f"+{p['desc']}",NEON_GREEN)

    def spawn_note(self):
        idx=random.choice(self.active_keys)
        self.notes.append({"col":idx,"y":-40,"hit":False,"missed":False})
        self.total_spawned+=1
        if self.note_style=="dual" and random.random()<0.25:
            others=[k for k in self.active_keys if k!=idx]
            if others:
                idx2=random.choice(others)
                self.notes.append({"col":idx2,"y":-40,"hit":False,"missed":False})
                self.total_spawned+=1
        elif self.note_style=="burst" and random.random()<0.35:
            for _ in range(2):
                self.notes.append({"col":random.choice(self.active_keys),
                                    "y":-40,"hit":False,"missed":False})
                self.total_spawned+=1
        elif self.note_style=="wave" and self.notes:
            last=self.notes[-1]["col"]
            try:
                pos=self.active_keys.index(last)
                nxt=self.active_keys[(pos+1)%len(self.active_keys)]
                self.notes[-1]["col"]=nxt
            except ValueError: pass

    def show_feedback(self,text,color):
        self.feedback_text=text; self.feedback_color=color
        self.feedback_timer=55

    def handle_battle_key(self,key):
        if key not in self.KEYS: return
        idx=self.KEYS.index(key)
        if idx not in self.active_keys: return
        if self.key_cd[idx]>0: return
        self.key_cd[idx]=4
        best=None; bd=9999
        for n in self.notes:
            if n["hit"] or n["missed"]: continue
            if n["col"]!=idx: continue
            d=abs(n["y"]-self.target_y)
            if d<bd: best=n; bd=d
        if best is not None and bd<=self.hit_window:
            best["hit"]=True
            self.player_combo+=1
            self.combo_dmg_bonus=min(10,(self.player_combo//5)*2)
            if self.player_combo%5==0:
                self._play("combo")
                self.show_feedback(f"Комбо x{self.player_combo}! +{self.combo_dmg_bonus} ATK",
                                    NEON_GOLD)
            dmg=self.get_attack_power()
            self.enemy["hp"]=max(0,self.enemy["hp"]-dmg)
            self.hit_flash=10; self.battle_flash=6
            if self.act==6 and self.enemy["boss"]:
                self.shake_timer=4; self.shake_mag=3
            self._play_index("hit",idx)
            if self.player_combo%5!=0:
                self.show_feedback(
                    ALL_LOCATIONS[self.current_loc]["battle_text"],NEON_CYAN)

    def draw_battle(self):
        self.buttons=[]
        loc=ALL_LOCATIONS[self.current_loc]
        # Тряска
        sx=sy=0
        if self.shake_timer>0:
            sx=random.randint(-self.shake_mag,self.shake_mag)
            sy=random.randint(-self.shake_mag,self.shake_mag)
        offset=(sx,sy)

        # Фон с тряской
        bg_surf=self.screen.copy()
        self.screen.fill(BG_DARK)
        # Молния
        if self.lightning_timer>0:
            lm=pygame.Surface((WIDTH,HEIGHT)); lm.set_alpha(80)
            lm.fill(NEON_WHITE if False else (255,255,255))
            self.screen.blit(lm,(0,0))

        if self.battle_flash>0:
            alpha=int(60*(self.battle_flash/20))
            fl=pygame.Surface((WIDTH,HEIGHT)); fl.set_alpha(alpha)
            fl.fill(NEON_CYAN); self.screen.blit(fl,(0,0))
        if self.hurt_flash>0:
            alpha=int(100*(self.hurt_flash/15))
            fl=pygame.Surface((WIDTH,HEIGHT)); fl.set_alpha(alpha)
            fl.fill(NEON_RED); self.screen.blit(fl,(0,0))

        act_color=ACTS[self.act]["color"]
        self.draw_text_center(f"Битва: {self.enemy['name']}",
                              self.f_head,act_color,22)

        if self.enemy_mods:
            mx=12; my=48
            for mid in self.enemy_mods:
                m=MODIFIERS[mid]
                t=self.f_tiny.render(f"◆ {m['name']}",True,m["color"])
                self.screen.blit(t,(mx,my)); my+=16

        eh_frac=self.enemy["hp"]/max(1,self.enemy["max_hp"])
        bw=500; eh=pygame.Rect(WIDTH//2-bw//2,48,bw,20)
        pygame.draw.rect(self.screen,(30,10,15),eh,border_radius=3)
        fw=int(bw*eh_frac)
        if fw>0:
            col=NEON_RED if self.enemy["boss"] else NEON_PINK
            pygame.draw.rect(self.screen,col,(eh.x,eh.y,fw,eh.h),border_radius=3)
        pygame.draw.rect(self.screen,NEON_RED,eh,width=2,border_radius=3)
        et=self.f_small.render(
            f"{self.enemy['name']} — {self.enemy['hp']}/{self.enemy['max_hp']}",
            True,TEXT_WHITE)
        self.screen.blit(et,et.get_rect(center=eh.center))

        ph_frac=self.player_hp/max(1,self.max_hp)
        ph=pygame.Rect(20,HEIGHT-35,220,20)
        pygame.draw.rect(self.screen,(30,15,20),ph,border_radius=3)
        fw=int(ph.w*ph_frac)
        if fw>0:
            pygame.draw.rect(self.screen,HP_RED,(ph.x,ph.y,fw,ph.h),border_radius=3)
        pygame.draw.rect(self.screen,HP_RED,ph,width=2,border_radius=3)
        pt=self.f_small.render(f"HP {self.player_hp}/{self.max_hp}",True,TEXT_WHITE)
        self.screen.blit(pt,pt.get_rect(center=ph.center))
        self.screen.blit(self.f_small.render(f"ATK {self.get_attack_power()}",
                                               True,NEON_ORANGE),(260,HEIGHT-30))

        if self.player_combo>0:
            cc=NEON_GOLD if self.player_combo>=5 else NEON_CYAN
            self.draw_text_center(f"🔥 Комбо x{self.player_combo}",
                                   self.f_small,cc,HEIGHT-55)
        if self.player_invuln>0:
            self.draw_text_center("🛡",self.f_head,NEON_CYAN,60)

        # Компаньон в углу
        if self.active_companion:
            c=COMPANIONS[self.active_companion]
            c_x=WIDTH-120; c_y=60
            self._draw_glow(c_x,c_y,30,c["color"])
            pygame.draw.circle(self.screen,c["color"],(c_x,c_y),12)
            pygame.draw.circle(self.screen,(20,20,30),(c_x,c_y),10)
            if not self.companion_assist_used:
                qs=self.f_small.render("[Q]",True,NEON_GOLD)
                self.screen.blit(qs,(c_x-50,c_y-8))

        # Кнопки зелий
        pot_list=[p for p in self.potions if p in POTIONS and self.potions[p]>0]
        for i,pid in enumerate(pot_list[:3]):
            rect=pygame.Rect(WIDTH-200,HEIGHT-130+i*38,190,34)
            p=POTIONS[pid]
            pygame.draw.rect(self.screen,BG_PANEL,rect,border_radius=5)
            pygame.draw.rect(self.screen,p["color"],rect,width=2,border_radius=5)
            self.screen.blit(self.f_tiny.render(
                f"[{i+1}] {p['name']} x{self.potions[pid]}",True,p["color"]),
                (rect.x+8,rect.y+8))
            self.buttons.append((rect,400+i))

        if self.hit_flash>0:
            dmg=self.get_attack_power()
            ds=self.f_big.render(f"-{dmg}",True,NEON_GOLD)
            self.screen.blit(ds,(WIDTH//2+60,130))

        # Тень
        t=self.enemy["hp"]/max(1,self.enemy["max_hp"])
        self.draw_shadow_figure(WIDTH//2+sx,175+sy,t,
                                 custom_color=self.enemy["color"],
                                 is_boss=self.enemy["boss"])

        # Колонки
        for i,k in enumerate(self.active_keys):
            x=self.col_x[i]+sx
            color=self.KEY_COLORS[k]
            pygame.draw.line(self.screen,DARK_LINE,(x,240),
                              (x,self.target_y-42+sy),2)
            zone=pygame.Rect(x-42,self.target_y-42+sy,84,84)
            pygame.draw.rect(self.screen,color,zone,width=2,border_radius=6)
            fl=pygame.Surface((80,80),pygame.SRCALPHA)
            fl.fill((*color,18)); self.screen.blit(fl,(x-40,self.target_y-40+sy))
            letter=self.f_key.render(self.KEY_LETTERS[k],True,color)
            self.screen.blit(letter,letter.get_rect(center=(x,self.target_y+75+sy)))

        for n in self.notes:
            try:
                ia=self.active_keys.index(n["col"]); x=self.col_x[ia]+sx
            except ValueError: continue
            if n["hit"]: col=NEON_GOLD
            elif n["missed"]: col=(42,42,62)
            else: col=self.KEY_COLORS[n["col"]]
            letter=self.f_note.render(self.KEY_LETTERS[n["col"]],True,col)
            self.screen.blit(letter,letter.get_rect(center=(x,n["y"]+sy)))

        # Частицы
        for p in self.particles:
            if p.get("lightning"):
                pygame.draw.line(self.screen,(255,255,255),
                                  (p["x"],p["y"]),
                                  (p["x"]+random.randint(-8,8),
                                   p["y"]+random.randint(0,10)),2)
            else:
                pygame.draw.circle(self.screen,p["color"],
                                    (int(p["x"]),int(p["y"])),2)

        if self.feedback_text:
            self.draw_text_center(self.feedback_text,self.f_sub,
                                   self.feedback_color,630)
        if self.companion_message:
            self.draw_text_center(self.companion_message,self.f_small,
                                   COMPANIONS[self.active_companion]["color"]
                                   if self.active_companion else TEXT_MAIN,580)
        self.draw_button("Сдаться",WIDTH-90,22,140,32,TEXT_DIM,0)

    # ═══════════════ ПОБЕДА / ПОРАЖЕНИЕ / ФИНАЛ ═══════════════
    def draw_win(self):
        self.buttons=[]
        loc=ALL_LOCATIONS[self.current_loc]
        self.draw_text_center("✦ ТЕНЬ ПОБЕЖДЕНА ✦",self.f_head,NEON_GOLD,45)
        self.draw_text_center(self.enemy["name"],self.f_big,NEON_PURPLE,90)
        self.draw_text_center(f"◈ +{self.enemy['shards']}",self.f_head,NEON_GOLD,130)
        self.draw_shadow_figure(WIDTH//2,220,1.0,
                                 custom_color=loc["enemy"].get("color"),
                                 is_boss=self.enemy["boss"])
        sl=[f'«{l}»' for l in loc["story"].split("\n")]
        self.draw_text_lines(sl,self.f_sub,NEON_CYAN,WIDTH//2,320)
        if self.companion_message:
            self.draw_text_center(self.companion_message,self.f_sub,
                                   COMPANIONS[self.active_companion]["color"]
                                   if self.active_companion else NEON_PINK,
                                   385)
        if self.drops_this_fight:
            box=pygame.Rect(WIDTH//2-260,400,520,110)
            pygame.draw.rect(self.screen,BG_PANEL_HI,box,border_radius=10)
            main=ITEMS[self.drops_this_fight[0]]
            rar=main.get("rarity","common"); mc=RARITY_COLORS[rar]
            pygame.draw.rect(self.screen,mc,box,width=2,border_radius=10)
            self.draw_text_center("НОВЫЙ ПРЕДМЕТ",self.f_small,NEON_GOLD,418)
            self.draw_text_center(main["name"],self.f_head,main["color"],448)
            self.draw_text_center(
                f"{SLOT_NAMES[main['slot']]} • {RARITY_NAMES[rar]} • {main['desc']}",
                self.f_tiny,TEXT_MAIN,476)
        else:
            box=pygame.Rect(WIDTH//2-260,400,520,80)
            pygame.draw.rect(self.screen,BG_PANEL_HI,box,border_radius=10)
            pygame.draw.rect(self.screen,TEXT_DIM,box,width=2,border_radius=10)
            self.draw_text_center("Тень ушла без следа...",self.f_sub,
                                   TEXT_DIM,440)
        self.draw_hero_front(WIDTH//2,590,scale=1.15)
        self.draw_button("Продолжить путь",WIDTH//2,665,300,40,NEON_CYAN,0)

    def draw_lose(self):
        self.buttons=[]
        self.set_music("sad")
        self.draw_text_center("ТЫ ПАЛ В БОЮ...",self.f_head,NEON_RED,130)
        self.draw_text_lines([
            "Тень победила. Но ты можешь попробовать снова.",
            "",
            "Совет: купи оружие в магазине (M), используй зелья (1/2/3),",
            "активируй компаньона (Q) и надень артефакты в инвентаре (I).",
        ],self.f_body,TEXT_MAIN,WIDTH//2,260)
        self.draw_hero_front(WIDTH//2,420,scale=1.15)
        self.draw_button("Попробовать снова",WIDTH//2,555,320,52,NEON_PINK,0)
        self.draw_button("Вернуться к карте",WIDTH//2,630,260,42,TEXT_DIM,1)

    def draw_end(self):
        self.buttons=[]
        self.set_music("happy")
        self.draw_text_center("✦ ГОРОД ПРОБУЖДАЕТСЯ ✦",self.f_big,NEON_GOLD,60)
        self.draw_text_lines([
            "Тени обрели голоса. Их истории вернулись к ним —",
            "и вместе с ними вернулся цвет.",
            "",
            "Забытый Город больше не молчит.",
            "Ты не сражался — ты слушал. И этого оказалось достаточно.",
        ],self.f_body,TEXT_MAIN,WIDTH//2,220)
        self.draw_text_center(
            f"⏱ Время: {self.format_time(self.final_time or self.elapsed)}",
            self.f_head,NEON_CYAN,330)
        self.draw_text_center(
            f"Предметы: {len(self.inventory)}/{len(ITEMS)}   Осколки: ◈ {self.shards}",
            self.f_small,NEON_GOLD,365)
        self.draw_text_center(
            f"Компаньоны: {len(self.companions)}/{len(COMPANIONS)}",
            self.f_small,NEON_PINK,388)
        self.draw_text_center("Спасибо за игру.",self.f_sub,NEON_PURPLE,425)
        self.draw_hero_front(WIDTH//2,545,scale=1.3)
        self.draw_button("Играть снова",WIDTH//2,650,280,48,NEON_CYAN,0)

    # ═══════════════ ОБРАБОТКА ═══════════════
    def handle_click(self,pos):
        for rect,idx in self.buttons:
            if rect.collidepoint(pos):
                if self.state==self.ST_PUZZLE:
                    self.handle_puzzle_click(pos,idx)
                else:
                    self.on_button(idx)
                return

    def enter_location(self,key):
        self.current_loc=key; self.state=self.ST_LOCATION
        self.keys_held.clear(); self.visited.add(key)

    def switch_act(self):
        self.act+=1; self.buildings=ACT_BUILDINGS[self.act]
        self.player["x"]=WIDTH//2; self.player["y"]=HEIGHT-100
        self.player["facing"]="up"
        self.keys_held.clear(); self.state=self.ST_ACT_INTRO
        self.save_game()

    def on_button(self,idx):
        s=self.state
        if s==self.ST_MENU:
            if idx==0:
                self.state=self.ST_ACT_INTRO
                self.game_start_time=_time.time()
                self.unlock_companion("lira")
            elif idx==1: self.load_game()
        elif s==self.ST_ACT_INTRO:
            if idx==0: self.state=self.ST_MAP
        elif s==self.ST_MAP:
            if idx==2:
                if self.act<6: self.switch_act()
                else: self.final_time=self.elapsed; self.state=self.ST_END
            elif idx==3: self.state=self.ST_INV; self.keys_held.clear()
            elif idx==4: self.state=self.ST_SHOP; self.keys_held.clear()
            elif idx==5: self.state=self.ST_COMPANIONS; self.keys_held.clear()
        elif s==self.ST_COMPANIONS:
            if idx==0: self.state=self.ST_MAP
            elif 10<=idx<10+len(COMPANION_ORDER):
                k=idx-10
                cid=COMPANION_ORDER[k]
                if cid in self.companions:
                    self.active_companion=cid
                    c=COMPANIONS[cid]
                    self.companion_message=f"{c['name']}: «{c['lines']['hello']}»"
                    self.companion_msg_timer=180
                    self._play("companion")
        elif s==self.ST_SHOP: self.on_shop_button(idx)
        elif s==self.ST_INV: self.on_inventory_button(idx)
        elif s==self.ST_LOCATION:
            if idx==0:
                key=self.current_loc
                if key in self.sounds_found:
                    loc=ALL_LOCATIONS[key]
                    if loc.get("puzzle") and key not in self.puzzles_done:
                        self.start_puzzle(loc["puzzle"])
                    else: self.start_battle()
                else:
                    self.sounds_found.add(key); self.state=self.ST_COLLECT
                    self._play("collect")
            elif idx==1: self.state=self.ST_MAP
            elif idx==2:
                loc=ALL_LOCATIONS[self.current_loc]
                if loc.get("puzzle"): self.start_puzzle(loc["puzzle"])
        elif s==self.ST_COLLECT:
            if idx==0: self.state=self.ST_LOCATION
        elif s==self.ST_BATTLE:
            if idx==0:
                self.state=self.ST_LOSE; self._play("lose")
            elif 400<=idx<410:
                pot_list=[p for p in self.potions
                           if p in POTIONS and self.potions[p]>0]
                k=idx-400
                if k<len(pot_list): self.use_potion(pot_list[k])
        elif s==self.ST_WIN:
            if idx==0: self.state=self.ST_MAP
        elif s==self.ST_LOSE:
            if idx==0: self.start_battle()
            elif idx==1: self.state=self.ST_MAP
        elif s==self.ST_END:
            if idx==0:
                # Рестарт
                self.sounds_found=set(); self.done=set(); self.puzzles_done=set()
                self.inventory=set(); self.equipped={}
                self.act=1; self.buildings=ACT_BUILDINGS[1]
                self.player={"x":WIDTH//2,"y":HEIGHT-100,"anim":0,
                             "moving":False,"facing":"up"}
                self.state=self.ST_MENU; self.keys_held.clear()
                self.shards=0; self.potions={}
                self.weapons_owned={"wood_stick"}; self.weapon="wood_stick"
                self.base_atk=0; self.base_def=0
                self.base_max_hp=100; self.max_hp=self.base_max_hp
                self.player_hp=self.max_hp
                self.epic_elixir_received=False
                self.elapsed=0.0; self.final_time=0.0
                self.game_start_time=None
                self.companions=set(); self.active_companion=None

    def handle_keydown(self,event):
        # F5 / F9 — работают везде
        if event.key==pygame.K_F5: self.save_game(); return
        if event.key==pygame.K_F9: self.load_game(); return

        if self.state==self.ST_MAP:
            if event.key in UP_KEYS: self.keys_held.add("up")
            if event.key in DOWN_KEYS: self.keys_held.add("down")
            if event.key in LEFT_KEYS: self.keys_held.add("left")
            if event.key in RIGHT_KEYS: self.keys_held.add("right")
            if event.unicode:
                ch=event.unicode.lower()
                if ch=='ц': self.keys_held.add("up")
                if ch=='ы': self.keys_held.add("down")
                if ch=='ф': self.keys_held.add("left")
                if ch=='в': self.keys_held.add("right")
            if event.key==pygame.K_e and self.nearby_building:
                self._play("click"); self.enter_location(self.nearby_building)
            if event.key==pygame.K_i: self.state=self.ST_INV; self.keys_held.clear()
            if event.key==pygame.K_m: self.state=self.ST_SHOP; self.keys_held.clear()
            if event.key==pygame.K_c:
                self.state=self.ST_COMPANIONS; self.keys_held.clear()
        elif self.state==self.ST_BATTLE:
            if event.key==pygame.K_q:
                self.use_companion_assist(); return
            if event.key in (pygame.K_1,pygame.K_2,pygame.K_3):
                pl=[p for p in self.potions
                     if p in POTIONS and self.potions[p]>0]
                n=event.key-pygame.K_1
                if n<len(pl): self.use_potion(pl[n])
                return
            name=pygame.key.name(event.key).lower()
            if event.unicode:
                ch=event.unicode.lower()
                mp={"ф":"a","ы":"s","в":"d","а":"f"}
                name=mp.get(ch,ch)
            self.handle_battle_key(name)
        elif self.state==self.ST_PUZZLE:
            if self.puzzle_kind=="arrows": self.handle_arrow_key(event.key)

    def handle_keyup(self,event):
        if self.state==self.ST_MAP:
            if event.key in UP_KEYS: self.keys_held.discard("up")
            if event.key in DOWN_KEYS: self.keys_held.discard("down")
            if event.key in LEFT_KEYS: self.keys_held.discard("left")
            if event.key in RIGHT_KEYS: self.keys_held.discard("right")
            if event.unicode:
                ch=event.unicode.lower()
                if ch=='ц': self.keys_held.discard("up")
                if ch=='ы': self.keys_held.discard("down")
                if ch=='ф': self.keys_held.discard("left")
                if ch=='в': self.keys_held.discard("right")

    # ═══════════════ ГЛАВНЫЙ ЦИКЛ ═══════════════
    def run(self):
        while self.running:
            self.time_accum+=1
            self.update_timer()
            if self.msg_toast_timer>0:
                self.msg_toast_timer-=1

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.running=False
                elif event.type==pygame.MOUSEMOTION:
                    self.hover_index=-1
                    for rect,idx in self.buttons:
                        if rect.collidepoint(event.pos):
                            self.hover_index=idx; break
                elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                    if self.state!=self.ST_BATTLE: self._play("click")
                    self.handle_click(event.pos)
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        if self.state in (self.ST_MENU,self.ST_END):
                            self.running=False
                        elif self.state==self.ST_BATTLE:
                            self.state=self.ST_LOSE; self._play("lose")
                        elif self.state==self.ST_MAP:
                            self.state=self.ST_MENU; self.keys_held.clear()
                        elif self.state==self.ST_INV: self.state=self.ST_MAP
                        elif self.state==self.ST_SHOP: self.state=self.ST_MAP
                        elif self.state==self.ST_COMPANIONS: self.state=self.ST_MAP
                        elif self.state==self.ST_PUZZLE: self.state=self.ST_LOCATION
                        elif self.state==self.ST_ACT_INTRO: self.state=self.ST_MAP
                        else:
                            self.state=self.ST_MAP; self.keys_held.clear()
                    else:
                        self.handle_keydown(event)
                elif event.type==pygame.KEYUP:
                    self.handle_keyup(event)

            if self.state==self.ST_MAP: self.update_map()
            elif self.state==self.ST_BATTLE: self.update_battle()
            elif self.state==self.ST_PUZZLE: self.update_puzzle()

            self.screen.fill(BG_DARK)

            st=self.state
            if st==self.ST_MENU: self.draw_menu()
            elif st==self.ST_ACT_INTRO: self.draw_act_intro()
            elif st==self.ST_MAP: self.draw_map()
            elif st==self.ST_INV: self.draw_inventory()
            elif st==self.ST_SHOP: self.draw_shop()
            elif st==self.ST_COMPANIONS: self.draw_companions()
            elif st==self.ST_LOCATION: self.draw_location()
            elif st==self.ST_COLLECT: self.draw_collect()
            elif st==self.ST_PUZZLE: self.draw_puzzle()
            elif st==self.ST_BATTLE: self.draw_battle()
            elif st==self.ST_WIN: self.draw_win()
            elif st==self.ST_LOSE: self.draw_lose()
            elif st==self.ST_END: self.draw_end()

            # Тост поверх всего
            if self.msg_toast_timer>0:
                t=self.f_head.render(self.msg_toast,True,getattr(self,"msg_color",TEXT_WHITE))
                pad=20
                box=pygame.Rect(WIDTH//2-t.get_width()//2-pad,40,
                                t.get_width()+pad*2,t.get_height()+pad)
                bg=pygame.Surface((box.w,box.h),pygame.SRCALPHA)
                bg.fill((0,0,0,200))
                self.screen.blit(bg,(box.x,box.y))
                pygame.draw.rect(self.screen,getattr(self,"msg_color",TEXT_WHITE),
                                  box,width=2,border_radius=6)
                self.screen.blit(t,t.get_rect(center=box.center))

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__=="__main__":
    EchoLocationGame().run()
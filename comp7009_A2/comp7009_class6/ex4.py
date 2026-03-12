import hashlib
import itertools

TARGET = "3281e6de7fa3c6fd6d6c8098347aeb06bd35b0f74b96f173c7b2d28135e14d45"
SALT = "5UA@/Mw^%He]SBaU"

username = "laplusbelle"
name = "Marie"
surname = "Curie"
pet = "Woof"
employer = "UKC"
mother = "Jean Neoskour"
father = "Jvaist Fairecourir"
husband = "Eltrofor"

birthday_day = 2
birthday_month = "January"
birthday_year = 1980

husband_day = 29
husband_month = "December"
husband_year = 1981

MONTH_NUM = {
    "January": "01", "February": "02", "March": "03", "April": "04",
    "May": "05", "June": "06", "July": "07", "August": "08",
    "September": "09", "October": "10", "November": "11", "December": "12"
}

def sha256_hex(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def date_formats(day, month, year):
    d2 = str(day).zfill(2)
    m2 = MONTH_NUM[month]
    y4 = str(year)
    y2 = y4[-2:]
    m3 = month[:3]

    return {
        f"{d2}{m2}{y4}",
        f"{d2}{m2}{y2}",
        f"{y4}{m2}{d2}",
        f"{m2}{d2}{y4}",
        f"{d2}-{m2}-{y4}",
        f"{d2}/{m2}/{y4}",
        f"{d2}.{m2}.{y4}",
        f"{d2}{m3}{y4}",
        f"{d2}{month}{y4}",
    }

def basic_variants(text):
    text_no_space = text.replace(" ", "")
    return {
        text,
        text_no_space,
        text.lower(),
        text_no_space.lower(),
        text.upper(),
        text_no_space.upper(),
        text.capitalize(),
        text_no_space.capitalize(),
        text.title().replace(" ", ""),
    }

def build_tokens():
    raw_items = [
        username,
        name,
        surname,
        pet,
        employer,
        mother,
        father,
        husband,
        name + surname,
        surname + name,
        mother.replace(" ", ""),
        father.replace(" ", "")
    ]

    raw_items.extend(date_formats(birthday_day, birthday_month, birthday_year))
    raw_items.extend(date_formats(husband_day, husband_month, husband_year))

    tokens = set()
    for item in raw_items:
        tokens.update(basic_variants(item))

    return sorted(tokens)

def candidates():
    tokens = build_tokens()

    suffixes = [
        "", "1", "12", "123", "!", "!!", "123!",
        "1980", "1981"
    ]
    separators = ["", "_", "-", "."]

    # single token + suffix
    for t in tokens:
        for suf in suffixes:
            yield t + suf

    # two-token combinations + suffix
    for a, b in itertools.permutations(tokens, 2):
        for sep in separators:
            for suf in suffixes:
                yield a + sep + b + suf

    # token + date + suffix
    dates = list(date_formats(birthday_day, birthday_month, birthday_year))
    dates += list(date_formats(husband_day, husband_month, husband_year))

    for t in tokens:
        for d in dates:
            for sep in separators:
                for suf in suffixes:
                    yield t + sep + d + suf
                    yield d + sep + t + suf

def check_password(password):
    # try the most common salted SHA-256 patterns
    possibilities = [
        password + SALT,
        SALT + password,
        password + ":" + SALT,
        SALT + ":" + password
    ]

    for item in possibilities:
        if sha256_hex(item) == TARGET:
            return True
    return False

tested = 0
seen = set()

for password in candidates():
    if password in seen:
        continue
    seen.add(password)

    tested += 1
    if check_password(password):
        print("FOUND password:", password)
        print("Tested:", tested)
        break
else:
    print("Password not found.")
    print("Tested:", tested)
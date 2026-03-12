KEYWORDS = [
"stud.jur",
"student",
"studentermedhjælper",
"studenter",
"ha.jur",
"cand.merc.jur",
"legal student"
]


def is_relevant(title):

    title = title.lower()

    for keyword in KEYWORDS:

        if keyword in title:
            return True

    return False

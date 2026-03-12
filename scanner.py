import json
import os

from sources import scan_law_firms, google_discovery
from filters import is_relevant
from mailer import send_email

SEEN_FILE = "seen_jobs.json"


def load_seen():

    if os.path.exists(SEEN_FILE):

        with open(SEEN_FILE) as f:
            return set(json.load(f))

    return set()



def save_seen(seen):

    with open(SEEN_FILE,"w") as f:
        json.dump(list(seen),f)



def main():

    seen = load_seen()

    jobs = []

    jobs.extend(scan_law_firms())
    jobs.extend(google_discovery())

    new_jobs = []

    for title,link in jobs:

        if not is_relevant(title):
            continue

        key = title + link

        if key in seen:
            continue

        seen.add(key)

        new_jobs.append((title,link))


    if new_jobs:

        body = "\n\n".join(
            f"{t}\n{l}" for t,l in new_jobs
        )

        send_email(body)


    save_seen(seen)



if __name__ == "__main__":
    main()

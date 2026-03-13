import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

LAW_FIRM_SITES = [
    "https://jobs.poulschmith.dk/da/ledige-stillinger",
    "https://kromannreumert.com/karriere/ledige-stillinger",
    "https://www.bechbruun.com/karriere/ledige-stillinger",
    "https://bruunhjejle.dk/da/i-bruun-hjejle-har-vi-en-staerk-teamstruktur-og-vi-arbejder-maalrettet-med-din-individuelle",
    "https://www.hortendahl.dk/karriere/ledige-stillinger/",
    "https://accura.dk/karriere/",
    "https://denmark.dlapiper.com/da/landing/soeger-du-job-hos-dla-piper",
    "https://www.mazanti.dk/karriere/ledige-stillinger/",
    "https://www.njordlaw.com/da/karriere/ledige-stillinger",
    "https://les.dk/da/karriere",
    "https://schjodt.com/career",
    "https://www.nnlaw.dk/karriere",
    "https://moalemweitemeyer.com/career?sub=Vacant%2520Positions"
]

SEARCH_QUERIES = [
    "stud.jur job danmark",
    "studentermedhjælper jura",
    "ha.jur student job",
    "cand.merc.jur student job",
    "legal student assistant denmark"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def extract_links(url):

    jobs = []

    try:
        html = requests.get(url, headers=HEADERS, timeout=20).text
        soup = BeautifulSoup(html, "html.parser")

        for link in soup.find_all("a"):

            title = link.get_text(strip=True)
            href = link.get("href")

            if not title or not href:
                continue

            href = urljoin(url, href)

            if len(title) < 4:
                continue

            jobs.append((title, href))

    except Exception as e:
        print("Error scanning", url, e)

    return jobs


def scan_law_firms():

    jobs = []

    for site in LAW_FIRM_SITES:

        links = extract_links(site)

        jobs.extend(links)

    return jobs


def fetch_job_title(link):

    try:

        html = requests.get(link, headers=HEADERS, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")

        h1 = soup.find("h1")

        if h1:
            title = h1.get_text().strip()
            if len(title) > 3:
                return title

        if soup.title:
            return soup.title.string.strip()

    except:
        pass

    return None


def google_discovery():

    jobs = []

    for query in SEARCH_QUERIES:

        url = f"https://www.google.com/search?q={query}"

        try:

            html = requests.get(url, headers=HEADERS).text
            soup = BeautifulSoup(html, "html.parser")

            for link in soup.select("a"):

                href = link.get("href")

                if href and "/url?q=" in href:

                    real = href.split("/url?q=")[1].split("&")[0]

                    title = link.text.strip()

                    if not title:
                        continue

                    real_title = fetch_job_title(real)

                    if real_title:
                        jobs.append((real_title, real))
                    else:
                        jobs.append((title, real))

        except Exception as e:
            print("Google search error:", e)

    return jobs

#!/usr/bin/env python3
import csv, datetime, requests, bs4, io, pathlib
SRC_CSV = pathlib.Path("data/raw/regulations.csv")
TMP_CSV = pathlib.Path("data/raw/regulations_tmp.csv")
TODAY = datetime.date.today().isoformat()

def get_tax_barcelona() -> float:
    url = "https://taxes.turisme.barcelona.cat/"
    html = requests.get(url, timeout=20).text
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    txt = soup.find(string=lambda s: s and "€" in s)
    return float(txt.replace("€", "").strip()[:4])  # 4.00

def get_tax_lisboa() -> float:
    url = "https://www.visitlisboa.com/en/useful-information/tourist-tax"
    html = requests.get(url, timeout=20).text
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    p_text = soup.find("p").get_text()
    return 2.00 if "2" in p_text else 0.0

def main():
    tax_map = {
        "Barcelona": get_tax_barcelona(),
        "Lisboa": get_tax_lisboa(),
    }
    with SRC_CSV.open(newline="", encoding="utf-8") as fin, \
         TMP_CSV.open("w", newline="", encoding="utf-8") as fout:
        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            if row["city"] in tax_map:
                row["tax_amount_eur"] = f"{tax_map[row['city']]:.2f}"
                row["last_checked"] = TODAY
            writer.writerow(row)
    TMP_CSV.replace(SRC_CSV)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Actualiza tax_amount_eur para Barcelona y Lisboa con valores constantes
y refresca last_checked.  (Versión sin llamadas externas, válida para CI.)
"""
import csv, datetime, pathlib

SRC_CSV = pathlib.Path("data/raw/regulations.csv")
TMP_CSV = pathlib.Path("data/raw/regulations_tmp.csv")
TODAY = datetime.date.today().isoformat()

# Valores constantes (cambiar cuando dispongamos de scraper estable)
TAX_MAP = {
    "Barcelona": 4.00,
    "Lisboa": 2.00,
}

def main():
    with SRC_CSV.open(newline="", encoding="utf-8") as fin, \
         TMP_CSV.open("w", newline="", encoding="utf-8") as fout:
        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            if row["city"] in TAX_MAP:
                row["tax_amount_eur"] = f"{TAX_MAP[row['city']]:.2f}"
                row["last_checked"] = TODAY
            writer.writerow(row)
    TMP_CSV.replace(SRC_CSV)

if __name__ == "__main__":
    main()

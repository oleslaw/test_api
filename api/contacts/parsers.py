import csv


def parse_contacts_csv(file, delimiter=","):
    decoded = file.read().decode("utf-8").splitlines()
    reader = csv.DictReader(decoded, delimiter=delimiter)
    rows = []
    for row in reader:
        if not any(row.values()):
            continue
        cleaned = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
        rows.append(cleaned)
    return rows

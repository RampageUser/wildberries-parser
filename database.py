import csv


def create_csv() -> None:
    with open("wb.csv", "w", encoding='utf-8') as document:
        writer = csv.writer(document)
        writer.writerow(("name", "brand", "price", "rate", "link"))
    print('CSV-file has been created')


def save_to_csv(data:list[dict]) -> None:
    with open("wb.csv", "a", encoding='utf-8') as document:
        writer = csv.DictWriter(document, fieldnames=["name", "brand", "price", "rate", "link"])
        writer.writerows(data)

import PyPDF4

def merge_pdfs(input_files, output_file):
    merger = PyPDF4.PdfFileMerger()

    # Füge jede PDF-Datei der Merger-Instanz hinzu
    for file in input_files:
        with open(file, 'rb') as pdf_file:
            merger.append(pdf_file)

    # Speichere die zusammengeführte PDF-Datei
    with open(output_file, 'wb') as output:
        merger.write(output)

    print("Die PDF-Dateien wurden erfolgreich zusammengeführt!")

files = [
    "C:\\Users\\Nadine\\Documents\\Studium\\Studium\\1234567890\\ME_Wellen\\ME_Wellennachweis\\PDFs\\Gesamt.pdf",
    "C:\\Users\\Nadine\\Documents\\Studium\\Studium\\1234567890\\ME_Wellen\\ME_Wellennachweis\\WellennachweisAntriebswelle.pdf",
    "C:\\Users\\Nadine\\Documents\\Studium\\Studium\\1234567890\\ME_Wellen\\ME_Wellennachweis\\WellennachweisZwischenwelle.pdf",
    "C:\\Users\\Nadine\\Documents\\Studium\\Studium\\1234567890\\ME_Wellen\\ME_Wellennachweis\\WellennachweisAbtriebswelle.pdf"
]

merge_pdfs(files, "3_4_Berechnungen.pdf")
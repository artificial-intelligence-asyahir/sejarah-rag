import pymupdf

def adding_metadata(filename: str):
    document = pymupdf.open("../../textbooks/SEJARAH_F5.pdf")
    document.set_metadata({
        "title": "Sejarah Tingkatan 5",
        "author": "Kementerian Pendidikan Malaysia",
        "subject": "Sejarah"
    })
    document.save("../../textbooks/sejarah_tingkatan_5.pdf")
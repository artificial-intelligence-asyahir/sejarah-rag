import pymupdf
from pathlib import Path

path_chapters = Path("../../chapters/")

def adding_metadata():
    document = pymupdf.open("../../chapters/sejarah_tingkatan_1_bab_1_mengenali_sejarah.pdf")
    document.set_metadata({
        "title": "Sejarah Tingkatan 5",
        "author": "Kementerian Pendidikan Malaysia",
        "subject": "Sejarah"
    })
    document.save("../../textbooks/sejarah_tingkatan_5.pdf")


def adding_subject_metadata():
    for file in path_chapters.iterdir():
        print(file)

        prefix = " ".join(file.stem.split("_")[3:])
        prefix = prefix.title()
        print(prefix)

        file_name = str(file)
        document = pymupdf.open(file_name)
        document.set_metadata({
            "subject": prefix
        })
        document.save(file_name, incremental=True, encryption=0)

if __name__ == "__main__":
    adding_subject_metadata()
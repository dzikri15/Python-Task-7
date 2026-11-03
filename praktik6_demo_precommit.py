"""Praktik 6 - Demonstrasi pre-commit hooks (black, flake8, isort).

File .pre-commit-config.yaml di repositori ini menjalankan tiga hook
sebelum setiap commit:
  - black   : auto-format kode
  - flake8  : linting PEP 8 + kompleksitas
  - isort   : sorting import (profil black)

Demo ini menulis sebuah file contoh yang sengaja melanggar standar,
lalu memeriksa apakah ketiga tool tersedia di mesin ini. Jika tersedia,
tool dijalankan dengan mode --check sehingga terlihat penolakannya.
Jika tidak tersedia, demo menjelaskan apa yang akan ditolak hook
pada mesin yang sudah terinstall pre-commit.

Jalankan dari direktori repositori ini:
    python3 praktik6_demo_precommit.py
"""

import shutil
import subprocess

CONTOH_KOTOR = '''import sys
import os
def hitung(a,b): return a+b
x = hitung( 2,3 )
print( "hasil:",x )
'''

CONTOH_BERSIH = '''import os
import sys


def hitung(a, b):
    return a + b


x = hitung(2, 3)
print("hasil:", x)
'''


def cek_tool(nama, perintah):
    """Jalankan satu tool dalam mode check, laporkan hasilnya."""
    path = shutil.which(nama)
    if path is None:
        print(f"  [{nama}] tidak terinstall di mesin ini.")
        print(f"        -> pada mesin dengan pre-commit, hook {nama} "
              f"akan MENOLAK commit berisi contoh di atas.")
        return
    hasil = subprocess.run(perintah, capture_output=True, text=True)
    print(f"  [{nama}] terinstall di {path}")
    print(f"        -> exit code {hasil.returncode} "
          f"({'DITOLAK' if hasil.returncode else 'lolos'} oleh hook)")
    keluaran = (hasil.stdout + hasil.stderr).strip()
    if keluaran:
        for baris in keluaran.splitlines()[:5]:
            print(f"           {baris}")


def main():
    with open("contoh_kotor.py", "w", encoding="utf-8") as f:
        f.write(CONTOH_KOTOR)

    print("File contoh_kotor.py (sengaja melanggar standar):")
    print("---")
    print(CONTOH_KOTOR, end="")
    print("---")
    print("Pelanggaran yang dikandungnya:")
    print("  - import tidak terurut (sys sebelum os) -> ditolak isort")
    print("  - spasi tidak konsisten, def satu baris -> ditolak black")
    print("  - (flake8 juga akan menandai pelanggaran gaya yang sama)")
    print("\nHasil pengecekan tool (mode --check, tanpa mengubah file):")
    cek_tool("black", ["black", "--check", "--diff", "contoh_kotor.py"])
    cek_tool("flake8", ["flake8", "--max-line-length=79", "contoh_kotor.py"])
    cek_tool("isort", ["isort", "--check-only", "--diff", "--profile=black",
                       "contoh_kotor.py"])

    print("\nVersi bersih setelah black + isort (yang lolos hook):")
    print("---")
    print(CONTOH_BERSIH, end="")
    print("---")
    print("Cara kerja gerbangnya: hook berjalan SEBELUM commit dibuat.")
    print("Kalau satu hook gagal, commit dibatalkan sampai kode diperbaiki,")
    print("sehingga kode yang tidak memenuhi standar tidak pernah masuk")
    print("ke repositori — reviewer pun fokus ke logika, bukan ke gaya.")
    print("\nFile konfigurasi yang dipakai: .pre-commit-config.yaml")


if __name__ == "__main__":
    main()

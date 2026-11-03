"""Praktik 5 - Identifikasi code smell dan refactoring.

Kode SEBELUM mengandung 5 code smell:
  1. Magic Number      : status == 3 tanpa penjelasan
  2. Duplicate Code    : validasi NIM ditulis di dua fungsi
  3. Long Method       : satu fungsi mengurus validasi + hitung + predikat
                         + beasiswa
  4. Deep Nesting      : if bertingkat 4 level untuk predikat
  5. Dead Code         : fungsi_tidak_terpakai() tidak pernah dipanggil

Kode SESUDAH menghilangkan kelimanya (konstanta, validasi terpusat, extract
method, guard clause, dead code dihapus) plus docstring dan type hints
sesuai PEP 8. Hasil sebelum dan sesudah dijamin sama.

Jalankan dari direktori repositori ini:
    python3 praktik5_refactoring.py
"""

# ---------------------------------------------------------------------------
# SEBELUM (mengandung 5 code smell)
# ---------------------------------------------------------------------------

def proses_nilai_mahasiswa_lama(data):
    """Versi lama: long method + deep nesting + magic number."""
    hasil = []
    for m in data:
        if m["nim"].isdigit() and len(m["nim"]) == 10:
            if m["nilai"]:
                total = 0
                for n in m["nilai"]:
                    total += n
                rata = total / len(m["nilai"])
                if rata >= 85:
                    predikat = "A"
                else:
                    if rata >= 70:
                        predikat = "B"
                    else:
                        if rata >= 55:
                            predikat = "C"
                        else:
                            predikat = "E"
                beasiswa = False
                if m["status"] == 3:  # magic number: apa itu 3?
                    if rata >= 85:
                        beasiswa = True
                hasil.append({"nim": m["nim"], "nama": m["nama"],
                              "rata": round(rata, 2), "predikat": predikat,
                              "beasiswa": beasiswa})
    return hasil


def cari_mahasiswa_lama(data, nim):
    """Validasi NIM ditulis ulang di sini (duplikasi)."""
    if nim.isdigit() and len(nim) == 10:
        for m in data:
            if m["nim"] == nim:
                return m
    return None


def fungsi_tidak_terpakai():
    """Dead code: tidak pernah dipanggil di mana pun."""
    return "tidak pernah dipakai"


# ---------------------------------------------------------------------------
# SESUDAH (refactoring)
# ---------------------------------------------------------------------------

STATUS_LULUS = 3
BATAS_BEASISWA = 85


def validasi_nim(nim: str) -> bool:
    """Validasi format NIM: string 10 digit angka."""
    return nim.isdigit() and len(nim) == 10


def hitung_rata_rata(nilai: list) -> float:
    """Hitung rata-rata list nilai; list kosong menghasilkan 0.0."""
    if not nilai:
        return 0.0
    return sum(nilai) / len(nilai)


def tentukan_predikat(rata: float) -> str:
    """Tentukan predikat dari rata-rata (flat if/elif, tanpa nesting)."""
    if rata >= 85:
        return "A"
    if rata >= 70:
        return "B"
    if rata >= 55:
        return "C"
    return "E"


def cek_beasiswa(status: int, rata: float) -> bool:
    """Beasiswa jika status lulus dan rata-rata mencapai batas."""
    return status == STATUS_LULUS and rata >= BATAS_BEASISWA


def proses_nilai_mahasiswa(data: list) -> list:
    """Proses nilai mahasiswa dengan guard clause.

    Baris yang NIM-nya tidak valid atau nilainya kosong dilewati.
    """
    hasil = []
    for m in data:
        if not validasi_nim(m["nim"]):
            continue
        if not m["nilai"]:
            continue
        rata = hitung_rata_rata(m["nilai"])
        hasil.append({
            "nim": m["nim"],
            "nama": m["nama"],
            "rata": round(rata, 2),
            "predikat": tentukan_predikat(rata),
            "beasiswa": cek_beasiswa(m["status"], rata),
        })
    return hasil


def main():
    # NIM demo 10 digit (sesuai aturan validasi modul); nama disingkat.
    data = [
        {"nim": "2024132000", "nama": "Dzikri", "nilai": [90, 85, 88],
         "status": 3},
        {"nim": "2024132030", "nama": "Alamsyah", "nilai": [75, 70, 72],
         "status": 3},
        {"nim": "2024132038", "nama": "Fakhry", "nilai": [60, 58, 62],
         "status": 1},
    ]

    print("Code smell yang diidentifikasi pada kode lama:")
    print("  1. Magic Number   : status == 3 tanpa penjelasan")
    print("  2. Duplicate Code : validasi NIM di dua fungsi")
    print("  3. Long Method    : satu fungsi mengurus 4 tanggung jawab")
    print("  4. Deep Nesting   : if predikat bertingkat 4 level")
    print("  5. Dead Code      : fungsi_tidak_terpakai() tidak dipanggil")
    print("\nRefactoring yang diterapkan:")
    print("  - Replace with Constant (STATUS_LULUS, BATAS_BEASISWA)")
    print("  - Extract Method (validasi_nim, hitung_rata_rata,")
    print("    tentukan_predikat, cek_beasiswa)")
    print("  - Guard Clause (continue untuk data tidak valid)")
    print("  - Remove Dead Code + docstring dan type hints (PEP 8)")

    lama = proses_nilai_mahasiswa_lama(data)
    baru = proses_nilai_mahasiswa(data)
    print("\nHasil kode lama:")
    for baris in lama:
        print(f"  {baris}")
    print("Hasil kode baru (refactoring):")
    for baris in baru:
        print(f"  {baris}")
    print(f"\nHasil sebelum dan sesudah sama: {lama == baru}")


if __name__ == "__main__":
    main()

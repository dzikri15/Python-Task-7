"""Praktik 2 - Hierarki custom exception untuk Sistem Informasi Perpustakaan.

Hierarki:
    PerpustakaanError (base)
    ├── BukuNotFoundError
    ├── BukuTidakTersediaError
    └── AnggotaNotFoundError

Fungsi pinjam_buku() memakai exception tersebut, dan program utama
mendemonstrasikan penanganan setiap jenis exception secara spesifik.

Jalankan dari direktori repositori ini:
    python3 praktik2_perpustakaan.py
"""


class PerpustakaanError(Exception):
    """Base exception untuk seluruh error SI Perpustakaan."""


class BukuNotFoundError(PerpustakaanError):
    """Buku dengan kode tersebut tidak ada di katalog."""

    def __init__(self, kode_buku):
        self.kode_buku = kode_buku
        super().__init__(f"Buku '{kode_buku}' tidak ditemukan di katalog")


class BukuTidakTersediaError(PerpustakaanError):
    """Buku ada, tetapi stoknya habis (semua sedang dipinjam)."""

    def __init__(self, kode_buku, judul):
        self.kode_buku = kode_buku
        self.judul = judul
        super().__init__(f"Buku '{judul}' ({kode_buku}) sedang tidak tersedia")


class AnggotaNotFoundError(PerpustakaanError):
    """ID anggota tidak terdaftar."""

    def __init__(self, id_anggota):
        self.id_anggota = id_anggota
        super().__init__(f"Anggota '{id_anggota}' tidak terdaftar")


# Data katalog dan anggota (in-memory)
BUKU = {
    "B001": {"judul": "Algoritma dan Pemrograman", "stok": 2},
    "B002": {"judul": "Basis Data", "stok": 0},
}

ANGGOTA = {
    "A001": "Muhammad Dzikri Sagara",
    "A002": "Jilan Jalilah",
}

PEMINJAMAN = []


def pinjam_buku(kode_buku, id_anggota):
    """Pinjam satu buku. Raise exception spesifik jika ada kondisi gagal."""
    if id_anggota not in ANGGOTA:
        raise AnggotaNotFoundError(id_anggota)
    if kode_buku not in BUKU:
        raise BukuNotFoundError(kode_buku)
    if BUKU[kode_buku]["stok"] <= 0:
        raise BukuTidakTersediaError(kode_buku, BUKU[kode_buku]["judul"])
    BUKU[kode_buku]["stok"] -= 1
    PEMINJAMAN.append({"kode_buku": kode_buku, "id_anggota": id_anggota})
    return (f"'{BUKU[kode_buku]['judul']}' berhasil dipinjam "
            f"oleh {ANGGOTA[id_anggota]}")


def main():
    print("=== Kasus 1: peminjaman berhasil ===")
    try:
        print(pinjam_buku("B001", "A001"))
    except PerpustakaanError as e:
        print(f"Gagal: {e}")

    print("\n=== Kasus 2: buku tidak ditemukan ===")
    try:
        print(pinjam_buku("B999", "A001"))
    except BukuNotFoundError as e:
        print(f"Gagal: {e}")

    print("\n=== Kasus 3: buku tidak tersedia (stok 0) ===")
    try:
        print(pinjam_buku("B002", "A001"))
    except BukuTidakTersediaError as e:
        print(f"Gagal: {e}")

    print("\n=== Kasus 4: anggota tidak terdaftar ===")
    try:
        print(pinjam_buku("B001", "A999"))
    except AnggotaNotFoundError as e:
        print(f"Gagal: {e}")

    print("\n=== Kasus 5: ditangkap di level base class ===")
    try:
        print(pinjam_buku("B999", "A999"))
    except PerpustakaanError as e:
        print(f"Gagal (ditangkap sebagai PerpustakaanError): {e}")

    print("\nStok akhir:")
    for kode, info in BUKU.items():
        print(f"  {kode} - {info['judul']}: {info['stok']}")
    print(f"Total peminjaman tercatat: {len(PEMINJAMAN)}")


if __name__ == "__main__":
    main()

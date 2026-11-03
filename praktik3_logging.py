"""Praktik 3 - Konfigurasi logging untuk aplikasi Sistem Informasi.

(a) File handler: RotatingFileHandler, merekam level DEBUG ke atas, dengan
    rotasi (maxBytes kecil supaya rotasi terlihat pada demo ini).
(b) Console handler: hanya level WARNING ke atas.
(c) Formatter menyertakan timestamp, level, nama logger, dan pesan.

Jalankan dari direktori repositori ini:
    python3 praktik3_logging.py

File log yang dihasilkan: si_akademik.log (+ hasil rotasi si_akademik.log.1
dst. jika ukuran melewati batas). File log lama dihapus di awal program
supaya hasil demo deterministik.
"""

import glob
import logging
import os
from logging.handlers import RotatingFileHandler

LOG_BASENAME = "si_akademik.log"


def setup_logger():
    """Bangun logger si_akademik dengan dua handler berbeda."""
    logger = logging.getLogger("si_akademik")
    logger.setLevel(logging.DEBUG)
    # Jangan teruskan ke root handler: tanpa ini, pesan WARNING ke atas
    # akan tercetak dua kali di konsol (handler sendiri + lastResort).
    logger.propagate = False

    # (a) File handler dengan rotasi: DEBUG ke atas.
    file_handler = RotatingFileHandler(
        LOG_BASENAME, maxBytes=1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_fmt)

    # (b) Console handler: WARNING ke atas saja.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_fmt = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_fmt)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def main():
    # Bersihkan log demo sebelumnya supaya hasil bisa diverifikasi.
    for path in glob.glob(LOG_BASENAME + "*"):
        os.remove(path)

    logger = setup_logger()

    # (c) Beberapa pesan pada berbagai level.
    logger.debug("Query SQL: SELECT * FROM mahasiswa WHERE nim='20241320004'")
    logger.info("User admin berhasil login dari 192.168.1.10")
    for i in range(1, 21):
        logger.debug("Detil proses pendaftaran mahasiswa ke-%d", i)
    logger.warning("Penggunaan memori mencapai 85%")
    logger.error("Gagal mengirim notifikasi email ke dosen@univ.ac.id")
    logger.critical("Koneksi database utama terputus!")

    # Tutup handler supaya buffer file ter-flush sebelum dibaca.
    for handler in logger.handlers:
        handler.close()

    # Verifikasi output pada kedua handler.
    print("\n--- Verifikasi ---")
    print("Konsol di atas hanya menampilkan WARNING, ERROR, dan CRITICAL")
    print("(pesan DEBUG dan INFO tidak muncul di konsol).")
    berkas = sorted(glob.glob(LOG_BASENAME + "*"))
    print(f"File log yang terbentuk: {', '.join(berkas)}")
    with open(LOG_BASENAME, encoding="utf-8") as f:
        baris = f.read().splitlines()
    print(f"Isi {LOG_BASENAME} ({len(baris)} baris terakhir dari rotasi):")
    for baris_log in baris:
        print(f"  {baris_log}")


if __name__ == "__main__":
    main()

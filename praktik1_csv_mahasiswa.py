"""Praktik 1 - Membaca data mahasiswa dari file CSV dengan penanganan exception
lengkap: FileNotFoundError, csv.Error, dan ValueError. Blok finally memastikan
file selalu ditutup, blok else menampilkan ringkasan hanya jika pembacaan
berhasil tanpa exception.

Jalankan dari direktori repositori ini:
    python3 praktik1_csv_mahasiswa.py
"""

import csv


def baca_mahasiswa(path):
    """Baca file CSV mahasiswa, kembalikan list dict atau None jika gagal.

    Format CSV: nim,nama,ipk (satu baris header + baris data).
    """
    f = None
    try:
        f = open(path, newline='', encoding='utf-8')
        pembaca = csv.reader(f, strict=True)
        next(pembaca)  # lewati header
        data = []
        for baris in pembaca:
            nim, nama, ipk = baris[0], baris[1], float(baris[2])
            data.append({'nim': nim, 'nama': nama, 'ipk': ipk})
    except FileNotFoundError:
        print(f"File tidak ditemukan: {path}")
        return None
    except csv.Error as e:
        print(f"File CSV rusak: {e}")
        return None
    except ValueError as e:
        print(f"Data tidak valid: {e}")
        return None
    else:
        total = sum(m['ipk'] for m in data)
        print(f"Ringkasan: {len(data)} mahasiswa, "
              f"rata-rata IPK {total / len(data):.2f}")
        return data
    finally:
        if f is not None:
            f.close()
            print(f"File {path} ditutup (finally).")


def main():
    print("=== Kasus 1: file valid ===")
    data = baca_mahasiswa("mahasiswa.csv")
    if data:
        for m in data:
            print(f"  {m['nim']} - {m['nama']} - IPK {m['ipk']}")

    print("\n=== Kasus 2: file tidak ada ===")
    baca_mahasiswa("tidak_ada.csv")

    print("\n=== Kasus 3: IPK tidak valid ===")
    baca_mahasiswa("mahasiswa_ipk_salah.csv")

    print("\n=== Kasus 4: CSV rusak (tanda kutip tidak ditutup) ===")
    baca_mahasiswa("mahasiswa_rusak.csv")


if __name__ == "__main__":
    main()

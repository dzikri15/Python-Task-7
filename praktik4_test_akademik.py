"""Praktik 4 - Unit test lengkap dengan unittest.

Fungsi yang diuji:
(a) hitung_ipk() - IPK dari list nilai {bobot, sks}
(b) validasi_nim() - format NIM 10 digit angka
(c) konversi_nilai_huruf() - angka 0-100 ke huruf

Skala konversi yang dipakai (didokumentasikan agar test tidak ambigu):
    >= 85: A | >= 80: B+ | >= 75: B | >= 70: C+ | >= 65: C | >= 55: D | < 55: E

Mencakup happy path, edge case, dan input tidak valid (17 test).

Jalankan dari direktori repositori ini:
    python3 praktik4_test_akademik.py
    python3 -m unittest praktik4_test_akademik -v
"""

import unittest


def hitung_ipk(nilai_list):
    """Hitung IPK dari list dict {'bobot': float, 'sks': int}.

    List kosong atau total SKS nol menghasilkan 0.0.
    """
    if not nilai_list:
        return 0.0
    total_bobot = sum(n['bobot'] * n['sks'] for n in nilai_list)
    total_sks = sum(n['sks'] for n in nilai_list)
    if total_sks == 0:
        return 0.0
    return total_bobot / total_sks


def validasi_nim(nim):
    """Validasi format NIM: string 10 digit angka."""
    return isinstance(nim, str) and len(nim) == 10 and nim.isdigit()


def konversi_nilai_huruf(angka):
    """Konversi angka 0-100 ke huruf (A, B+, B, C+, C, D, E).

    Raise TypeError untuk bukan angka, ValueError untuk di luar 0-100.
    """
    if not isinstance(angka, (int, float)):
        raise TypeError("Nilai harus berupa angka")
    if angka < 0 or angka > 100:
        raise ValueError("Nilai harus berada di rentang 0-100")
    if angka >= 85:
        return "A"
    if angka >= 80:
        return "B+"
    if angka >= 75:
        return "B"
    if angka >= 70:
        return "C+"
    if angka >= 65:
        return "C"
    if angka >= 55:
        return "D"
    return "E"


class TestHitungIPK(unittest.TestCase):
    def test_normal(self):
        nilai = [
            {'bobot': 4.0, 'sks': 3},
            {'bobot': 3.0, 'sks': 2},
            {'bobot': 3.7, 'sks': 3},
        ]
        # (12 + 6 + 11.1) / 8 = 29.1 / 8 = 3.6375
        self.assertAlmostEqual(hitung_ipk(nilai), 3.6375)

    def test_kosong(self):
        self.assertEqual(hitung_ipk([]), 0.0)

    def test_sks_nol(self):
        nilai = [{'bobot': 4.0, 'sks': 0}]
        self.assertEqual(hitung_ipk(nilai), 0.0)


class TestValidasiNIM(unittest.TestCase):
    def test_benar(self):
        self.assertTrue(validasi_nim("2024132000"))

    def test_mengandung_huruf(self):
        self.assertFalse(validasi_nim("20241AB004"))

    def test_panjang_salah(self):
        self.assertFalse(validasi_nim("202413200"))

    def test_kosong(self):
        self.assertFalse(validasi_nim(""))


class TestKonversiNilaiHuruf(unittest.TestCase):
    def test_batas_a(self):
        self.assertEqual(konversi_nilai_huruf(95), "A")
        self.assertEqual(konversi_nilai_huruf(85), "A")

    def test_batas_b_plus(self):
        self.assertEqual(konversi_nilai_huruf(84), "B+")
        self.assertEqual(konversi_nilai_huruf(80), "B+")

    def test_batas_b(self):
        self.assertEqual(konversi_nilai_huruf(79), "B")
        self.assertEqual(konversi_nilai_huruf(75), "B")

    def test_batas_c_plus(self):
        self.assertEqual(konversi_nilai_huruf(74), "C+")
        self.assertEqual(konversi_nilai_huruf(70), "C+")

    def test_batas_c(self):
        self.assertEqual(konversi_nilai_huruf(69), "C")
        self.assertEqual(konversi_nilai_huruf(65), "C")

    def test_batas_d(self):
        self.assertEqual(konversi_nilai_huruf(64), "D")
        self.assertEqual(konversi_nilai_huruf(55), "D")

    def test_batas_e(self):
        self.assertEqual(konversi_nilai_huruf(54), "E")
        self.assertEqual(konversi_nilai_huruf(0), "E")

    def test_lebih_dari_100(self):
        with self.assertRaises(ValueError):
            konversi_nilai_huruf(105)

    def test_negatif(self):
        with self.assertRaises(ValueError):
            konversi_nilai_huruf(-5)

    def test_bukan_angka(self):
        with self.assertRaises(TypeError):
            konversi_nilai_huruf("delapan puluh")


if __name__ == "__main__":
    unittest.main(verbosity=2)

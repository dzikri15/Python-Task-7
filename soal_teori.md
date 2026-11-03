# Soal Teori — Pertemuan 7

## 1. Perbedaan syntax error dan exception

**Syntax error** terjadi saat parser Python membaca kode, sebelum program dijalankan
sama sekali. Penyebabnya adalah kode yang melanggar aturan tata bahasa Python.
Program tidak bisa berjalan sampai kesalahan ini diperbaiki.

```python
print("Hello"          # SyntaxError: kurung tidak ditutup
if True
    print("x")         # SyntaxError: titik dua dan indentasi salah
```

**Exception** terjadi saat program sedang berjalan (runtime), padahal sintaksnya
sudah benar. Penyebabnya adalah kondisi tak terduga saat eksekusi, misalnya data
yang tidak sesuai.

```python
hasil = 10 / 0         # ZeroDivisionError
data = [1, 2, 3]
print(data[10])        # IndexError
```

Jadi: syntax error = kode salah tulis, ketahuan sebelum jalan; exception = kode
benar tulis tapi gagal saat jalan, dan bisa ditangani dengan `try-except`.

## 2. Perbedaan blok else dan finally

| Blok | Kapan dijalankan | Kegunaan |
|---|---|---|
| `else` | Hanya jika blok `try` selesai **tanpa** exception | Kode yang hanya boleh jalan kalau operasi berhasil |
| `finally` | **Selalu**, ada exception maupun tidak | Pembersihan sumber daya (tutup file, tutup koneksi) |

```python
try:
    f = open("data.csv")
    isi = f.read()
except FileNotFoundError:
    print("File tidak ada")
else:
    print("Baca berhasil, isi:", len(isi), "karakter")  # hanya kalau tidak error
finally:
    f.close()  # selalu ditutup, berhasil maupun gagal
```

## 3. Mengapa urutan blok except penting?

Python memeriksa blok `except` dari atas ke bawah dan memakai blok pertama yang
cocok. Karena exception membentuk hierarki (subclass–superclass), exception yang
lebih umum akan menangkap semua subclass-nya. Kalau `except Exception` ditulis
paling atas, semua error masuk ke sana dan blok `except` yang lebih spesifik di
bawahnya tidak pernah tercapai (menjadi kode mati).

```python
try:
    nilai = int("abc")
except Exception:        # SALAH urutan: menangkap semuanya, termasuk ValueError
    print("Error umum")
except ValueError:       # tidak pernah tercapai
    print("Input bukan angka")
```

Aturan: tulis dari yang paling spesifik ke yang paling umum
(`ValueError` → `LookupError` → `Exception`).

## 4. Keuntungan hierarki custom exception

Dibanding memakai exception bawaan secara langsung, hierarki custom exception:

1. **Bermakna secara domain** — `NIMFormatError` langsung menjelaskan masalah
   bisnisnya, bukan sekadar `ValueError` yang generik.
2. **Penanganan berlapis** — penangan di level superclass menangkap semua
   subclass-nya, sedangkan penangan subclass menangani kasus spesifik.
3. **Stabil terhadap perubahan teknis** — hierarki bisnis tidak berubah walau
   implementasi teknis (database, library) berganti.

Contoh konteks Sistem Informasi Akademik:

```python
class SIAkademikError(Exception):
    """Base exception seluruh error SI Akademik."""

class MahasiswaError(SIAkademikError):
    """Error terkait data mahasiswa."""

class NIMFormatError(MahasiswaError):
    def __init__(self, nim):
        super().__init__(f"NIM '{nim}' tidak sesuai format")

class NIMDuplikatError(MahasiswaError):
    def __init__(self, nim):
        super().__init__(f"NIM '{nim}' sudah terdaftar")

class MatakuliahError(SIAkademikError):
    """Error terkait mata kuliah."""
```

Dengan hierarki ini, `except MahasiswaError` menangkap `NIMFormatError` dan
`NIMDuplikatError` sekaligus, sementara `except SIAkademikError` menangkap
semuanya — lapisan presentasi cukup menangani level umum, lapisan bisnis
menangani level spesifik.

## 5. Debugging dengan print statement vs pdb

| Aspek | print statement | pdb |
|---|---|---|
| Cara kerja | Menambah `print` di titik kritis, jalankan ulang | Breakpoint interaktif, program dijeda |
| Inspeksi | Hanya nilai yang sempat di-print | Variabel apa pun bisa dicek (`p`), step (`n`/`s`), stack (`w`) |
| Biaya ubah | Edit kode + jalankan ulang tiap hipotesis | Tanpa edit kode, eksplorasi langsung |
| Produksi | Harus dibersihkan manual, rawan tertinggal | Jangan pernah tertinggal (`breakpoint()` memblokir aplikasi) |

**Kapan masing-masing tepat:** print cocok untuk bug sederhana yang lokasinya
sudah jelas (cek nilai satu-dua variabel). pdb tepat untuk bug yang alurnya
panjang atau kondisinya sulit direproduksi — misalnya nilai variabel berubah di
tengah loop — karena bisa dijeda dan ditelusuri baris per baris tanpa menebak.

## 6. Lima level logging standar

| Level | Nilai | Kapan digunakan | Contoh pesan (konteks SI) |
|---|---|---|---|
| DEBUG | 10 | Informasi diagnostik detail | `Query SQL: SELECT * FROM mahasiswa WHERE nim='20241320004'` |
| INFO | 20 | Konfirmasi operasi normal | `User admin berhasil login dari 192.168.1.10` |
| WARNING | 30 | Kondisi berpotensi masalah | `Penggunaan memori mencapai 85%` |
| ERROR | 40 | Error yang masih bisa ditangani | `Gagal mengirim notifikasi email ke dosen@univ.ac.id` |
| CRITICAL | 50 | Error fatal sistem | `Koneksi database utama terputus!` |

Logger hanya merekam pesan dengan level sama atau lebih tinggi dari threshold
yang disetel. Karena itu threshold berbeda per lingkungan: DEBUG di development,
INFO (atau WARNING) di produksi, supaya log tidak dibanjiri detail yang tidak
diperlukan.

## 7. Perbedaan setUp dan setUpClass

| Metode | Dijalankan | Kegunaan |
|---|---|---|
| `setUp` | Sebelum **setiap** test method | Menyiapkan kondisi awal yang segar per test (data test, objek) |
| `setUpClass` | **Sekali** sebelum seluruh test method di kelas (`@classmethod`) | Setup mahal yang cukup sekali (koneksi database, file besar) |

`setUp` dipakai kalau tiap test butuh kondisi awal yang bersih dan saling
terisolasi — misalnya tabel dihapus lalu diisi satu baris sebelum tiap test.
`setUpClass` dipakai kalau setup-nya mahal dan aman dipakai bersama, misalnya
membuka satu koneksi database untuk seluruh kelas, lalu ditutup di
`tearDownClass`. Pasangannya: `tearDown` (bersih-bersih per test) dan
`tearDownClass` (bersih-bersih sekali per kelas).

## 8. Prinsip DRY

**DRY (Don't Repeat Yourself):** setiap pengetahuan dalam sistem harus punya
satu representasi tunggal. Kalau logika yang sama ditulis di dua tempat,
perubahan di satu tempat mudah tidak disinkronkan ke tempat lain — itulah
sumber bug duplikasi.

Pelanggaran DRY — validasi NIM ditulis dua kali:

```python
def proses_pendaftaran(data):
    if not data['nim'].isdigit() or len(data['nim']) != 10:
        raise ValueError("NIM tidak valid")
    # ... proses pendaftaran

def update_mahasiswa(data):
    if not data['nim'].isdigit() or len(data['nim']) != 10:
        raise ValueError("NIM tidak valid")  # DUPLIKASI
    # ... proses update
```

Refactoring — validasi dipusatkan ke satu fungsi:

```python
def validasi_nim(nim):
    if not nim.isdigit() or len(nim) != 10:
        raise ValueError(f"NIM '{nim}' tidak valid")

def proses_pendaftaran(data):
    validasi_nim(data['nim'])
    # ... proses pendaftaran

def update_mahasiswa(data):
    validasi_nim(data['nim'])
    # ... proses update
```

Kalau aturan berubah (misalnya NIM jadi 11 digit), cukup ubah satu tempat.

## 9. Empat code smell dan refactoring-nya

| Code Smell | Gejala | Refactoring |
|---|---|---|
| Magic Number | Angka tanpa penjelasan, mis. `if status == 3` | Replace with Constant: `STATUS_LULUS = 3` |
| Duplicate Code | Kode serupa di beberapa tempat | Extract Method / Extract Class |
| Long Method | Fungsi > 20–30 baris, banyak tanggung jawab | Extract Method: pecah per tanggung jawab |
| Deep Nesting | `if` bertingkat > 3 level | Guard Clause: kembalikan lebih awal untuk kasus gagal |
| Dead Code | Fungsi/kode yang tidak pernah dijalankan | Remove Dead Code: hapus |
| God Class | Satu kelas terlalu banyak tanggung jawab | Extract Class: pecah per tanggung jawab |

Contoh guard clause menggantikan deep nesting:

```python
# Sebelum (deep nesting)
def proses(data):
    if data:
        if data.get('status') == 'pending':
            if data.get('approved_by'):
                return eksekusi(data)

# Sesudah (guard clause)
def proses(data):
    if not data:
        return None
    if data.get('status') != 'pending':
        return None
    if not data.get('approved_by'):
        return None
    return eksekusi(data)
```

## 10. Peran static analysis tools dalam code review

| Tool | Fungsi utama |
|---|---|
| pylint | Linting komprehensif + skor kualitas kode |
| flake8 | Pelanggaran PEP 8, kompleksitas, masalah import |
| black | Auto-format kode (gaya konsisten, tanpa debat) |
| mypy | Type checking statis berdasarkan type hints |

Tanpa alat ini, reviewer manusia menghabiskan waktu untuk hal mekanis (spasi,
urutan import, nama variabel) dan bisa melewatkan masalah logika. Dengan alat
ini, masalah style dan potensi bug tertangkap otomatis **sebelum** review
manusia, sehingga reviewer fokus pada hal yang butuh pertimbangan manusia:
kebenaran logika, arsitektur, dan kebutuhan bisnis.

Integrasi ke CI/CD meningkatkan efektivitasnya karena menjadi gerbang wajib,
bukan imbauan: pre-commit hook menjalankan black/flake8/isort di mesin
pengembang sebelum commit dibuat, dan pipeline CI menjalankan ulang lint +
type check — kalau gagal, merge ditolak. Standar kualitas jadi konsisten di
seluruh tim tanpa bergantung pada ketelitian reviewer per orang.

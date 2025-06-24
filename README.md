# Aplikasi IoT PBL

Aplikasi ini adalah bagian dari proyek PBL (Project Based Learning) untuk mata kuliah IoT. Aplikasi ini menggunakan FastAPI untuk menyediakan API yang dapat digunakan untuk mengelola data barang.

## Prasyarat

- Python 3.x
- MySQL Server
- Pip (Python Package Manager)

## Pengaturan Lingkungan Lokal

1. Pastikan MySQL server berjalan di komputer Anda
2. Buat database dengan nama `iot_3a`:
   ```
   mysql -u root -p
   CREATE DATABASE iot_3a;
   exit;
   ```
3. Import struktur database dari file `iot.sql`:
   ```
   mysql -u root -p iot_3a < iot.sql
   ```

## Konfigurasi

1. Sesuaikan file `.env` dengan kredensial MySQL Anda:
   ```
   DB_USER=username_mysql_anda
   DB_PASS=password_mysql_anda
   DB_NAME=iot_3a
   DB_HOST=localhost
   ```

## Instalasi Dependensi

```
pip install -r requirements.txt
```

## Menjalankan Aplikasi Lokal

```
python main.py
```

Aplikasi akan berjalan di `http://localhost:8080`

## Deployment ke VPS Ubuntu

1. Upload semua file ke VPS Ubuntu
2. Berikan izin eksekusi pada script setup:
   ```
   chmod +x setup_vps.sh
   ```
3. Jalankan script setup:
   ```
   ./setup_vps.sh
   ```
4. Script akan mengatur semua yang diperlukan:
   - Menginstal dependensi sistem
   - Mengkonfigurasi MySQL
   - Membuat database dan user
   - Mengimpor skema database
   - Menginstal dependensi Python
   - Mengkonfigurasi Nginx sebagai reverse proxy
   - Mengatur aplikasi sebagai layanan systemd

Setelah script selesai, aplikasi akan berjalan di `http://IP_SERVER` dan dokumentasi API akan tersedia di `http://IP_SERVER/docs`.

## Penggunaan API

### Dokumentasi API
```
GET /docs
```

### Mendapatkan Status Aplikasi
```
GET /
```

### Menambahkan Data Barang
```
POST /barang
Content-Type: application/json

{
  "id": "123",
  "tipe": "Besar",
  "jenis": "Padat"
}
```

### Mendapatkan Semua Data Barang
```
GET /barang
```

### Mendapatkan Data Barang Berdasarkan Tipe
```
GET /barang/by-tipe
```

### Mendapatkan Data Barang Berdasarkan Jenis
```
GET /barang/by-jenis
```

Nilai yang valid untuk `tipe`: "Besar", "Kecil", "Sedang"
Nilai yang valid untuk `jenis`: "Kimia", "Cair", "Padat"

## Struktur Database

Tabel `barang`:
- `id` (varchar): ID unik barang
- `tipe` (enum): Tipe barang (Besar, Kecil, Sedang)
- `jenis` (enum): Jenis barang (Kimia, Cair, Padat)
- `jumlah` (int): Jumlah barang (default: 1)

## Troubleshooting

Jika terjadi error "Can't connect to MySQL server", pastikan:
1. MySQL server berjalan
2. Kredensial di file `.env` benar
3. Database `iot_3a` sudah dibuat

Untuk melihat log aplikasi di VPS:
```
sudo journalctl -u iot-pbl
``` 
#!/bin/bash

# Update sistem
echo "Memperbarui sistem..."
sudo apt update
sudo apt upgrade -y

# Instal dependensi
echo "Menginstal dependensi..."
sudo apt install -y python3 python3-pip python3-venv mysql-server nginx

# Konfigurasi MySQL
echo "Mengkonfigurasi MySQL..."
sudo systemctl enable mysql
sudo systemctl start mysql

# Buat database dan user (ganti password sesuai kebutuhan)
echo "Membuat database dan user..."
sudo mysql -e "CREATE DATABASE IF NOT EXISTS iot_3a;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'iot_user'@'localhost' IDENTIFIED BY 'iot_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON iot_3a.* TO 'iot_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Import skema database
echo "Mengimpor skema database..."
sudo mysql iot_3a < iot.sql

# Buat virtual environment
echo "Membuat virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Instal dependensi Python
echo "Menginstal dependensi Python..."
pip install -r requirements.txt
pip install gunicorn

# Konfigurasi .env
echo "Mengkonfigurasi .env..."
cat > .env << EOF
DB_USER=iot_user
DB_PASS=iot_password
DB_NAME=iot_3a
DB_HOST=localhost
EOF

# Konfigurasi Nginx
echo "Mengkonfigurasi Nginx..."
sudo tee /etc/nginx/sites-available/iot-pbl << EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/iot-pbl /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Konfigurasi systemd service
echo "Mengkonfigurasi systemd service..."
sudo cp iot-pbl.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable iot-pbl
sudo systemctl start iot-pbl

echo "Instalasi selesai!"
echo "API berjalan di http://IP_SERVER"
echo "Dokumentasi API tersedia di http://IP_SERVER/docs" 
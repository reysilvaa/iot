import os
import pymysql
import sqlalchemy
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
import uvicorn
import traceback

load_dotenv()

app = FastAPI(
    title="API IoT PBL",
    description="API untuk Project Based Learning IoT",
    version="1.0.0"
)

# Aktifkan CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model data untuk input barang
class BarangInput(BaseModel):
    id: str
    tipe: str
    jenis: str

# Fungsi koneksi database
def connect():
    try:
        db_user = os.environ["DB_USER"]
        db_pass = os.environ["DB_PASS"]
        db_name = os.environ["DB_NAME"]
        db_host = os.environ["DB_HOST"]
        
        # Cek apakah berjalan di lingkungan lokal
        if db_host == "localhost":
            return sqlalchemy.create_engine(
                sqlalchemy.engine.url.URL.create(
                    drivername="mysql+pymysql",
                    username=db_user,
                    password=db_pass,
                    host=db_host,
                    database=db_name,
                )
            )
        else:
            # Untuk VPS, gunakan koneksi host biasa
            return sqlalchemy.create_engine(
                sqlalchemy.engine.url.URL.create(
                    drivername="mysql+pymysql",
                    username=db_user,
                    password=db_pass,
                    host=db_host,
                    database=db_name,
                )
            )
    except Exception as e:
        print(f"Kesalahan koneksi database: {e}")
        return None

db = connect()

@app.get("/")
async def root():
    return {"message": "Aplikasi IoT PBL berjalan! Gunakan endpoint /docs untuk dokumentasi API."}

@app.post("/barang")
async def tambah_barang(barang: BarangInput):
    try:
        if db is None:
            raise HTTPException(status_code=500, detail="Koneksi database tidak tersedia")
            
        # Validasi tipe dan jenis
        valid_tipe = ["Besar", "Kecil", "Sedang"]
        valid_jenis = ["Kimia", "Cair", "Padat"]
        
        if barang.tipe not in valid_tipe:
            raise HTTPException(status_code=400, detail=f"Tipe tidak valid. Pilihan: {', '.join(valid_tipe)}")
            
        if barang.jenis not in valid_jenis:
            raise HTTPException(status_code=400, detail=f"Jenis tidak valid. Pilihan: {', '.join(valid_jenis)}")

        query = """
            INSERT INTO barang (id, tipe, jenis)
            VALUES (:id, :tipe, :jenis)
            ON DUPLICATE KEY UPDATE jumlah = jumlah + 1
        """

        with db.connect() as conn:
            conn.execute(sqlalchemy.text(query), {
                "id": barang.id,
                "tipe": barang.tipe,
                "jenis": barang.jenis
            })
            conn.commit()

        return {"status": "success", "data": {"jenis": barang.jenis}}

    except HTTPException as e:
        raise e
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/barang")
async def daftar_barang():
    try:
        if db is None:
            raise HTTPException(status_code=500, detail="Koneksi database tidak tersedia")
            
        query = "SELECT * FROM barang"

        with db.connect() as conn:
            result = conn.execute(sqlalchemy.text(query))
            rows = result.fetchall()

        data = [dict(row._mapping) for row in rows]

        return {"status": "success", "data": data}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/barang/by-tipe")
async def barang_by_tipe():
    try:
        if db is None:
            raise HTTPException(status_code=500, detail="Koneksi database tidak tersedia")
            
        query = "SELECT * FROM barang_type_group_view"

        with db.connect() as conn:
            result = conn.execute(sqlalchemy.text(query))
            rows = result.fetchall()

        data = [dict(row._mapping) for row in rows]

        return {"status": "success", "data": data}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/barang/by-jenis")
async def barang_by_jenis():
    try:
        if db is None:
            raise HTTPException(status_code=500, detail="Koneksi database tidak tersedia")
            
        query = "SELECT * FROM barang_jenis_group_view"

        with db.connect() as conn:
            result = conn.execute(sqlalchemy.text(query))
            rows = result.fetchall()

        data = [dict(row._mapping) for row in rows]

        return {"status": "success", "data": data}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True) 
import os
import pymysql
import sqlalchemy
from flask import Request, make_response
from dotenv import load_dotenv
import flask
import traceback

load_dotenv()

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
            db_socket_dir = os.environ["INSTANCE_CONNECTION_NAME"]
            return sqlalchemy.create_engine(
                sqlalchemy.engine.url.URL.create(
                    drivername="mysql+pymysql",
                    username=db_user,
                    password=db_pass,
                    database=db_name,
                    query={
                        "unix_socket": f"/cloudsql/{db_socket_dir}"
                    }
                )
            )
    except Exception as e:
        print(f"Kesalahan koneksi database: {e}")
        return None

db = connect()

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def handle_request():
    request = flask.request
    # Handle preflight request
    if request.method == 'OPTIONS':
        # Allows POST requests from any origin with the Content-Type header
        # and caches preflight response for 3600s
        response = make_response('', 204)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Max-Age'] = '3600'
        return response
        
    if request.method == 'GET':
        return "Aplikasi IoT PBL berjalan! Gunakan POST untuk mengirim data."

    try:
        if db is None:
            raise Exception("Koneksi database tidak tersedia")
            
        data = request.get_json(force=True)

        # Required fields
        id = data.get("id")
        tipe = data.get("tipe")
        jenis = data.get("jenis")

        if not id or not tipe:
            raise KeyError("id or tipe")

        query = """
            INSERT INTO barang (id, tipe, jenis)
            VALUES (:id, :tipe, :jenis)
            ON DUPLICATE KEY UPDATE jumlah = jumlah + 1
        """

        with db.connect() as conn:
            conn.execute(sqlalchemy.text(query), {
                "id": id,
                "tipe": tipe,
                "jenis": jenis
            })
            conn.commit()

        response = make_response({
            "status": "success",
            "data": {
                "jenis": jenis
                }
            }, 200)

    except KeyError as e:
        response = make_response({"error": f"Missing required field: {e}"}, 400)
    except Exception as e:
        print(traceback.format_exc())
        response = make_response({"error": str(e)}, 500)

    # Apply CORS headers to the actual response
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# Fungsi main untuk kompatibilitas dengan Cloud Functions
def main(request):
    return handle_request()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

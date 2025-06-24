import os
import pymysql
import sqlalchemy
from flask import Request
from dotenv import load_dotenv
load_dotenv()

def connect():
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_socket_dir =  os.environ["INSTANCE_CONNECTION_NAME"]

    return sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            database=db_name,
            query={
                "unix_socket": "/cloudsql/{}".format(
                    db_socket_dir
                )
            }
        )
    )

db = connect()

def main(request: Request):
    try:
        query = "SELECT * FROM `iot_3a`.`barang_jenis_group_view`"

        with db.connect() as conn:
            result = conn.execute(sqlalchemy.text(query))
            rows = result.fetchall()

        data = [dict(row._mapping) for row in rows]

        return {"status": "success", "data": data}, 200

    except Exception as e:
        return {"error": str(e)}, 500

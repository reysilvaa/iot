drop table if exists `barang`;
drop view if exists `iot_3a`.`barang_type_group_view`;
drop view if exists `iot_3a`.`barang_jenis_group_view`;

CREATE TABLE barang(
  id varchar(255) PRIMARY KEY,
  tipe ENUM('Besar','Kecil','Sedang') NOT NULL,
  jenis ENUM('Kimia','Cair','Padat') NOT NULL,
  jumlah int UNSIGNED NOT NULL DEFAULT(1)
);

CREATE VIEW iot_3a.barang_type_group_view AS (
  SELECT 
  ROW_NUMBER() OVER (ORDER BY tipe) as row_no,
  tipe as tipe_barang,
  CAST(SUM(jumlah) AS UNSIGNED INTEGER) AS as jumlah_barang
  FROM
  barang
  GROUP BY tipe
);

CREATE VIEW iot_3a.barang_jenis_group_view AS (
  SELECT 
  ROW_NUMBER() OVER (ORDER BY jenis) as row_no,
  jenis as jenis_barang,
  CAST(SUM(jumlah) AS UNSIGNED INTEGER) as jumlah_barang
  FROM
  barang
  GROUP BY jenis
);
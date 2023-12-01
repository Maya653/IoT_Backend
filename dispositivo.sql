CREATE TABLE dispositivo(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    dispositivo VARCHAR(20) NOT NULL,
    valor tinyint  NOT NULL DEFAULT 0

);
INSERT INTO dispositivo(dispositivo, valor) VALUES  ('led', 0), ('sensor', 0);
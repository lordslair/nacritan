CREATE TABLE IF NOT EXISTS pcs (
id        INT      NOT NULL PRIMARY KEY,
level     INT      NOT NULL,
name      TEXT     NOT NULL,
wounds    TEXT     NULL,
guildId   INT      NULL,
guildName TEXT     NULL,
x         INT      NULL,
y         INT      NULL,
user      TEXT     NOT NULL,
date      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS pcsInfos (
id        INT      NOT NULL PRIMARY KEY,
name      TEXT     NOT NULL,
race      TEXT     NOT NULL,
img       TEXT     NULL,
dla       DATETIME NOT NULL,
pas       INT      NOT NULL,
pos       INT      NOT NULL,
xp        INT      NOT NULL,
xpMax     INT      NOT NULL,
user      TEXT     NOT NULL,
date      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS pcsCaracs (
id        INT      NOT NULL PRIMARY KEY,
name      TEXT     NOT NULL,
pv        INT      NOT NULL,
pvMax     INT      NOT NULL,
attM      INT      NOT NULL,
defM      INT      NOT NULL,
degM      INT      NOT NULL,
arm       INT      NOT NULL,
mmM       INT      NOT NULL,
pc        INT      NULL,
user      TEXT     NOT NULL,
date      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS npcs (
id        INT      NOT NULL PRIMARY KEY,
level     INT      NOT NULL,
name      TEXT     NOT NULL,
wounds    TEXT     NULL,
x         INT      NOT NULL,
y         INT      NOT NULL,
user      TEXT     NOT NULL,
date      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS places (
id        INT      NOT NULL PRIMARY KEY,
level     INT      NOT NULL,
name      TEXT     NOT NULL,
townId    INT      NULL,
townName  TEXT     NULL,
x         INT      NOT NULL,
y         INT      NOT NULL,
user      TEXT     NOT NULL,
date      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS resources (
id        INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
level     INT      NOT NULL,
name      TEXT     NOT NULL,
x         INT      NOT NULL,
y         INT      NOT NULL,
user      TEXT     NOT NULL,
date      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS objects (
id        INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
name      TEXT     NOT NULL,
x         INT      NOT NULL,
y         INT      NOT NULL,
user      TEXT     NOT NULL,
date      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS tiles (
id        INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
x         INT      NOT NULL,
y         INT      NOT NULL,
type      TEXT     NOT NULL,
user      TEXT     NOT NULL,
date      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS jsons (
id        INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
data      TEXT     NOT NULL,
date      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);

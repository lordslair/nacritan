<?php

try {
// Nouvel objet de base SQLite
   $db_handle = new PDO('sqlite:nacridan.db');
// Quelques options
   $db_handle->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (Exception $e) {
   die('Erreur : '.$e->getMessage());
}

header('Access-Control-Allow-Origin: *');

$json = file_get_contents('php://input');
$arr  = json_decode($json, true);

if ( $arr )
{

  $sql_jsons = 'REPLACE INTO jsons ( id, data) VALUES (?, ?)';
  $req_jsons = $db_handle->prepare($sql_jsons);
  $req_jsons->execute(array(time(), $json));

  foreach ($arr as $elem)
  {
    $req_tiles = $db_handle->prepare('REPLACE INTO tiles ( x, y, type )
                                      SELECT ?, ?, ?
                                      WHERE NOT EXISTS (SELECT 1 FROM tiles WHERE x = '.$elem['x'].' AND y = '.$elem['y'].')');

    $req_tiles->execute(array($elem['x'], $elem['y'], $elem['type']));

    if ( $elem['items']['places'] )
    {
      foreach ($elem['items']['places'] as $place)
      {
        if ( !is_null($place['id']) )
        {
          $sql_places = 'INSERT OR REPLACE INTO places ( id, level, name, townId, townName, x, y )
                                           VALUES (
                                                   COALESCE(?, (SELECT id        FROM places WHERE id = '.$place['id'].')),
                                                   COALESCE(?, (SELECT level     FROM places WHERE id = '.$place['id'].')),
                                                   COALESCE(?, (SELECT name      FROM places WHERE id = '.$place['id'].')),
                                                   COALESCE(?, (SELECT townId    FROM places WHERE id = '.$place['id'].')),
                                                   COALESCE(?, (SELECT townName  FROM places WHERE id = '.$place['id'].')),
                                                   COALESCE(?, (SELECT x         FROM places WHERE id = '.$place['id'].')),
                                                   COALESCE(?, (SELECT y         FROM places WHERE id = '.$place['id'].'))
                                                  )';

          $req_places = $db_handle->prepare($sql_places);
          $req_places->execute(array($place['id'], $place['level'], $place['name'], $place['townId'], $place['townName'], $elem['x'], $elem['y']));
        }
      }
    }

    if ( $elem['items']['pcs'] )
    {
      foreach ($elem['items']['pcs'] as $pc)
      {
        $sql_pcs = 'INSERT OR REPLACE INTO pcs ( id, level, name, wounds, guildId, guildName, x, y )
                                      VALUES (
                                              COALESCE(?, (SELECT id        FROM pcs WHERE id = '.$pc['id'].')),
                                              COALESCE(?, (SELECT level     FROM pcs WHERE id = '.$pc['id'].')),
                                              COALESCE(?, (SELECT name      FROM pcs WHERE id = '.$pc['id'].')),
                                              COALESCE(?, (SELECT wounds    FROM pcs WHERE id = '.$pc['id'].')),
                                              COALESCE(?, (SELECT guildId   FROM pcs WHERE id = '.$pc['id'].')),
                                              COALESCE(?, (SELECT guildName FROM pcs WHERE id = '.$pc['id'].')),
                                              COALESCE(?, (SELECT x         FROM pcs WHERE id = '.$pc['id'].')),
                                              COALESCE(?, (SELECT y         FROM pcs WHERE id = '.$pc['id'].'))
                                             )';

        $req_pcs = $db_handle->prepare($sql_pcs);
        $req_pcs->execute(array($pc['id'], $pc['level'], $pc['name'], $pc['wounds'], $pc['guildId'], $pc['guildName'], $elem['x'], $elem['y']));
      }
    }

    if ( $elem['items']['npcs'] )
    {
      foreach ($elem['items']['npcs'] as $npc)
      {
        $sql_npcs = 'INSERT OR REPLACE INTO npcs ( id, level, name, wounds, x, y )
                                       VALUES (
                                               COALESCE(?, (SELECT id        FROM npcs WHERE id = '.$npc['id'].')),
                                               COALESCE(?, (SELECT level     FROM npcs WHERE id = '.$npc['id'].')),
                                               COALESCE(?, (SELECT name      FROM npcs WHERE id = '.$npc['id'].')),
                                               COALESCE(?, (SELECT wounds    FROM npcs WHERE id = '.$npc['id'].')),
                                               COALESCE(?, (SELECT x         FROM npcs WHERE id = '.$npc['id'].')),
                                               COALESCE(?, (SELECT y         FROM npcs WHERE id = '.$npc['id'].'))
                                              )';
        $req_npcs = $db_handle->prepare($sql_npcs);
        $req_npcs->execute(array($npc['id'], $npc['level'], $npc['name'], $npc['wounds'], $elem['x'], $elem['y']));
      }
    }
  }
}
?>

<?php

try {
// Nouvel objet de base SQLite
   $db_handle = new PDO('sqlite:nacridan.db');
// Quelques options
   $db_handle->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (Exception $e) {
   die('Erreur : '.$e->getMessage());
}

$files = glob('*.{txt}', GLOB_BRACE);
foreach($files as $file) {
  echo $file."\n";

  $arr = json_decode(file_get_contents($file), true);

  if ( $arr )
  {
    foreach ($arr as $elem)
    {
      $req_tiles = $db_handle->prepare('REPLACE INTO tiles ( x, y, type )
                                        SELECT ?, ?, ?
                                        WHERE NOT EXISTS (SELECT 1 FROM tiles WHERE x = '.$elem['x'].' AND y = '.$elem['y'].')');

      $req_tiles->execute(array($elem['x'], $elem['y'], $elem['type']));

      if ( $elem['items']['places'] and $elem['items']['places']['id'] )
      {
        foreach ($elem['items']['places'] as $place)
        {
          $req_places = $db_handle->prepare('REPLACE INTO places ( id, level, name, townId, townName, x, y )
                                             SELECT ?, ?, ?, ?, ?, ?, ?
                                             WHERE NOT EXISTS (SELECT 1 FROM places WHERE id = '.$place['id'].')');

          $req_places->execute(array($place['id'], $place['level'], $place['name'], $place['townId'], $place['townName'], $elem['x'], $elem['y']));
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
}
?>

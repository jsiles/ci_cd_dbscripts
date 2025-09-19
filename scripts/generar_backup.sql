set heading off
set feedback off
set long 100000
set pagesize 0
set linesize 200
spool backups/backup_&&1..sql

SELECT dbms_metadata.get_ddl(object_type, object_name, owner)
FROM all_objects
WHERE owner = upper('APPUSER')
  AND object_type IN ('PROCEDURE','FUNCTION','PACKAGE','TRIGGER');

spool off
exit;

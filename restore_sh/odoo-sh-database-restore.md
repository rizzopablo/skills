     1 ---                                                                                                                                                                                                
name: odoo-sh-database-restore                                                                                                                                                                     
description: Restore an odoo.sh database dump (SQL + filestore) when standard odoo-bin db load fails due to permission or \restrict issues                                                         
type: skill                                                                                                                                                                                        
---                                                                                                                                                                                                
                                                                                                                                                                                                   
# Odoo.sh Database Restore Skill                                                                                                                                                                   
                                                                                                                                                                                                   
Restores a database from an odoo.sh backup when `odoo-bin db load` fails with permission errors or `\restrict` incompatibility.                                                                    
                                                                                                                                                                                                   
## Problem                                                                                                                                                                                         
                                                                                                                                                                                                   
`odoo-bin db load` may fail with:                                                                                                                                                                  
- `must be owner of database` — cannot drop existing database                                                                                                                                      
- `backslash commands are restricted` — dump uses odoo.sh's `\restrict` security feature incompatible with standard psql                                                                           
- `permission denied` — the database user lacks superuser privileges                                                                                                                               
                                                                                                                                                                                                   
## Solution                                                                                                                                                                                        
                                                                                                                                                                                                   
### Step 1: Get database connection details                                                                                                                                                        
                                                                                                                                                                                                   
Find the environment variables:                                                                                                                                                                    
```bash                                                                                                                                                                                            
env | grep -E "PGHOST|PGDATABASE|PGUSER|PGPASSWORD"                                                                                                                                                
```                                                                                                                                                                                                
                                                                                                                                                                                                   
Expected output:                                                                                                                                                                                   
```                                                                                                                                                                                                
PGHOST=192.168.x.x                                                                                                                                                                                 
PGDATABASE=your-database-name                                                                                                                                                                      
PGUSER=p_your_database_user                                                                                                                                                                        
PGPASSWORD=your-password                                                                                                                                                                           
```                                                                                                                                                                                                
                                                                                                                                                                                                   
### Step 2: Clean the dump file                                                                                                                                                                    
                                                                                                                                                                                                   
Remove odoo.sh's `\restrict` and `\unrestrict` commands:                                                                                                                                           
```bash                                                                                                                                                                                            
# Find the line numbers                                                                                                                                                                            
grep -n "^\\\\restrict\|^\\\\unrestrict" /path/to/dump.sql                                                                                                                                         
                                                                                                                                                                                                   
# Remove them (replace 5 and 302236 with actual line numbers)                                                                                                                                      
sed -e '5d' -e '302236d' /path/to/dump.sql > /tmp/dump_cleaned.sql                                                                                                                                 
```                                                                                                                                                                                                
                                                                                                                                                                                                   
### Step 3: Clean existing database objects                                                                                                                                                        
                                                                                                                                                                                                   
Create a cleanup script (`/tmp/clean_database.sql`):                                                                                                                                               
```sql                                                                                                                                                                                             
DO $$                                                                                                                                                                                              
DECLARE r RECORD;                                                                                                                                                                                  
BEGIN                                                                                                                                                                                              
    -- Drop all tables                                                                                                                                                                             
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP                                                                                                                    
        EXECUTE 'DROP TABLE IF EXISTS public.' || quote_ident(r.tablename) || ' CASCADE';                                                                                                          
    END LOOP;                                                                                                                                                                                      
                                                                                                                                                                                                   
    -- Drop all sequences                                                                                                                                                                          
    FOR r IN (SELECT sequencename FROM pg_sequences WHERE schemaname = 'public') LOOP                                                                                                              
        EXECUTE 'DROP SEQUENCE IF EXISTS public.' || quote_ident(r.sequencename) || ' CASCADE';                                                                                                    
    END LOOP;                                                                                                                                                                                      
                                                                                                                                                                                                   
    -- Drop all views                                                                                                                                                                              
    FOR r IN (SELECT viewname FROM pg_views WHERE schemaname = 'public') LOOP                                                                                                                      
        EXECUTE 'DROP VIEW IF EXISTS public.' || quote_ident(r.viewname) || ' CASCADE';                                                                                                            
    END LOOP;                                                                                                                                                                                      
                                                                                                                                                                                                   
    -- Drop user functions (skip system functions)                                                                                                                                                 
    FOR r IN (SELECT p.proname FROM pg_proc p                                                                                                                                                      
              JOIN pg_namespace n ON p.pronamespace = n.oid                                                                                                                                        
              WHERE n.nspname = 'public'                                                                                                                                                           
              AND NOT EXISTS (SELECT 1 FROM pg_depend d WHERE d.objid = p.oid AND d.deptype = 'e')) LOOP                                                                                           
        BEGIN                                                                                                                                                                                      
            EXECUTE 'DROP FUNCTION IF EXISTS public.' || quote_ident(r.proname) || ' CASCADE';                                                                                                     
        EXCEPTION WHEN OTHERS THEN                                                                                                                                                                 
            RAISE NOTICE 'Could not drop function %: %', r.proname, SQLERRM;                                                                                                                       
        END;                                                                                                                                                                                       
    END LOOP;                                                                                                                                                                                      
                                                                                                                                                                                                   
    -- Drop user types (skip system types)                                                                                                                                                         
    FOR r IN (SELECT t.typname FROM pg_type t                                                                                                                                                      
              JOIN pg_namespace n ON t.typnamespace = n.oid                                                                                                                                        
              WHERE n.nspname = 'public'                                                                                                                                                           
              AND NOT EXISTS (SELECT 1 FROM pg_depend d WHERE d.objid = t.oid AND d.deptype = 'e')) LOOP                                                                                           
        BEGIN                                                                                                                                                                                      
            EXECUTE 'DROP TYPE IF EXISTS public.' || quote_ident(r.typname) || ' CASCADE';                                                                                                         
        EXCEPTION WHEN OTHERS THEN                                                                                                                                                                 
            RAISE NOTICE 'Could not drop type %: %', r.typname, SQLERRM;                                                                                                                           
        END;                                                                                                                                                                                       
    END LOOP;                                                                                                                                                                                      
                                                                                                                                                                                                   
    -- Drop extensions (keep system ones)                                                                                                                                                          
    FOR r IN (SELECT extname FROM pg_extension                                                                                                                                                     
              WHERE extname NOT IN ('plpgsql', 'tablefunc', 'pg_trgm', 'unaccent', 'vector')) LOOP                                                                                                 
        BEGIN                                                                                                                                                                                      
            EXECUTE 'DROP EXTENSION IF EXISTS ' || quote_ident(r.extname) || ' CASCADE';                                                                                                           
        EXCEPTION WHEN OTHERS THEN                                                                                                                                                                 
            RAISE NOTICE 'Could not drop extension %: %', r.extname, SQLERRM;                                                                                                                      
        END;                                                                                                                                                                                       
    END LOOP;                                                                                                                                                                                      
END $$;                                                                                                                                                                                            
```                                                                                                                                                                                                
                                                                                                                                                                                                   
Execute the cleanup:                                                                                                                                                                               
```bash                                                                                                                                                                                            
PGPASSWORD="$PGPASSWORD" psql -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE" -f /tmp/clean_database.sql                                                                                                
```                                                                                                                                                                                                
                                                                                                                                                                                                   
Verify tables are gone:                                                                                                                                                                            
```bash                                                                                                                                                                                            
PGPASSWORD="$PGPASSWORD" psql -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE" -c "SELECT COUNT(*) FROM pg_tables WHERE schemaname = 'public';"                                                          
```                                                                                                                                                                                                
Expected: `0`                                                                                                                                                                                      
                                                                                                                                                                                                   
### Step 4: Load the cleaned dump                                                                                                                                                                  
                                                                                                                                                                                                   
```bash                                                                                                                                                                                            
PGPASSWORD="$PGPASSWORD" psql -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE" \                                                                                                                         
  --no-psqlrc -v ON_ERROR_STOP=0 -f /tmp/dump_cleaned.sql > /tmp/restore_output.log 2>&1                                                                                                           
                                                                                                                                                                                                   
echo "Exit code: $?"                                                                                                                                                                               
grep -c "error:" /tmp/restore_output.log  # Should be 0                                                                                                                                            
```                                                                                                                                                                                                
                                                                                                                                                                                                   
Verify restoration:                                                                                                                                                                                
```bash                                                                                                                                                                                            
PGPASSWORD="$PGPASSWORD" psql -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE" -c "                                                                                                                      
SELECT 'res_users' as table_name, COUNT(*) FROM res_users                                                                                                                                          
UNION ALL SELECT 'res_partner', COUNT(*) FROM res_partner                                                                                                                                          
UNION ALL SELECT 'ir_module_module', COUNT(*) FROM ir_module_module;"                                                                                                                              
```                                                                                                                                                                                                
                                                                                                                                                                                                   
### Step 5: Restore filestore (if available)                                                                                                                                                       
                                                                                                                                                                                                   
If the backup is a `.zip` file containing both `dump.sql` and `filestore/`:                                                                                                                        
                                                                                                                                                                                                   
```bash                                                                                                                                                                                            
# Extract filestore                                                                                                                                                                                
cd /tmp                                                                                                                                                                                            
unzip -o /path/to/backup.zip filestore/* -d /tmp/extracted_fs/                                                                                                                                     
                                                                                                                                                                                                   
# Replace existing filestore                                                                                                                                                                       
rm -rf /home/odoo/data/filestore/$PGDATABASE                                                                                                                                                       
cp -r /tmp/extracted_fs/filestore /home/odoo/data/filestore/$PGDATABASE                                                                                                                            
chown -R odoo:odoo /home/odoo/data/filestore/$PGDATABASE                                                                                                                                           
```                                                                                                                                                                                                
                                                                                                                                                                                                   
### Step 6: Restart Odoo service                                                                                                                                                                   
                                                                                                                                                                                                   
In odoo.sh environments, send HUP to the supervisor:                                                                                                                                               
```bash                                                                                                                                                                                            
kill -HUP 1                                                                                                                                                                                        
```                                                                                                                                                                                                
                                                                                                                                                                                                   
Or start a worker manually:                                                                                                                                                                        
```bash                                                                                                                                                                                            
odoo-bin --database="$PGDATABASE" --workers=0 --no-http --proxy-mode \                                                                                                                             
  --data-dir=/home/odoo/data --config=/home/odoo/.config/odoo/odoo.conf &                                                                                                                          
```                                                                                                                                                                                                
                                                                                                                                                                                                   
Verify it's running:                                                                                                                                                                               
```bash                                                                                                                                                                                            
tail -30 /home/odoo/logs/odoo.log | grep "Modules loaded"                                                                                                                                          
ps aux | grep odoo-bin | grep -v grep                                                                                                                                                              
```                                                                                                                                                                                                
                                                                                                                                                                                                   
## Common Issues                                                                                                                                                                                   
                                                                                                                                                                                                   
| Error | Cause | Solution |                                                                                                                                                                       
|-------|-------|----------|                                                                                                                                                                       
| `must be owner of database` | Cannot DROP DATABASE | Use the table-by-table cleanup approach |                                                                                                   
| `backslash commands are restricted` | `\restrict` in dump | Remove `\restrict` and `\unrestrict` lines |                                                                                         
| `invalid command \N` | psql misinterpreting COPY data | Use `--no-psqlrc` flag |                                                                                                                 
| `permission denied for function/type` | System objects from extensions | Exclude extension-owned objects in cleanup |                                                                            
| Process killed (OOM) | Loading large dump in Python | Use psql instead of Python psycopg2 |                                                                                                      
| Process killed (OOM) | runing parallel tasks | Don't run tasks in parallel, only one by one |                                                                                                      


## Verification Checklist                                                                                                                                                                          
                                                                                                                                                                                                   
- [ ] Tables count matches expected (typically 700+)                                                                                                                                               
- [ ] Key modules show `installed` state                                                                                                                                                           
- [ ] Filestore exists with correct ownership                                                                                                                                                      
- [ ] Odoo process is running                                                                                                                                                                      
- [ ] Logs show "Modules loaded" without errors                                                                                                                                                    
- [ ] Web interface responds (test with `curl`)  

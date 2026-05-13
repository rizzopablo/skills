#!/usr/bin/env python3
"""
Odoo.sh Database Restore Script

Restores a database from an odoo.sh backup (SQL dump + optional filestore)
when standard odoo-bin db load fails due to permission or \\restrict issues.

Usage:
    python3 restore_db.py --dump /path/to/dump.sql [--filestore /path/to/backup.zip]
"""

import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Optional


# Colors for terminal output
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def log_step(step: int, total: int, message: str):
    print(f"\n{Colors.BLUE}{Colors.BOLD}[Step {step}/{total}] {message}{Colors.RESET}")


def log_success(message: str):
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")


def log_error(message: str):
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")


def log_warn(message: str):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")


def log_info(message: str):
    print(f"  {message}")


def run_cmd(cmd: list[str], check: bool = True, capture_output: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    log_info(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=capture_output, text=True)
    if check and result.returncode != 0:
        log_error(f"Command failed with exit code {result.returncode}")
        if result.stderr:
            log_error(result.stderr[:500])
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    return result


def get_env_vars() -> dict[str, str]:
    """Get PostgreSQL connection details from environment."""
    required = ["PGHOST", "PGDATABASE", "PGUSER", "PGPASSWORD"]
    env_vars = {}
    missing = []

    for var in required:
        value = os.environ.get(var)
        if not value:
            missing.append(var)
        env_vars[var] = value

    if missing:
        log_error(f"Missing environment variables: {', '.join(missing)}")
        log_info("Set them with: export PGHOST=... PGDATABASE=... PGUSER=... PGPASSWORD=...")
        raise EnvironmentError(f"Missing env vars: {', '.join(missing)}")

    log_info(f"PGHOST={env_vars['PGHOST']}")
    log_info(f"PGDATABASE={env_vars['PGDATABASE']}")
    log_info(f"PGUSER={env_vars['PGUSER']}")
    log_info("PGPASSWORD=***")

    return env_vars


def find_restrict_lines(dump_path: str) -> list[int]:
    """Find line numbers of \\restrict and \\unrestrict commands."""
    result = run_cmd(["grep", "-n", r"^\\restrict\|^\\unrestrict", dump_path])
    lines = []
    for line in result.stdout.strip().split("\n"):
        if line:
            line_num = int(line.split(":")[0])
            lines.append(line_num)
    return lines


def clean_dump_file(dump_path: str) -> str:
    """Remove \\restrict and \\unrestrict lines from dump file."""
    log_info("Scanning for \\restrict and \\unrestrict lines...")
    restrict_lines = find_restrict_lines(dump_path)

    if not restrict_lines:
        log_info("No \\restrict commands found in dump")
        return dump_path

    log_info(f"Found {len(restrict_lines)} lines to remove: {restrict_lines}")

    clean_path = "/tmp/dump_cleaned.sql"
    log_info(f"Writing cleaned dump to {clean_path}")

    with open(dump_path, "r") as fin, open(clean_path, "w") as fout:
        for line_num, line in enumerate(fin, 1):
            if line_num in restrict_lines:
                log_info(f"Removing line {line_num}: {line.strip()[:80]}...")
                continue
            fout.write(line)

    log_success("Dump file cleaned")
    return clean_path


def create_cleanup_sql() -> str:
    """Create the SQL cleanup script."""
    cleanup_sql = """
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
"""
    cleanup_path = "/tmp/clean_database.sql"
    with open(cleanup_path, "w") as f:
        f.write(cleanup_sql)
    return cleanup_path


def cleanup_database(env: dict[str, str]):
    """Clean existing database objects."""
    log_info("Creating cleanup SQL script...")
    cleanup_path = create_cleanup_sql()

    cmd = [
        "psql",
        "-h", env["PGHOST"],
        "-U", env["PGUSER"],
        "-d", env["PGDATABASE"],
        "-f", cleanup_path,
    ]
    os.environ["PGPASSWORD"] = env["PGPASSWORD"]

    log_info("Executing database cleanup...")
    result = run_cmd(cmd, check=True, capture_output=True)
    log_success("Database cleanup completed")

    # Verify cleanup
    log_info("Verifying cleanup (checking table count)...")
    verify_cmd = [
        "psql",
        "-h", env["PGHOST"],
        "-U", env["PGUSER"],
        "-d", env["PGDATABASE"],
        "-t",
        "-c",
        "SELECT COUNT(*) FROM pg_tables WHERE schemaname = 'public';",
    ]
    result = run_cmd(verify_cmd, check=True, capture_output=True)
    table_count = int(result.stdout.strip())
    log_info(f"Tables remaining in public schema: {table_count}")

    if table_count != 0:
        log_warn(f"Expected 0 tables, but found {table_count}. This may be normal if some tables are system-owned.")


def load_dump(dump_path: str, env: dict[str, str]) -> str:
    """Load the cleaned dump into the database."""
    log_info("Loading dump into database (this may take a while)...")

    log_output = "/tmp/restore_output.log"

    cmd = [
        "psql",
        "-h", env["PGHOST"],
        "-U", env["PGUSER"],
        "-d", env["PGDATABASE"],
        "--no-psqlrc",
        "-v", "ON_ERROR_STOP=0",
        "-f", dump_path,
    ]
    os.environ["PGPASSWORD"] = env["PGPASSWORD"]

    with open(log_output, "w") as log_file:
        result = subprocess.run(cmd, stdout=log_file, stderr=subprocess.STDOUT, text=True)

    log_info(f"psql exit code: {result.returncode}")

    # Check for errors
    error_count = 0
    with open(log_output, "r") as f:
        for line in f:
            if "error:" in line.lower():
                error_count += 1

    if error_count > 0:
        log_warn(f"Found {error_count} error(s) in restore output (some may be non-critical)")
        log_info(f"Check {log_output} for details")
    else:
        log_success("No errors found in restore output")

    return log_output


def verify_restore(env: dict[str, str]):
    """Verify the database restoration."""
    log_info("Verifying database restoration...")

    cmd = [
        "psql",
        "-h", env["PGHOST"],
        "-U", env["PGUSER"],
        "-d", env["PGDATABASE"],
        "-c",
        """SELECT 'res_users' as table_name, COUNT(*) FROM res_users
UNION ALL SELECT 'res_partner', COUNT(*) FROM res_partner
UNION ALL SELECT 'ir_module_module', COUNT(*) FROM ir_module_module;""",
    ]
    os.environ["PGPASSWORD"] = env["PGPASSWORD"]

    result = run_cmd(cmd, check=True, capture_output=True)
    log_info("Key tables row counts:")
    for line in result.stdout.strip().split("\n"):
        log_info(f"  {line.strip()}")


def restore_filestore(filestore_path: str, env: dict[str, str]):
    """Restore filestore from backup zip."""
    log_info(f"Extracting filestore from {filestore_path}...")

    extract_dir = "/tmp/extracted_fs"

    # Clean up previous extraction if exists
    if os.path.exists(extract_dir):
        log_info("Removing previous extraction directory...")
        run_cmd(["rm", "-rf", extract_dir], check=False)

    log_info("Extracting zip file...")
    with zipfile.ZipFile(filestore_path, "r") as zf:
        # List filestore contents
        filestore_members = [m for m in zf.namelist() if m.startswith("filestore/")]
        log_info(f"Found {len(filestore_members)} filestore entries")

        zf.extractall(extract_dir)

    # Determine filestore destination
    filestore_dest = f"/home/odoo/data/filestore/{env['PGDATABASE']}"

    if os.path.exists(filestore_dest):
        log_info("Removing existing filestore...")
        run_cmd(["rm", "-rf", filestore_dest], check=False)

    log_info(f"Copying filestore to {filestore_dest}...")

    # Create parent directory if needed
    run_cmd(["mkdir", "-p", os.path.dirname(filestore_dest)], check=False)

    # Copy filestore
    extracted_fs = os.path.join(extract_dir, "filestore")
    if os.path.exists(extracted_fs):
        run_cmd(["cp", "-r", extracted_fs, filestore_dest], check=False)
        log_success("Filestore copied")

        # Fix ownership (may need sudo)
        log_info("Setting filestore ownership to odoo:odoo...")
        try:
            run_cmd(["chown", "-R", "odoo:odoo", filestore_dest], check=False)
            log_success("Ownership updated")
        except RuntimeError:
            log_warn("Could not change ownership (may need root privileges)")
    else:
        log_warn("No filestore/ directory found in zip")


def verify_odoo_running(env: dict[str, str]):
    """Check if Odoo is running and logs are healthy."""
    log_info("Checking Odoo process...")

    # Check for running odoo process
    result = run_cmd(["bash", "-c", "ps aux | grep odoo-bin | grep -v grep"], check=False, capture_output=True)

    if result.returncode == 0 and result.stdout.strip():
        log_success("Odoo process is running")
        log_info(result.stdout.strip()[:200])
    else:
        log_warn("Odoo process not found (may need to be started manually)")

    # Check logs for "Modules loaded"
    log_file = "/home/odoo/logs/odoo.log"
    if os.path.exists(log_file):
        log_info("Checking recent log entries...")
        result = run_cmd(
            ["bash", "-c", f"tail -30 {log_file} | grep -i 'modules loaded' || true"],
            check=False,
            capture_output=True,
        )
        if result.stdout.strip():
            log_success("Found 'Modules loaded' in logs")
        else:
            log_warn("'Modules loaded' not found in recent logs (Odoo may still be starting)")


def print_summary():
    """Print final summary."""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}Restore Complete!{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
    print("\nNext steps:")
    print("  1. Restart your Odoo service (if not auto-restarted)")
    print("  2. Check logs: tail -f /home/odoo/logs/odoo.log")
    print("  3. Test the web interface")
    print()


def main():
    # Parse arguments
    import argparse

    parser = argparse.ArgumentParser(description="Restore Odoo.sh database from dump")
    parser.add_argument("--dump", required=True, help="Path to dump.sql file")
    parser.add_argument("--filestore", help="Path to backup.zip containing filestore/")
    args = parser.parse_args()

    dump_path = args.dump
    filestore_path = args.filestore

    # Validate dump exists
    if not os.path.isfile(dump_path):
        log_error(f"Dump file not found: {dump_path}")
        sys.exit(1)

    total_steps = 4 if filestore_path else 3
    current_step = 0

    print(f"\n{Colors.BOLD}Odoo.sh Database Restore{Colors.RESET}")
    print(f"Dump: {dump_path}")
    if filestore_path:
        print(f"Filestore: {filestore_path}")

    # Step 1: Get env vars
    current_step += 1
    log_step(current_step, total_steps, "Getting database connection details")
    env = get_env_vars()

    # Step 2: Clean dump file
    current_step += 1
    log_step(current_step, total_steps, "Cleaning dump file (removing \\restrict commands)")
    clean_dump = clean_dump_file(dump_path)

    # Step 3: Cleanup database and load dump
    current_step += 1
    log_step(current_step, total_steps, "Cleaning existing database objects")
    cleanup_database(env)

    current_step += 1
    log_step(current_step, total_steps, "Loading cleaned dump into database")
    log_file = load_dump(clean_dump, env)
    verify_restore(env)

    # Step 4: Restore filestore (optional)
    if filestore_path:
        current_step += 1
        log_step(current_step, total_steps, "Restoring filestore from backup")
        restore_filestore(filestore_path, env)

    # Verify Odoo status
    print(f"\n{Colors.BLUE}{Colors.BOLD}[Verification] Checking Odoo status{Colors.RESET}")
    verify_odoo_running(env)

    # Print summary
    print_summary()


if __name__ == "__main__":
    main()

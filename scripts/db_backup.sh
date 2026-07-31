#!/bin/bash
# ==============================================================================
# NYAYA SETU - DATABASE BACKUP SCRIPT
# ==============================================================================
# This script creates a compressed pg_dump backup of the PostgreSQL database,
# prunes backups older than 7 days, and is designed to be run via cron.

set -e

BACKUP_DIR="/var/backups/nyayasetu"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
FILENAME="nyayasetu_db_$TIMESTAMP.sql.gz"
BACKUP_PATH="$BACKUP_DIR/$FILENAME"

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

echo "[$(date)] Starting database backup..."

# Assuming script runs on host where docker container 'nyayasetu-db-1' is running.
# Alternatively, if run inside the container, replace the docker exec with direct pg_dump.
docker exec nyayasetu-db-1 pg_dump -U nyayasetu_admin nyayasetu | gzip > "$BACKUP_PATH"

echo "[$(date)] Backup completed: $BACKUP_PATH"

# Prune old backups (Keep last 7 days)
echo "[$(date)] Pruning backups older than 7 days..."
find "$BACKUP_DIR" -type f -name "*.sql.gz" -mtime +7 -exec rm {} \;

echo "[$(date)] Pruning complete."

# (Optional) Sync to Cloud Storage like AWS S3
# aws s3 cp "$BACKUP_PATH" s3://nyayasetu-backups/db/

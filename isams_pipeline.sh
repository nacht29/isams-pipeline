#!/bin/bash

# Static file paths
#LOG_FILE="/var/log/tmp.log"
LOG_FILE="/var/log/isams_pipeline.log"
ARCHIVE_DIR="/var/log/isams_pipeline_arch"

archive_log() {
	TIMESTAMP=$(date +%Y%m%d_%H%M%S)
	ARCHIVE_LOG="$ARCHIVE_DIR/isams_pipeline_$TIMESTAMP.log"

	# Create archive copy
	cp "$LOG_FILE" "$ARCHIVE_LOG" 2>/dev/null

	# Verify creation
	if [ -f "$ARCHIVE_LOG" ]; then
		echo "Log archive created: $ARCHIVE_LOG"
	else
		echo "ERROR: Failed to create log archive!" >&2
		exit 1
	fi
}

interrupted() {
	echo "$(date) isams_pipeline interrupted" | tee -a "$LOG_FILE"
	archive_log # Archive before exit
	exit 1
}

# Trap signals
trap 'interrupted' SIGINT SIGTERM

# Start with clean log file
> "$LOG_FILE"

# Main pipeline execution
{
	echo "===== START: $(date) ====="
	cd /home/isams_pipeline/ || exit 1
	source myvenv/bin/activate
	cd /home/isams_pipeline/ || exit 1
	python iSAMS.py 2>&1
	echo "===== END: $(date) ====="
} | tee -a "$LOG_FILE"

# Final archive
archive_log


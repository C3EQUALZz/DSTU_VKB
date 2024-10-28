#!/bin/bash

current_date=$(date +%s)

snapshots_dir="/timeshift/snapshots"

cd "$snapshots_dir" || exit 1

for dir in */ ; do
  snapshot_date="${dir%/}"

  snapshot_timestamp=$(date -d "${snapshot_date:0:10} ${snapshot_date:11:2}:${snapshot_date:14:2}:${snapshot_date:17:2}" +%s)

  # Здесь время в секундах, здесь написано на 7 дней
  if (( (current_date - snapshot_timestamp) > 604800 )); then
    echo "Deleting snapshot: $dir (older than 7 days)"
    sudo rm -rf "$dir"
  else
    echo "Snapshot $dir is not older than 7 days, not deleting."
  fi
done
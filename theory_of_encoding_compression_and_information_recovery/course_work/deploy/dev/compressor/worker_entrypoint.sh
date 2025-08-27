#!/bin/sh
set -e

echo 'Starting worker...'
python -m taskiq worker --ack-type when_saved src.compressor.worker:create_taskiq_app src.compressor.infrastructure.task_manager.text.tasks
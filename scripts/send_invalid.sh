set -e
cd "$(dirname "$0")/.."
docker compose exec -T api python - < scripts/send_invalid.py
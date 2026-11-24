set -e
cd "$(dirname "$0")/.."
docker compose exec -T api python - "$@" < scripts/burst.py
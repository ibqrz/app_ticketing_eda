set -e
cd "$(dirname "$0")/.."
docker compose up -d --scale payment-service="${1:-2}" --no-recreate
docker compose ps payment-service
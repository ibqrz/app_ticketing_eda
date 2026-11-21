set -e
cd "$(dirname "$0")/.."
if ! command -v docker >/dev/null 2>&1; then
  echo "Docker nao encontrado. Instale o Docker Desktop e tente novamente."
  exit 1
fi
if [ ! -f .env ]; then
  cp .env.example .env
fi
docker compose up -d --build
echo "Frontend:            http://localhost:8080"
echo "API (documentacao):  http://localhost:8000/docs"
echo "RabbitMQ (painel):   http://localhost:15672  (usuario e senha do arquivo .env)"
import argparse
import json
import time
import urllib.request
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("--count", type=int, default=10)
parser.add_argument("--ticket", type=int, default=1)
parser.add_argument("--type", default="Pista")
parser.add_argument("--quantity", type=int, default=1)
parser.add_argument("--url", default="http://localhost:8000")
parser.add_argument("--wait", type=int, default=90)
args = parser.parse_args()


def call(path, payload=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        args.url + path,
        data=data,
        headers=headers,
        method="POST" if payload is not None else "GET",
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)


stamp = int(time.time())
session = call(
    "/api/auth/register",
    {
        "name": f"Cliente Rajada {stamp}",
        "email": f"rajada{stamp}@exemplo.com.br",
        "password": "senha-rajada-123",
    },
)
token = session["token"]
print("usuario criado:", session["user"]["email"])

ids = set()
for index in range(1, args.count + 1):
    result = call(
        "/api/orders",
        {"ticket_id": args.ticket, "ticket_type": args.type, "quantity": args.quantity},
        token,
    )
    ids.add(result["order_id"])
    print(f"pedido {index} aceito: {result['order_id']} ({result['message']})")

deadline = time.time() + args.wait
orders = []
while time.time() < deadline:
    found = call("/api/orders?scope=purchased&limit=100", token=token)
    found += call("/api/orders?scope=tracking&limit=100", token=token)
    orders = [order for order in found if order["id"] in ids]
    if len(orders) == len(ids) and all(o["status"] != "PROCESSING" for o in orders):
        break
    time.sleep(1)

print()
print("status:", dict(Counter(order["status"] for order in orders)))
print("distribuicao por instancia de pagamento:")
for instance, total in Counter(order["processed_by"] for order in orders).items():
    print(f"  {instance}: {total} pedido(s)")

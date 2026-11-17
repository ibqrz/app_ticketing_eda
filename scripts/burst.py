import argparse
import json
import time
import urllib.request
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("--count", type=int, default=10)
parser.add_argument("--ticket", type=int, default=1)
parser.add_argument("--quantity", type=int, default=1)
parser.add_argument("--url", default="http://localhost:8000")
parser.add_argument("--wait", type=int, default=90)
args = parser.parse_args()


def call(path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        args.url + path,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST" if payload is not None else "GET",
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.load(response)


ids = set()
for index in range(1, args.count + 1):
    result = call(
        "/api/orders",
        {
            "ticket_type_id": args.ticket,
            "quantity": args.quantity,
            "customer_name": f"Cliente {index}",
            "customer_email": f"cliente{index}@exemplo.com.br",
        },
    )
    ids.add(result["order_id"])
    print(f"pedido {index} aceito: {result['order_id']} ({result['message']})")

deadline = time.time() + args.wait
orders = []
while time.time() < deadline:
    recent = call(f"/api/orders?limit={min(max(args.count, 1), 50)}")
    orders = [order for order in recent if order["id"] in ids]
    if len(orders) == len(ids) and all(o["status"] != "PROCESSING" for o in orders):
        break
    time.sleep(1)

print()
print("status:", dict(Counter(order["status"] for order in orders)))
print("distribuicao por instancia de pagamento:")
for instance, total in Counter(order["processed_by"] for order in orders).items():
    print(f"  {instance}: {total} pedido(s)")

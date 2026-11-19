CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    tickets JSONB NOT NULL DEFAULT '[]'::jsonb
);

CREATE TABLE sessions (
    token_hash TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    info JSONB NOT NULL,
    image TEXT,
    available INTEGER NOT NULL CHECK (available >= 0)
);

CREATE TABLE orders (
    id UUID PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users (id),
    ticket_id INTEGER NOT NULL REFERENCES tickets (id),
    ticket_type TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    total NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE stock_reservations (
    order_id UUID PRIMARY KEY,
    ticket_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('RESERVED', 'SOLD_OUT', 'CONFIRMED', 'RELEASED')),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE payments (
    order_id UUID PRIMARY KEY,
    amount NUMERIC(10, 2) NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('APPROVED', 'REFUSED')),
    reason TEXT,
    processed_by TEXT NOT NULL,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    order_id UUID NOT NULL,
    kind TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (order_id, kind)
);

CREATE INDEX orders_user_created_idx ON orders (user_id, created_at DESC);

CREATE VIEW order_overview AS
SELECT
    o.id,
    o.user_id,
    o.ticket_id,
    o.ticket_type,
    o.quantity,
    o.total,
    o.created_at,
    t.info ->> 'name' AS ticket_name,
    t.info ->> 'location' AS location,
    t.image,
    (t.info ->> 'dtEvent')::timestamptz AS dt_event,
    (t.info ->> 'dtEvent')::timestamptz > now() AS active,
    p.reason,
    p.processed_by,
    CASE
        WHEN p.status = 'REFUSED' THEN 'REFUSED'
        WHEN p.status = 'APPROVED' AND r.status = 'CONFIRMED' THEN 'CONFIRMED'
        ELSE 'PROCESSING'
    END AS status,
    CASE
        WHEN p.status = 'REFUSED' THEN 'REFUSED'
        WHEN p.status = 'APPROVED' AND r.status = 'CONFIRMED' THEN 'CONFIRMED'
        WHEN p.status = 'APPROVED' THEN 'PAID'
        WHEN r.status = 'RESERVED' THEN 'RESERVED'
        ELSE 'RECEIVED'
    END AS stage
FROM orders o
JOIN tickets t ON t.id = o.ticket_id
LEFT JOIN stock_reservations r ON r.order_id = o.id
LEFT JOIN payments p ON p.order_id = o.id;

INSERT INTO tickets (info, image, available) VALUES
(
    '{
        "name": "Festival Horizonte de Rock",
        "description": "Três palcos, quinze bandas e uma noite inteira de rock nacional ao ar livre.",
        "organizer": "Horizonte Produções",
        "location": "Arena Central, São Paulo",
        "dtCreated": "2026-10-01T12:00:00-03:00",
        "dtExpiration": "2027-03-20T20:00:00-03:00",
        "dtEvent": "2027-03-20T20:00:00-03:00",
        "types": [
            {"name": "Pista", "price": 350.00},
            {"name": "Camarote", "price": 900.00}
        ]
    }'::jsonb,
    NULL,
    240
),
(
    '{
        "name": "Noite do Stand-up Nacional",
        "description": "Seis comediantes, um palco e muita risada em uma noite de humor sem filtro.",
        "organizer": "Cia. do Riso",
        "location": "Teatro Municipal, Rio de Janeiro",
        "dtCreated": "2026-10-05T12:00:00-03:00",
        "dtExpiration": "2027-04-10T21:00:00-03:00",
        "dtEvent": "2027-04-10T21:00:00-03:00",
        "types": [
            {"name": "Plateia", "price": 120.00},
            {"name": "Mesa VIP", "price": 480.00}
        ]
    }'::jsonb,
    NULL,
    6
),
(
    '{
        "name": "Oficina de Fotografia Urbana",
        "description": "Aprenda composição, luz natural e edição caminhando pelo centro da cidade com fotógrafos profissionais.",
        "organizer": "Olhar Coletivo",
        "location": "Espaço Criativo, Curitiba",
        "dtCreated": "2026-10-12T12:00:00-03:00",
        "dtExpiration": "2027-05-08T09:00:00-03:00",
        "dtEvent": "2027-05-08T09:00:00-03:00",
        "types": [
            {"name": "Ingresso único", "price": 200.00}
        ]
    }'::jsonb,
    NULL,
    30
),
(
    '{
        "name": "Feira Gastronômica Sabores do Brasil",
        "description": "Mais de quarenta expositores com pratos regionais, show ao vivo e área infantil.",
        "organizer": "Mesa Brasil Eventos",
        "location": "Pavilhão das Nações, Salvador",
        "dtCreated": "2026-10-20T12:00:00-03:00",
        "dtExpiration": "2027-06-12T11:00:00-03:00",
        "dtEvent": "2027-06-12T11:00:00-03:00",
        "types": [
            {"name": "Entrada", "price": 60.00},
            {"name": "Degustação", "price": 180.00}
        ]
    }'::jsonb,
    NULL,
    500
),
(
    '{
        "name": "Dev Summit Floripa",
        "description": "Um dia de palestras e workshops sobre arquitetura de software, nuvem e dados.",
        "organizer": "Comunidade Dev Sul",
        "location": "Centro de Convenções, Florianópolis",
        "dtCreated": "2026-11-02T12:00:00-03:00",
        "dtExpiration": "2027-07-24T08:30:00-03:00",
        "dtEvent": "2027-07-24T08:30:00-03:00",
        "types": [
            {"name": "Padrão", "price": 280.00},
            {"name": "Premium", "price": 620.00}
        ]
    }'::jsonb,
    NULL,
    120
);

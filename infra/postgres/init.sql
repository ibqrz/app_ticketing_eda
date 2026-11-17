CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    venue TEXT NOT NULL,
    city TEXT NOT NULL,
    starts_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE ticket_types (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events (id),
    name TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price > 0)
);

CREATE TABLE orders (
    id UUID PRIMARY KEY,
    ticket_type_id INTEGER NOT NULL REFERENCES ticket_types (id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    total NUMERIC(10, 2) NOT NULL,
    customer_name TEXT NOT NULL,
    customer_email TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE stock_items (
    ticket_type_id INTEGER PRIMARY KEY REFERENCES ticket_types (id),
    available INTEGER NOT NULL CHECK (available >= 0)
);

CREATE TABLE stock_reservations (
    order_id UUID PRIMARY KEY,
    ticket_type_id INTEGER NOT NULL,
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

CREATE VIEW order_overview AS
SELECT
    o.id,
    o.quantity,
    o.total,
    o.created_at,
    e.title AS event_title,
    t.name AS ticket_name,
    p.reason,
    p.processed_by,
    CASE
        WHEN p.status = 'APPROVED' THEN 'CONFIRMED'
        WHEN p.status = 'REFUSED' THEN 'REFUSED'
        ELSE 'PROCESSING'
    END AS status
FROM orders o
JOIN ticket_types t ON t.id = o.ticket_type_id
JOIN events e ON e.id = t.event_id
LEFT JOIN payments p ON p.order_id = o.id;

INSERT INTO events (title, venue, city, starts_at) VALUES
    ('Festival Horizonte de Rock', 'Arena Central', 'São Paulo', '2027-03-20 20:00:00-03'),
    ('Noite do Stand-up Nacional', 'Teatro Municipal', 'Rio de Janeiro', '2027-04-10 21:00:00-03'),
    ('Oficina de Fotografia Urbana', 'Espaço Criativo', 'Curitiba', '2027-05-08 09:00:00-03');

INSERT INTO ticket_types (event_id, name, price) VALUES
    (1, 'Pista', 350.00),
    (1, 'Camarote', 900.00),
    (2, 'Plateia', 120.00),
    (2, 'Mesa VIP', 480.00),
    (3, 'Ingresso único', 200.00);

INSERT INTO stock_items (ticket_type_id, available) VALUES
    (1, 200),
    (2, 40),
    (3, 150),
    (4, 6),
    (5, 30);

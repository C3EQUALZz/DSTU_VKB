FROM postgres:17.4-alpine

# Копируем SSL-сертификаты
COPY certs/ca.pem /var/lib/postgresql/ca.pem
COPY certs/server-cert.pem /var/lib/postgresql/server-cert.pem
COPY certs/server-key.pem /var/lib/postgresql/server-key.pem

# Устанавливаем правильные права
RUN chown postgres:postgres /var/lib/postgresql/server-key.pem \
    && chmod 600 /var/lib/postgresql/server-key.pem \
    && chmod 644 /var/lib/postgresql/ca.pem \
    && chmod 644 /var/lib/postgresql/server-cert.pem
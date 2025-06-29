FROM postgres:17.4-alpine

# On Windows root will own the files, and they will have permissions 755
COPY certs/ca.pem /var/lib/postgresql/ca.pem
COPY certs/server-cert.pem /var/lib/postgresql/server-cert.pem
COPY certs/server-key.pem /var/lib/postgresql/server-key.pem

# update the privileges on the .key, no need to touch the .crt
RUN chmod 600 /var/lib/postgresql/server-key.pem
RUN chown postgres:postgres /var/lib/postgresql/server-key.pem
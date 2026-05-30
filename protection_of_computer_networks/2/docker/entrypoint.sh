#!/usr/bin/env bash
set -euo pipefail

# Подменяем backend для iptables на legacy — ufw на bookworm работает стабильнее
# с iptables-legacy, а Docker под Apple Silicon по умолчанию даёт nf_tables.
update-alternatives --set iptables /usr/sbin/iptables-legacy || true
update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy || true

service ssh start
service nginx start

exec sleep infinity

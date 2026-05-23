#!/usr/bin/env bash
# Прогон SonarQube по всем 4 лабам.
#
# Использование:
#   1) just sonar-up                       # поднять SonarQube
#   2) Создать .env в корне с SONAR_TOKEN  # из UI: My Account → Security
#   3) ./scripts/sonar-scan-all.sh         # запустить сканирование
set -euo pipefail

# Загружаем .env, если есть.
if [[ -f .env ]]; then
    set -a
    # shellcheck disable=SC1091
    . .env
    set +a
fi

: "${SONAR_HOST_URL:=http://localhost:9000}"
: "${SONAR_TOKEN:?Установи SONAR_TOKEN в .env или окружении (см. docker/sonarqube/.env.example)}"

if ! command -v sonar-scanner >/dev/null; then
    echo "❌ sonar-scanner не найден. Установи: brew install sonar-scanner (macOS) или https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/scanners/sonarscanner/" >&2
    exit 1
fi

LABS=(lab_01_rsa lab_02_sha256 lab_03_prng lab_04_nist)

# Сначала собираем clippy-отчёт в JSON для всего workspace,
# затем для каждой лабы оставляем только её замечания.
echo "→ Прогоняю cargo clippy --message-format=json --workspace…"
cargo clippy --workspace --message-format=json --all-targets > /tmp/clippy-workspace.json || true

for lab in "${LABS[@]}"; do
    echo ""
    echo "═══════════════════════════════════════"
    echo "  Сканирую $lab"
    echo "═══════════════════════════════════════"

    crate_dir="crates/$lab"
    if [[ ! -d "$crate_dir" ]]; then
        echo "⚠️  $crate_dir не найден, пропускаю."
        continue
    fi

    # Фильтруем clippy-отчёт по конкретному крейту.
    grep "\"$lab\"" /tmp/clippy-workspace.json > "$crate_dir/clippy.json" || true

    (
        cd "$crate_dir"
        sonar-scanner \
            -Dsonar.host.url="$SONAR_HOST_URL" \
            -Dsonar.token="$SONAR_TOKEN"
    )
done

echo ""
echo "✅ Все 4 проекта обработаны. Открой $SONAR_HOST_URL в браузере."

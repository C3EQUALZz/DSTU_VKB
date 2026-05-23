#!/usr/bin/env bash
# Автоматическая настройка SonarQube для лаб 5.
#
# Что делает:
#   1. Ждёт, пока SonarQube ответит api/system/status = UP.
#   2. Меняет пароль admin на $SONAR_ADMIN_PASSWORD (по умолчанию psia-admin-2026).
#   3. Создаёт пользовательский токен `psia-scan`.
#   4. Создаёт 4 проекта: lab_01_rsa, lab_02_sha256, lab_03_prng, lab_04_nist.
#   5. Пишет всё в .env в корне.
#
# Использование:
#   just sonar-up         # один раз поднять контейнеры
#   just sonar-bootstrap  # ← этот скрипт; идемпотентный, можно запускать повторно

set -euo pipefail

SONAR_URL="${SONAR_HOST_URL:-http://localhost:9000}"
ENV_FILE=".env"
PROJECTS=(lab_01_rsa lab_02_sha256 lab_03_prng lab_04_nist)
NEW_PASSWORD="${SONAR_ADMIN_PASSWORD:-psia-admin-2026}"
TOKEN_NAME="psia-scan"

if ! command -v curl >/dev/null; then
    echo "❌ curl не установлен" >&2
    exit 1
fi

# Если в текущем .env уже лежит работающий токен — пропускаем повторную генерацию.
if [[ -f "$ENV_FILE" ]] && grep -q '^SONAR_TOKEN=.\+' "$ENV_FILE"; then
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    if curl -sf -u "$SONAR_TOKEN:" "$SONAR_URL/api/authentication/validate" 2>/dev/null \
        | grep -q '"valid":true'; then
        echo "✓ В $ENV_FILE уже действительный SONAR_TOKEN — пропускаю bootstrap."
        echo "  (Удали .env, чтобы пересоздать.)"
        exit 0
    fi
    echo "⚠️  Существующий SONAR_TOKEN недействителен, пересоздаю."
fi

# 1) Ждём readiness.
echo "→ Жду готовности SonarQube на $SONAR_URL …"
for _ in $(seq 1 90); do
    if curl -sf "$SONAR_URL/api/system/status" 2>/dev/null | grep -q '"status":"UP"'; then
        break
    fi
    sleep 2
done
if ! curl -sf "$SONAR_URL/api/system/status" 2>/dev/null | grep -q '"status":"UP"'; then
    echo "❌ SonarQube не отвечает за 180 секунд." >&2
    echo "   Подними его: just sonar-up" >&2
    exit 1
fi
echo "✓ SonarQube готов"

# 2) Меняем пароль admin'а (HTTP 204 при успехе, 401 если уже не admin/admin).
echo "→ Меняю пароль admin → $NEW_PASSWORD …"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -u "admin:admin" -X POST \
    "$SONAR_URL/api/users/change_password" \
    --data-urlencode "login=admin" \
    --data-urlencode "previousPassword=admin" \
    --data-urlencode "password=$NEW_PASSWORD" || true)
case "$HTTP_CODE" in
    204) echo "✓ Пароль admin сменён.";;
    401|403)
        # Пробуем валидировать с новым паролем — возможно уже сменён.
        if curl -sf -u "admin:$NEW_PASSWORD" "$SONAR_URL/api/authentication/validate" 2>/dev/null \
            | grep -q '"valid":true'; then
            echo "ℹ️  Пароль уже был сменён на $NEW_PASSWORD — продолжаю."
        else
            echo "❌ admin/admin не работает и admin/$NEW_PASSWORD тоже." >&2
            echo "   Возможно, кто-то уже сменил пароль на другое. Удали том sonarqube_data:" >&2
            echo "   docker compose -f docker/sonarqube/compose.yaml down -v" >&2
            exit 1
        fi
        ;;
    *)
        echo "❌ Неожиданный код ответа смены пароля: $HTTP_CODE" >&2
        exit 1
        ;;
esac

AUTH="admin:$NEW_PASSWORD"

# 3) Удаляем существующий одноимённый токен, если был (нельзя пересоздать поверх).
curl -sS -u "$AUTH" -X POST "$SONAR_URL/api/user_tokens/revoke" \
    --data-urlencode "name=$TOKEN_NAME" >/dev/null 2>&1 || true

# 4) Генерируем новый токен.
echo "→ Генерирую токен $TOKEN_NAME …"
TOKEN_JSON=$(curl -sS -u "$AUTH" -X POST "$SONAR_URL/api/user_tokens/generate" \
    --data-urlencode "name=$TOKEN_NAME")
# Достаём поле "token" без jq.
TOKEN=$(printf '%s' "$TOKEN_JSON" \
    | sed -n 's/.*"token":"\([^"]*\)".*/\1/p')
if [[ -z "$TOKEN" ]]; then
    echo "❌ Не удалось распарсить ответ /api/user_tokens/generate: $TOKEN_JSON" >&2
    exit 1
fi
echo "✓ Токен получен."

# 5) Создаём проекты (идемпотентно — повторный create даёт 400, его игнорируем).
for KEY in "${PROJECTS[@]}"; do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -u "$AUTH" -X POST \
        "$SONAR_URL/api/projects/create" \
        --data-urlencode "name=$KEY" \
        --data-urlencode "project=$KEY" || true)
    case "$HTTP_CODE" in
        200) echo "✓ Проект создан: $KEY";;
        400) echo "ℹ️  Проект $KEY уже существует — пропускаю.";;
        *) echo "⚠️  Не удалось создать $KEY (HTTP $HTTP_CODE)";;
    esac
done

# 6) Пишем .env.
cat > "$ENV_FILE" <<EOF
# Сгенерировано scripts/sonar-bootstrap.sh — не редактируй вручную.
SONAR_HOST_URL=$SONAR_URL
SONAR_TOKEN=$TOKEN
SONAR_ADMIN_PASSWORD=$NEW_PASSWORD
EOF
chmod 600 "$ENV_FILE"

echo ""
echo "════════════════════════════════════════════════════════"
echo "✅ Готово. SonarQube настроен для лаб 5."
echo ""
echo "  URL:          $SONAR_URL"
echo "  Логин/пароль: admin / $NEW_PASSWORD"
echo "  Токен:        записан в $ENV_FILE (chmod 600)"
echo "  Проекты:      ${PROJECTS[*]}"
echo ""
echo "Дальше:  just sonar-scan-all"
echo "════════════════════════════════════════════════════════"

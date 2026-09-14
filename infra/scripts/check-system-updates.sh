#!/usr/bin/env bash

set -u

EXIT_CODE=0

echo "=========================================="
echo " CentopeIA - System Update Check"
echo "=========================================="
echo
echo "Host:       $(hostname)"
echo "Data:       $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "Kernel:     $(uname -r)"
echo

echo "=== SISTEMA ==="
grep -E '^(PRETTY_NAME|VERSION_ID)=' /etc/os-release
echo

echo "=== UPDATES DISPONÍVEIS ==="
UPDATES="$(apt list --upgradable 2>/dev/null | tail -n +2)"

if [ -n "$UPDATES" ]; then
    echo "$UPDATES"
else
    echo "Nenhuma atualização disponível."
fi
echo

echo "=== REBOOT ==="
if [ -f /var/run/reboot-required ]; then
    echo "ATENÇÃO: reboot necessário."
    cat /var/run/reboot-required

    if [ -f /var/run/reboot-required.pkgs ]; then
        echo
        echo "Pacotes relacionados:"
        cat /var/run/reboot-required.pkgs
    fi
else
    echo "Nenhum reboot necessário."
fi
echo

echo "=== DISCO ==="
df -h /
echo

echo "=== DOCKER ==="
if command -v docker >/dev/null 2>&1; then
    docker version --format \
      'Client: {{.Client.Version}} | Server: {{.Server.Version}}' 2>/dev/null \
      || {
          echo "ATENÇÃO: Docker instalado, mas não foi possível consultar o daemon."
          EXIT_CODE=1
      }

    echo
    echo "Containers:"
    docker ps --format \
      'table {{.Names}}\t{{.Image}}\t{{.Status}}' 2>/dev/null \
      || {
          echo "ATENÇÃO: não foi possível consultar os containers."
          EXIT_CODE=1
      }
else
    echo "ATENÇÃO: Docker não encontrado."
    EXIT_CODE=1
fi
echo

echo "=== CENTOPEIA HEALTH ==="
if command -v curl >/dev/null 2>&1; then
    if curl --fail --silent --show-error \
        --max-time 10 \
        http://localhost:8000/health; then
        echo
        echo "Health check concluído com sucesso."
    else
        echo
        echo "ATENÇÃO: health check da CentopeIA falhou."
        EXIT_CODE=1
    fi
else
    echo "ATENÇÃO: curl não encontrado."
    EXIT_CODE=1
fi

echo
echo "=========================================="
echo " Verificação concluída"
echo " Exit code: $EXIT_CODE"
echo "=========================================="

exit "$EXIT_CODE"

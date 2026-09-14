#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="/var/log/centopeia"
TIMESTAMP="$(date '+%Y%m%d_%H%M%S')"
LOG_FILE="${LOG_DIR}/system-update-${TIMESTAMP}.log"

if [ "${EUID}" -ne 0 ]; then
    echo "Este script precisa ser executado com sudo/root."
    echo
    echo "Use:"
    echo "  sudo $0"
    exit 1
fi

mkdir -p "$LOG_DIR"

exec > >(tee -a "$LOG_FILE") 2>&1

echo "=========================================="
echo " CentopeIA - System Update"
echo "=========================================="
echo
echo "Host:       $(hostname)"
echo "Data:       $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "Kernel:     $(uname -r)"
echo "Log:        $LOG_FILE"
echo

echo "=== PRE-CHECK ==="

if [ -x "${SCRIPT_DIR}/check-system-updates.sh" ]; then
    sudo -u "${SUDO_USER:-root}" \
        "${SCRIPT_DIR}/check-system-updates.sh" || {
            echo
            echo "ATENÇÃO: o pre-check encontrou problemas."
            echo "A atualização foi cancelada."
            exit 1
        }
else
    echo "ERRO: check-system-updates.sh não encontrado."
    exit 1
fi

echo
echo "=== APT UPDATE ==="
apt update

echo
echo "=== PACOTES DISPONÍVEIS ==="
UPDATES="$(apt list --upgradable 2>/dev/null | tail -n +2)"

if [ -z "$UPDATES" ]; then
    echo "Nenhuma atualização disponível."
    echo
    echo "Nenhuma alteração será realizada."
    exit 0
fi

echo "$UPDATES"

echo
echo "=========================================="
echo " Revise os pacotes acima."
echo "=========================================="
echo

read -r -p "Deseja continuar com a atualização? [y/N]: " RESPONSE

case "$RESPONSE" in
    y|Y|yes|YES|Yes)
        ;;
    *)
        echo "Atualização cancelada pelo operador."
        exit 0
        ;;
esac

echo
echo "=== APT UPGRADE ==="
DEBIAN_FRONTEND=noninteractive apt upgrade -y

echo
echo "=== REBOOT ==="
if [ -f /var/run/reboot-required ]; then
    echo "ATENÇÃO: reboot necessário."

    if [ -f /var/run/reboot-required.pkgs ]; then
        echo
        echo "Pacotes relacionados:"
        cat /var/run/reboot-required.pkgs
    fi
else
    echo "Nenhum reboot necessário."
fi

echo
echo "=== POST-CHECK ==="

if [ -n "${SUDO_USER:-}" ] && [ "${SUDO_USER}" != "root" ]; then
    sudo -u "$SUDO_USER" \
        "${SCRIPT_DIR}/check-system-updates.sh"
else
    "${SCRIPT_DIR}/check-system-updates.sh"
fi

echo
echo "=========================================="
echo " Manutenção concluída"
echo " Log: $LOG_FILE"
echo "=========================================="

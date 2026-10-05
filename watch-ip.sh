#!/bin/bash
# Announces devbox.local on the LAN via mDNS (like avahi on Linux/Raspberry Pi).
# Requires no hostname change — uses macOS native dns-sd.
# Usage: ./watch-ip.sh [interface]   (default: en0)

INTERFACE="${1:-en0}"
CURRENT_IP=""
DNSSD_PID=""

echo "Watching $INTERFACE — will announce devbox.local via mDNS..."

cleanup() {
  [ -n "$DNSSD_PID" ] && kill "$DNSSD_PID" 2>/dev/null
  echo "Stopped."
  exit 0
}
trap cleanup INT TERM

while true; do
  NEW_IP=$(ipconfig getifaddr "$INTERFACE" 2>/dev/null)

  if [ -n "$NEW_IP" ] && [ "$NEW_IP" != "$CURRENT_IP" ]; then
    # Drop previous registration
    [ -n "$DNSSD_PID" ] && kill "$DNSSD_PID" 2>/dev/null

    # Register devbox.local → NEW_IP via mDNS multicast
    dns-sd -P devbox _workstation._tcp local 9 devbox.local "$NEW_IP" > /dev/null 2>&1 &
    DNSSD_PID=$!

    echo "[$(date '+%H:%M:%S')] devbox.local → $NEW_IP  (pid=$DNSSD_PID)"
    CURRENT_IP="$NEW_IP"
  fi

  sleep 30
done

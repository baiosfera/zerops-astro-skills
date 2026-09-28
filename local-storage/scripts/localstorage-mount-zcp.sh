#!/usr/bin/env bash
# ==============================================================================
# Zerops Local Storage Control-Plane Mount Automator (localstorage-mount-zcp.sh)
# Version: 1.0 (Zero-Friction ZCP SSHFS & Remote Kernel Bind Mount Engine)
# ==============================================================================
set -euo pipefail

ACTION="${1:-status}"
HOSTNAME="${2:-localstorage}"
TARGET_MOUNT="/var/www/$HOSTNAME"

usage() {
    echo "Usage: $0 [mount|unmount|status] [storage_hostname]"
    echo "Example: $0 mount localstorage"
    exit 1
}

check_remote() {
    if ! ssh -o BatchMode=yes -o ConnectTimeout=5 "$HOSTNAME" "echo ok" >/dev/null 2>&1; then
        echo "❌ Error: Cannot connect to storage service '$HOSTNAME' via SSH."
        echo "   Ensure '$HOSTNAME' is provisioned and running in this Zerops project."
        exit 1
    fi
}

do_status() {
    echo "============================================================"
    echo "  📦 Local Storage Status: [$HOSTNAME] -> [$TARGET_MOUNT]"
    echo "============================================================"
    
    if mountpoint -q "$TARGET_MOUNT" 2>/dev/null; then
        echo "✓ Control-plane mount: ACTIVE at $TARGET_MOUNT"
        df -h "$TARGET_MOUNT" | awk 'NR==1 || NR==2'
    else
        echo "ℹ️ Control-plane mount: NOT MOUNTED at $TARGET_MOUNT"
    fi

    if ssh -o BatchMode=yes -o ConnectTimeout=5 "$HOSTNAME" "echo ok" >/dev/null 2>&1; then
        echo "✓ Remote SSH connection: REACHABLE"
        local remote_bind
        remote_bind=$(ssh "$HOSTNAME" "mountpoint -q /var/www && echo 'ACTIVE' || echo 'MISSING'")
        echo "✓ Remote /var/www bind mount: $remote_bind"
    else
        echo "⚠️ Remote SSH connection: UNREACHABLE"
    fi
}

do_mount() {
    echo "============================================================"
    echo "  🚀 Mounting Local Storage: [$HOSTNAME] -> [$TARGET_MOUNT]"
    echo "============================================================"
    check_remote

    echo "1. Verifying remote persistent storage on '$HOSTNAME'..."
    ssh "$HOSTNAME" "sudo mkdir -p /var/www /data"

    echo "2. Ensuring remote bind mount (/data <-> /var/www)..."
    ssh "$HOSTNAME" "
        if ! mountpoint -q /var/www; then
            sudo mount --bind /data /var/www
        fi
        if ! grep -q '/data /var/www' /etc/fstab 2>/dev/null; then
            echo '/data /var/www none bind 0 0' | sudo tee -a /etc/fstab >/dev/null
        fi
        sudo chown -R zerops:zerops /var/www /data 2>/dev/null || true
    "

    echo "3. Preparing local mount point '$TARGET_MOUNT'..."
    mkdir -p "$TARGET_MOUNT"

    if mountpoint -q "$TARGET_MOUNT" 2>/dev/null; then
        echo "✓ Already mounted at $TARGET_MOUNT"
    else
        echo "4. Executing SSHFS mount..."
        sshfs -o allow_other,default_permissions,reconnect "$HOSTNAME":/var/www "$TARGET_MOUNT"
        if mountpoint -q "$TARGET_MOUNT"; then
            echo "✅ Successfully mounted $HOSTNAME at $TARGET_MOUNT"
        else
            echo "❌ SSHFS mount failed."
            exit 1
        fi
    fi

    echo "5. Verifying contents:"
    ls -la "$TARGET_MOUNT"
}

do_unmount() {
    echo "============================================================"
    echo "  🧹 Unmounting Local Storage: [$TARGET_MOUNT]"
    echo "============================================================"
    if mountpoint -q "$TARGET_MOUNT" 2>/dev/null; then
        fusermount3 -u "$TARGET_MOUNT" 2>/dev/null || fusermount3 -uz "$TARGET_MOUNT"
        echo "✅ Successfully unmounted $TARGET_MOUNT"
    else
        echo "ℹ️ $TARGET_MOUNT is not a mount point."
    fi
}

case "$ACTION" in
    mount)
        do_mount
        ;;
    unmount|umount)
        do_unmount
        ;;
    status)
        do_status
        ;;
    *)
        usage
        ;;
esac

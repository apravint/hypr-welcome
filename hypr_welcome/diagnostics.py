"""
Hypr-Welcome Hardware & Compositor Diagnostics
"""

import subprocess
import shutil

def run_cmd(cmd: str) -> str:
    try:
        return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "Unknown"

def get_system_diagnostics():
    cpu = run_cmd("lscpu | grep 'Model name' | cut -d: -f2 | xargs") or "Generic x86_64"
    gpu = run_cmd("lspci | grep -E 'VGA|3D' | cut -d: -f3 | xargs") or "Integrated Graphics"
    mem = run_cmd("free -h | awk '/^Mem:/ {print $2 \" Total / \" $7 \" Available\"}'") or "Available"
    
    # Wayland display count
    monitors = run_cmd("hyprctl monitors -j | grep -c '\"id\"'") or "1"
    
    # Audio daemon
    pipewire = "Active (PipeWire)" if shutil.which("pipewire") and subprocess.run(["pgrep", "-x", "pipewire"], capture_output=True).returncode == 0 else "Inactive"

    return [
        ("Processor", cpu),
        ("GPU Acceleration", gpu),
        ("System Memory", mem),
        ("Active Displays", f"{monitors} Connected Monitor(s)"),
        ("Audio Subsystem", pipewire),
        ("Wayland Compositor", "Hyprland (Native Wayland)"),
    ]

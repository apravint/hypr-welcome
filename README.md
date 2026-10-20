<div align="center">

# 🚀 hypr-welcome

**Aesthetic First-Boot Onboarding Guide & Hardware Diagnostics Dashboard for Hyprland**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Compositor: Hyprland](https://img.shields.io/badge/Compositor-Hyprland%200.56%2B-cyan.svg)](https://hyprland.org)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)

<p align="center">
  <b>A plug-and-play visual onboarding dashboard that eliminates the steep learning curve for new Hyprland users.</b>
</p>

</div>

---

## ⚡ The Problem

Hyprland and dynamic tiling window managers are famously challenging for newcomers. New users are often dumped into an empty black screen with no visual cues on what keybindings to press, whether their GPU is accelerating Wayland properly, or how to launch apps.

**`hypr-welcome` solves this with an interactive first-boot onboarding dashboard.**

---

## 📸 Features

* **⌨️ Visual Keybinding Cheat Sheet:** Elegant card grid displaying core shortcuts (`Super+Enter`, `Super+Space`, `Super+Q`, `Super+F`, workspaces, floating toggles).
* **⚡ Automated Hardware Diagnostics:** Live detection of CPU architecture, GPU 3D acceleration, active Wayland displays, and PipeWire audio server state.
* **🎯 First-Boot State Tracking:** Add 1 line to your `hyprland.conf`; `hypr-welcome` only opens on first login until the user clicks "Complete Setup".
* **🎨 Modern Dark Aesthetic:** Built with PyGObject (GTK 3) featuring an obsidian background (`#0b0d13`), cyan accents (`#00f0ff`), and JetBrains Mono badges.

---

## 🚀 Quickstart

### 1. Installation

```bash
pip install hypr-welcome
```

Make sure GTK 3 PyGObject runtime is installed:
```bash
# Ubuntu / Debian
sudo apt install python3-gi gir1.2-gtk-3.0

# Arch Linux
sudo pacman -S python-gobject gtk3

# Fedora
sudo dnf install python3-gobject gtk3
```

### 2. Integration with `hyprland.conf`

Add this single line to your `~/.config/hypr/hyprland.conf`:
```ini
# First-Boot Interactive Onboarding Guide
exec-once = hypr-welcome --first-boot-only
```

Once the user clicks **"Complete Setup & Launch Desktop"**, it creates `~/.local/state/hypr-welcome/.onboarded` and won't trigger on subsequent logins.

To test or launch anytime:
```bash
hypr-welcome
```

To reset the onboarding state for testing:
```bash
hypr-welcome --reset
```

---

## 🧪 Testing

```bash
python -m unittest discover -s tests
```

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details. Created by [Ayyappa Pravin (@apravint)](https://github.com/apravint).

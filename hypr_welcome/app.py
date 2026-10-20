"""
Hypr-Welcome GTK Application
"""

import sys
import os
import subprocess
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from .diagnostics import get_system_diagnostics

ONBOARDED_FLAG = os.path.expanduser("~/.local/state/hypr-welcome/.onboarded")

CSS = b"""
* {
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
}

window {
    background-color: #0b0d13;
}

.header-title {
    font-size: 26px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 4px;
}

.header-sub {
    font-size: 14px;
    color: #94a3b8;
    margin-bottom: 12px;
}

.badge {
    background-color: rgba(0, 240, 255, 0.15);
    color: #00f0ff;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 4px;
    border: 1px solid rgba(0, 240, 255, 0.3);
}

.card {
    background-color: #131722;
    border: 1px solid #1e2538;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 4px 6px;
}

.shortcut-key {
    background-color: #1e293b;
    color: #00f0ff;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 6px;
    border: 1px solid #334155;
}

.shortcut-desc {
    font-size: 13px;
    color: #e2e8f0;
    font-weight: 500;
}

.btn-primary {
    background: linear-gradient(135deg, #00f0ff 0%, #0080ff 100%);
    color: #000000;
    font-weight: 700;
    font-size: 14px;
    border-radius: 6px;
    border: none;
    padding: 10px 24px;
}

.btn-primary:hover {
    background: linear-gradient(135deg, #33f3ff 0%, #3399ff 100%);
}
"""

class HyprWelcomeWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Welcome to Hyprland")
        self.set_default_size(760, 520)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)

        # Header
        header = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        header.set_margin_top(24)
        header.set_margin_bottom(12)
        header.set_margin_start(28)
        header.set_margin_end(28)

        badge_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        badge = Gtk.Label(label="HYPRLAND COMPOSITOR ONBOARDING")
        badge.get_style_context().add_class("badge")
        badge_box.pack_start(badge, False, False, 0)
        header.pack_start(badge_box, False, False, 0)

        title = Gtk.Label(label="Welcome to your Wayland Desktop")
        title.get_style_context().add_class("header-title")
        title.set_xalign(0)
        header.pack_start(title, False, False, 0)

        sub = Gtk.Label(label="Smooth dynamic tiling, GPU hardware acceleration & keybinding cheat sheet")
        sub.get_style_context().add_class("header-sub")
        sub.set_xalign(0)
        header.pack_start(sub, False, False, 0)

        main_box.pack_start(header, False, False, 0)

        # Tabs
        notebook = Gtk.Notebook()
        notebook.set_margin_start(24)
        notebook.set_margin_end(24)
        notebook.set_margin_bottom(16)
        main_box.pack_start(notebook, True, True, 0)

        notebook.append_page(self.create_shortcuts_tab(), Gtk.Label(label="⌨️ Keybindings"))
        notebook.append_page(self.create_diagnostics_tab(), Gtk.Label(label="⚡ System Audit"))

        # Footer
        footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        footer.set_margin_start(28)
        footer.set_margin_end(28)
        footer.set_margin_bottom(20)

        btn_finish = Gtk.Button(label="Complete Setup & Launch Desktop")
        btn_finish.get_style_context().add_class("btn-primary")
        btn_finish.connect("clicked", self.on_finish_clicked)
        footer.pack_end(btn_finish, False, False, 0)

        main_box.pack_start(footer, False, False, 0)

    def create_shortcuts_tab(self):
        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_margin_top(8)
        vbox.set_margin_bottom(8)

        shortcuts = [
            ("Super + Enter", "Spawn Terminal Emulator"),
            ("Super + Space", "Open Application Launcher (Wofi / Rofi)"),
            ("Super + Q", "Close / Kill Active Window"),
            ("Super + F", "Toggle Active Window Fullscreen"),
            ("Super + V", "Toggle Floating Window State"),
            ("Super + 1..9", "Switch to Workspace 1 through 9"),
            ("Super + Shift + 1..9", "Move Active Window to Workspace 1 through 9"),
            ("Super + Mouse Drag", "Move / Resize Floating Window"),
            ("Super + M", "Exit / Log Out of Hyprland Session"),
        ]

        for key, desc in shortcuts:
            card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
            card.get_style_context().add_class("card")
            
            k_lbl = Gtk.Label(label=key)
            k_lbl.get_style_context().add_class("shortcut-key")
            card.pack_start(k_lbl, False, False, 0)

            d_lbl = Gtk.Label(label=desc)
            d_lbl.get_style_context().add_class("shortcut-desc")
            d_lbl.set_xalign(0)
            card.pack_start(d_lbl, True, True, 0)

            vbox.pack_start(card, False, False, 0)

        scroller.add(vbox)
        return scroller

    def create_diagnostics_tab(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox.set_margin_top(12)
        vbox.set_margin_start(8)
        vbox.set_margin_end(8)

        diag_items = get_system_diagnostics()

        for label, val in diag_items:
            card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            card.get_style_context().add_class("card")

            lbl = Gtk.Label(label=label)
            lbl.get_style_context().add_class("shortcut-key")
            card.pack_start(lbl, False, False, 0)

            v_lbl = Gtk.Label(label=val)
            v_lbl.get_style_context().add_class("shortcut-desc")
            v_lbl.set_xalign(0)
            card.pack_start(v_lbl, True, True, 0)

            vbox.pack_start(card, False, False, 0)

        return vbox

    def on_finish_clicked(self, widget):
        os.makedirs(os.path.dirname(ONBOARDED_FLAG), exist_ok=True)
        with open(ONBOARDED_FLAG, "w") as f:
            f.write("1\n")
        self.destroy()

def run_app():
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(CSS)
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    app = HyprWelcomeWindow()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

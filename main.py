import json
import psutil
import re
import signal
import sys
import time

from pypresence import Presence
from types import FrameType
from typing import TypedDict, cast


class Config(TypedDict):
    blacklist: list[str]
    overrides: dict[str, str]


# === CONFIG ===
CONFIG_PATH = "config.json"
SCAN_INTERVAL = 5  # seconds
DISCORD_CLIENT_ID = "1371226484022317127"

# === LOAD CONFIG ===
with open(CONFIG_PATH) as f:
    cfg = cast(Config, json.load(f))

BLACKLIST = set(cfg["blacklist"])

# Normalize override keys to lowercase for case-insensitive matching
OVERRIDES = {key.lower(): value for key, value in cfg.get("overrides", {}).items()}

# === CONNECT TO DISCORD ===
rpc = Presence(DISCORD_CLIENT_ID)
rpc.connect()
print(f"Connected to Discord RPC (Client ID: {DISCORD_CLIENT_ID})")


# Handle termination signals to clear Discord presence
def _clear_and_exit(_signum: int, _frame: FrameType | None):
    rpc.clear()
    sys.exit(0)


_ = signal.signal(signal.SIGTERM, _clear_and_exit)
_ = signal.signal(signal.SIGINT, _clear_and_exit)


def clean_name(path: str) -> str:
    """
    Normalize Windows-style and Unix-style paths, strip ".exe",
    filter out blacklisted names, apply overrides for abbreviations,
    and auto-split CamelCase names.
    """
    if not path:
        return ""
    # Normalize Windows backslashes to forward slashes
    path_norm = path.replace("\\\\", "/").replace("\\", "/")
    # Extract the filename component (preserve original case)
    filename = path_norm.rsplit("/", 1)[-1]
    filename_lower = filename.lower()
    # Only consider .exe files
    if not filename_lower.endswith(".exe"):
        return ""
    # Strip the .exe suffix
    base_orig = filename[:-4]  # original case
    base_lower = filename_lower[:-4]  # lowercase for checks
    # Remove Unreal Engine build suffixes like "-Win64-Shipping"
    base_lower = re.sub(r"-(win(?:32|64)-shipping)$", "", base_lower)
    base_orig = re.sub(r"-(Win(?:32|64)-Shipping)$", "", base_orig)
    # Blacklist check
    if base_lower in BLACKLIST:
        return ""
    # Overrides for known abbreviations
    if base_lower in OVERRIDES:
        return OVERRIDES[base_lower]
    # Auto-split CamelCase (e.g., "TheMessenger" -> "The Messenger")
    # Only split at lowercase->uppercase boundaries to avoid breaking all-caps names
    split_name = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", base_orig)
    return split_name


def scan_for_game() -> str:
    for proc in psutil.process_iter(["exe", "cmdline"]):
        try:
            exe_path = proc.info.get("exe") or ""
            cmdline: list[str] = proc.info.get("cmdline") or []
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

        # First, check the executable path itself
        name = clean_name(exe_path)
        if name:
            return name

        # Next, scan any ".exe" entries in the command-line args
        for arg in cmdline:
            name = clean_name(arg)
            if name:
                return name

    return ""


def main():
    print("Starting main loop...")
    last = None
    while True:
        game = scan_for_game()
        if game != last:
            last = game
            if game:
                print(f"→ Detected game: {game}")
                rpc.update(details=game, start=int(time.time()))
            else:
                print("→ No game detected, clearing presence")
                rpc.clear()
        time.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    main()

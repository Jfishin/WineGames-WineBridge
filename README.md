
# WineGames - WineBridge 

[![Wine-Bridge-icon.png](https://i.postimg.cc/d7PLcdf7/pic.png)](https://postimg.cc/d7PLcdf7)

A lightweight macOS status-menu app that detects Windows games launched via Wine and automatically updates your Discord Rich Presence with the current game. Buillt with Python and bundled with [Platypus](https://github.com/sveinbjornt/Platypus)

---

## Quick Start

- **Install Homebrew**  
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```
- **Install Python via Homebrew**  
  ```bash
  brew install python
  ```

1. **Download** the latest ZIP from GitHub Releases.
2. **Unzip** and **double-click** `WineBridge.app` to launch it.
3. Click **Start** in the menu bar icon.
4. 🎮 Launch a Windows game via Wine—your Discord status will update automatically.
5. Click **Stop**, then **Quit** when you’re done.

> **Note:** Quitting the app without stopping will leave the scanner running. Always **Stop** first.

---

## How it Works

WineGames-WineBridge works by first looking for processes on your system **ONLY** with the .exe process. It then goes through the blacklist and whats left is hopefully the game process name. It strips out .exe and -Win64-Shipping (for unreal engine games). It then sends the clean game name to the native Discord RPC via pypresense. The scripts were bundled with Platypus for users to just download and have a nifty little menu bar app. 

## Extra Configuration

You may run into unwanted processes being sent to Discord, or have a abreviated gamename.exe

1. **Right-click** on `WineBridge.app` and choose **Show Package Contents**.
2. Navigate to `Contents/Resources/config.json` and open it in your editor of choice (TextEdit, VS Code, etc.).
3. Edit the JSON to suit your setup:
- Blacklist is for processes you **don't** want being sent to discord.
- Ovverrides is for abreviated game names. (example hl2.exe is Half Life 2, also note you dont need to put in .exe into the config.)
   ```json
   {
     "blacklist": [
       "wine",
       "explorer",
       "steam"
     ],
     "overrides": {
       "hl2": "Half Life 2",
       "precinct": "The Precinct",
	   "d2": " Diablo 2 Ressurrected"
     }
   }
   ```
4. Make sure to **save** the Config file, then in the menu bar app click **Stop**, then **Start** again to apply changes.

---


[![Screenshot-2025-05-11-at-4-45-23-PM.png](https://i.postimg.cc/sDFxPPV4/Screenshot-2025-05-11-at-4-45-23-PM.png)](https://postimg.cc/9zpcC7wD)

I am not a developer, i just vibe coded this up with chatgpt. If there is any questions best way to contact me is in the [Mac Gaming Discord](https://discord.gg/JKxywARX) @Jfishin

Enjoy Discord status updates for your Wine games on macOS!!
---

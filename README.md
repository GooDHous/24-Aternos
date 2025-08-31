![Header](/IMG/1.png)
<a href="https://github.com/GooDHous/24-Aternos-ReWORKED/"><img src="https://badgen.net/github/stars/GooDHous/24-Aternos-ReWORKED/" alt="GitHub stars"/></a>
<a href="https://github.com/GooDHous/24-Aternos-ReWORKED/"><img src="https://badgen.net/github/watchers/GooDHous/24-Aternos-ReWORKED/" alt="GitHub watchers"/></a>
<a href="https://github.com/GooDHous/24-Aternos-ReWORKED/"><img src="https://badgen.net/github/forks/GooDHous/24-Aternos-ReWORKED/s" alt="GitHub forks"/></a>

# `24 Aternos Reworked`
### This is a bot that does not allow your minecraft server to shut down on the [Aternos](https://aternos.org) hosting.
##### The bot is fully configurable, controlled in a game chat on the server.

## `creator's contacts`
- [Discord](https://discord.gg/PAm52zgFAF)


## `translations`
| <sub>EN</sub> [English](README.md) | <sub>RU</sub> [Русский](README_RU.md) |
|-------------------------|----------------------------|

## `Disclaimer`
> This bot is made for educational purposes and does not encourage you to use it. You are solely responsible for your server!

 - You can use the source code in your projects (only preferably provide a link to me ;) )

## `Supported OS`

 * Windows ✅
 * Linux ✅
 * Mac ✅

## `Features`

 * Supports Minecraft 1.8, 1.9, 1.10, 1.11, 1.12, 1.13, 1.14, 1.15, 1.16, 1.17, 1.18, 1.19, 1.20 and 1.21.
 * Anti-AFK
 * chat control
 * auto respawn
 * auto reconect
 * GUI (*python*)

# `Installation`

* Download last [Release](https://github.com/GooDHous/24-Aternos-ReWORKED/releases/latest)


 * [Python](https://www.python.org) 3.X
 * First install [Node.js](https://nodejs.dev)

```bash
pip install javascript
```
## Or

```bash
pip install -r requirements.txt
```

## And

```bash
npm install mineflayer
```

# `Usage`

### Python

 * 1. edit config.ini
 * 2. py main.py
 * 3. use GUI

### Configuration File

```ini
[server]
host=127.0.0.1
port=25565
chat=local

[bot]
name=GooDHous
register=/login reg123 reg123
login=/login reg123
language=en_US

[command]
position=;pos
start=;start
stop=;stop
```

---

**`[server]` Section**
*   **`host=`**
    *   **Description:** The IP address of the server.
    *   **Example:** `127.0.0.1` (local machine), `mc.example.com` (domain), `192.168.1.10` (local network IP).

*   **`port=`**
    *   **Description:** The port of the server.
    *   **Example:** `25565` (default Minecraft server port).

*   **`chat=`**
    *   **Description:** An optional parameter (defaults to `local` if missing). Determines whether to add a `!` prefix before the bot's chat commands.
    *   **`local`:** Use this if your server does **not** have a plugin that separates local and global chat . No prefix is added.
    *   **`global`:** Use this if your server **has** such a plugin. The prefix `!` will be added before the bot's messages to send them to the global chat.
    *   *This parameter is optional and can be omitted or left empty.*

**`[bot]` Section**
*   **`name=`**
    *   **Description:** The bot's username (nickname/minecraft account name).

*   **`register=`**
    *   **Description:** An optional parameter. Executes a registration command when the bot joins the server (e.g., `/reg password123 password123` or `/register pass123`).
    *   *This parameter is optional and can be omitted or left empty.*

*   **`login=`**
    *   **Description:** An optional parameter. Executes a login command when the bot joins the server (e.g., `/login password123`).
    *   *This parameter is optional and can be omitted or left empty.*

*   **`language=`**
    *   **Description:** An optional parameter. Select ui language (en_US, ru_RU)  

**`[command]` Section**
*   **`position=`**
    *   **Description:** The in-game command the bot will listen for to trigger its "get position" function.
    *   **Example:** `;pos` means the bot will react when a player types `;pos` in chat.

*   **`start=`**
    *   **Description:** The in-game command to start the anti afk.
    *   **Example:** `;start`

*   **`stop=`**
    *   **Description:** The in-game command to stop the anti afk.
    *   **Example:** `;stop`

##### When you turn off the computer, the bot will also turn off!

![GUI](/IMG/3.png)

### Standard bot management via game chat

 * ;pos - bot position in the world (*python*)
 * ;start - enable AntiAFK
 * ;stop - disable AntiAFK

# `Thanks`

- [mineflayer](https://github.com/PrismarineJS/mineflayer)

# `Support me`

### Put a ⭐ and Fork if this bot turned out to be useful to you
### For support me just join our discord server
- [Discord](https://discord.gg/PAm52zgFAF)









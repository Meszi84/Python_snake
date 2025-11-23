# Python_snake
-----

````markdown
# 🐍 Python Snake Game

Egy klasszikus Snake játék modern köntösben, Python és Pygame használatával. A projekt célja a retro élmény felújítása extra funkciókkal, mint a hangeffektek, a helyi toplista és a modern irányítás.

## ✨ Funkciók

* **🏆 Toplista Rendszer:** A játék elmenti a legjobb 10 eredményt egy helyi `highscores.json` fájlba. A játék végén megtekinthető a ranglista.
* **🔊 Hangeffektek:** Egyedi hangok a játék indításához, az evéshez és a "Game Over" eseményhez.
* **🎮 Modern Irányítás:** Kényelmes **WASD** billentyűkiosztás a nyilak helyett.
* **👤 Játékos Profil:** Név megadása indításkor, ami megjelenik a toplistán.
* **🔄 Wrap-Around Pálya:** A kígyó nem hal meg a falnál, hanem átjön a túloldalon.
* **💾 Perzisztens Adatok:** A pontszámok megmaradnak a program újraindítása után is.

## 🕹️ Irányítás

| Billentyű | Funkció |
| :--- | :--- |
| **W / A / S / D** | A kígyó mozgatása (Fel / Balra / Le / Jobbra) |
| **SPACE** | Játék indítása / Újrakezdés |
| **ENTER** | Név véglegesítése |
| **ESC** | Kilépés |

## 🛠️ Telepítés és Futtatás

A játék futtatásához Python 3.x szükséges.

1. **Klónozd le a repót (vagy töltsd le a fájlokat):**
   ```bash
   git clone [https://github.com/felhasznaloneved/snake-game.git](https://github.com/felhasznaloneved/snake-game.git)
   cd snake-game
````

2.  **Telepítsd a függőségeket:**

    ```bash
    pip install pygame
    ```

3.  **Indítsd el a játékot:**

    ```bash
    python snake_game.py
    ```

## 📦 Csomagolás .EXE fájlba (Windows)

Ha önálló, hordozható alkalmazást szeretnél készíteni (ami tartalmazza a hangokat és az ikont is), használd a **PyInstaller**-t.

### 1\. PyInstaller telepítése:

```bash
pip install pyinstaller
```

### 2\. A build parancs futtatása:

Ez a parancs egyetlen fájlba (`--onefile`) csomagolja a játékot, elrejti a konzolt (`--noconsole`), és beleégeti a `sounds` mappát az alkalmazásba.

*(Feltételezve, hogy van egy `snake.ico` ikonod és egy `sounds` mappád)*

```bash
python -m PyInstaller --onefile --noconsole --icon=snake.ico --add-data "sounds;sounds" snake_game.py
```

A kész alkalmazást a létrejövő **`dist`** mappában találod.

## 📂 Fájlstruktúra

  * `snake_game.py` - A játék fő kódja.
  * `sounds/` - A hangfájlokat tartalmazó mappa (`start.ogg`, `eat.ogg`, `gameover.ogg`).
  * `highscores.json` - Automatikusan létrejön a pontszámok tárolására.

-----

*Készítette: [Meszi84]*

```

---

### Hogyan használd ezt?

1.  Ha van már GitHub repód, hozz létre benne egy **`README.md`** nevű fájlt.
2.  Másold bele a fenti szöveget.
3.  Ahol látod a `[Meszi84]` vagy `https://github.com/Meszi84/...` részeket, írd át a sajátodra.
4.  Ha nincs ikonod, töröld ki a parancsból a `--icon=snake.ico` részt.

Sok sikert a projekthez a GitHubon! 🚀
```

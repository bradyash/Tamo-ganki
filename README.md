# Tamo-ganki

Tamo-ganki (a.k.a. **AnkiPet – Wandering Sprite**) is a Tamagotchi‑style companion for Anki. An animated sprite lives inside Anki’s main window and reacts to your study habits—answer cards correctly to keep your pet happy and healthy!

---

## Features

- **Animated pet widget** docked in Anki’s main window  
  (idle, walk, and attack animations powered by PyQt6).
- **Persistent stats** stored in your Anki profile:
  - Happiness
  - Hunger
  - Health
  - Study streak
- **Behavior tied to your reviews**  
  - Correct answers (Ease > 1) feed and play with the pet, triggering a brief “attack” animation.  
  - Incorrect answers or missed days neglect the pet, increasing hunger and lowering happiness/health.
- **Automatic daily check-ins** to update streaks and apply penalties for skipped days.

Compatible with Anki versions **2.1.35–2.1.60**.

---

## Installation

1. **Download**
   - Grab the latest release ZIP from this repository or clone/download the project and create a ZIP of its contents (ensure `manifest.json` is at the root of the ZIP).
2. **Install in Anki**
   - Open **Anki → Tools → Add-ons → Install from file…**
   - Select the downloaded ZIP and confirm.
3. **Restart Anki**  
   The pet widget will appear docked on the right side of the main window. You can move or undock it like any standard Anki dock widget.

---

## Usage

- **Review as usual.** Each answer updates the pet’s stats shown under the sprite.
  - *Correct answers* (Good/Hard/Easy) feed and play with the pet.
  - *Incorrect answers* (Again) neglect the pet.
- **Keep your streak.** Opening Anki daily maintains your streak and avoids stat penalties.
- Stats persist across sessions; close Anki and return later without losing progress.

---

## Development / Customization

1. Clone or fork this repository.
2. Modify `pet.py`, `pet_widget.py`, or the `images/` assets.
3. Zip the modified project (including `manifest.json`) and install via Anki’s add-on dialog as described above.

---

## Credits

Created by **Brady Ash**  
If you enjoy Tamo-ganki, consider supporting the author on [Ko-fi](https://ko-fi.com/S6S61KBCPT).

Happy studying—and take good care of your AnkiPet!


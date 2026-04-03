# rosary

`rosary` is a terminal UI application for praying the Holy Rosary step by step. It uses [Textual](https://textual.textualize.io/) for the interface and `bible-api.com` for scripture and translation data.

## Features

- Guided Rosary flow from the opening prayers through the final prayers
- English and Latin prayer modes
- Bible translation selection in English mode
- Automatic mystery-set suggestion based on the current day of the week
- Intentions screen before the Rosary begins
- Scripture passages displayed for each mystery when available
- Fallback translation list if the live translation API is unavailable

## Requirements

- Python 3.13 or newer
- A terminal that can run Textual applications
- Internet access for live scripture lookups and translation fetching

## Installation

### Option 1: using `pip`

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Then run:

```bash
rosary
```

### Option 2: using `uv`

```bash
uv sync
uv run rosary
```

## What the app does

When you start the program, it walks through this flow:

1. **Welcome screen**
   - Choose **English** or **Latin**.
   - In English mode, select a Bible translation from the available list.
   - In Latin mode, the app uses the Latin prayer texts and defaults to the Clementine Vulgate option.

2. **Mystery selection**
   - The app suggests the traditional mystery set for the current weekday:

   | Day | Suggested mysteries |
   | --- | --- |
   | Monday | Joyful |
   | Tuesday | Sorrowful |
   | Wednesday | Glorious |
   | Thursday | Luminous |
   | Friday | Sorrowful |
   | Saturday | Joyful |
   | Sunday | Glorious |

   You can keep the suggested set or choose a different one.

3. **Intentions screen**
   - A short prompt invites you to offer your intentions before beginning.

4. **Guided Rosary screen**
   - Opening prayers:
     - Sign of the Cross
     - Apostles' Creed
     - Our Father
     - three Hail Marys
     - Glory Be
   - Five decades:
     - each mystery announcement includes a description
     - scripture is shown for mysteries with a direct biblical reference
     - the decade prayers are grouped together on one screen
   - Closing prayers:
     - Hail Holy Queen
     - Closing Prayer
     - Sign of the Cross

For mysteries such as the Assumption and Coronation, where the app does not use a direct scripture passage, it displays a short doctrinal note instead.

## Keyboard controls

### Selection screens

- `q` — quit
- `escape` — go back (where available)
- arrow keys / standard Textual navigation — move through options
- `enter` — activate the selected control

### Rosary screen

- `space` or `right arrow` — next step
- `backspace` or `left arrow` — previous step
- `q` — quit
- `r` — pray again after completion

## Project layout

```text
src/rosary/
├── api.py              # bible-api.com client
├── app.py              # top-level Textual app
├── main.py             # CLI entry point
├── mysteries.py        # mystery definitions and weekday suggestion logic
├── prayers.py          # English and Latin prayer texts
└── screens/
    ├── welcome.py
    ├── mystery_select.py
    ├── intentions.py
    └── rosary.py
```

## Notes

- If `bible-api.com` cannot be reached when loading translations, the app falls back to a built-in translation list.
- Scripture text fetches are performed lazily as you move through the mysteries.
- In Latin mode, scripture references are still resolved using the English-form reference strings used by the app.

## License

See `LICENSE`.

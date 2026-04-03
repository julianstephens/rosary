# rosary

`rosary` is a terminal application for praying the Holy Rosary step by step. It guides you through the opening prayers, the five decades, and the closing prayers in a clean Textual interface, with mystery descriptions and scripture references included along the way.

## Features

- Guided Rosary flow from beginning to end
- English and Latin prayer modes
- Bible translation selection in English mode
- Automatic mystery recommendation based on the day of the week
- Intentions prompt before the Rosary begins
- Scripture lookups for mysteries with direct biblical references
- Built-in fallback translation list if the live API is unavailable

## Requirements

- Python 3.13 or newer
- A terminal that supports Textual applications
- Internet access for live translation and scripture fetching

## Installation

### From PyPI

```bash
pip install rosary
```

If you prefer an isolated CLI install:

```bash
pipx install rosary
```

## Quick start

Run the app with:

```bash
rosary
```

You will then:

1. Choose **English** or **Latin**.
2. Select a Bible translation in English mode.
3. Accept the suggested mystery set for the day or choose another one.
4. Offer your intentions.
5. Move through the Rosary one step at a time.

## Mystery schedule

The app suggests the traditional mystery set for the current weekday:

| Day | Mysteries |
| --- | --- |
| Monday | Joyful |
| Tuesday | Sorrowful |
| Wednesday | Glorious |
| Thursday | Luminous |
| Friday | Sorrowful |
| Saturday | Joyful |
| Sunday | Glorious |

You can always override the suggestion from the selection screen.

## Keyboard controls

### Selection screens

- `q` to quit
- `escape` to go back when available
- arrow keys to move through options
- `enter` to confirm a selection

### Rosary screen

- `space` or `right arrow` for the next step
- `backspace` or `left arrow` for the previous step
- `q` to quit
- `r` to start again after completion

## Included prayer flow

The guided flow includes:

- Sign of the Cross
- Apostles' Creed
- Our Father
- three Hail Marys
- Glory Be
- five decades with mystery descriptions
- Hail Holy Queen
- Closing Prayer
- Sign of the Cross

For mysteries such as the Assumption and Coronation, the app shows a doctrinal note when no direct scripture passage is used.

## Development

To work on the project locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Or with `uv`:

```bash
uv sync
uv run rosary
```

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

## License

See `LICENSE`.

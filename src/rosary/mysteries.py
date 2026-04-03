"""Rosary mystery sets and day-of-week suggestion logic."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Mystery:
    name: str
    description: str
    scripture_ref: str  # e.g. "Luke 1:26-38" — passed to bible-api.com


@dataclass(frozen=True)
class MysterySet:
    name: str
    mysteries: tuple[Mystery, ...]


JOYFUL = MysterySet(
    name="Joyful Mysteries",
    mysteries=(
        Mystery(
            name="The Annunciation",
            description="The Angel Gabriel announces to Mary that she will conceive the Son of God.",
            scripture_ref="Luke 1:26-33",
        ),
        Mystery(
            name="The Visitation",
            description="Mary visits her cousin Elizabeth, who is carrying John the Baptist.",
            scripture_ref="Luke 1:39-45",
        ),
        Mystery(
            name="The Nativity",
            description="Jesus is born in Bethlehem.",
            scripture_ref="Luke 2:6-12",
        ),
        Mystery(
            name="The Presentation",
            description="Mary and Joseph present Jesus in the Temple.",
            scripture_ref="Luke 2:22-24",
        ),
        Mystery(
            name="The Finding in the Temple",
            description="The young Jesus is found teaching in the Temple after being lost for three days.",
            scripture_ref="Luke 2:46-49",
        ),
    ),
)

SORROWFUL = MysterySet(
    name="Sorrowful Mysteries",
    mysteries=(
        Mystery(
            name="The Agony in the Garden",
            description="Jesus prays in the Garden of Gethsemane, sweating blood before his Passion.",
            scripture_ref="Luke 22:41-44",
        ),
        Mystery(
            name="The Scourging at the Pillar",
            description="Jesus is bound and brutally scourged by Roman soldiers.",
            scripture_ref="John 19:1",
        ),
        Mystery(
            name="The Crowning with Thorns",
            description="The soldiers place a crown of thorns on Jesus and mock him as king.",
            scripture_ref="John 19:2-3",
        ),
        Mystery(
            name="The Carrying of the Cross",
            description="Jesus carries his cross to Calvary, falling under its weight.",
            scripture_ref="John 19:17",
        ),
        Mystery(
            name="The Crucifixion",
            description="Jesus is nailed to the cross and dies for the sins of all humanity.",
            scripture_ref="John 19:28-30",
        ),
    ),
)

GLORIOUS = MysterySet(
    name="Glorious Mysteries",
    mysteries=(
        Mystery(
            name="The Resurrection",
            description="Jesus rises from the dead on the third day.",
            scripture_ref="John 20:1-2",
        ),
        Mystery(
            name="The Ascension",
            description="Jesus ascends into heaven forty days after the Resurrection.",
            scripture_ref="Acts 1:9-11",
        ),
        Mystery(
            name="The Descent of the Holy Spirit",
            description="The Holy Spirit descends on the Apostles at Pentecost.",
            scripture_ref="Acts 2:1-4",
        ),
        Mystery(
            name="The Assumption of Mary",
            description="At the end of her earthly life, Mary is taken body and soul into heaven.",
            scripture_ref="Revelation 12:1",
        ),
        Mystery(
            name="The Coronation of Mary",
            description="Mary is crowned Queen of Heaven and Earth.",
            scripture_ref="Revelation 12:1",
        ),
    ),
)

LUMINOUS = MysterySet(
    name="Luminous Mysteries",
    mysteries=(
        Mystery(
            name="The Baptism of Jesus",
            description="Jesus is baptized by John in the Jordan, and the Holy Spirit descends as a dove.",
            scripture_ref="Matthew 3:16-17",
        ),
        Mystery(
            name="The Wedding at Cana",
            description="At Mary's intercession, Jesus performs his first miracle — water into wine.",
            scripture_ref="John 2:3-5",
        ),
        Mystery(
            name="The Proclamation of the Kingdom",
            description="Jesus preaches repentance and the coming of the Kingdom of God.",
            scripture_ref="Mark 1:14-15",
        ),
        Mystery(
            name="The Transfiguration",
            description="Jesus is transfigured on Mount Tabor, revealing his divine glory.",
            scripture_ref="Matthew 17:1-2",
        ),
        Mystery(
            name="The Institution of the Eucharist",
            description="At the Last Supper, Jesus institutes the Eucharist.",
            scripture_ref="Luke 22:19-20",
        ),
    ),
)

ALL_SETS: dict[str, MysterySet] = {
    "Joyful": JOYFUL,
    "Sorrowful": SORROWFUL,
    "Glorious": GLORIOUS,
    "Luminous": LUMINOUS,
}

# Traditional day assignments (Luminous added by John Paul II for Thursday)
_DAY_TO_SET: dict[int, str] = {
    0: "Joyful",  # Monday
    1: "Sorrowful",  # Tuesday
    2: "Glorious",  # Wednesday
    3: "Luminous",  # Thursday
    4: "Sorrowful",  # Friday
    5: "Joyful",  # Saturday
    6: "Glorious",  # Sunday
}


def suggest_mystery_set() -> str:
    """Return the key for the traditionally suggested mystery set for today."""
    return _DAY_TO_SET[date.today().weekday()]

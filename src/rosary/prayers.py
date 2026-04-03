"""Static text for all standard Rosary prayers."""

from __future__ import annotations

SIGN_OF_THE_CROSS = """\
In the name of the Father,
and of the Son,
and of the Holy Spirit.
Amen."""

APOSTLES_CREED = """\
I believe in God,
the Father almighty,
Creator of heaven and earth,
and in Jesus Christ, his only Son, our Lord,
who was conceived by the Holy Spirit,
born of the Virgin Mary,
suffered under Pontius Pilate,
was crucified, died and was buried;
he descended into hell;
on the third day he rose again from the dead;
he ascended into heaven,
and is seated at the right hand of God the Father almighty;
from there he will come to judge the living and the dead.

I believe in the Holy Spirit,
the holy catholic Church,
the communion of saints,
the forgiveness of sins,
the resurrection of the body,
and life everlasting.
Amen."""

OUR_FATHER = """\
Our Father, who art in heaven,
hallowed be thy name;
thy kingdom come,
thy will be done
on earth as it is in heaven.
Give us this day our daily bread,
and forgive us our trespasses,
as we forgive those who trespass against us;
and lead us not into temptation,
but deliver us from evil.
Amen."""

HAIL_MARY = """\
Hail Mary, full of grace.
The Lord is with thee.
Blessed art thou amongst women,
and blessed is the fruit of thy womb, Jesus.
Holy Mary, Mother of God,
pray for us sinners,
now and at the hour of our death.
Amen."""

GLORY_BE = """\
Glory be to the Father,
and to the Son,
and to the Holy Spirit,
as it was in the beginning,
is now, and ever shall be,
world without end.
Amen."""

FATIMA_PRAYER = """\
O my Jesus, forgive us our sins,
save us from the fires of hell,
lead all souls to heaven,
especially those in most need of thy mercy.
Amen."""

HAIL_HOLY_QUEEN = """\
Hail, Holy Queen, Mother of Mercy,
our life, our sweetness, and our hope.
To thee do we cry, poor banished children of Eve;
to thee do we send up our sighs,
mourning and weeping in this valley of tears.
Turn, then, most gracious advocate,
thine eyes of mercy toward us;
and after this, our exile,
show unto us the blessed fruit of thy womb, Jesus.
O clement, O loving, O sweet Virgin Mary.

V. Pray for us, O Holy Mother of God.
R. That we may be made worthy of the promises of Christ."""

CLOSING_PRAYER = """\
O God, whose only-begotten Son,
by His life, death, and resurrection,
has purchased for us the rewards of eternal life;
grant, we beseech Thee,
that by meditating upon these mysteries
of the most holy Rosary of the Blessed Virgin Mary,
we may imitate what they contain
and obtain what they promise.
Through the same Christ our Lord.
Amen."""

FINAL_SIGN_OF_THE_CROSS = SIGN_OF_THE_CROSS


# ── Latin prayers ─────────────────────────────────────────────────────────────

SIGN_OF_THE_CROSS_LA = """\
In nomine Patris,
et Filii,
et Spiritus Sancti.
Amen."""

APOSTLES_CREED_LA = """\
Credo in Deum Patrem omnipotentem,
Creatorem caeli et terrae.
Et in Iesum Christum, Filium eius unicum, Dominum nostrum:
qui conceptus est de Spiritu Sancto,
natus ex Maria Virgine,
passus sub Pontio Pilato,
crucifixus, mortuus, et sepultus,
descendit ad inferos,
tertia die resurrexit a mortuis,
ascendit ad caelos,
sedet ad dexteram Dei Patris omnipotentis,
inde venturus est iudicare vivos et mortuos.
Credo in Spiritum Sanctum,
sanctam Ecclesiam catholicam,
sanctorum communionem,
remissionem peccatorum,
carnis resurrectionem,
vitam aeternam.
Amen."""

OUR_FATHER_LA = """\
Pater noster, qui es in caelis,
sanctificetur nomen tuum;
adveniat regnum tuum;
fiat voluntas tua,
sicut in caelo, et in terra.
Panem nostrum cotidianum da nobis hodie;
et dimitte nobis debita nostra,
sicut et nos dimittimus debitoribus nostris;
et ne nos inducas in tentationem;
sed libera nos a malo.
Amen."""

HAIL_MARY_LA = """\
Ave Maria, gratia plena,
Dominus tecum.
Benedicta tu in mulieribus,
et benedictus fructus ventris tui, Iesus.
Sancta Maria, Mater Dei,
ora pro nobis peccatoribus,
nunc et in hora mortis nostrae.
Amen."""

GLORY_BE_LA = """\
Gloria Patri, et Filio,
et Spiritui Sancto.
Sicut erat in principio,
et nunc et semper,
et in saecula saeculorum.
Amen."""

FATIMA_PRAYER_LA = """\
O mi Iesu, dimitte nobis debita nostra,
libera nos ab igne inferni,
perduc in caelum omnes animas,
praesertim eas quae maxime indigent misericordia tua.
Amen."""

HAIL_HOLY_QUEEN_LA = """\
Salve, Regina, Mater misericordiae,
vita, dulcedo, et spes nostra, salve.
Ad te clamamus, exsules filii Hevae.
Ad te suspiramus, gementes et flentes
in hac lacrimarum valle.
Eia ergo, advocata nostra,
illos tuos misericordes oculos ad nos converte.
Et Iesum, benedictum fructum ventris tui,
nobis post hoc exsilium ostende.
O clemens, O pia, O dulcis Virgo Maria.

V. Ora pro nobis, sancta Dei Genitrix.
R. Ut digni efficiamur promissionibus Christi."""

CLOSING_PRAYER_LA = """\
Deus, cuius Unigenitus per vitam, mortem et resurrectionem suam
nobis salutis aeternae praemia comparavit:
concede, quaesumus,
ut haec mysteria sacratissimo beatae Mariae Virginis Rosario colentes,
imitemur quod continent,
et assequamur quod promittunt.
Per eundem Christum Dominum nostrum.
Amen."""


# ── Prayer sets ───────────────────────────────────────────────────────────────

_PRAYERS_EN: dict[str, str] = {
    "sign_of_the_cross": SIGN_OF_THE_CROSS,
    "apostles_creed": APOSTLES_CREED,
    "our_father": OUR_FATHER,
    "hail_mary": HAIL_MARY,
    "glory_be": GLORY_BE,
    "fatima_prayer": FATIMA_PRAYER,
    "hail_holy_queen": HAIL_HOLY_QUEEN,
    "closing_prayer": CLOSING_PRAYER,
}

_PRAYERS_LA: dict[str, str] = {
    "sign_of_the_cross": SIGN_OF_THE_CROSS_LA,
    "apostles_creed": APOSTLES_CREED_LA,
    "our_father": OUR_FATHER_LA,
    "hail_mary": HAIL_MARY_LA,
    "glory_be": GLORY_BE_LA,
    "fatima_prayer": FATIMA_PRAYER_LA,
    "hail_holy_queen": HAIL_HOLY_QUEEN_LA,
    "closing_prayer": CLOSING_PRAYER_LA,
}


def get_prayers(language: str) -> dict[str, str]:
    """Return the prayer dict for the given language ('English' or 'Latin')."""
    return _PRAYERS_LA if language == "Latin" else _PRAYERS_EN

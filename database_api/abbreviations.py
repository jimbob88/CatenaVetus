from typing import Dict

# https://catholic-resources.org/Bible/Abbreviations-Abreviaciones.htm
# Abbreviations and alternative names
abbr_and_alt = {
    "Genesis": ["Gen"],
    "Exodus": ["Exod"],
    "Leviticus": ["Lev"],
    "Numbers": ["Num"],
    "Deuteronomy": ["Deut"],
    "Joshua": ["Josh"],
    "Judges": ["Judg"],
    "Ruth": ["Ruth"],
    "1 Samuel": ["1 Sam"],
    "2 Samuel": ["2 Sam"],
    "1 Kings": ["1 Kgs"],
    "2 Kings": ["2 Kgs"],
    "1 Chronicles": ["1 Chr"],
    "2 Chronicles": ["2 Chr"],
    "Ezra": ["Ezra"],
    "Nehemiah": ["Neh"],
    "Tobit": ["Tob"],
    "Judith": ["Jud"],
    "Esther": ["Esth"],
    "1 Maccabees": ["1 Macc"],
    "2 Maccabees": ["2 Macc"],
    "Job": ["Job"],
    "Psalms": ["Ps"],
    "Proverbs": ["Prov"],
    "Ecclesiastes": ["Eccel", "Qoheleth", "Qoh"],
    "Song of Solomon": ["Song", "Song of Songs", "Canticle of Canticles", "Cant"],
    "Wisdom": ["Wisdom of Solomon", "Wis"],
    "Sirach": ["Sir", "Ecclesiasticus", "Ecclus"],
    "Isaiah": ["Isa"],
    "Jeremiah": ["Jer"],
    "Lamentations": ["Lam"],
    "Baruch": ["Bar"],
    "Ezekiel": ["Ezek"],
    "Daniel": ["Dan"],
    "Hosea": ["Hos"],
    "Joel": ["Joel"],
    "Amos": ["Amos"],
    "Obadiah": ["Obad"],
    "Jonah": ["Jonah"],
    "Micah": ["Mic"],
    "Nahum": ["Nah"],
    "Habakkuk": ["Hab"],
    "Zephaniah": ["Zeph"],
    "Haggai": ["Hag"],
    "Zechariah": ["Zech"],
    "Malachi": ["Mal"],
    "Matthew": ["Matt", "Mat", "Mt"],
    "Mark": ["Mark", "Mk"],
    "Luke": ["Luke", "Lu", "Lk"],
    "John": ["John", "Jn"],
    "Acts": ["Acts of the Apostles", "Acts"],
    "Romans": ["Rom"],
    "1 Corinthians": ["1 Cor", "I Cor", "I Corinthians"],
    "2 Corinthians": ["2 Cor", "II Cor", "II Corinthians"],
    "Galatians": ["Gal"],
    "Ephesians": ["Eph"],
    "Philippians": ["Phil"],
    "Colossians": ["Col"],
    "1 Thessalonians": ["1 Thess", "I Thess", "I Thessalonians"],
    "2 Thessalonians": ["2 Thess", "II Thess", "II Thessalonians"],
    "1 Timothy": ["1 Tim", "I Tim", "I Timothy"],
    "2 Timothy": ["2 Tim", "II Tim", "II Timothy"],
    "Titus": ["Titus"],
    "Philemon": ["Phlm", "Philem"],
    "Hebrews": ["Heb"],
    "James": ["Jas"],
    "1 Peter": ["1 Pet", "1 Pt"],
    "2 Peter": ["2 Pet", "2 Pt"],
    "1 John": ["1 John", "1 Jn", "I Jn", "I John"],
    "2 John": ["2 John", "2 Jn", "II Jn", "II John"],
    "3 John": ["3 John", "3 Jn", "III Jn", "III John"],
    "Jude": ["Jude"],
    "Revelation": ["Rev", "Apocalypse", "Apoc"]
}

# Allows you to reverse Mk -> Mark
alt_to_fullname: Dict[str, str] = {
    alt_name.lower(): database_name
    for database_name, alt_names in abbr_and_alt.items()
    for alt_name in alt_names
}
alt_to_fullname.update({
    database_name.lower(): database_name for database_name in abbr_and_alt.keys()
})

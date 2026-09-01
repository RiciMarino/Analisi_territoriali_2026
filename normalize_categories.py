from pathlib import Path

p = Path('data.js')
s = p.read_text(encoding='utf-8')

replacements = {
    '"Categoria":"Juniores F"': '"Categoria":"Juniores Femminile"',
    '"Categoria":"Juniores M"': '"Categoria":"Juniores Maschile"',
    '"Categoria":"Open F"': '"Categoria":"Open Femminile"',
    '"Categoria":"Open M"': '"Categoria":"Open Maschile"',
    '"Categoria":"Top J F"': '"Categoria":"Top Junior F"',
    '"Categoria":"Top J M"': '"Categoria":"Top Junior M"',
}

counts = {}
for old, new in replacements.items():
    counts[old] = s.count(old)
    s = s.replace(old, new)

p.write_text(s, encoding='utf-8')
for old, count in counts.items():
    print(f'{old}: {count} sostituzioni')

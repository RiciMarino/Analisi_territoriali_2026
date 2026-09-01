from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = """function tableData(status){
 return BASE_DATA.filter(x=>x.Status===status).map(x=>[
  x.Disciplina,x.Categoria,x.Regione,x.Comitato,x.Squadre,
  x.Note ? `<span class=\"note-pill\">${esc(x.Note)}</span>` : ''
 ]);
}"""

new = """function tableData(status){
 return BASE_DATA.filter(x=>{
  const tipo=norm(x.Tipo).toLocaleLowerCase('it');
  return x.Status===status && !tipo.startsWith('regional');
 }).map(x=>[
  x.Disciplina,x.Categoria,x.Regione,x.Comitato,x.Squadre,
  x.Note ? `<span class=\"note-pill\">${esc(x.Note)}</span>` : ''
 ]);
}"""

if old not in s:
    raise SystemExit('Blocco tableData atteso non trovato: nessuna modifica eseguita.')

s2 = s.replace(old, new, 1)
if s2.count("function tableData(status)") != 1:
    raise SystemExit('Controllo fallito: numero inatteso di funzioni tableData.')

p.write_text(s2, encoding='utf-8')
print('OK: record regionali esclusi dalle tabelle C.U. e Mostra dati insieme.')

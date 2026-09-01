from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old=''' <nav class="tabs">\n  <button class="tabbtn active" data-pane="summaryPane">Riepilogo attività</button>\n  <button class="tabbtn" data-pane="regionalPane">Attività regionali <span class="badge" id="regionalCount">0</span></button>'''
new=''' <nav class="tabs">\n  <button class="tabbtn active" data-pane="regionalPane">Attività regionali <span class="badge" id="regionalCount">0</span></button>\n  <button class="tabbtn" data-pane="summaryPane">Riepilogo attività</button>'''
if old not in s:
    raise SystemExit('Blocco tab non trovato')
s=s.replace(old,new,1)
old2=''' <section class="panel">\n  <div class="pane active" id="summaryPane">\n   <p class="small-note">Per ogni disciplina e categoria, le regioni sono ordinate per numero di squadre in ordine decrescente.</p>\n   <div id="summaryContainer"></div>\n  </div>\n\n  <div class="pane" id="regionalPane">\n   <p class="small-note">Sono considerate esclusivamente le righe del foglio BASE DATI in cui la colonna Tipo contiene “Regionali”. Per ogni disciplina e categoria, le regioni sono ordinate per numero di squadre in ordine decrescente.</p>\n   <div id="regionalContainer"></div>\n  </div>'''
new2=''' <section class="panel">\n  <div class="pane active" id="regionalPane">\n   <p class="small-note">Sono considerate esclusivamente le righe del foglio BASE DATI in cui la colonna Tipo contiene “Regionali”. Per ogni disciplina e categoria, le regioni sono ordinate per numero di squadre in ordine decrescente.</p>\n   <div id="regionalContainer"></div>\n  </div>\n\n  <div class="pane" id="summaryPane">\n   <p class="small-note">Per ogni disciplina e categoria, le regioni sono ordinate per numero di squadre in ordine decrescente.</p>\n   <div id="summaryContainer"></div>\n  </div>'''
if old2 not in s:
    raise SystemExit('Blocco pannelli non trovato')
s=s.replace(old2,new2,1)
p.write_text(s,encoding='utf-8')

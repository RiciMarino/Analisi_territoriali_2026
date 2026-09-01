from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) Estrai i due dataset già presenti nell'HTML, senza modificarne il contenuto.
m_base = re.search(r"const BASE_DATA = (\[.*?\]);\nconst SUMMARY_DATA = ", s, re.S)
m_sum = re.search(r"const SUMMARY_DATA = (\[.*?\]);\n\nconst norm", s, re.S)
if not m_base or not m_sum:
    raise SystemExit('Dataset non trovati nel formato atteso')

base_data = m_base.group(1)
summary_data = m_sum.group(1)

Path('data.js').write_text(
    'const BASE_DATA = ' + base_data + ';\n' +
    'const SUMMARY_DATA = ' + summary_data + ';\n',
    encoding='utf-8'
)

# 2) Rimuovi i dataset incorporati dall'HTML e carica data.js prima dello script applicativo.
s = re.sub(
    r"const BASE_DATA = \[.*?\];\nconst SUMMARY_DATA = \[.*?\];\n\n",
    '',
    s,
    count=1,
    flags=re.S
)

needle = '<script>\nconst norm = v =>'
replacement = '<script src="data.js"></script>\n<script>\nconst norm = v =>'
if needle not in s:
    raise SystemExit('Punto di inserimento data.js non trovato')
s = s.replace(needle, replacement, 1)

# 3) Riordina i filtri nell'interfaccia: Regione, Comitato, Disciplina, Categoria.
old_filters = '''   <div class="col-12 col-md-3"><label>Disciplina</label><select id="fDisc" class="form-select"><option value="">Tutte</option></select></div>
   <div class="col-12 col-md-3"><label>Categoria</label><select id="fCat" class="form-select"><option value="">Tutte</option></select></div>
   <div class="col-12 col-md-3"><label>Regione</label><select id="fReg" class="form-select"><option value="">Tutte</option></select></div>
   <div class="col-12 col-md-3"><label>Comitato</label><select id="fCom" class="form-select"><option value="">Tutti</option></select></div>'''
new_filters = '''   <div class="col-12 col-md-3"><label>Regione</label><select id="fReg" class="form-select"><option value="">Tutte</option></select></div>
   <div class="col-12 col-md-3"><label>Comitato</label><select id="fCom" class="form-select"><option value="">Tutti</option></select></div>
   <div class="col-12 col-md-3"><label>Disciplina</label><select id="fDisc" class="form-select"><option value="">Tutte</option></select></div>
   <div class="col-12 col-md-3"><label>Categoria</label><select id="fCat" class="form-select"><option value="">Tutte</option></select></div>'''
if s.count(old_filters) != 1:
    raise SystemExit(f'Blocco filtri inatteso: {s.count(old_filters)} occorrenze')
s = s.replace(old_filters, new_filters, 1)

# 4) Sostituisci i KPI statici con KPI dinamici basati sui filtri attivi.
old_kpis = '''document.getElementById('kpiTeams').textContent=fmt(BASE_DATA.reduce((s,x)=>s+x.Squadre,0));
document.getElementById('kpiActivities').textContent=new Set(BASE_DATA.map(x=>x.Disciplina)).size;
document.getElementById('kpiCommittees').textContent=new Set(BASE_DATA.map(x=>x.Comitato)).size;
document.getElementById('kpiNotOk').textContent=BASE_DATA.filter(x=>x.Status==='Non soddisfa C.U.').length;'''
new_kpis = '''function updateKpis(){
 const fDisc=norm($('#fDisc').val()),fCat=norm($('#fCat').val()),fReg=norm($('#fReg').val()),fCom=norm($('#fCom').val());
 const rows=BASE_DATA.filter(x=>(!fDisc||x.Disciplina===fDisc)&&(!fCat||x.Categoria===fCat)&&(!fReg||x.Regione===fReg)&&(!fCom||x.Comitato===fCom));
 document.getElementById('kpiTeams').textContent=fmt(rows.reduce((s,x)=>s+Number(x.Squadre||0),0));
 document.getElementById('kpiActivities').textContent=new Set(rows.map(x=>norm(x.Disciplina)).filter(Boolean)).size;
 document.getElementById('kpiCommittees').textContent=new Set(rows.map(x=>norm(x.Comitato)).filter(Boolean)).size;
 document.getElementById('kpiNotOk').textContent=rows.filter(x=>x.Status==='Non soddisfa C.U.').length;
}
updateKpis();'''
if s.count(old_kpis) != 1:
    raise SystemExit(f'Blocco KPI inatteso: {s.count(old_kpis)} occorrenze')
s = s.replace(old_kpis, new_kpis, 1)

# 5) Ogni applicazione dei filtri aggiorna anche i KPI.
old_apply = ''' renderSummary();
 renderRegionalSummary();
}
$('#fDisc,#fCat,#fReg,#fCom').on('change',applyFilters);'''
new_apply = ''' renderSummary();
 renderRegionalSummary();
 updateKpis();
}
$('#fDisc,#fCat,#fReg,#fCom').on('change',applyFilters);'''
if s.count(old_apply) != 1:
    raise SystemExit(f'Blocco applyFilters inatteso: {s.count(old_apply)} occorrenze')
s = s.replace(old_apply, new_apply, 1)

# Controlli di sicurezza minimi.
assert 'const BASE_DATA = [' not in s
assert 'const SUMMARY_DATA = [' not in s
assert '<script src="data.js"></script>' in s
assert "const vals=[norm($('#fDisc').val()),norm($('#fCat').val()),norm($('#fReg').val()),norm($('#fCom').val())];" in s
assert s.count('function updateKpis(){') == 1

p.write_text(s, encoding='utf-8')
print('OK: index.html migrato e data.js creato')

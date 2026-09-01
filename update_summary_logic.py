from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

pattern=r"function renderSummary\(\)\{.*?\n\}\nfunction renderRegionalSummary\(\)\{"
replacement=r'''function renderSummary(){
 const fDisc=norm($('#fDisc').val()),fCat=norm($('#fCat').val()),fReg=norm($('#fReg').val());
 const rows=SUMMARY_DATA.filter(x=>(!fDisc||x.Disciplina===fDisc)&&(!fCat||x.Categoria===fCat)&&(!fReg||x.Regione===fReg));
 const groups={};
 rows.forEach(x=>{
  const key=x.Disciplina+'|||'+x.Categoria;
  (groups[key]??=[]).push(x);
 });
 let out='';
 Object.keys(groups).sort((a,b)=>a.localeCompare(b,'it')).forEach(key=>{
  const [disc,cat]=key.split('|||');
  const items=groups[key].map(x=>{
   const regionalSquadre=BASE_DATA.filter(r=>{
    const tipo=norm(r.Tipo).toLocaleLowerCase('it');
    return tipo.startsWith('regional') &&
           r.Disciplina===x.Disciplina &&
           r.Categoria===x.Categoria &&
           r.Regione===x.Regione;
   }).reduce((sum,r)=>sum+Number(r.Squadre||0),0);
   const totaleSquadre=Number(x.Squadre||0);
   return {...x, Regionali:regionalSquadre, Provinciali:Math.max(0,totaleSquadre-regionalSquadre)};
  }).sort((a,b)=>b.Squadre-a.Squadre || a.Regione.localeCompare(b.Regione,'it'));
  const totale=items.reduce((sum,x)=>sum+Number(x.Squadre||0),0);
  out+=`<div class="group-card"><div class="group-title" style="justify-content:flex-start;gap:18px"><span>${esc(disc)} · ${esc(cat)}</span><span>${fmt(totale)} squadre</span></div>
  <div class="table-responsive"><table class="table table-sm table-striped summary-table mb-0">
  <thead><tr><th>Regione</th><th>Squadre regionali</th><th>Squadre provinciali</th></tr></thead><tbody>`;
  items.forEach(x=>out+=`<tr><td>${esc(x.Regione)}</td><td><strong>${fmt(x.Regionali)}</strong></td><td><strong>${fmt(x.Provinciali)}</strong></td></tr>`);
  out+='</tbody></table></div></div>';
 });
 document.getElementById('summaryContainer').innerHTML=out||'<div class="text-muted">Nessun dato corrispondente ai filtri.</div>';
}
function renderRegionalSummary(){'''

new_s,n=re.subn(pattern,replacement,s,flags=re.S)
if n!=1:
    raise SystemExit(f'Blocco renderSummary trovato {n} volte, atteso 1. Nessuna modifica effettuata.')
p.write_text(new_s,encoding='utf-8')
print('Riepilogo aggiornato: regionali/provinciali separati e totale avvicinato al titolo.')

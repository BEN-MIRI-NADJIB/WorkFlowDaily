import streamlit as st
from datetime import date, datetime, timedelta
import json
from pathlib import Path

st.set_page_config(page_title="WorkFlow", layout="wide")
DATA=Path("tasks.json")
TYPES=["Projet","Réunion","Administratif","Développement","Analyse","Autre"]
PRIORITIES=["Basse","Normale","Haute"]
DAYS=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
MONTHS=["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]

def load():
    if "tasks" not in st.session_state:
        try: st.session_state.tasks=json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else []
        except Exception: st.session_state.tasks=[]
def save():
    try: DATA.write_text(json.dumps(st.session_state.tasks,ensure_ascii=False,indent=2),encoding="utf-8")
    except Exception: pass
def dparse(v): return datetime.strptime(v,"%Y-%m-%d").date()
def in_period(v,p):
    d=dparse(v); now=date.today()
    if p=="Jour": return d==now
    if p=="Semaine":
        start=now-timedelta(days=now.weekday()); return start<=d<start+timedelta(days=7)
    if p=="Mois": return d.year==now.year and d.month==now.month
    return d.year==now.year
def filtered(kind,name):
    if kind=="day":
        monday=date.today()-timedelta(days=date.today().weekday()); target=monday+timedelta(days=DAYS.index(name))
        return [t for t in st.session_state.tasks if t["date"]==target.isoformat()]
    if kind=="month":
        m=MONTHS.index(name)+1; y=date.today().year
        return [t for t in st.session_state.tasks if dparse(t["date"]).year==y and dparse(t["date"]).month==m]
    return [t for t in st.session_state.tasks if t["type"]==name]
def task_list(items,prefix):
    if not items: st.info("Aucune tâche dans cette rubrique."); return
    for t in sorted(items,key=lambda x:(x["date"],x.get("done",False))):
        with st.container(border=True):
            a,b,c=st.columns([.07,.76,.17])
            done=a.checkbox("",value=t.get("done",False),key=f"{prefix}_done_{t['id']}")
            if done!=t.get("done",False): t["done"]=done; save(); st.rerun()
            b.markdown(f"~~{t['title']}~~" if t.get("done") else f"**{t['title']}**")
            dt=dparse(t["date"]); b.caption(f"{DAYS[dt.weekday()]} {dt.strftime('%d/%m/%Y')} · {t['type']} · Priorité {t['priority'].lower()}")
            if c.button("Supprimer",key=f"{prefix}_del_{t['id']}",use_container_width=True):
                st.session_state.tasks=[x for x in st.session_state.tasks if x["id"]!=t["id"]]; save(); st.rerun()

load()
if "selection" not in st.session_state: st.session_state.selection=None
st.markdown('''<style>
.stApp{background:#f5f7fb;color:#111827}.block-container{max-width:1500px;padding-top:4rem}h1,h2,h3,p,label{color:#111827!important}.hero{font-size:3.4rem;font-weight:800;letter-spacing:-.05em}.sub{color:#667085;margin-bottom:2rem}.title{font-size:1.6rem;font-weight:800;margin:2.2rem 0 .3rem}.hint{color:#667085;margin-bottom:1rem}.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin:1rem 0 2rem}.kpi{background:#fff;border:1px solid #e1e7f0;border-radius:18px;padding:22px;box-shadow:0 8px 24px #0f172a0d}.kpi b{font-size:2rem;display:block;margin-top:8px}.orghead{background:linear-gradient(90deg,#f1f3f6,#fff);border:1px solid #dfe5ed;border-radius:18px 18px 0 0;padding:20px;font-weight:800;letter-spacing:.08em}.orgsub{background:#fff;border-left:1px solid #dfe5ed;border-right:1px solid #dfe5ed;color:#667085;padding:10px 18px}.detail{background:#fff;border:1px solid #dfe5ed;border-radius:18px;padding:20px;margin:1.5rem 0;box-shadow:0 8px 25px #0f172a0d}.detail small{color:#667085;letter-spacing:.1em}.detail strong{font-size:1.35rem;display:block;margin-top:5px}[data-testid="stForm"],[data-testid="stVerticalBlockBorderWrapper"]{background:#fff!important;border-radius:18px!important;border:1px solid #dfe5ed!important}.stButton>button,.stFormSubmitButton>button{background:#315bea!important;color:#fff!important;border:0!important;border-radius:10px!important}.stButton>button p,.stFormSubmitButton>button p{color:#fff!important}.org div[data-testid="stButton"]>button{background:#fff!important;color:#263043!important;border:1px solid #e5e9f0!important;box-shadow:none!important}.org div[data-testid="stButton"]>button p{color:#263043!important;text-align:left;width:100%}@media(max-width:900px){.kpis{grid-template-columns:1fr 1fr}}@media(max-width:600px){.kpis{grid-template-columns:1fr}}
</style>''',unsafe_allow_html=True)
st.markdown('<div class="hero">WorkFlow</div><div class="sub">Mon espace d\'organisation professionnelle</div>',unsafe_allow_html=True)
st.markdown('<div class="title">Nouvelle tâche</div><div class="hint">Ajoute et planifie une tâche professionnelle</div>',unsafe_allow_html=True)
with st.form("new",clear_on_submit=True):
    title=st.text_input("Tâche"); a,b,c=st.columns(3)
    with a: typ=st.selectbox("Type",TYPES)
    with b: dt=st.date_input("Date",date.today())
    with c: pr=st.selectbox("Priorité",PRIORITIES,index=1)
    if st.form_submit_button("Ajouter",use_container_width=True) and title.strip():
        st.session_state.tasks.insert(0,{"id":str(datetime.now().timestamp()),"title":title.strip(),"type":typ,"date":dt.isoformat(),"priority":pr,"done":False}); save(); st.rerun()
st.markdown('<div class="title">Synthèse</div>',unsafe_allow_html=True)
period=st.segmented_control("Période",["Jour","Semaine","Mois","Année"],default="Jour") or "Jour"
visible=[t for t in st.session_state.tasks if in_period(t["date"],period)]; done=sum(t.get("done",False) for t in visible); total=len(visible); high=sum(1 for t in visible if t["priority"]=="Haute" and not t.get("done")); pct=round(done*100/total) if total else 0
st.markdown(f'<div class="kpis"><div class="kpi">TOTAL<b>{total}</b></div><div class="kpi">TERMINÉES<b>{done}</b></div><div class="kpi">À FAIRE<b>{total-done}</b></div><div class="kpi">PRIORITÉ HAUTE<b>{high}</b></div></div>',unsafe_allow_html=True)
st.markdown('<div class="title">Organisation rapide</div><div class="hint">Clique sur une ligne pour voir les tâches correspondantes</div>',unsafe_allow_html=True)
week_start=date.today()-timedelta(days=date.today().weekday())
dc={n:sum(1 for t in st.session_state.tasks if t["date"]==(week_start+timedelta(days=i)).isoformat()) for i,n in enumerate(DAYS)}
mc={n:sum(1 for t in st.session_state.tasks if dparse(t["date"]).year==date.today().year and dparse(t["date"]).month==i+1) for i,n in enumerate(MONTHS)}
tc={n:sum(1 for t in st.session_state.tasks if t["type"]==n) for n in TYPES}
cols=st.columns(3)
for col,heading,names,counts,kind in [(cols[0],"JOURS",DAYS,dc,"day"),(cols[1],"MOIS",MONTHS,mc,"month"),(cols[2],"CATÉGORIES",TYPES,tc,"type")]:
    with col:
        st.markdown(f'<div class="orghead">{heading}</div><div class="orgsub">Clique pour ouvrir</div>',unsafe_allow_html=True)
        st.markdown('<div class="org">',unsafe_allow_html=True)
        for name in names:
            if st.button(f"{name} · {counts[name]}",key=f"{kind}_{name}",use_container_width=True): st.session_state.selection=(kind,name)
        st.markdown('</div>',unsafe_allow_html=True)
if st.session_state.selection:
    kind,name=st.session_state.selection; items=filtered(kind,name)
    st.markdown(f'<div class="detail"><small>DÉTAIL DE LA RUBRIQUE</small><strong>{name}</strong>{len(items)} tâche(s)</div>',unsafe_allow_html=True)
    close,_=st.columns([.15,.85])
    with close:
        if st.button("Fermer",use_container_width=True): st.session_state.selection=None; st.rerun()
    task_list(items,"filter")
st.markdown(f'<div class="title">Mes tâches · {period}</div>',unsafe_allow_html=True)
task_list(visible,"main")
st.divider(); st.caption("WorkFlow V4")

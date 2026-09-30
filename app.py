import streamlit as st
from datetime import date, datetime, timedelta
import json
from pathlib import Path

st.set_page_config(page_title="WorkFlow", page_icon="💼", layout="wide")

DATA = Path("tasks.json")
TYPES = ["Projet", "Réunion", "Administratif", "Développement", "Analyse", "Autre"]
PRIORITIES = ["Basse", "Normale", "Haute"]

def load_tasks():
    if "tasks" not in st.session_state:
        try:
            st.session_state.tasks = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else []
        except Exception:
            st.session_state.tasks = []

def save_tasks():
    try:
        DATA.write_text(json.dumps(st.session_state.tasks, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass

def in_period(task_date, period):
    d = datetime.strptime(task_date, "%Y-%m-%d").date()
    now = date.today()
    if period == "Jour": return d == now
    if period == "Semaine":
        start = now - timedelta(days=now.weekday())
        return start <= d < start + timedelta(days=7)
    if period == "Mois": return d.year == now.year and d.month == now.month
    return d.year == now.year

def rerun():
    st.rerun()

load_tasks()
st.markdown("""<style>
.stApp{background:#07101e}.block-container{max-width:1200px;padding-top:2rem}.wf-card{background:#101b2d;border:1px solid #24334a;border-radius:18px;padding:20px;margin-bottom:16px}.muted{color:#91a0b7}.big{font-size:48px;font-weight:800}.task{background:#101b2d;border:1px solid #24334a;border-radius:14px;padding:13px;margin:8px 0}
</style>""", unsafe_allow_html=True)

st.title("💼 WorkFlow")
st.caption("Mon espace d'organisation professionnelle")

left, right = st.columns([2.2, 1])
with left:
    st.subheader("Nouvelle tâche")
    with st.form("new_task", clear_on_submit=True):
        title = st.text_input("Tâche", placeholder="Ex. Finaliser la présentation GDP")
        c1,c2,c3=st.columns(3)
        with c1: task_type=st.selectbox("Type", TYPES)
        with c2: task_date=st.date_input("Date", value=date.today())
        with c3: priority=st.selectbox("Priorité", PRIORITIES, index=1)
        submitted=st.form_submit_button("+ Ajouter", use_container_width=True)
        if submitted and title.strip():
            st.session_state.tasks.insert(0,{"id":str(datetime.now().timestamp()),"title":title.strip(),"type":task_type,"date":task_date.isoformat(),"priority":priority,"done":False})
            save_tasks(); rerun()

with right:
    period=st.segmented_control("Période", ["Jour","Semaine","Mois","Année"], default="Jour") or "Jour"

visible=[t for t in st.session_state.tasks if in_period(t["date"],period)]
done=sum(t["done"] for t in visible); total=len(visible); pct=round(done*100/total) if total else 0

with right:
    st.subheader("Synthèse")
    st.markdown(f'<div class="big">{pct}%</div><div class="muted">des tâches terminées</div>', unsafe_allow_html=True)
    st.progress(pct/100 if pct else 0)
    a,b=st.columns(2); a.metric("Total",total); b.metric("Terminées",done)
    a,b=st.columns(2); a.metric("À faire",total-done); b.metric("Priorité haute",sum(1 for t in visible if t["priority"]=="Haute" and not t["done"]))
    if visible:
        counts={}
        for t in visible: counts[t["type"]]=counts.get(t["type"],0)+1
        st.caption("Répartition par type")
        for k,v in sorted(counts.items(), key=lambda x:-x[1]): st.write(f"{k}: **{v}**")

with left:
    st.subheader(f"Mes tâches · {period}")
    if not visible: st.info("Aucune tâche pour cette période.")
    for t in sorted(visible,key=lambda x:x["date"]):
        with st.container(border=True):
            c1,c2,c3=st.columns([0.12,0.72,0.16])
            checked=c1.checkbox("",value=t["done"],key="done_"+t["id"])
            if checked!=t["done"]:
                t["done"]=checked; save_tasks(); rerun()
            label=f"~~{t['title']}~~" if t["done"] else f"**{t['title']}**"
            c2.markdown(label); c2.caption(f"{t['date']} · {t['type']} · Priorité {t['priority'].lower()}")
            if c3.button("Supprimer",key="del_"+t["id"]):
                st.session_state.tasks=[x for x in st.session_state.tasks if x["id"]!=t["id"]]; save_tasks(); rerun()

st.divider()
st.caption("WorkFlow V2 Streamlit")

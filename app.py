import streamlit as st
from datetime import date, datetime, timedelta
import json
from pathlib import Path

st.set_page_config(page_title="WorkFlow", layout="wide", initial_sidebar_state="collapsed")

DATA = Path("tasks.json")
TYPES = ["Projet", "Réunion", "Administratif", "Développement", "Analyse", "Autre"]
PRIORITIES = ["Basse", "Normale", "Haute"]
DAYS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
MONTHS = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]


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


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()


def period_filter(task_date, period):
    d = parse_date(task_date)
    now = date.today()
    if period == "Jour":
        return d == now
    if period == "Semaine":
        monday = now - timedelta(days=now.weekday())
        return monday <= d < monday + timedelta(days=7)
    if period == "Mois":
        return d.year == now.year and d.month == now.month
    return d.year == now.year


def tasks_for(group, value):
    if group == "Jour":
        monday = date.today() - timedelta(days=date.today().weekday())
        target = monday + timedelta(days=DAYS.index(value))
        return [t for t in st.session_state.tasks if t["date"] == target.isoformat()]
    if group == "Mois":
        month = MONTHS.index(value) + 1
        year = date.today().year
        return [t for t in st.session_state.tasks if parse_date(t["date"]).year == year and parse_date(t["date"]).month == month]
    return [t for t in st.session_state.tasks if t["type"] == value]


def task_rows(items, prefix):
    if not items:
        st.info("Aucune tâche.")
        return
    for task in sorted(items, key=lambda x: (x["done"], x["date"], x["priority"])):
        with st.container(border=True):
            check, body, action = st.columns([0.08, 0.75, 0.17], vertical_alignment="center")
            state = check.checkbox("", value=task["done"], key=f"{prefix}_done_{task['id']}")
            if state != task["done"]:
                task["done"] = state
                save_tasks()
                st.rerun()
            title = f"~~{task['title']}~~" if task["done"] else f"**{task['title']}**"
            body.markdown(title)
            d = parse_date(task["date"])
            body.caption(f"{DAYS[d.weekday()]} {d.strftime('%d/%m')} · {task['type']} · {task['priority']}")
            if action.button("Supprimer", key=f"{prefix}_delete_{task['id']}", use_container_width=True):
                st.session_state.tasks = [x for x in st.session_state.tasks if x["id"] != task["id"]]
                save_tasks()
                st.rerun()


load_tasks()

st.markdown("""
<style>
:root{--navy:#0f172a;--muted:#64748b;--blue:#2563eb;--violet:#7c3aed;--green:#059669;--red:#dc2626;--line:#e2e8f0}
*{font-family:"Segoe UI",Arial,sans-serif;box-sizing:border-box}
.stApp{background:linear-gradient(135deg,#f8fbff 0%,#f4f2ff 48%,#f7fafc 100%);color:var(--navy)}
.block-container{max-width:1600px!important;padding:1.2rem 2rem 1.5rem!important}
header[data-testid="stHeader"]{background:transparent}
h1,h2,h3,p,label,.stMarkdown{color:var(--navy)!important}
.topbar{display:flex;align-items:center;justify-content:space-between;margin-bottom:.7rem}
.brand{font-size:2.15rem;font-weight:850;letter-spacing:-.055em;line-height:1}
.brand span{background:linear-gradient(90deg,var(--blue),var(--violet));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.tagline{font-size:.78rem;color:var(--muted);margin-top:.28rem}
.today{background:#fff;border:1px solid var(--line);border-radius:14px;padding:.65rem .9rem;color:#475569;font-size:.78rem;box-shadow:0 8px 25px rgba(15,23,42,.05)}
.section-label{font-size:.68rem;letter-spacing:.12em;font-weight:800;color:#8491a3;margin:.15rem 0 .45rem}
[data-testid="stForm"]{background:rgba(255,255,255,.94)!important;border:1px solid var(--line)!important;border-radius:18px!important;padding:14px 16px!important;box-shadow:0 10px 30px rgba(15,23,42,.06)}
[data-baseweb="input"]>div,[data-baseweb="select"]>div{background:#fff!important;border-color:#cbd5e1!important;border-radius:10px!important}
[data-baseweb="input"] input,input{color:var(--navy)!important;-webkit-text-fill-color:var(--navy)!important;background:#fff!important}
[data-baseweb="select"] *{color:var(--navy)!important}
.stFormSubmitButton>button,.stButton>button{border:0!important;border-radius:10px!important;background:linear-gradient(100deg,var(--blue),#4f46e5)!important;color:#fff!important;font-weight:700!important;min-height:38px!important;transition:.18s}
.stFormSubmitButton>button p,.stButton>button p{color:#fff!important}
.stFormSubmitButton>button:hover,.stButton>button:hover{transform:translateY(-1px);box-shadow:0 8px 18px rgba(37,99,235,.22)}
[data-testid="stSegmentedControl"]{background:#e9eef7!important;border-radius:12px!important;padding:3px!important}
[data-testid="stSegmentedControl"] button p{color:#475569!important}
[data-testid="stSegmentedControl"] button[aria-pressed="true"]{background:#fff!important;box-shadow:0 3px 10px rgba(15,23,42,.1)!important}
[data-testid="stSegmentedControl"] button[aria-pressed="true"] p{color:var(--blue)!important;font-weight:800!important}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:.55rem 0 .75rem}
.kpi{background:rgba(255,255,255,.95);border:1px solid var(--line);border-radius:15px;padding:12px 14px;box-shadow:0 7px 20px rgba(15,23,42,.045);position:relative;overflow:hidden}
.kpi:before{content:"";position:absolute;left:0;top:0;width:4px;height:100%;background:var(--accent)}
.kpi small{font-size:.62rem;letter-spacing:.1em;font-weight:800;color:#8491a3}.kpi strong{display:block;font-size:1.6rem;line-height:1.1;margin-top:5px}.kpi span{font-size:.68rem;color:var(--muted)}
.panel-title{font-size:1rem;font-weight:800;letter-spacing:-.02em;margin:0}.panel-sub{font-size:.7rem;color:var(--muted);margin:.15rem 0 .5rem}
[data-testid="stVerticalBlockBorderWrapper"]{background:rgba(255,255,255,.96)!important;border:1px solid var(--line)!important;border-radius:16px!important;box-shadow:0 8px 24px rgba(15,23,42,.045)}
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlockBorderWrapper"]{box-shadow:none!important;border-radius:12px!important}
[data-testid="stAlert"]{border-radius:12px!important;padding:.55rem .7rem!important}
[data-testid="stCaptionContainer"] p{color:var(--muted)!important;font-size:.68rem!important}
div[data-testid="stCheckbox"]{padding-top:.25rem}
.compact-note{background:linear-gradient(110deg,#eff6ff,#f5f3ff);border:1px solid #dbeafe;border-radius:12px;padding:.55rem .75rem;font-size:.72rem;color:#475569;margin-bottom:.55rem}
@media(max-width:900px){.block-container{padding:1rem!important}.topbar{align-items:flex-start}.today{display:none}.kpis{grid-template-columns:1fr 1fr}}
@media(max-width:540px){.kpis{grid-template-columns:1fr 1fr}.brand{font-size:1.8rem}}
</style>
""", unsafe_allow_html=True)

now_label = date.today().strftime("%d/%m/%Y")
st.markdown(f'<div class="topbar"><div><div class="brand"><span>Work</span>Flow</div><div class="tagline">Organisation professionnelle rapide et claire</div></div><div class="today">Aujourd’hui · {now_label}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section-label">AJOUT RAPIDE</div>', unsafe_allow_html=True)
with st.form("quick_add", clear_on_submit=True, border=True):
    c1, c2, c3, c4, c5 = st.columns([3.4, 1.35, 1.35, 1.25, 1.2], vertical_alignment="bottom")
    title = c1.text_input("Tâche", placeholder="Nouvelle tâche...", label_visibility="collapsed")
    task_type = c2.selectbox("Type", TYPES, label_visibility="collapsed")
    task_date = c3.date_input("Date", value=date.today(), label_visibility="collapsed")
    priority = c4.selectbox("Priorité", PRIORITIES, index=1, label_visibility="collapsed")
    submitted = c5.form_submit_button("Ajouter", use_container_width=True)
    if submitted and title.strip():
        st.session_state.tasks.insert(0, {"id":str(datetime.now().timestamp()),"title":title.strip(),"type":task_type,"date":task_date.isoformat(),"priority":priority,"done":False})
        save_tasks()
        st.rerun()

filter_col, spacer = st.columns([2.2, 5.8])
with filter_col:
    period = st.segmented_control("Période", ["Jour","Semaine","Mois","Année"], default="Jour", label_visibility="collapsed") or "Jour"
visible = [t for t in st.session_state.tasks if period_filter(t["date"], period)]
done = sum(1 for t in visible if t["done"])
total = len(visible)
high = sum(1 for t in visible if t["priority"] == "Haute" and not t["done"])
pct = round(done * 100 / total) if total else 0
st.markdown(f'''<div class="kpis"><div class="kpi" style="--accent:#2563eb"><small>TOTAL</small><strong>{total}</strong><span>{period.lower()}</span></div><div class="kpi" style="--accent:#059669"><small>TERMINÉES</small><strong>{done}</strong><span>{pct}% effectué</span></div><div class="kpi" style="--accent:#7c3aed"><small>À FAIRE</small><strong>{total-done}</strong><span>restantes</span></div><div class="kpi" style="--accent:#dc2626"><small>URGENTES</small><strong>{high}</strong><span>priorité haute</span></div></div>''', unsafe_allow_html=True)

left, center, right = st.columns([1.2, 2.25, 1.2], gap="medium")

with left:
    with st.container(border=True, height=545):
        st.markdown('<div class="panel-title">Organisation</div><div class="panel-sub">Choisis un filtre</div>', unsafe_allow_html=True)
        group = st.radio("Classement", ["Jour","Mois","Catégorie"], horizontal=True, label_visibility="collapsed")
        if group == "Jour":
            options = DAYS
        elif group == "Mois":
            options = MONTHS
        else:
            options = TYPES
        choice = st.selectbox("Rubrique", options, label_visibility="collapsed")
        items = tasks_for(group, choice)
        st.markdown(f'<div class="compact-note"><b>{choice}</b> · {len(items)} tâche(s)</div>', unsafe_allow_html=True)
        task_rows(items, "organizer")

with center:
    with st.container(border=True, height=545):
        st.markdown(f'<div class="panel-title">Tâches · {period}</div><div class="panel-sub">{total} élément(s), {done} terminé(s)</div>', unsafe_allow_html=True)
        status = st.segmented_control("Statut", ["Toutes","À faire","Terminées"], default="Toutes", label_visibility="collapsed") or "Toutes"
        shown = visible
        if status == "À faire": shown = [t for t in visible if not t["done"]]
        if status == "Terminées": shown = [t for t in visible if t["done"]]
        task_rows(shown, "main")

with right:
    with st.container(border=True, height=545):
        st.markdown('<div class="panel-title">Priorités</div><div class="panel-sub">Charge de la période</div>', unsafe_allow_html=True)
        counts = {p:sum(1 for t in visible if t["priority"] == p) for p in PRIORITIES}
        st.metric("Haute", counts["Haute"])
        st.progress(counts["Haute"] / max(total,1), text="Haute")
        st.metric("Normale", counts["Normale"])
        st.progress(counts["Normale"] / max(total,1), text="Normale")
        st.metric("Basse", counts["Basse"])
        st.progress(counts["Basse"] / max(total,1), text="Basse")
        st.divider()
        type_counts = {t:sum(1 for x in visible if x["type"] == t) for t in TYPES}
        top_types = sorted(type_counts.items(), key=lambda x:x[1], reverse=True)[:3]
        st.markdown('<div class="panel-title">Top catégories</div>', unsafe_allow_html=True)
        for name, count in top_types:
            st.caption(f"{name} · {count}")

st.caption("WorkFlow · Tableau de travail compact")

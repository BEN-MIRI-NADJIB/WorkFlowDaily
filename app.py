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
:root{--ink:#162033;--muted:#6d7b91;--blue:#3478f6;--blue2:#635bff;--cyan:#10b7c9;--green:#17a673;--amber:#f59e0b;--red:#ea526f;--line:#dfe7f2;--white:#fff}
*{font-family:"Segoe UI Variable","Segoe UI",Arial,sans-serif;box-sizing:border-box}
.stApp{background:radial-gradient(circle at 4% 8%,rgba(52,120,246,.12),transparent 24%),radial-gradient(circle at 96% 5%,rgba(99,91,255,.11),transparent 22%),linear-gradient(145deg,#f8fbff 0%,#f5f3ff 52%,#f8fafc 100%);color:var(--ink)}
.block-container{max-width:1680px!important;padding:1.05rem 1.75rem 1.1rem!important}
header[data-testid="stHeader"]{background:transparent;height:2.2rem}
#MainMenu,footer{visibility:hidden}
h1,h2,h3,p,label,.stMarkdown{color:var(--ink)!important}
.topbar{display:flex;align-items:center;justify-content:space-between;margin:-.2rem 0 .65rem}
.brand{font-size:2.25rem;font-weight:900;letter-spacing:-.065em;line-height:1}
.brand span{background:linear-gradient(90deg,var(--blue),var(--blue2),var(--cyan));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.tagline{font-size:.78rem;color:var(--muted);margin-top:.3rem;letter-spacing:.01em}
.today{background:rgba(255,255,255,.82);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.9);border-radius:15px;padding:.65rem .9rem;color:#4b5c75;font-size:.76rem;box-shadow:0 10px 30px rgba(34,56,92,.08)}
.section-label{font-size:.64rem;letter-spacing:.15em;font-weight:850;color:#8795aa;margin:.1rem 0 .4rem}
[data-testid="stForm"]{background:rgba(255,255,255,.91)!important;backdrop-filter:blur(14px);border:1px solid rgba(221,230,242,.9)!important;border-radius:18px!important;padding:12px 15px!important;box-shadow:0 12px 34px rgba(32,52,86,.065)}
[data-baseweb="input"]>div,[data-baseweb="select"]>div{background:#fff!important;border:1px solid #d8e1ed!important;border-radius:11px!important;transition:border-color .18s,box-shadow .18s,transform .18s}
[data-baseweb="input"]>div:focus-within,[data-baseweb="select"]>div:focus-within{border-color:#76a8ff!important;box-shadow:0 0 0 4px rgba(52,120,246,.11)!important;transform:translateY(-1px)}
[data-baseweb="input"] input,input{color:var(--ink)!important;-webkit-text-fill-color:var(--ink)!important;background:#fff!important}
[data-baseweb="select"] *{color:var(--ink)!important}
.stFormSubmitButton>button,.stButton>button{border:0!important;border-radius:11px!important;background:linear-gradient(105deg,var(--blue),var(--blue2))!important;color:#fff!important;font-weight:750!important;min-height:39px!important;box-shadow:0 7px 18px rgba(52,120,246,.19);transition:transform .17s,box-shadow .17s,filter .17s}
.stFormSubmitButton>button p,.stButton>button p{color:#fff!important}
.stFormSubmitButton>button:hover,.stButton>button:hover{transform:translateY(-2px);filter:saturate(1.1);box-shadow:0 11px 25px rgba(52,120,246,.28)}
.stFormSubmitButton>button:active,.stButton>button:active{transform:translateY(0) scale(.985)}
[data-testid="stSegmentedControl"]{background:#e9eef7!important;border-radius:13px!important;padding:3px!important;box-shadow:inset 0 1px 3px rgba(15,23,42,.06)}
[data-testid="stSegmentedControl"] button{border-radius:10px!important;transition:all .18s}
[data-testid="stSegmentedControl"] button p{color:#52627a!important;font-size:.75rem!important}
[data-testid="stSegmentedControl"] button[aria-pressed="true"]{background:#fff!important;box-shadow:0 4px 12px rgba(30,45,75,.11)!important}
[data-testid="stSegmentedControl"] button[aria-pressed="true"] p{color:var(--blue)!important;font-weight:800!important}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:11px;margin:.55rem 0 .75rem}
.kpi{background:rgba(255,255,255,.91);backdrop-filter:blur(10px);border:1px solid rgba(223,231,242,.93);border-radius:16px;padding:12px 15px;box-shadow:0 8px 24px rgba(29,47,78,.05);position:relative;overflow:hidden;transition:transform .2s,box-shadow .2s}
.kpi:hover{transform:translateY(-3px);box-shadow:0 15px 30px rgba(29,47,78,.09)}
.kpi:before{content:"";position:absolute;left:0;top:0;width:4px;height:100%;background:var(--accent)}
.kpi:after{content:"";position:absolute;width:70px;height:70px;border-radius:50%;right:-30px;top:-32px;background:var(--accent);opacity:.07}
.kpi small{font-size:.6rem;letter-spacing:.12em;font-weight:850;color:#8795aa}.kpi strong{display:block;font-size:1.65rem;line-height:1.05;margin-top:5px;letter-spacing:-.04em}.kpi span{font-size:.65rem;color:var(--muted)}
.panel-title{font-size:1rem;font-weight:850;letter-spacing:-.025em;margin:0}.panel-sub{font-size:.68rem;color:var(--muted);margin:.12rem 0 .5rem}
[data-testid="stVerticalBlockBorderWrapper"]{background:rgba(255,255,255,.93)!important;backdrop-filter:blur(12px);border:1px solid rgba(222,230,241,.95)!important;border-radius:18px!important;box-shadow:0 10px 28px rgba(28,47,78,.055);transition:box-shadow .2s,border-color .2s}
[data-testid="stVerticalBlockBorderWrapper"]:hover{border-color:#d1def0!important;box-shadow:0 14px 34px rgba(28,47,78,.075)}
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlockBorderWrapper"]{box-shadow:none!important;border-radius:12px!important;background:#fff!important;transition:transform .17s,border-color .17s}
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlockBorderWrapper"]:hover{transform:translateX(2px);border-color:#bcd0ee!important}
[data-testid="stAlert"]{border-radius:12px!important;padding:.5rem .65rem!important;background:#eef5ff!important;border:1px solid #d7e7ff!important}
[data-testid="stCaptionContainer"] p{color:var(--muted)!important;font-size:.65rem!important}
div[data-testid="stCheckbox"]{padding-top:.2rem}
[data-testid="stMetric"]{background:linear-gradient(145deg,#fff,#f8fbff);border:1px solid #e2e9f3;border-radius:13px;padding:9px 11px;margin-bottom:4px}
[data-testid="stMetricLabel"] p{color:var(--muted)!important;font-size:.7rem!important}[data-testid="stMetricValue"]{font-size:1.35rem!important;color:var(--ink)!important;font-weight:850!important}
[data-testid="stProgress"]>div>div{background:#e8edf5!important;border-radius:20px!important}[data-testid="stProgress"]>div>div>div{background:linear-gradient(90deg,var(--blue),var(--blue2),var(--cyan))!important;border-radius:20px!important;transition:width .7s cubic-bezier(.2,.8,.2,1)}
.compact-note{background:linear-gradient(110deg,#eef6ff,#f4f1ff);border:1px solid #d9e6fb;border-radius:12px;padding:.55rem .72rem;font-size:.7rem;color:#4d5e76;margin-bottom:.5rem;box-shadow:inset 0 1px 0 rgba(255,255,255,.7)}
.quick-tip{font-size:.65rem;color:#7b899c;text-align:right;margin-top:-.1rem}
@keyframes enter{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.block-container>div{animation:enter .38s ease both}
@media(max-width:1000px){.block-container{padding:1rem!important}.today{display:none}.kpis{grid-template-columns:1fr 1fr}.topbar{align-items:flex-start}}
@media(max-width:560px){.brand{font-size:1.85rem}.kpis{grid-template-columns:1fr 1fr}.kpi{padding:10px 12px}}
</style>
""", unsafe_allow_html=True)

now_label = date.today().strftime("%d/%m/%Y")
st.markdown(f'<div class="topbar"><div><div class="brand"><span>Work</span>Flow</div><div class="tagline">Pilotez votre journée avec clarté</div></div><div class="today">Aujourd’hui · {now_label}</div></div>', unsafe_allow_html=True)

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

st.markdown('<div class="quick-tip">Tout est accessible depuis cet écran, sans navigation inutile.</div>', unsafe_allow_html=True)

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

st.caption("WorkFlow · Tableau de travail intelligent")

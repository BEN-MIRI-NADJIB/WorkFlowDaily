import streamlit as st
from datetime import date, datetime, timedelta
import json
from pathlib import Path

st.set_page_config(page_title="WorkFlow", layout="wide")

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
    if period == "Jour":
        return d == now
    if period == "Semaine":
        start = now - timedelta(days=now.weekday())
        return start <= d < start + timedelta(days=7)
    if period == "Mois":
        return d.year == now.year and d.month == now.month
    return d.year == now.year


def rerun():
    st.rerun()


def last_7_days(tasks):
    today = date.today()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    return [(d, sum(1 for t in tasks if t.get("done") and t.get("date") == d.isoformat())) for d in days]


load_tasks()

st.markdown("""
<style>
:root{--ink:#111827;--muted:#667085;--blue:#2563eb;--purple:#7c3aed;--cyan:#0891b2;--red:#ef4444;--green:#10b981;--line:#e2e8f0}
*{font-family:"Segoe UI",Arial,sans-serif}.stApp{background:radial-gradient(circle at 8% 4%,rgba(37,99,235,.12),transparent 25%),radial-gradient(circle at 92% 8%,rgba(124,58,237,.09),transparent 22%),linear-gradient(180deg,#f8fbff,#f1f5fb)!important;color:var(--ink)!important}.block-container{max-width:1240px;padding-top:5rem!important;padding-bottom:4rem}.wf-title{font-size:3.5rem;font-weight:800;letter-spacing:-.05em;line-height:1;color:var(--ink);margin:0}.wf-title:after{content:"";display:block;width:72px;height:5px;margin-top:15px;border-radius:9px;background:linear-gradient(90deg,var(--blue),var(--purple),var(--cyan));animation:pulseLine 3s ease-in-out infinite}.wf-subtitle{color:var(--muted);font-size:1.02rem;margin:1.1rem 0 2.5rem}.big{font-size:3.4rem;font-weight:800;letter-spacing:-.05em;background:linear-gradient(90deg,#1d4ed8,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1}.muted{color:var(--muted)!important;margin:.45rem 0 1rem}.overview-title{font-size:1.65rem;font-weight:800;letter-spacing:-.03em;margin:2.4rem 0 .2rem;color:var(--ink)}.overview-title:before{content:"";display:inline-block;width:5px;height:23px;border-radius:5px;background:linear-gradient(#2563eb,#7c3aed);margin-right:10px;vertical-align:-3px}.overview-sub{color:var(--muted);margin-bottom:1rem}.dashboard{display:grid;grid-template-columns:1.05fr 1.25fr 1.7fr;gap:16px;margin-bottom:2.4rem}.dash-card{background:rgba(255,255,255,.94);border:1px solid #e1e8f2;border-radius:22px;padding:20px;min-height:220px;box-shadow:0 12px 32px rgba(15,23,42,.06);transition:transform .25s ease,box-shadow .25s ease}.dash-card:hover{transform:translateY(-4px);box-shadow:0 20px 42px rgba(15,23,42,.1)}.card-top{font-size:.68rem;letter-spacing:.13em;font-weight:800;color:#8a98aa;margin-bottom:18px}.completion{display:flex;align-items:center;gap:18px}.ring{--p:0deg;width:118px;height:118px;border-radius:50%;background:conic-gradient(#2563eb 0 var(--p),#e8edf5 var(--p) 360deg);display:grid;place-items:center;position:relative;flex:0 0 auto}.ring:after{content:"";position:absolute;width:84px;height:84px;border-radius:50%;background:#fff}.ring-content{position:relative;z-index:2;text-align:center}.ring-content strong{display:block;font-size:1.55rem;color:var(--ink)}.ring-content span{font-size:.65rem;color:#7c899a}.completion-info strong{font-size:1.3rem;color:var(--ink);display:block}.completion-info span{font-size:.75rem;color:var(--muted);display:block;margin-top:3px}.completion-info small{font-size:.72rem;font-weight:700;color:#2563eb;display:block;margin-top:13px}.p-row{display:grid;grid-template-columns:60px 1fr 24px;align-items:center;gap:8px;margin:15px 0}.p-row b{font-size:.73rem;color:#475569}.track{height:9px;background:#edf1f6;border-radius:20px;overflow:hidden}.fill{display:block;height:100%;min-width:3px;border-radius:20px;animation:grow .8s ease both}.fill-high{background:linear-gradient(90deg,#ef4444,#f97316)}.fill-normal{background:linear-gradient(90deg,#2563eb,#6366f1)}.fill-low{background:linear-gradient(90deg,#10b981,#22c55e)}.p-row em{font-style:normal;font-size:.75rem;font-weight:800;color:#334155;text-align:right}.priority-note{border-top:1px solid #edf1f6;margin-top:17px;padding-top:12px;color:var(--muted);font-size:.7rem}.priority-note strong{color:#ef4444}.mini-chart{height:135px;display:flex;align-items:flex-end;gap:10px;padding:3px 4px 0;border-bottom:1px solid #e5eaf1}.day-col{height:100%;flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center}.day-value{height:18px;font-size:.66rem;font-weight:800;color:#475569}.day-bar{width:min(31px,72%);min-height:5px;border-radius:7px 7px 2px 2px;background:linear-gradient(180deg,#7c3aed,#2563eb);box-shadow:0 6px 12px rgba(79,70,229,.18);animation:rise .7s ease both}.day-label{font-size:.58rem;color:#8492a6;margin-top:7px;white-space:nowrap}.activity-foot{text-align:center;color:var(--muted);font-size:.7rem;margin-top:11px}h1,h2,h3,p,label,.stMarkdown{color:var(--ink)!important}[data-testid="stCaptionContainer"] p,[data-testid="stMetricLabel"] p{color:var(--muted)!important}[data-testid="stMetricValue"]{color:var(--ink)!important;font-weight:800!important}[data-testid="stForm"],[data-testid="stVerticalBlockBorderWrapper"]{background:rgba(255,255,255,.92)!important;border:1px solid #dfe7f1!important;border-radius:20px!important;box-shadow:0 10px 30px rgba(15,23,42,.055);transition:.22s ease}[data-testid="stForm"]{padding:22px}[data-testid="stVerticalBlockBorderWrapper"]:hover{transform:translateY(-2px);box-shadow:0 15px 35px rgba(15,23,42,.09)}[data-baseweb="input"]>div,[data-baseweb="select"]>div{background:#fff!important;border-color:#cbd5e1!important;border-radius:12px!important}[data-baseweb="input"] input,input{color:var(--ink)!important;-webkit-text-fill-color:var(--ink)!important;background:#fff!important}[data-baseweb="select"] *{color:var(--ink)!important}[data-baseweb="popover"],[role="listbox"],[role="option"]{background:#fff!important;color:var(--ink)!important}[data-testid="stDateInput"] input{color:var(--ink)!important;-webkit-text-fill-color:var(--ink)!important}.stFormSubmitButton>button,.stButton>button{background:linear-gradient(100deg,#2563eb,#4f46e5)!important;color:#fff!important;border:0!important;border-radius:12px!important;font-weight:700!important;box-shadow:0 8px 18px rgba(37,99,235,.2);transition:.18s ease}.stFormSubmitButton>button p,.stButton>button p{color:#fff!important}.stFormSubmitButton>button:hover,.stButton>button:hover{transform:translateY(-2px);box-shadow:0 12px 24px rgba(37,99,235,.28)}[data-testid="stSegmentedControl"]{background:#e9eef7!important;border-radius:14px!important;padding:4px!important}[data-testid="stSegmentedControl"] button{background:transparent!important;border:0!important;color:#475569!important}[data-testid="stSegmentedControl"] button p{color:#475569!important}[data-testid="stSegmentedControl"] button[aria-pressed="true"]{background:#fff!important;box-shadow:0 4px 12px rgba(15,23,42,.1)!important}[data-testid="stSegmentedControl"] button[aria-pressed="true"] p{color:#1d4ed8!important;font-weight:800!important}[data-testid="stProgress"]>div>div>div{background:linear-gradient(90deg,#2563eb,#7c3aed,#06b6d4)!important}[data-testid="stMetric"]{background:linear-gradient(145deg,#fff,#f8fbff);border:1px solid #e1e8f2;border-radius:16px;padding:13px 14px;transition:.2s ease}[data-testid="stMetric"]:hover{transform:translateY(-3px)}[data-testid="stAlert"]{background:#eff6ff!important;border:1px solid #c7d9f7!important;border-radius:14px!important}[data-testid="stAlert"] p{color:#173b70!important}[data-testid="stCheckbox"] label span{color:var(--ink)!important}hr{border-color:#dbe4f0!important;margin-top:2rem!important}@keyframes pulseLine{0%,100%{transform:scaleX(1)}50%{transform:scaleX(1.25)}}@keyframes grow{from{width:0}}@keyframes rise{from{height:5px;opacity:.35}}@media(max-width:950px){.dashboard{grid-template-columns:1fr}.dash-card{min-height:auto}.activity{min-height:220px}}@media(max-width:800px){.block-container{padding-top:4.5rem!important}.wf-title{font-size:2.7rem}.completion{justify-content:center}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="wf-title">WorkFlow</div><div class="wf-subtitle">Mon espace d\'organisation professionnelle</div>', unsafe_allow_html=True)

left, right = st.columns([2.2, 1])
with left:
    st.subheader("Nouvelle tâche")
    with st.form("new_task", clear_on_submit=True):
        title = st.text_input("Tâche", placeholder="Ex. Finaliser la présentation GDP")
        c1, c2, c3 = st.columns(3)
        with c1:
            task_type = st.selectbox("Type", TYPES)
        with c2:
            task_date = st.date_input("Date", value=date.today())
        with c3:
            priority = st.selectbox("Priorité", PRIORITIES, index=1)
        submitted = st.form_submit_button("+ Ajouter", use_container_width=True)
        if submitted and title.strip():
            st.session_state.tasks.insert(0, {"id": str(datetime.now().timestamp()), "title": title.strip(), "type": task_type, "date": task_date.isoformat(), "priority": priority, "done": False})
            save_tasks()
            rerun()

with right:
    period = st.segmented_control("Période", ["Jour", "Semaine", "Mois", "Année"], default="Jour") or "Jour"

visible = [t for t in st.session_state.tasks if in_period(t["date"], period)]
done = sum(t["done"] for t in visible)
total = len(visible)
pct = round(done * 100 / total) if total else 0

with right:
    st.subheader("Synthèse")
    st.markdown(f'<div class="big">{pct}%</div><div class="muted">des tâches terminées</div>', unsafe_allow_html=True)
    st.progress(pct / 100 if pct else 0)
    a, b = st.columns(2)
    a.metric("Total", total)
    b.metric("Terminées", done)
    a, b = st.columns(2)
    a.metric("À faire", total - done)
    b.metric("Priorité haute", sum(1 for t in visible if t["priority"] == "Haute" and not t["done"]))
    if visible:
        counts = {}
        for t in visible:
            counts[t["type"]] = counts.get(t["type"], 0) + 1
        st.caption("Répartition par type")
        for k, v in sorted(counts.items(), key=lambda x: -x[1]):
            st.write(f"{k}: **{v}**")

# Dashboard visuel sans graphique Streamlit classique
priority_counts = {p: sum(1 for t in visible if t["priority"] == p) for p in PRIORITIES}
max_priority = max(max(priority_counts.values()), 1)
high_open = sum(1 for t in visible if t["priority"] == "Haute" and not t["done"])
angle = round(pct * 3.6)
week = last_7_days(st.session_state.tasks)
week_max = max(max((v for _, v in week), default=0), 1)
week_html = "".join(
    f'<div class="day-col"><div class="day-value">{v if v else ""}</div><div class="day-bar" style="height:{max(5, round(v / week_max * 100)) if v else 5}%"></div><div class="day-label">{d.strftime("%d/%m")}</div></div>'
    for d, v in week
)

st.markdown('<div class="overview-title">Vue d’ensemble</div><div class="overview-sub">Avancement, priorités et rythme des 7 derniers jours</div>', unsafe_allow_html=True)

html = f"""
<div class="dashboard">
  <div class="dash-card">
    <div class="card-top">AVANCEMENT</div>
    <div class="completion">
      <div class="ring" style="--p:{angle}deg"><div class="ring-content"><strong>{pct}%</strong><span>terminé</span></div></div>
      <div class="completion-info"><strong>{done} / {total}</strong><span>tâches clôturées</span><small>{total-done} restantes</small></div>
    </div>
  </div>
  <div class="dash-card">
    <div class="card-top">PRIORITÉS</div>
    <div class="p-row"><b>Haute</b><div class="track"><i class="fill fill-high" style="width:{priority_counts['Haute']/max_priority*100:.0f}%"></i></div><em>{priority_counts['Haute']}</em></div>
    <div class="p-row"><b>Normale</b><div class="track"><i class="fill fill-normal" style="width:{priority_counts['Normale']/max_priority*100:.0f}%"></i></div><em>{priority_counts['Normale']}</em></div>
    <div class="p-row"><b>Basse</b><div class="track"><i class="fill fill-low" style="width:{priority_counts['Basse']/max_priority*100:.0f}%"></i></div><em>{priority_counts['Basse']}</em></div>
    <div class="priority-note"><strong>{high_open}</strong> tâche(s) haute priorité encore ouverte(s)</div>
  </div>
  <div class="dash-card activity">
    <div class="card-top">ACTIVITÉ · 7 JOURS</div>
    <div class="mini-chart">{week_html}</div>
    <div class="activity-foot">Tâches terminées quotidiennement</div>
  </div>
</div>
"""
st.markdown(html, unsafe_allow_html=True)

with left:
    st.subheader(f"Mes tâches · {period}")
    if not visible:
        st.info("Aucune tâche pour cette période.")
    for t in sorted(visible, key=lambda x: x["date"]):
        with st.container(border=True):
            c1, c2, c3 = st.columns([0.12, 0.72, 0.16])
            checked = c1.checkbox("", value=t["done"], key="done_" + t["id"])
            if checked != t["done"]:
                t["done"] = checked
                save_tasks()
                rerun()
            label = f"~~{t['title']}~~" if t["done"] else f"**{t['title']}**"
            c2.markdown(label)
            c2.caption(f"{t['date']} · {t['type']} · Priorité {t['priority'].lower()}")
            if c3.button("Supprimer", key="del_" + t["id"]):
                st.session_state.tasks = [x for x in st.session_state.tasks if x["id"] != t["id"]]
                save_tasks()
                rerun()

st.divider()
st.caption("WorkFlow V2 Streamlit")

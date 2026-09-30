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


def rerun():
    st.rerun()


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()


def in_period(task_date, period):
    d = parse_date(task_date)
    now = date.today()
    if period == "Jour":
        return d == now
    if period == "Semaine":
        start = now - timedelta(days=now.weekday())
        return start <= d < start + timedelta(days=7)
    if period == "Mois":
        return d.year == now.year and d.month == now.month
    return d.year == now.year


def count_days(tasks):
    counts = {name: 0 for name in DAYS}
    for task in tasks:
        counts[DAYS[parse_date(task["date"]).weekday()]] += 1
    return counts


def count_months(tasks):
    counts = {name: 0 for name in MONTHS}
    for task in tasks:
        counts[MONTHS[parse_date(task["date"]).month - 1]] += 1
    return counts


def panel_group(title, rows, color="blue"):
    body = []
    for label, count in rows:
        badge = f'<span class="list-count">{count}</span>' if count else ''
        body.append(
            f'<div class="organizer-row"><span class="list-lines {color}"><i></i><i></i><i></i></span>'
            f'<span class="list-label">{label}</span>{badge}</div>'
        )
    return (
        f'<section class="organizer-group"><div class="organizer-group-title">'
        f'<span class="outline-square"></span><span>{title}</span><span class="chevron">&#8963;</span></div>'
        f'<div class="organizer-group-body">{"".join(body)}</div></section>'
    )


load_tasks()

st.markdown("""
<style>
:root{--ink:#111827;--muted:#667085;--blue:#315bea;--violet:#7357e8;--green:#16a085;--red:#ef4444}
*{font-family:"Segoe UI",Arial,sans-serif;box-sizing:border-box}
.stApp{background:radial-gradient(circle at 7% 3%,rgba(49,91,234,.09),transparent 24%),radial-gradient(circle at 94% 5%,rgba(115,87,232,.07),transparent 23%),#f5f7fb!important;color:var(--ink)!important}
.block-container{max-width:1540px!important;padding:5rem 2.5rem 4rem!important}
.wf-title{font-size:3.5rem;font-weight:800;letter-spacing:-.055em;line-height:1;color:#101828}
.wf-title:after{content:"";display:block;width:76px;height:5px;margin-top:16px;border-radius:8px;background:linear-gradient(90deg,#315bea,#7357e8,#0891b2);animation:pulse 3s ease-in-out infinite}
.wf-subtitle{color:var(--muted);font-size:1.03rem;margin:1.1rem 0 2.6rem}
.section-title{font-size:1.65rem;font-weight:800;letter-spacing:-.03em;color:#101828;margin:2.5rem 0 .25rem}
.section-sub{color:var(--muted);font-size:.88rem;margin-bottom:1.1rem}
h1,h2,h3,p,label,.stMarkdown{color:var(--ink)!important}
[data-testid="stForm"],[data-testid="stVerticalBlockBorderWrapper"]{background:#fff!important;border:1px solid #e0e6ef!important;border-radius:22px!important;box-shadow:0 11px 30px rgba(15,23,42,.055);transition:.22s}
[data-testid="stForm"]{padding:25px}
[data-testid="stVerticalBlockBorderWrapper"]:hover{transform:translateY(-2px);box-shadow:0 17px 38px rgba(15,23,42,.085)}
[data-baseweb="input"]>div,[data-baseweb="select"]>div{background:#fff!important;border-color:#cbd5e1!important;border-radius:12px!important}
[data-baseweb="input"] input,input{color:#111827!important;-webkit-text-fill-color:#111827!important;background:#fff!important}
[data-baseweb="select"] *{color:#111827!important}
[data-baseweb="popover"],[role="listbox"],[role="option"]{background:#fff!important;color:#111827!important}
.stFormSubmitButton>button,.stButton>button{background:linear-gradient(100deg,#315bea,#5147db)!important;color:#fff!important;border:0!important;border-radius:12px!important;font-weight:700!important;box-shadow:0 8px 18px rgba(49,91,234,.18);transition:.18s}
.stFormSubmitButton>button p,.stButton>button p{color:#fff!important}
.stFormSubmitButton>button:hover,.stButton>button:hover{transform:translateY(-2px);box-shadow:0 12px 24px rgba(49,91,234,.27)}
[data-testid="stSegmentedControl"]{background:#e9eef7!important;border-radius:14px!important;padding:4px!important;max-width:760px}
[data-testid="stSegmentedControl"] button{background:transparent!important;border:0!important}
[data-testid="stSegmentedControl"] button p{color:#475569!important}
[data-testid="stSegmentedControl"] button[aria-pressed="true"]{background:#fff!important;box-shadow:0 4px 12px rgba(15,23,42,.1)!important}
[data-testid="stSegmentedControl"] button[aria-pressed="true"] p{color:#1d4ed8!important;font-weight:800!important}
[data-testid="stCheckbox"] label span{color:#111827!important}
[data-testid="stAlert"]{background:#eff6ff!important;border:1px solid #c7d9f7!important;border-radius:14px!important}
[data-testid="stAlert"] p{color:#173b70!important}
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin:1.2rem 0 2.4rem}
.kpi{position:relative;background:#fff;border:1px solid #e1e7f0;border-radius:21px;padding:24px 26px;min-height:140px;box-shadow:0 10px 26px rgba(15,23,42,.05);overflow:hidden;transition:.22s}
.kpi:hover{transform:translateY(-4px);box-shadow:0 18px 38px rgba(15,23,42,.09)}
.kpi:before{content:"";position:absolute;left:0;top:0;width:5px;height:100%;background:var(--a)}
.kpi-label{font-size:.7rem;font-weight:800;letter-spacing:.11em;color:#8491a3}
.kpi-value{font-size:2.25rem;font-weight:800;color:#101828;margin-top:12px}
.kpi-note{font-size:.74rem;color:#667085;margin-top:6px}
.visual-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:2.5rem}
.visual-card{background:#fff;border:1px solid #e0e6ef;border-radius:22px;padding:30px;min-height:300px;box-shadow:0 12px 30px rgba(15,23,42,.055);transition:.22s}
.visual-card:hover{transform:translateY(-3px);box-shadow:0 18px 40px rgba(15,23,42,.09)}
.card-kicker{font-size:.7rem;font-weight:800;letter-spacing:.12em;color:#8a97a8;margin-bottom:24px}
.progress-layout{display:flex;align-items:center;gap:42px;padding:10px 0}
.ring{--p:0deg;width:165px;height:165px;border-radius:50%;background:conic-gradient(#315bea 0 var(--p),#ebeff5 var(--p) 360deg);display:grid;place-items:center;position:relative;flex:0 0 auto}
.ring:after{content:"";position:absolute;width:119px;height:119px;border-radius:50%;background:#fff}
.ring div{z-index:2;text-align:center}.ring strong{display:block;font-size:2.1rem;color:#101828}.ring span{font-size:.69rem;color:#7d8999}
.progress-text strong{display:block;font-size:1.85rem;color:#101828}.progress-text span{display:block;color:#667085;font-size:.88rem;margin-top:4px}.progress-text small{display:block;color:#315bea;font-weight:700;margin-top:17px}
.priority-row{display:grid;grid-template-columns:85px 1fr 32px;gap:14px;align-items:center;margin:24px 0}.priority-row b{font-size:.8rem;color:#475569}.track{height:12px;border-radius:20px;background:#edf1f6;overflow:hidden}.fill{display:block;height:100%;min-width:3px;border-radius:20px;animation:grow .85s ease both}.fill.high{background:linear-gradient(90deg,#ef4444,#f97316)}.fill.normal{background:linear-gradient(90deg,#315bea,#7357e8)}.fill.low{background:linear-gradient(90deg,#10b981,#22c55e)}.priority-row em{font-style:normal;font-size:.8rem;font-weight:800;color:#334155}.priority-foot{border-top:1px solid #eef1f5;padding-top:16px;color:#667085;font-size:.75rem}.priority-foot strong{color:#ef4444}
.organizer{background:#fff;border:1px solid #dde5ef;border-radius:22px;overflow:hidden;box-shadow:0 12px 32px rgba(15,23,42,.055);margin:1.2rem 0 2.6rem}
.organizer-header{padding:25px 28px;border-bottom:1px solid #e8ecf2}.organizer-header strong{font-size:1.15rem;color:#101828}.organizer-header span{display:block;color:#667085;font-size:.8rem;margin-top:5px}
.organizer-columns{display:grid;grid-template-columns:1fr 1fr 1fr}.organizer-group{border-right:1px solid #e9edf2;min-height:420px}.organizer-group:last-child{border-right:0}
.organizer-group-title{height:64px;display:grid;grid-template-columns:24px 1fr 22px;gap:12px;align-items:center;padding:0 22px;background:linear-gradient(90deg,#f3f5f7,#fbfcfd);border-bottom:1px solid #e9edf2;font-size:.9rem;letter-spacing:.03em;color:#252c38}
.outline-square{width:18px;height:18px;border:1.5px solid #4b5563;border-radius:3px;position:relative}.outline-square:after{content:"";position:absolute;width:1px;height:7px;background:#4b5563;left:5px;top:4px}.chevron{font-size:1rem;color:#4b5563}
.organizer-group-body{padding:10px 0 16px}.organizer-row{min-height:61px;display:grid;grid-template-columns:35px 1fr auto;gap:14px;align-items:center;padding:0 22px;transition:.17s}.organizer-row:hover{background:#f4f6f9}
.list-lines{width:25px;display:flex;flex-direction:column;gap:5px}.list-lines i{height:1.5px;width:25px;background:#486176}.list-lines.blue i{background:#526fe9}.list-lines.green i{background:#12a184}.list-label{font-size:1rem;color:#252d3a}.list-count{min-width:26px;height:26px;border-radius:13px;padding:0 8px;display:grid;place-items:center;background:#edf0f3;font-size:.74rem;color:#303744}
.activity-card{background:#fff;border:1px solid #e0e6ef;border-radius:22px;padding:30px;box-shadow:0 12px 30px rgba(15,23,42,.055);margin-bottom:2.6rem}.activity-bars{height:225px;display:flex;align-items:flex-end;gap:18px;border-bottom:1px solid #e5eaf1;padding:5px 26px 0}.day-col{height:100%;flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end}.day-value{height:24px;color:#475569;font-size:.74rem;font-weight:800}.day-bar{width:min(50px,65%);min-height:6px;border-radius:9px 9px 2px 2px;background:linear-gradient(180deg,#7357e8,#315bea);box-shadow:0 7px 15px rgba(49,91,234,.15);animation:rise .75s ease both}.day-label{font-size:.68rem;color:#7e8b9d;margin-top:9px;padding-bottom:10px}.activity-caption{text-align:center;color:#667085;font-size:.78rem;margin-top:14px}
@keyframes pulse{0%,100%{transform:scaleX(1)}50%{transform:scaleX(1.22)}}@keyframes grow{from{width:0}}@keyframes rise{from{height:6px;opacity:.25}}
@media(max-width:1050px){.visual-grid,.organizer-columns{grid-template-columns:1fr}.organizer-group{border-right:0;border-bottom:1px solid #e9edf2;min-height:auto}.kpi-grid{grid-template-columns:1fr 1fr}}
@media(max-width:700px){.block-container{padding:4.5rem 1rem 3rem!important}.wf-title{font-size:2.7rem}.kpi-grid{grid-template-columns:1fr}.progress-layout{flex-direction:column;text-align:center}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="wf-title">WorkFlow</div><div class="wf-subtitle">Mon espace d\'organisation professionnelle</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Nouvelle tâche</div><div class="section-sub">Ajoute et planifie une tâche professionnelle</div>', unsafe_allow_html=True)
with st.form("new_task", clear_on_submit=True):
    title = st.text_input("Tâche", placeholder="Ex. Finaliser la présentation GDP")
    a, b, c = st.columns(3)
    with a:
        task_type = st.selectbox("Type", TYPES)
    with b:
        task_date = st.date_input("Date", value=date.today())
    with c:
        priority = st.selectbox("Priorité", PRIORITIES, index=1)
    submitted = st.form_submit_button("+ Ajouter", use_container_width=True)
    if submitted and title.strip():
        st.session_state.tasks.insert(0, {
            "id": str(datetime.now().timestamp()),
            "title": title.strip(),
            "type": task_type,
            "date": task_date.isoformat(),
            "priority": priority,
            "done": False,
        })
        save_tasks()
        rerun()

st.markdown('<div class="section-title">Synthèse</div><div class="section-sub">Indicateurs et charge de travail pour la période choisie</div>', unsafe_allow_html=True)
period = st.segmented_control("Période", ["Jour", "Semaine", "Mois", "Année"], default="Jour") or "Jour"
visible = [t for t in st.session_state.tasks if in_period(t["date"], period)]
done = sum(1 for t in visible if t.get("done"))
total = len(visible)
todo = total - done
high_open = sum(1 for t in visible if t.get("priority") == "Haute" and not t.get("done"))
pct = round(done * 100 / total) if total else 0

kpi_html = f"""
<div class="kpi-grid">
  <div class="kpi" style="--a:#315bea"><div class="kpi-label">TOTAL</div><div class="kpi-value">{total}</div><div class="kpi-note">tâches sur la période</div></div>
  <div class="kpi" style="--a:#10b981"><div class="kpi-label">TERMINÉES</div><div class="kpi-value">{done}</div><div class="kpi-note">{pct}% d'avancement</div></div>
  <div class="kpi" style="--a:#7357e8"><div class="kpi-label">À FAIRE</div><div class="kpi-value">{todo}</div><div class="kpi-note">restent à traiter</div></div>
  <div class="kpi" style="--a:#ef4444"><div class="kpi-label">PRIORITÉ HAUTE</div><div class="kpi-value">{high_open}</div><div class="kpi-note">encore ouvertes</div></div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

priority_counts = {p: sum(1 for t in visible if t.get("priority") == p) for p in PRIORITIES}
max_priority = max(max(priority_counts.values()), 1)
angle = round(pct * 3.6)
visual_html = f"""
<div class="visual-grid">
  <div class="visual-card">
    <div class="card-kicker">AVANCEMENT GLOBAL</div>
    <div class="progress-layout">
      <div class="ring" style="--p:{angle}deg"><div><strong>{pct}%</strong><span>terminé</span></div></div>
      <div class="progress-text"><strong>{done} / {total}</strong><span>tâches clôturées</span><small>{todo} tâche(s) restante(s)</small></div>
    </div>
  </div>
  <div class="visual-card">
    <div class="card-kicker">RÉPARTITION DES PRIORITÉS</div>
    <div class="priority-row"><b>Haute</b><div class="track"><i class="fill high" style="width:{priority_counts['Haute']/max_priority*100:.0f}%"></i></div><em>{priority_counts['Haute']}</em></div>
    <div class="priority-row"><b>Normale</b><div class="track"><i class="fill normal" style="width:{priority_counts['Normale']/max_priority*100:.0f}%"></i></div><em>{priority_counts['Normale']}</em></div>
    <div class="priority-row"><b>Basse</b><div class="track"><i class="fill low" style="width:{priority_counts['Basse']/max_priority*100:.0f}%"></i></div><em>{priority_counts['Basse']}</em></div>
    <div class="priority-foot"><strong>{high_open}</strong> tâche(s) haute priorité encore ouverte(s)</div>
  </div>
</div>
"""
st.markdown(visual_html, unsafe_allow_html=True)

st.markdown('<div class="section-title">Organisation rapide</div><div class="section-sub">Vue large inspirée de ton exemple, avec Jours, Mois et Catégories séparés</div>', unsafe_allow_html=True)
week_tasks = [t for t in st.session_state.tasks if in_period(t["date"], "Semaine")]
year_tasks = [t for t in st.session_state.tasks if in_period(t["date"], "Année")]
day_counts = count_days(week_tasks)
month_counts = count_months(year_tasks)
type_counts = {name: sum(1 for t in visible if t.get("type") == name) for name in TYPES}
month_rows = [(name, count) for name, count in month_counts.items() if count]
if not month_rows:
    month_rows = [(MONTHS[date.today().month - 1], 0)]

organizer = '<div class="organizer"><div class="organizer-header"><strong>Classement du travail</strong><span>Chaque rubrique dispose de son propre espace et les compteurs apparaissent à droite.</span></div><div class="organizer-columns">'
organizer += panel_group("JOURS", [(name, day_counts[name]) for name in DAYS], "")
organizer += panel_group("MOIS", month_rows, "blue")
organizer += panel_group("CATÉGORIES", [(name, type_counts[name]) for name in TYPES], "green")
organizer += '</div></div>'
st.markdown(organizer, unsafe_allow_html=True)

week = []
today = date.today()
for i in range(6, -1, -1):
    d = today - timedelta(days=i)
    value = sum(1 for t in st.session_state.tasks if t.get("done") and t.get("date") == d.isoformat())
    week.append((d, value))
week_max = max(max((value for _, value in week), default=0), 1)
week_html = ''.join(
    f'<div class="day-col"><div class="day-value">{value if value else ""}</div>'
    f'<div class="day-bar" style="height:{max(6, round(value / week_max * 100)) if value else 6}%"></div>'
    f'<div class="day-label">{d.strftime("%d/%m")}</div></div>'
    for d, value in week
)
st.markdown(
    f'<div class="activity-card"><div class="card-kicker">ACTIVITÉ DES 7 DERNIERS JOURS</div>'
    f'<div class="activity-bars">{week_html}</div><div class="activity-caption">Nombre de tâches terminées chaque jour</div></div>',
    unsafe_allow_html=True,
)

st.markdown(f'<div class="section-title">Mes tâches · {period}</div><div class="section-sub">Liste détaillée pour la période sélectionnée</div>', unsafe_allow_html=True)
if not visible:
    st.info("Aucune tâche pour cette période.")

for t in sorted(visible, key=lambda x: x["date"]):
    with st.container(border=True):
        c1, c2, c3 = st.columns([0.07, 0.77, 0.16])
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
st.caption("WorkFlow V3")

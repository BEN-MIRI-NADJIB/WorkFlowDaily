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
        DATA.write_text(
            json.dumps(st.session_state.tasks, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
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


def last_7_days_chart_data(tasks):
    today = date.today()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    return {
        "Jour": [d.strftime("%d/%m") for d in days],
        "Terminées": [
            sum(
                1
                for task in tasks
                if task.get("done") is True and task.get("date") == d.isoformat()
            )
            for d in days
        ],
    }


load_tasks()

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root{--ink:#0f172a;--muted:#64748b;--primary:#2563eb;--violet:#7c3aed;--cyan:#0891b2;--green:#059669;--surface:#ffffff;--line:#dbe4f0}
*{font-family:Inter,"Segoe UI",sans-serif}.stApp{background:radial-gradient(circle at 6% 4%,rgba(37,99,235,.13),transparent 24%),radial-gradient(circle at 94% 8%,rgba(124,58,237,.10),transparent 22%),linear-gradient(180deg,#f8fbff 0%,#f1f5fb 52%,#eef3f9 100%)!important;color:var(--ink)!important}.block-container{max-width:1240px;padding-top:5rem!important;padding-bottom:4rem}.wf-title{font-size:3.6rem;font-weight:800;letter-spacing:-.055em;line-height:1;color:#0f172a!important;margin:0}.wf-title::after{content:"";display:block;width:74px;height:6px;border-radius:10px;margin-top:16px;background:linear-gradient(90deg,var(--primary),var(--violet),var(--cyan));animation:wfGlow 3s ease-in-out infinite}.wf-subtitle{color:var(--muted)!important;font-size:1.03rem;margin:1.15rem 0 2.5rem}.big{font-size:3.5rem;font-weight:800;letter-spacing:-.05em;background:linear-gradient(90deg,#1d4ed8,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.05;margin:.4rem 0}.muted{color:var(--muted)!important;margin:.45rem 0 1rem}.chart-heading{color:var(--ink)!important;font-size:1.02rem;font-weight:800;margin:1.45rem 0 .18rem}.chart-caption{color:var(--muted)!important;font-size:.78rem;margin-bottom:.65rem}h1,h2,h3,p,label,.stMarkdown{color:var(--ink)!important}h2,h3{letter-spacing:-.025em}[data-testid="stCaptionContainer"] p,[data-testid="stMetricLabel"] p{color:var(--muted)!important}[data-testid="stMetricValue"]{color:var(--ink)!important;font-weight:800!important}
[data-testid="stForm"],[data-testid="stVerticalBlockBorderWrapper"]{background:rgba(255,255,255,.88)!important;border:1px solid rgba(203,213,225,.75)!important;border-radius:20px!important;box-shadow:0 10px 35px rgba(15,23,42,.06),inset 0 1px 0 rgba(255,255,255,.75);backdrop-filter:blur(12px);transition:transform .25s ease,box-shadow .25s ease,border-color .25s ease}[data-testid="stForm"]{padding:22px}[data-testid="stVerticalBlockBorderWrapper"]:hover{transform:translateY(-2px);border-color:#b6c9e5!important;box-shadow:0 16px 38px rgba(15,23,42,.10)}
[data-baseweb="input"]>div,[data-baseweb="select"]>div{background:#fff!important;border-color:#cbd5e1!important;border-radius:12px!important;transition:box-shadow .2s ease,border-color .2s ease}[data-baseweb="input"]>div:focus-within,[data-baseweb="select"]>div:focus-within{border-color:#60a5fa!important;box-shadow:0 0 0 4px rgba(37,99,235,.10)!important}[data-baseweb="input"] input,input{color:var(--ink)!important;-webkit-text-fill-color:var(--ink)!important;background:#fff!important}[data-baseweb="select"] *{color:var(--ink)!important}[data-baseweb="popover"],[role="listbox"],[role="option"]{background:#fff!important;color:var(--ink)!important}[data-testid="stDateInput"] input{color:var(--ink)!important;-webkit-text-fill-color:var(--ink)!important}
.stFormSubmitButton>button,.stButton>button{background:linear-gradient(100deg,#2563eb,#4f46e5)!important;color:#fff!important;border:0!important;border-radius:12px!important;font-weight:700!important;box-shadow:0 8px 18px rgba(37,99,235,.20);transition:transform .18s ease,box-shadow .18s ease,filter .18s ease}.stFormSubmitButton>button p,.stButton>button p{color:#fff!important}.stFormSubmitButton>button:hover,.stButton>button:hover{transform:translateY(-2px);filter:brightness(1.05);box-shadow:0 12px 24px rgba(37,99,235,.28)}.stFormSubmitButton>button:active,.stButton>button:active{transform:translateY(0)}
[data-testid="stSegmentedControl"]{background:#e9eef7!important;border-radius:14px!important;padding:4px!important;box-shadow:inset 0 1px 3px rgba(15,23,42,.06)}[data-testid="stSegmentedControl"] button{background:transparent!important;color:#475569!important;border:0!important;border-radius:10px!important;transition:all .2s ease}[data-testid="stSegmentedControl"] button p{color:#475569!important}[data-testid="stSegmentedControl"] button[aria-pressed="true"]{background:#fff!important;box-shadow:0 5px 12px rgba(15,23,42,.10)!important}[data-testid="stSegmentedControl"] button[aria-pressed="true"] p{color:#1d4ed8!important;font-weight:800!important}
[data-testid="stProgress"]{margin:.7rem 0 1.15rem}[data-testid="stProgress"]>div>div{background:#e2e8f0!important;border-radius:99px!important}[data-testid="stProgress"]>div>div>div{background:linear-gradient(90deg,#2563eb,#7c3aed,#06b6d4)!important;border-radius:99px!important;transition:width .7s cubic-bezier(.2,.8,.2,1)}
[data-testid="stMetric"]{background:linear-gradient(145deg,#fff,#f8fbff);border:1px solid #e1e8f2;border-radius:16px;padding:13px 14px;box-shadow:0 6px 18px rgba(15,23,42,.045);transition:transform .22s ease,box-shadow .22s ease}[data-testid="stMetric"]:hover{transform:translateY(-3px);box-shadow:0 12px 24px rgba(15,23,42,.08)}[data-testid="stAlert"]{background:linear-gradient(110deg,#eff6ff,#eef2ff)!important;color:#173b70!important;border:1px solid #c7d9f7!important;border-radius:14px!important}[data-testid="stAlert"] p{color:#173b70!important}[data-testid="stCheckbox"] label span{color:var(--ink)!important}[data-testid="stVegaLiteChart"]{background:linear-gradient(180deg,#fff,#f8fbff);border:1px solid #dfe7f2;border-radius:18px;padding:10px;box-shadow:0 10px 25px rgba(15,23,42,.05);overflow:hidden}hr{border-color:#dbe4f0!important;margin-top:2rem!important}
@keyframes wfGlow{0%,100%{transform:scaleX(1);opacity:.9}50%{transform:scaleX(1.25);opacity:1}}@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}.block-container>div{animation:fadeUp .45s ease both}@media(max-width:800px){.block-container{padding-top:4.5rem!important}.wf-title{font-size:2.7rem}[data-testid="stMetric"]{padding:10px}.big{font-size:3rem}}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="wf-title">WorkFlow</div>'
    '<div class="wf-subtitle">Mon espace d\'organisation professionnelle</div>',
    unsafe_allow_html=True,
)

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
            st.session_state.tasks.insert(
                0,
                {
                    "id": str(datetime.now().timestamp()),
                    "title": title.strip(),
                    "type": task_type,
                    "date": task_date.isoformat(),
                    "priority": priority,
                    "done": False,
                },
            )
            save_tasks()
            rerun()

with right:
    period = (
        st.segmented_control(
            "Période",
            ["Jour", "Semaine", "Mois", "Année"],
            default="Jour",
        )
        or "Jour"
    )

visible = [t for t in st.session_state.tasks if in_period(t["date"], period)]
done = sum(t["done"] for t in visible)
total = len(visible)
pct = round(done * 100 / total) if total else 0

with right:
    st.subheader("Synthèse")
    st.markdown(
        f'<div class="big">{pct}%</div>'
        '<div class="muted">des tâches terminées</div>',
        unsafe_allow_html=True,
    )
    st.progress(pct / 100 if pct else 0)

    a, b = st.columns(2)
    a.metric("Total", total)
    b.metric("Terminées", done)

    a, b = st.columns(2)
    a.metric("À faire", total - done)
    b.metric(
        "Priorité haute",
        sum(1 for t in visible if t["priority"] == "Haute" and not t["done"]),
    )

    st.markdown(
        '<div class="chart-heading">Performance sur 7 jours</div>'
        '<div class="chart-caption">Évolution quotidienne des tâches terminées</div>',
        unsafe_allow_html=True,
    )
    chart_data = last_7_days_chart_data(st.session_state.tasks)
    st.area_chart(
        chart_data,
        x="Jour",
        y="Terminées",
        color="#2563EB",
        height=235,
    )

    priority_data = {
        "Priorité": ["Haute", "Normale", "Basse"],
        "Tâches": [
            sum(1 for t in visible if t["priority"] == "Haute"),
            sum(1 for t in visible if t["priority"] == "Normale"),
            sum(1 for t in visible if t["priority"] == "Basse"),
        ],
    }
    if sum(priority_data["Tâches"]) > 0:
        st.markdown(
            '<div class="chart-heading">Répartition des priorités</div>'
            '<div class="chart-caption">Charge de travail pour la période sélectionnée</div>',
            unsafe_allow_html=True,
        )
        st.bar_chart(
            priority_data,
            x="Priorité",
            y="Tâches",
            color="#7C3AED",
            height=220,
        )

    if visible:
        counts = {}
        for t in visible:
            counts[t["type"]] = counts.get(t["type"], 0) + 1
        st.caption("Répartition par type")
        for k, v in sorted(counts.items(), key=lambda x: -x[1]):
            st.write(f"{k}: **{v}**")

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
            c2.caption(
                f"{t['date']} · {t['type']} · Priorité {t['priority'].lower()}"
            )

            if c3.button("Supprimer", key="del_" + t["id"]):
                st.session_state.tasks = [
                    x for x in st.session_state.tasks if x["id"] != t["id"]
                ]
                save_tasks()
                rerun()

st.divider()
st.caption("WorkFlow V2 Streamlit")

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
.stApp { background:#f4f7fb !important; color:#172033 !important; }
.block-container { max-width:1200px; padding-top:4.5rem !important; padding-bottom:3rem; }
.wf-title { font-size:3rem; font-weight:800; color:#172033 !important; line-height:1.15; padding-top:.35rem; margin:0 0 .7rem 0; }
.wf-subtitle { color:#667085 !important; margin:0 0 2.25rem 0; line-height:1.5; }
.big { font-size:3rem; font-weight:800; color:#172033 !important; line-height:1.1; margin-top:.35rem; }
.muted { color:#667085 !important; margin:.3rem 0 .8rem; }
.chart-heading { color:#172033; font-size:1rem; font-weight:700; margin:1.25rem 0 .1rem; }
.chart-caption { color:#667085; font-size:.8rem; margin-bottom:.5rem; }
h1,h2,h3,p,label,.stMarkdown { color:#172033 !important; }
[data-testid="stCaptionContainer"] p { color:#667085 !important; }
[data-testid="stMetricLabel"] p { color:#667085 !important; }
[data-testid="stMetricValue"] { color:#172033 !important; }
[data-testid="stForm"] { background:#ffffff !important; border:1px solid #dbe3ee !important; border-radius:16px; padding:20px; }
[data-testid="stVerticalBlockBorderWrapper"] { background:#ffffff !important; border-color:#dbe3ee !important; border-radius:14px !important; }
[data-baseweb="input"] > div, [data-baseweb="select"] > div { background:#ffffff !important; border-color:#cbd5e1 !important; }
[data-baseweb="input"] input, input { color:#172033 !important; -webkit-text-fill-color:#172033 !important; background:#ffffff !important; }
[data-baseweb="select"] * { color:#172033 !important; }
[data-baseweb="popover"], [role="listbox"], [role="option"] { background:#ffffff !important; color:#172033 !important; }
[data-testid="stDateInput"] input { color:#172033 !important; -webkit-text-fill-color:#172033 !important; }
.stFormSubmitButton > button, .stButton > button { background:#2563eb !important; color:#ffffff !important; border:1px solid #2563eb !important; font-weight:700; }
.stFormSubmitButton > button p, .stButton > button p { color:#ffffff !important; }
.stFormSubmitButton > button:hover, .stButton > button:hover { background:#1d4ed8 !important; border-color:#1d4ed8 !important; }
[data-testid="stSegmentedControl"] { background:transparent !important; }
[data-testid="stSegmentedControl"] button { background:#ffffff !important; color:#344054 !important; border-color:#cbd5e1 !important; }
[data-testid="stSegmentedControl"] button p { color:#344054 !important; }
[data-testid="stSegmentedControl"] button[aria-pressed="true"] { background:#2563eb !important; color:#ffffff !important; }
[data-testid="stSegmentedControl"] button[aria-pressed="true"] p { color:#ffffff !important; }
[data-testid="stProgressBar"] > div > div { background:#2563eb !important; }
[data-testid="stAlert"] { background:#eaf2ff !important; color:#173b70 !important; border:1px solid #bfd5fa !important; }
[data-testid="stAlert"] p { color:#173b70 !important; }
[data-testid="stCheckbox"] label span { color:#172033 !important; }
[data-testid="stVegaLiteChart"] { background:#ffffff; border:1px solid #dbe3ee; border-radius:14px; padding:8px; }
hr { border-color:#dbe3ee !important; }
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
        '<div class="chart-heading">Évolution sur 7 jours</div>'
        '<div class="chart-caption">Nombre de tâches terminées par jour</div>',
        unsafe_allow_html=True,
    )
    chart_data = last_7_days_chart_data(st.session_state.tasks)
    st.line_chart(
        chart_data,
        x="Jour",
        y="Terminées",
        color="#2563EB",
        height=230,
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

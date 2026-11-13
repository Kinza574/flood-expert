import streamlit as st
from engine import RULES, facts_from_inputs, run_engine

st.set_page_config(page_title="Monsoon Flood Advisor", page_icon="🌧️")
st.title("🌧️ Monsoon Flood-Risk Advisor")
st.caption(f"Expert system for urban homes in Pakistan  |  {len(RULES)} IF-THEN rules")

with st.form("inputs"):
    st.subheader("Weather")
    rain_mm = st.slider("Expected rainfall in next 24 hours (mm)", 0, 300, 60)
    hours = st.slider("How many hours will it rain?", 1, 24, 4)
    tide_high = st.checkbox("It is high tide (coastal areas)")

    st.subheader("Your area and home")
    area = st.selectbox("Area type", ["Elevated / well-drained", "Low-lying",
                                      "Near a nullah (drain/stream)", "Coastal"])
    floor = st.selectbox("Where do you live?", ["Ground floor", "Basement", "First floor or above"])
    road_level = st.selectbox("Your house compared to the road",
                              ["Higher than the road", "Same level as the road", "Lower than the road"])
    house_type = st.selectbox("House type", ["Pukka (concrete)", "Kacha (mud / weak)"])
    drain = st.selectbox("Drain near your home", ["Clean and working", "Partly blocked",
                                                  "Fully blocked", "Overflows even in light rain"])
    past_flood = st.selectbox("Has your home flooded before?", ["Never", "Once", "Often"])

    st.subheader("Your situation")
    vulnerable = st.checkbox("Children, elderly or sick people live with me")
    vehicle = st.checkbox("My vehicle is parked in a low spot")
    wiring = st.checkbox("I have low or exposed wiring / sockets")
    roof_leak = st.checkbox("My roof leaks")
    kit = st.checkbox("I have an emergency kit")
    water = st.checkbox("I have stored drinking water")
    power = st.checkbox("I have backup power (UPS / torch / power bank)")
    barriers = st.checkbox("I have sandbags or flood barriers")

    go = st.form_submit_button("Check my flood risk", use_container_width=True)

if go:
    answers = dict(rain_mm=rain_mm, hours=hours, tide_high=tide_high, area=area, floor=floor,
                   road_level=road_level, house_type=house_type, drain=drain, past_flood=past_flood,
                   vulnerable=vulnerable, vehicle=vehicle, wiring=wiring, roof_leak=roof_leak,
                   kit=kit, water=water, power=power, barriers=barriers)
    facts, fired, advice, risk = run_engine(facts_from_inputs(answers))

    label = risk.replace("_", " ")
    if risk in ("CRITICAL_RISK", "HIGH_RISK"):
        st.error(f"### 🚨 {label}")
    elif risk == "MODERATE_RISK":
        st.warning(f"### ⚠️ {label}")
    else:
        st.success(f"### ✅ {label}")

    st.subheader("What you should do")
    for a in advice:
        st.markdown(f"- {a}")

    with st.expander(f"Why? ({len(fired)} rules fired)"):
        for r in fired:
            cond = " AND ".join(r.conditions).replace("~", "NOT ")
            out = r.then if r.then else "give advice"
            st.markdown(f"**{r.id}** (stage {r.stage}): IF `{cond}` THEN `{out}`")

with st.expander(f"See the full rule base ({len(RULES)} rules)"):
    for r in RULES:
        cond = " AND ".join(r.conditions).replace("~", "NOT ")
        st.markdown(f"**{r.id}**: IF `{cond}` THEN `{r.then or 'advice'}`")

st.caption("This is a student project for general guidance. In an emergency, call Rescue 1122.")

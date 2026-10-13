import io, math
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd
import streamlit as st

st.set_page_config(page_title="BuildPlan India", page_icon="🏗️", layout="wide")
st.markdown("""
<style>
.block-container{padding-top:1.2rem;max-width:1450px}
.hero{padding:1.25rem 1.5rem;border-radius:16px;background:linear-gradient(120deg,#102a56,#1769aa);color:white;margin-bottom:1rem}
.hero h1{color:white;margin:0}.hero p{color:#e0edff;margin:.35rem 0 0}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>🏗️ BuildPlan India</h1><p>Building planning, structural concept, analysis demo, quantities and costs</p></div>', unsafe_allow_html=True)
st.warning("Educational prototype only. Not for construction or permit approval. A qualified architect/structural engineer must verify current standards, site conditions, soil report, loads, local rules and every design.")

with st.sidebar:
    st.header("Project inputs")
    kind = st.selectbox("Building type", ["Residential house", "Apartment", "Office", "Retail / shop", "School / institutional"])
    area = st.number_input("Built-up area per floor (m²)", 25.0, 10000.0, 120.0, 5.0)
    floors = st.number_input("Number of floors", 1, 30, 3, 1)
    location = st.text_input("Building location", "Hyderabad, Telangana, India")
    plot_l = st.number_input("Approx. footprint length (m)", 5.0, 100.0, 12.0, 0.5)
    plot_w = st.number_input("Approx. footprint width (m)", 5.0, 100.0, 10.0, 0.5)
    preference = st.selectbox("Residential room layout", ["2 bedrooms", "3 bedrooms", "Open-plan / flexible"])
    finish = st.selectbox("Cost scenario", ["Basic", "Standard", "Premium"], index=1)
    contingency = st.slider("Contingency (%)", 0, 25, 10)

total_area = area * floors
aspect = plot_l / plot_w
plan_w = math.sqrt(area * aspect)
plan_h = area / plan_w
rate = {"Basic": 1650, "Standard": 2100, "Premium": 2800}[finish]
labour_share = {"Basic": .28, "Standard": .30, "Premium": .32}[finish]
sqft = total_area * 10.7639
base_cost = sqft * rate
labour = base_cost * labour_share
materials = base_cost - labour
cont_cost = base_cost * contingency / 100
total_cost = base_cost + cont_cost
concrete = total_area * .20
steel = concrete * 100
masonry = total_area * .12
plaster = total_area * 2.8
cement = concrete * 7
sand = concrete * .45
aggregate = concrete * .90

def png(fig):
    b = io.BytesIO()
    fig.savefig(b, format="png", dpi=180, bbox_inches="tight")
    b.seek(0)
    return b.getvalue()

def floorplan():
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.add_patch(Rectangle((0, 0), plan_w, plan_h, fill=False, lw=3, color="#183b63"))
    if kind == "Residential house":
        if preference == "3 bedrooms":
            zones = [(0,plan_h*.5,plan_w*.34,plan_h*.5,"BEDROOM 2"),(plan_w*.34,plan_h*.5,plan_w*.33,plan_h*.5,"BEDROOM 3"),(plan_w*.67,plan_h*.5,plan_w*.33,plan_h*.5,"KITCHEN"),(0,0,plan_w*.34,plan_h*.5,"BEDROOM 1"),(plan_w*.34,0,plan_w*.33,plan_h*.5,"LIVING / DINING"),(plan_w*.67,0,plan_w*.33,plan_h*.5,"BATH / UTILITY")]
        else:
            zones = [(0,plan_h*.5,plan_w*.42,plan_h*.5,"BEDROOM 1"),(plan_w*.42,plan_h*.5,plan_w*.58,plan_h*.5,"KITCHEN"),(0,0,plan_w*.42,plan_h*.5,"BEDROOM 2"),(plan_w*.42,0,plan_w*.58,plan_h*.5,"LIVING / DINING")]
    elif kind in ("Office", "Retail / shop"):
        zones = [(0,0,plan_w*.72,plan_h,"OPEN WORK / SALES"),(plan_w*.72,0,plan_w*.28,plan_h*.5,"SERVICES"),(plan_w*.72,plan_h*.5,plan_w*.28,plan_h*.5,"MEETING / STORE")]
    elif kind == "School / institutional":
        zones = [(0,0,plan_w*.72,plan_h,"CLASS / ACTIVITY"),(plan_w*.72,0,plan_w*.28,plan_h*.5,"SUPPORT"),(plan_w*.72,plan_h*.5,plan_w*.28,plan_h*.5,"CIRCULATION")]
    else:
        zones = [(0,0,plan_w*.5,plan_h*.5,"UNIT A"),(plan_w*.5,0,plan_w*.5,plan_h*.5,"UNIT B"),(0,plan_h*.5,plan_w*.5,plan_h*.5,"UNIT C"),(plan_w*.5,plan_h*.5,plan_w*.5,plan_h*.5,"UNIT D")]
    for x, y, w, h, label in zones:
        ax.add_patch(Rectangle((x, y), w, h, fill=False, lw=1.8, color="#244a72"))
        ax.text(x+w/2, y+h/2, label, ha="center", va="center", fontsize=9, weight="bold", wrap=True)
    ax.plot([plan_w*.05, plan_w*.16], [0, 0], lw=5, color="white")
    ax.plot([plan_w*.05, plan_w*.16], [0, 0], lw=2, color="#16805d")
    ax.text(plan_w*.105, -plan_h*.06, "ENTRY (concept)", ha="center", fontsize=8, color="#16805d")
    ax.set_xlim(-plan_w*.1, plan_w*1.03); ax.set_ylim(-plan_h*.15, plan_h*1.04)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(f"Preliminary room-zoning concept · {kind}", weight="bold")
    fig.tight_layout()
    return fig

def gridfig(nx, ny):
    fig, ax = plt.subplots(figsize=(8, 5))
    xs = [i*plan_w/nx for i in range(nx+1)]
    ys = [j*plan_h/ny for j in range(ny+1)]
    for i, x in enumerate(xs):
        ax.plot([x, x], [0, plan_h], lw=2, color="#3c83b8")
        ax.text(x, -plan_h*.04, chr(65+i), ha="center")
    for j, y in enumerate(ys):
        ax.plot([0, plan_w], [y, y], lw=2, color="#3c83b8")
        ax.text(-plan_w*.03, y, str(j+1), ha="right", va="center")
    for x in xs:
        for y in ys:
            ax.scatter(x, y, s=75, marker="s", color="#173d68")
    ax.set_xlim(-plan_w*.1, plan_w*1.04); ax.set_ylim(-plan_h*.1, plan_h*1.05)
    ax.set_aspect("equal"); ax.set_xlabel("Concept length (m)"); ax.set_ylabel("Concept width (m)")
    ax.set_title("Conceptual column / beam grid — not for construction")
    ax.grid(alpha=.15); fig.tight_layout()
    return fig

tabs = st.tabs(["Overview", "1 · Inputs", "2 · Planning", "3 · Structural layout", "4 · Analysis", "5 · Design & Indian standards", "6 · Quantities", "7 · Cost", "8 · Final output"])
with tabs[0]:
    st.subheader("Project dashboard")
    a,b,c,d = st.columns(4)
    a.metric("Total built-up area", f"{total_area:,.1f} m²")
    b.metric("Floors", int(floors))
    c.metric("Indicative cost", f"₹{total_cost:,.0f}")
    d.metric("Location", location.split(",")[0] if location else "Not entered")
    for title, desc in [("01 · Inputs","Building type, area, floors and location"),("02 · Planning","Room-zoning drawing"),("03 · Structural layout","Conceptual column / beam grid"),("04 · Analysis","Standalone beam SFD and BMD"),("05 · Design","Standards checklist and professional verification"),("06 · Quantities","Rough material allowances"),("07 · Cost","Scenario estimate and contingency"),("08 · Output","Download report, CSV and PNG drawings")]:
        st.markdown(f"**{title}** — {desc}")
    st.caption("Rule-based prototype, not a generative AI model or whole-building structural analysis engine.")
with tabs[1]:
    st.subheader("Project input summary")
    summary = pd.DataFrame([["Building type",kind],["Location",location],["Area per floor",f"{area:.1f} m²"],["Number of floors",int(floors)],["Total built-up area",f"{total_area:.1f} m²"],["Finish scenario",finish]], columns=["Input","Value"])
    st.dataframe(summary, use_container_width=True, hide_index=True)
    st.info("The app does not infer local approvals or hazard parameters from the location string. Verify the actual jurisdiction and site-specific conditions.")
with tabs[2]:
    st.subheader("2 · Preliminary planning")
    st.write(f"Concept zoning for **{kind}** in **{location}**.")
    fp = floorplan(); st.pyplot(fp); st.download_button("Download floor plan concept (PNG)", png(fp), "concept_floor_plan.png", "image/png"); plt.close(fp)
    st.caption("Schematic zoning only; it does not verify setbacks, windows, ventilation, accessibility, fire escape or permit requirements.")
with tabs[3]:
    st.subheader("3 · Structural layout")
    gx = st.slider("Grid bays along length", 2, 6, 3); gy = st.slider("Grid bays along width", 2, 5, 2)
    gf = gridfig(gx, gy); st.pyplot(gf); st.download_button("Download structural grid (PNG)", png(gf), "concept_structural_grid.png", "image/png"); plt.close(gf)
    st.caption("Grid dots represent conceptual column locations and lines represent schematic beam axes. No member or foundation sizes are designed.")
with tabs[4]:
    st.subheader("4 · Structural analysis demo")
    st.warning("Standalone textbook beam example only; it is not connected to the building grid above.")
    c1, c2 = st.columns(2)
    L = c1.slider("Simply supported span (m)", 2.0, 10.0, 4.0, .5); w = c2.slider("Uniform load (kN/m)", 1.0, 40.0, 10.0, 1.0)
    x = [i*L/300 for i in range(301)]; R = w*L/2; V = [R-w*z for z in x]; M = [R*z-w*z*z/2 for z in x]
    a,b,c = st.columns(3); a.metric("Reaction each end", f"{R:.2f} kN"); b.metric("Max shear magnitude", f"{R:.2f} kN"); c.metric("Max moment", f"{w*L*L/8:.2f} kN·m")
    fig, ax = plt.subplots(figsize=(8,3)); ax.plot(x,V); ax.axhline(0,color="black",lw=.7); ax.fill_between(x,V,0,alpha=.15); ax.set(title="Shear force diagram (SFD)",xlabel="Distance (m)",ylabel="Shear (kN)"); ax.grid(alpha=.2); st.pyplot(fig); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8,3)); ax.plot(x,M,color="#c94747"); ax.axhline(0,color="black",lw=.7); ax.fill_between(x,M,0,alpha=.15,color="#c94747"); ax.set(title="Bending moment diagram (BMD)",xlabel="Distance (m)",ylabel="Moment (kN·m)"); ax.grid(alpha=.2); st.pyplot(fig); plt.close(fig)
    st.markdown("Formulas: reactions = wL/2; maximum moment = wL²/8. No whole-building analysis or deflection calculation is provided.")
with tabs[5]:
    st.subheader("5 · Design notes and standards checklist")
    st.markdown("""
| Reference | Topic | Prototype status |
|---|---|---|
| National Building Code of India (NBC) | Planning and safety framework | Reference checklist only |
| IS 456 | Plain/reinforced concrete | No complete code checks |
| Applicable IS 875 parts | Dead, imposed and wind loads | No project load schedule |
| Applicable IS 1893 provisions | Earthquake-resistant design | No site-specific seismic analysis |
| IS 13920 where applicable | Ductile detailing | Not implemented |
| Relevant foundation standards | Foundations | Requires geotechnical report |
| IS 1200 series where applicable | Quantity measurement | Rough allowances only |
| Telangana/local authority rules | Local planning approvals | Must be checked for actual site |
""")
    st.error("No construction-ready reinforcement or member sizes are generated. Verify current editions/amendments and jurisdiction with official sources and qualified professionals.")
    st.markdown("[Bureau of Indian Standards — National Building Code](https://www.bis.gov.in/standards/national-building-code/?lang=en)")
with tabs[6]:
    st.subheader("6 · Rough quantity estimation")
    qdf = pd.DataFrame([["RCC concrete",round(concrete,2),"m³","0.20 m³/m² total area"],["Reinforcing steel",round(steel,0),"kg","100 kg/m³ concrete"],["Masonry",round(masonry,2),"m³","0.12 m³/m² total area"],["Plaster allowance",round(plaster,2),"m²","2.8 m²/m² total area"],["Cement allowance",round(cement,0),"bags","7 bags/m³ concrete; not mix design"],["Sand allowance",round(sand,2),"m³","0.45 m³/m³ concrete"],["Aggregate allowance",round(aggregate,2),"m³","0.90 m³/m³ concrete"]], columns=["Item","Estimated quantity","Unit","Assumption"])
    st.dataframe(qdf, use_container_width=True, hide_index=True); st.download_button("Download quantities CSV", qdf.to_csv(index=False), "quantity_estimate.csv", "text/csv")
    st.caption("Not a measured BOQ. Real quantities require drawings, specifications, openings, mix design, waste factors and a measurement standard.")
with tabs[7]:
    st.subheader("7 · Indicative cost estimate")
    cdf = pd.DataFrame([["Materials allowance",materials],["Labour allowance",labour],["Base estimate",base_cost],[f"Contingency ({contingency}%)",cont_cost],["TOTAL scenario estimate",total_cost]], columns=["Cost item","Amount (INR)"])
    st.dataframe(cdf.style.format({"Amount (INR)":"₹{:,.0f}"}), use_container_width=True, hide_index=True)
    st.metric("Estimated total", f"₹{total_cost:,.0f}")
    st.caption(f"Assumed scenario rate: ₹{rate:,}/sq ft × {sqft:,.0f} sq ft. Not a verified current local quotation; confirm with contractors and suppliers.")
with tabs[8]:
    st.subheader("8 · Final output package")
    report = f"""BUILDPLAN INDIA — PRELIMINARY PROJECT SUMMARY
Generated: {date.today().isoformat()}
Building type: {kind}
Location: {location}
Area per floor: {area:.2f} m²
Floors: {int(floors)}
Total built-up area: {total_area:.2f} m²
Finish scenario: {finish}

ROUGH QUANTITY ALLOWANCES — NOT A BOQ
Concrete: {concrete:.2f} m³
Steel: {steel:.0f} kg
Masonry: {masonry:.2f} m³
Plaster: {plaster:.2f} m²
Cement allowance: {cement:.0f} bags
Sand: {sand:.2f} m³
Aggregate: {aggregate:.2f} m³

INDICATIVE COST SCENARIO
Base estimate: INR {base_cost:.0f}
Materials allowance: INR {materials:.0f}
Labour allowance: INR {labour:.0f}
Contingency: INR {cont_cost:.0f}
Total: INR {total_cost:.0f}

STANDARDS TO VERIFY
NBC India; IS 456; applicable IS 875 parts; applicable IS 1893 provisions;
IS 13920 where applicable; relevant foundation standards; IS 1200 series where applicable;
and current Telangana/local authority rules for the actual site.

LIMITATIONS
Educational prototype only. Drawings are conceptual; beam analysis is a standalone textbook example.
Quantities/costs are rough assumptions. No safety or code compliance is certified.
Not for construction, tendering or permits. A qualified architect and structural engineer must verify
current standards, site conditions, soil report, loads, drawings and calculations.
"""
    st.download_button("Download project report (TXT)", report, "buildplan_project_report.txt", "text/plain")
    st.download_button("Download quantities (CSV)", qdf.to_csv(index=False), "buildplan_quantities.csv", "text/csv")
    fp = floorplan(); st.download_button("Download floor-plan drawing (PNG)", png(fp), "concept_floor_plan.png", "image/png"); plt.close(fp)
    gf = gridfig(3,2); st.download_button("Download structural-grid drawing (PNG)", png(gf), "concept_structural_grid.png", "image/png"); plt.close(gf)
    st.success("Downloadable concept package is ready. These are preliminary planning artifacts, not approved construction documents.")
st.divider()
st.caption("BuildPlan India v3 · Verify current BIS standards and local authority requirements before professional use.")

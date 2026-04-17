import streamlit as st
import pandas as pd
from fpdf import FPDF
import requests
from io import BytesIO
from datetime import date
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go 

# --- 1. قاعدة بيانات المشاريع ---
PROJECTS_DATABASE = {
    "SILA MASDAR": {"url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=0&single=true&output=csv", "gov_pct": 2.0, "admin_fees": 625, "res_fee": 20000},
    "KHALIFA CITY": {"url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=1491192679&single=true&output=csv", "gov_pct": 1.0, "admin_fees": 625, "res_fee": 20000},
    "SENSI": {"url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=1661552566&single=true&output=csv", "gov_pct": 2.0, "admin_fees": 625, "res_fee": 50000},
    "RHILLS": {"url":"https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=517225281&single=true&output=csv", "gov_pct": 4.0, "admin_fees": 1194, "res_fee": 20000},
    "Reportage Oceana": {"url":"https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=557415114&single=true&output=csv", "gov_pct": 2.5, "admin_fees": 5350, "res_fee": 20000},
    "BAIA-RAHA": {"url":"https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=2096076774&single=true&output=csv", "gov_pct": 2, "admin_fees": 625, "res_fee": 50000},
    "TAORMINA1 and TAORMINA2": {"url":"https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=689409724&single=true&output=csv", "gov_pct": 4.0, "admin_fees": 1194, "res_fee": 20000},
    "BRABUS": {"url":"https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=523704081&single=true&output=csv", "gov_pct": 2.0, "admin_fees": 625, "res_fee": 50000},
    "BRABUSTH": {"url":"https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=56857260&single=true&output=csv", "gov_pct": 2.0, "admin_fees": 625, "res_fee": 100000},
    "VERDANA 6W & 6X & 6Y": {"url":"https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=688428190&single=true&output=csv", "gov_pct": 4.0, "admin_fees": 1194, "res_fee": 20000},
    "VERDANA N TH": {"url":"https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=1654006326&single=true&output=csv", "gov_pct": 4.0, "admin_fees": 1194, "res_fee": 20000},
    "VERDANA N R": {"url":"https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=1593282205&single=true&output=csv", "gov_pct": 4.0, "admin_fees": 1194, "res_fee": 20000},
    "VERDANA 10 R": {"url":"https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=833822872&single=true&output=csv", "gov_pct": 4.0, "admin_fees": 1194, "res_fee": 20000},
    "VERDANA 9 R": {"url":"https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=1641737645&single=true&output=csv", "gov_pct": 4.0, "admin_fees": 1194, "res_fee": 20000},
    "VERDANA 8 R": {"url":"https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=2138617608&single=true&output=csv", "gov_pct": 4.0, "admin_fees": 1194, "res_fee": 20000},
    "VERDANA 7 R": {"url":"https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=1423929833&single=true&output=csv", "gov_pct": 4.0, "admin_fees": 1194, "res_fee": 20000},
    "VERDANA 6 R": {"url":"https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=290574832&single=true&output=csv", "gov_pct": 4.0, "admin_fees": 1194, "res_fee": 20000},
    "VERDANA 5 R": {"url":"https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=1269333085&single=true&output=csv", "gov_pct": 4.0, "admin_fees": 1194, "res_fee": 20000}
}

PHOTO_BANK_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSLDSBkzA1ZpD1qCRFjl4TiNWldYobalUdgwADyljTFkWMJrvVXajgFxegKWDr2SA-UcuAc8mGonW36/pub?gid=1714647206&single=true&output=csv"
LOGO_URL = "https://i.ibb.co/N2SSy8kX/ICON-BLACK.jpg"

ALL_PLANS = {
    "30% DP / 5% Disc / 70% Handover": {"dp_pct": 30, "disc": 5, "default_monthly": 0.0},
    "30% DP / 0% Disc / 70% Handover": {"dp_pct": 30, "disc": 0, "default_monthly": 0.0},



    "5% DP / 5% Disc / 1% Monthly": {"dp_pct": 5, "disc": 5, "default_monthly": 1.0},



    "5% DP / 0% Disc / 1% Monthly": {"dp_pct": 5, "disc": 0, "default_monthly": 1.0},



    "5% DP / 2.5% Disc / 1% Monthly": {"dp_pct": 5, "disc": 2.5, "default_monthly": 1.0},



    "10% DP / 5% Disc / 1% Monthly": {"dp_pct": 10, "disc": 5, "default_monthly": 1.0},
    "10% DP / 0% Disc / 1% Monthly": {"dp_pct": 10, "disc": 0, "default_monthly": 1.0},



    "20% DP / 15% Disc / 1% Monthly": {"dp_pct": 20, "disc": 15, "default_monthly": 1.0},
    "20% DP / 5% Disc / 1% Monthly": {"dp_pct": 20, "disc": 5, "default_monthly": 1.0},



    "10% DP / 10% Disc / 1% Monthly": {"dp_pct": 10, "disc": 10, "default_monthly": 1.0},



    "20% DP / 10% Disc / 1% Monthly": {"dp_pct": 20, "disc": 10, "default_monthly": 1.0},



    "30% DP / 15% Disc / 1% Monthly": {"dp_pct": 30, "disc": 15, "default_monthly": 1.0},
    "30% DP / 10% Disc / 1% Monthly": {"dp_pct": 30, "disc": 10, "default_monthly": 1.0},



    "20% DP / 80% Handover (No Disc)": {"dp_pct": 20, "disc": 0, "default_monthly": 0.0},



    "20% DP / 2% Disc / 10%@12m / 70% HO": {"dp_pct": 20, "disc": 2, "default_monthly": 0.0, "is_special": True},



    "25% Discount Cash": {"dp_pct": 100, "disc": 25, "default_monthly": 0.0},



    "30% Discount Cash": {"dp_pct": 100, "disc": 30, "default_monthly": 0.0},
    "35% Discount Cash": {"dp_pct": 100, "disc": 35, "default_monthly": 0.0},



    "18% Discount Cash": {"dp_pct": 100, "disc": 18, "default_monthly": 0.0},



    "No discount (Full in 1 month)": {"dp_pct": 100, "disc": 0, "default_monthly": 0.0},



    "40% DISCOUNT Plan 12 (Cash 40% Disc)": {"dp_pct": 100, "disc": 40, "default_monthly": 0.0}


}

# --- Functions ---
@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except: return None

def get_handover_date(unit_data):
    for col in ['Handover Date', 'Handover', 'Completion']:
        val = unit_data.get(col)
        if val and str(val).lower() != 'nan':
            try: return pd.to_datetime(val).date()
            except: continue
    return date(2028, 12, 31)

def calculate_schedule(selling_price, plan_cfg, settings, start_date, handover_date, res_fee):
    plan = [{"Milestone": "Reservation", "Date": "Now", "Percent": "-", "Amount": res_fee}]
    dp_val = (selling_price * (plan_cfg['dp_pct'] / 100)) - res_fee
    if dp_val > 0:
        plan.append({"Milestone": "Down Payment", "Date": start_date.strftime("%b-%y"), "Percent": f"{plan_cfg['dp_pct']}%", "Amount": dp_val})
    
    curr_d = start_date + relativedelta(months=1)
    monthly_amt = selling_price * (settings['monthly_pct'] / 100)
    total_paid = res_fee + max(0, dp_val)
    
    while curr_d < handover_date and total_paid < (selling_price * 0.9):
        if monthly_amt > 0:
            plan.append({"Milestone": "Monthly", "Date": curr_d.strftime("%b-%y"), "Percent": f"{settings['monthly_pct']}%", "Amount": monthly_amt})
            total_paid += monthly_amt
        curr_d += relativedelta(months=1)
    
    plan.append({"Milestone": "Handover", "Date": handover_date.strftime("%b-%y"), "Percent": "Balance", "Amount": selling_price - total_paid})
    return plan

# --- App UI ---
st.set_page_config(page_title="Reportage Smart Agent", layout="wide")
st.title("🏗️ Reportage Sales AI")

with st.sidebar:
    st.header("⚙️ Configuration")
    comparison_mode = st.toggle("🔄 Activate Comparison Mode", value=False)
    project_name = st.selectbox("Select Project:", list(PROJECTS_DATABASE.keys()))
    df_inv = load_data(PROJECTS_DATABASE[project_name]["url"])
    df_photos = load_data(PHOTO_BANK_URL)
    selected_plan = st.selectbox("Payment Plan:", list(ALL_PLANS.keys()))
    m_pct = st.number_input("Monthly %", 0.0, 5.0, float(ALL_PLANS[selected_plan]["default_monthly"]))

if df_inv is not None:
    if not comparison_mode:
        unit_id = st.selectbox("Select Unit:", df_inv['Plot + Unit No.'].unique())
        u_data = df_inv[df_inv['Plot + Unit No.'] == unit_id].iloc[0]
        
        # الحسابات
        price = float(str(u_data['Original Price (AED)']).replace(',', ''))
        disc = ALL_PLANS[selected_plan]['disc']
        selling_price = price * (1 - disc/100)
        
        st.divider()
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.metric("Final Price", f"{selling_price:,.0f} AED")
            # عرض صورة الـ Unit Type
            if df_photos is not None:
                bed = str(u_data.get('Bedrooms', '')).replace('.0', '').strip()
                match = df_photos[df_photos['Project'].astype(str).str.contains(project_name.split()[0], case=False)]
                match = match[match['Bedrooms'].astype(str).str.contains(bed)]
                if not match.empty:
                    st.image(match.iloc[0]['Layout_URL'], caption=f"Layout for {bed} Bedroom", width='stretch')
                else:
                    st.info("📷 Layout image not found in database for this type.")

        with col2:
            # الرسم البياني (تم تحديثه ليعمل 100%)
            fig = go.Figure(go.Pie(labels=['Selling Price', 'Discount'], values=[selling_price, price-selling_price], hole=.3))
            fig.update_layout(height=300, margin=dict(l=0, r=0, b=0, t=0))
            st.plotly_chart(fig, width='stretch')

        # الجدول
        sched = calculate_schedule(selling_price, ALL_PLANS[selected_plan], {'monthly_pct': m_pct}, date.today(), get_handover_date(u_data), PROJECTS_DATABASE[project_name]["res_fee"])
        st.subheader("📅 Payment Schedule")
        st.table(pd.DataFrame(sched))

    else:
        # وضع المقارنة
        st.subheader("🔄 Units Comparison")
        u1 = st.selectbox("Unit 1:", df_inv['Plot + Unit No.'].unique())
        u2 = st.selectbox("Unit 2:", df_inv['Plot + Unit No.'].unique())
        
        d1 = df_inv[df_inv['Plot + Unit No.'] == u1].iloc[0]
        d2 = df_inv[df_inv['Plot + Unit No.'] == u2].iloc[0]
        
        p1 = float(str(d1['Original Price (AED)']).replace(',', ''))
        p2 = float(str(d2['Original Price (AED)']).replace(',', ''))
        
        fig_comp = go.Figure(data=[
            go.Bar(name='Original Price', x=[u1, u2], y=[p1, p2]),
            go.Bar(name='Discounted Price', x=[u1, u2], y=[p1*0.9, p2*0.9])
        ])
        st.plotly_chart(fig_comp, width='stretch')

else:
    st.error("Connection Error: Check your internet or Google Sheet links.")

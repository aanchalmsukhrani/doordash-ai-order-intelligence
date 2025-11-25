import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/predict-eta"

st.set_page_config(page_title="Smart Delivery ETA", layout="wide")

# ----- Custom CSS to make it feel app-like -----
st.markdown(
    """
    <style>
    body {
        background-color: #f6f6f6;
    }
    .main .block-container {
        max-width: 980px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 1.5rem 1.75rem;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.07);
        border: 1px solid #f1f1f1;
    }
    .eta-card {
        background: linear-gradient(135deg, #ffe9e5, #ffffff);
        border-radius: 16px;
        padding: 1.75rem 1.75rem 1.5rem 1.75rem;
        box-shadow: 0 10px 24px rgba(148, 27, 12, 0.18);
        border: 1px solid #ffd3c8;
    }
    .page-title {
        font-size: 1.8rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .brand-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.85rem;
        padding: 0.25rem 0.8rem;
        border-radius: 999px;
        background-color: #fff3f0;
        color: #b42318;
        font-weight: 600;
    }
    .section-subtitle {
        font-size: 0.95rem;
        color: #6b7280;
        margin-top: 0.25rem;
    }
    .status-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    .status-low {
        background-color: #ecfdf3;
        color: #166534;
        border: 1px solid #bbf7d0;
    }
    .status-high {
        background-color: #fef2f2;
        color: #b91c1c;
        border: 1px solid #fecaca;
    }
    .eta-number {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin-bottom: 0.1rem;
    }
    .eta-label {
        font-size: 0.95rem;
        color: #4b5563;
    }
    .eta-meta {
        font-size: 0.85rem;
        color: #6b7280;
        margin-top: 0.4rem;
    }
    .stButton>button {
        border-radius: 999px;
        padding: 0.4rem 1.4rem;
        background: #f9735b;
        color: white;
        border: none;
        font-weight: 600;
        font-size: 0.95rem;
    }
    .stButton>button:hover {
        background: #ea4b33;
        color: white;
    }
    .field-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #4b5563;
    }
    .hint {
        font-size: 0.78rem;
        color: #9ca3af;
        margin-top: -0.35rem;
        margin-bottom: 0.1rem;
    }
    hr {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 0.6rem 0 1rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----- Header -----
col_logo, col_meta = st.columns([3, 1], gap="small")

with col_logo:
    st.markdown(
        """
        <div class="page-title">
            <span>🚗 Smart Delivery ETA</span>
        </div>
        <div class="section-subtitle">
            Live ETA & delay risk for a DoorDash-style food delivery order.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_meta:
    st.markdown(
        """
        <div style="display:flex;justify-content:flex-end;">
          <div class="brand-pill">● LIVE demo</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")  # spacer

left, right = st.columns([1.1, 0.9], gap="large")

# ----- LEFT: Order context -----
with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Order context")
    st.caption("Tune these to simulate different delivery situations (peak vs off-peak, rain, etc.).")

    with st.form("eta_form"):
        st.markdown('<span class="field-label">Trip details</span>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            distance_km = st.slider("Distance from restaurant (km)", 0.5, 15.0, 3.0, 0.1)
            st.markdown('<p class="hint">Approximate straight-line distance.</p>', unsafe_allow_html=True)
        with col_b:
            estimated_travel_time_min = st.slider("Estimated travel time (min)", 5.0, 40.0, 16.0, 0.5)
            st.markdown('<p class="hint">Rough time driver spends on road.</p>', unsafe_allow_html=True)

        st.markdown("---", unsafe_allow_html=True)

        st.markdown('<span class="field-label">Restaurant & time</span>', unsafe_allow_html=True)
        col_c, col_d = st.columns(2)
        with col_c:
            prep_time_min = st.slider("Restaurant prep time (min)", 5, 40, 18, 1)
        with col_d:
            hour_of_day = st.slider("Local time (0–23h)", 0, 23, 19, 1)
            day_of_week = st.selectbox(
                "Day of week",
                options=list(range(7)),
                index=5,
                format_func=lambda x: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][x],
            )

        st.markdown("---", unsafe_allow_html=True)

        st.markdown('<span class="field-label">Conditions</span>', unsafe_allow_html=True)
        col_e, col_f = st.columns(2)
        with col_e:
            is_raining = st.selectbox(
                "Weather",
                options=[0, 1],
                format_func=lambda x: "🌧️ Raining" if x == 1 else "☀️ Clear / Dry",
            )
        with col_f:
            courier_experience = st.selectbox(
                "Courier experience",
                options=[0, 1, 2],
                format_func=lambda x: {0: "New dasher", 1: "Regular", 2: "Expert"}[x],
            )

        st.write("")
        submitted = st.form_submit_button("Track my order")

    st.markdown("</div>", unsafe_allow_html=True)

# ----- RIGHT: ETA card -----
with right:
    st.markdown('<div class="eta-card">', unsafe_allow_html=True)

    st.markdown("#### When should this order arrive?")
    st.caption("We estimate the delivery time and whether this order is at risk of being late.")

    if submitted:
        payload = {
            "distance_km": distance_km,
            "prep_time_min": prep_time_min,
            "estimated_travel_time_min": estimated_travel_time_min,
            "hour_of_day": hour_of_day,
            "day_of_week": day_of_week,
            "is_raining": is_raining,
            "courier_experience": courier_experience,
        }

        with st.spinner("Talking to the ETA service…"):
            try:
                resp = requests.post(API_URL, json=payload, timeout=5)
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                st.error(f"Something went wrong while predicting ETA: {e}")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                eta = data["predicted_eta_min"]
                delay_prob = data["delay_probability"]
                risk_tag = data["risk_tag"]

                st.markdown(
                    f"""
                    <div style="margin-top:0.6rem;">
                        <div class="eta-number">{eta:.1f} min</div>
                        <div class="eta-label">Estimated arrival for this order</div>
                        <div class="eta-meta">
                            Based on distance, prep time, time of day, weather, and courier experience.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Status chip
                if risk_tag == "high_delay_risk":
                    st.markdown(
                        f"""
                        <div class="status-chip status-high">
                            <span>⚠️ High chance of delay</span>
                            <span>({delay_prob*100:.1f}% likelihood)</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.write("")
                    st.write(
                        "We’d flag this order to ops and proactively update the customer’s ETA "
                        "or send a small make-good credit."
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="status-chip status-low">
                            <span>✅ On-time likely</span>
                            <span>({delay_prob*100:.1f}% chance of delay)</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.write("")
                    st.write(
                        "We’re confident this order will arrive close to the promised time. "
                        "No additional action is needed from support."
                    )
    else:
        st.write("")
        st.info(
            "Use the controls on the left to simulate different delivery scenarios — "
            "busy Friday nights, rainy days, new vs expert dashers — and see how ETA & "
            "delay risk respond."
        )

    st.markdown("</div>", unsafe_allow_html=True)

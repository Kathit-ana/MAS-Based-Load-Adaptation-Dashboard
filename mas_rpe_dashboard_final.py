
# MAS-RPE Load Adaptation Analysis with Interpretation & Dashboard (Streamlit-compatible)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load the dataset
df = pd.read_excel("mas_rpe_dataset_scientific_ratios.xlsx")
df['session_date'] = pd.to_datetime(df['session_date'])
df['week'] = df['session_date'].dt.isocalendar().week

# Streamlit UI setup
st.title("MAS-Based Load Adaptation Dashboard")
st.markdown("Use this dashboard to analyze MAS-based interval training and make data-driven coaching decisions.")

# Athlete filter
selected_athlete = st.selectbox("Select Athlete", df['athlete_id'].unique())
athlete_df = df[df['athlete_id'] == selected_athlete]

# --- Plot 1: RPE over Time ---
st.subheader("📈 RPE Trend Over Time")
st.line_chart(athlete_df[['session_date', 'RPE']].set_index('session_date'))

# --- Plot 2: %MAS vs RPE ---
st.subheader("🎯 %MAS vs RPE")
fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.scatterplot(data=athlete_df, x='%MAS_target', y='RPE', hue='interval_duration', ax=ax1, s=100)
ax1.set_xlabel('%MAS Target')
ax1.set_ylabel('RPE')
ax1.set_title('%MAS vs. RPE')
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig1)

# --- Work-to-Rest Ratio Overview ---
st.subheader("⚖️ Work:Rest Ratio")
avg_wr_ratio = athlete_df['work_rest_ratio'].mean()
st.metric("Average Work:Rest Ratio", f"{avg_wr_ratio:.2f}")

# --- Plot 3: Total Work Time vs RPE ---
st.subheader("💪 Total Work Volume vs RPE")
fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.scatterplot(data=athlete_df, x='total_work_time_min', y='RPE', hue='%MAS_target', ax=ax2, s=100)
ax2.set_xlabel('Total Work Time (min)')
ax2.set_ylabel('RPE')
ax2.set_title('Work Volume vs RPE')
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig2)

# --- Interpretation Summary ---
st.subheader("🧠 Interpretation")
def interpret_rpe_trend(df):
    trend = df.sort_values('session_date')
    rpe_change = trend['RPE'].iloc[-1] - trend['RPE'].iloc[0]
    avg_work = trend['total_work_time_min'].mean()

    if rpe_change >= 2 and avg_work > 15:
        return "🔺 RPE is increasing with high volume — athlete may be overloaded. Consider deloading."
    elif rpe_change >= 2 and avg_work <= 15:
        return "⚠️ RPE is increasing but volume is low — likely high-intensity sessions. Monitor recovery."
    elif rpe_change <= -2:
        return "🟢 RPE is decreasing — athlete likely adapting well. Progression possible."
    else:
        return "⚖️ RPE stable — maintain current load. Minor adjustments based on sport context."

st.info(interpret_rpe_trend(athlete_df))

# --- Coach Report Overview ---
st.subheader("📋 Adaptation Summary Report")
report_lines = []
for athlete in df['athlete_id'].unique():
    athlete_data = df[df['athlete_id'] == athlete].sort_values('session_date')
    change = athlete_data['RPE'].iloc[-1] - athlete_data['RPE'].iloc[0]
    avg_work = athlete_data['total_work_time_min'].mean()
    if change >= 2 and avg_work > 15:
        status = "Overreaching – needs deload"
    elif change >= 2 and avg_work <= 15:
        status = "High-intensity effort – monitor closely"
    elif change <= -2:
        status = "Adapting – respond well"
    else:
        status = "Stable – monitor"
    report_lines.append(f"{athlete}: {status} (Δ RPE = {change:.1f})")

for line in report_lines:
    st.markdown(f"- {line}")

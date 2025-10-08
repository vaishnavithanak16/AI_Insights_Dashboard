import streamlit as st
import pandas as pd
from openai import OpenAI

# 🌟 PAGE SETUP
st.set_page_config(page_title="AI Insights Dashboard", layout="wide")
st.title("🤖 AI-Generated Insights Dashboard")
st.caption("Upload a CSV file — watch AI summarize trends, anomalies, and key findings.")

# 🔑 INITIALIZE CLIENT (use your real key here)
client = OpenAI(api_key="your_api_secret_key")

# 📂 FILE UPLOAD
uploaded_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])

if uploaded_file:
    # 🧹 READ & PREVIEW DATA
    df = pd.read_csv(uploaded_file)
    st.subheader("👀 Data Preview")
    st.dataframe(df.head())

    # 🧩 CREATE SUMMARY
    data_summary = df.describe(include="all").to_string()

    prompt = f"""
    You are a senior data analyst. Analyze the dataset summary below and write
    5 short, useful insights that describe key trends, anomalies, or recommendations.

    Dataset Summary:
    {data_summary}
    """

    # 🚀 GENERATE INSIGHTS
    if st.button("✨ Generate AI Insights"):
        with st.spinner("Analyzing with GPT..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert data analyst who explains data clearly."},
                        {"role": "user", "content": prompt}
                    ]
                )
                insights = response.choices[0].message.content
                st.success("Here are your AI-Generated Insights:")
                st.write(insights)
            except Exception as e:
                st.error(f"⚠️ Error generating insights: {e}")
else:
    st.info("👆 Upload a CSV file to begin.")

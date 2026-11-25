import streamlit as st
from groq import Groq
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

# Clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

st.set_page_config(page_title="🏢 Corporate Intelligence Tool", layout="wide")
st.title("🏢 Corporate Intelligence Tool")
st.markdown("Enter a company name to research it using AI!")

company_name = st.text_input("Company Name", placeholder="e.g. Blinkit, Swiggy, Zomato")

if st.button("Research Company") and company_name:
    with st.spinner(f"Researching {company_name}..."):
        
        prompt = f"""You are a Corporate Intelligence Analyst. Research the company: {company_name}
        
Return the following details in a structured format:
- Company Overview
- Founded Year
- Headquarters
- CEO Name
- Annual Revenue (approx)
- Key Competitors (list 3-5)
- Tech Stack (list 3-5 technologies)
- AI/ML Adoption level and examples
- Company Valuation
- Key Competitive Advantages (list 2-3)

Be concise and factual."""

        response = groq_client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = response.choices[0].message.content
        
        # Save to Supabase
        supabase.table("companies").insert({
            "company_name": company_name,
            "overview": result
        }).execute()
        
        st.success(f"✅ {company_name} researched and saved!")
        st.markdown(result)

# Show saved companies
st.divider()
st.subheader("📊 Previously Researched Companies")
data = supabase.table("companies").select("company_name, created_at").execute()
if data.data:
    for row in data.data:
        st.write(f"✓ {row['company_name']} — {row['created_at'][:10]}")
else:
    st.info("No companies researched yet.")
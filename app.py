"""
हिंदी वित्त सलाहकार - LangChain Multi-Agent Finance Advisor
LangChain-powered Hindi Finance Advisor using Qwen 2.5-7B
"""

import streamlit as st
from calc import calculate_sip, format_inr
from llm import get_llm
from agents import run_multi_agent_flow
from utils import save_conversation


# ============================================================================
# 🎨 PAGE CONFIGURATION
# ============================================================================

st.set_page_config(page_title="हिंदी वित्त सलाहकार", page_icon="💰", layout="wide")


# ============================================================================
# 🧠 LLM INITIALIZATION
# ============================================================================

@st.cache_resource
def initialize_llm():
    """Initialize and cache Qwen 2.5-7B LLM."""
    try:
        return get_llm(repo_id="Qwen/Qwen2.5-7B-Instruct", temperature=0.7, max_tokens=512)
    except ValueError as e:
        st.error(f"⚠️ {str(e)}")
        st.info("कृपया .env में HUGGINGFACEHUB_API_TOKEN जोड़ें")
        st.info("Token: https://huggingface.co/settings/tokens")
        st.stop()
    except Exception as e:
        st.error(f"❌ LLM initialization error: {e}")
        st.stop()


# ============================================================================
# 🖥 STREAMLIT UI
# ============================================================================

def main():
    """Main application function"""
    
    st.title("💰 हिंदी वित्त सलाहकार")
    st.subheader("बहु-एजेंट प्रणाली के साथ व्यक्तिगत वित्तीय योजना")
    
    st.markdown("---")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("📝 अपनी जानकारी दर्ज करें")
        
        # Model info
        st.subheader("🤖 AI मॉडल")
        st.success("✅ Qwen 2.5-7B Instruct - मुफ्त हिंदी समर्थन")
        st.info("💡 .env फाइल में HUGGINGFACEHUB_API_TOKEN आवश्यक")
        st.info("🔗 Token प्राप्त करें: https://huggingface.co/settings/tokens")
        
        st.markdown("---")
        
        monthly_income = st.number_input(
            "मासिक आय (₹)",
            min_value=0,
            value=50000,
            step=5000,
            help="आपकी कुल मासिक आय"
        )
        
        target_amount = st.number_input(
            "लक्ष्य राशि (₹)",
            min_value=0,
            value=1000000,
            step=50000,
            help="आप कितनी राशि जुटाना चाहते हैं?"
        )
        
        years = st.number_input(
            "समय सीमा (वर्ष)",
            min_value=1,
            max_value=30,
            value=5,
            help="आपके पास कितने वर्ष हैं?"
        )
        
        risk_profile = st.selectbox(
            "जोखिम प्रोफाइल",
            ["कम जोखिम (Low)", "मध्यम जोखिम (Medium)", "उच्च जोखिम (High)"],
            index=1
        )
        
        annual_return = st.slider(
            "अपेक्षित वार्षिक रिटर्न (%)",
            min_value=5.0,
            max_value=15.0,
            value=12.0,
            step=0.5,
            help="आप कितना रिटर्न की उम्मीद करते हैं?"
        )
        
        notes = st.text_area(
            "अतिरिक्त नोट्स (वैकल्पिक)",
            placeholder="कोई विशेष आवश्यकता या लक्ष्य..."
        )
        
        st.markdown("---")
        generate_button = st.button("🚀 योजना बनाएं", type="primary", use_container_width=True)
    
    # Main content area
    if generate_button:
        if monthly_income <= 0 or target_amount <= 0:
            st.error("⚠️ कृपया वैध आय और लक्ष्य राशि दर्ज करें")
            return
        
        # Prepare user data
        user_data = {
            "monthly_income": monthly_income,
            "target_amount": target_amount,
            "years": years,
            "risk_profile": risk_profile,
            "annual_return": annual_return,
            "notes": notes
        }
        
        # Step 1: Calculate SIP deterministically
        st.header("📊 गणना परिणाम")
        with st.spinner("SIP गणना हो रही है..."):
            sip_calc = calculate_sip(target_amount, years, annual_return)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("आवश्यक मासिक SIP", format_inr(sip_calc['monthly_sip']))
        
        with col2:
            st.metric("कुल निवेश", format_inr(sip_calc['total_investment']))
        
        with col3:
            st.metric("अपेक्षित रिटर्न", format_inr(sip_calc['expected_returns']))
        
        with col4:
            sip_percentage = (sip_calc['monthly_sip'] / monthly_income) * 100
            st.metric("आय का %", f"{sip_percentage:.1f}%")
        
        st.markdown("---")
        
        # Step 2: Initialize LLM (cached)
        with st.spinner("AI मॉडल लोड हो रहा है (Qwen 2.5-7B)..."):
            llm = initialize_llm()
        
        st.success("✅ Qwen 2.5-7B Instruct तैयार है!")
        
        # Step 3: Run Multi-Agent System
        st.header("🤖 एजेंट विश्लेषण")
        
        with st.spinner("एजेंट काम कर रहे हैं..."):
            advisor_output, risk_output, planner_output = run_multi_agent_flow(
                llm, user_data, sip_calc
            )
        
        # Display Agent Outputs
        st.subheader("1️⃣ सलाहकार (Advisor Agent)")
        with st.expander("✅ सलाहकार की राय देखें", expanded=True):
            st.info(advisor_output)
        
        st.subheader("2️⃣ जोखिम विश्लेषक (Risk Analyst Agent)")
        with st.expander("✅ जोखिम विश्लेषण देखें", expanded=True):
            st.warning(risk_output)
        
        st.subheader("3️⃣ योजनाकर्त्ता (Planner Agent)")
        with st.expander("✅ अंतिम वित्तीय योजना देखें", expanded=True):
            st.success(planner_output)
        
        st.markdown("---")
        
        # Final Plan Display
        st.header("📋 आपकी पूर्ण वित्तीय योजना")
        
        st.markdown(f"""
### 🎯 लक्ष्य विवरण
- **लक्ष्य राशि:** {format_inr(target_amount)}
- **समय सीमा:** {years} वर्ष
- **आवश्यक मासिक SIP:** {format_inr(sip_calc['monthly_sip'])}
- **कुल निवेश:** {format_inr(sip_calc['total_investment'])}
- **अपेक्षित लाभ:** {format_inr(sip_calc['expected_returns'])}

### 💼 एजेंट सुझाव

**सलाहकार की राय:**
{advisor_output}

**जोखिम विश्लेषण:**
{risk_output}

**अंतिम योजना:**
{planner_output}

---
⚠️ **अस्वीकरण:** यह एक AI-जनित योजना है। कृपया किसी प्रमाणित वित्तीय सलाहकार से परामर्श करें।
        """)
        
        # Save conversation
        st.markdown("---")
        with st.spinner("योजना सहेजी जा रही है..."):
            filename = save_conversation(
                user_data, sip_calc,
                advisor_output, risk_output, planner_output
            )
        
        st.success(f"✅ योजना सफलतापूर्वक सहेजी गई: `{filename}`")
        
        # Download button
        import os
        with open(filename, 'r', encoding='utf-8') as f:
            st.download_button(
                label="📥 योजना डाउनलोड करें (JSON)",
                data=f.read(),
                file_name=os.path.basename(filename),
                mime="application/json"
            )
    
    else:
        # Welcome screen
        st.info("👈 बाईं ओर अपनी जानकारी दर्ज करें और 'योजना बनाएं' बटन पर क्लिक करें")
        
        st.markdown("""
        ### 🌟 यह प्रणाली कैसे काम करती है?
        
        1. **📝 जानकारी दर्ज करें**: अपनी आय, लक्ष्य, और समय सीमा बताएं
        
        2. **🔢 गणना**: सिस्टम स्वचालित रूप से आवश्यक SIP की गणना करता है
        
        3. **🤖 तीन एजेंट काम करते हैं**:
           - **सलाहकार**: प्रारंभिक सुझाव देता है
           - **जोखिम विश्लेषक**: जोखिम की जांच करता है
           - **योजनाकर्त्ता**: अंतिम योजना बनाता है
        
        4. **📋 पूर्ण योजना**: आपको एक विस्तृत हिंदी योजना मिलती है
        
        5. **💾 सहेजें**: योजना JSON फाइल में सहेजी जाती है
        
        ---
        
        ### 🛠️ विशेषताएं:
        - ✅ पूर्णतः हिंदी में
        - ✅ तीन AI एजेंट
        - ✅ सटीक गणितीय गणना
        - ✅ जोखिम विश्लेषण
        - ✅ व्यावहारिक योजना
        - ✅ JSON में सहेजें
        """)


if __name__ == "__main__":
    main()

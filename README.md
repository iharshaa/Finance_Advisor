# 💰 हिंदी वित्त सलाहकार (Hindi Finance Advisor)

A complete multi-agent Hindi-only Personal Finance Advisor system using LangChain framework with Qwen 2.5-7B, deterministic calculations, and Streamlit UI.

## 🎯 Features

- **3 Hindi-Speaking AI Agents**:
  - 🧑‍💼 **सलाहकार (Advisor)**: Provides initial financial guidance
  - 🔍 **जोखिम विश्लेषक (Risk Analyst)**: Analyzes risks and suggests safer alternatives
  - 📊 **योजनाकर्त्ता (Planner)**: Creates structured action plans with budget breakdown

- **Deterministic Calculations**: SIP/EMI calculator with exact mathematical formulas
- **Pure Hindi Interface**: All outputs in Devanagari script
- **Clean Architecture**: Modular code split into separate files
- **JSON Logging**: Save conversations with timestamps
- **Cached LLM**: Efficient resource usage with Streamlit caching

## 📂 Project Structure

```
finance_advisor/
├── app.py              # Streamlit UI (entry point)
├── agents.py           # LangChain multi-agent system
├── llm.py              # LangChain LLM factory (Qwen 2.5-7B)
├── calc.py             # Deterministic SIP/EMI calculators
├── utils.py            # Conversation logging utilities
├── requirements.txt    # Python dependencies (6 packages)
├── README.md           # This file
├── QUICKSTART.md       # Quick start guide
├── ARCHITECTURE.md     # Architecture documentation
├── PROJECT_SUMMARY.md  # Project summary
├── .env                # Environment variables (create this)
├── .env.example        # Environment template
├── .gitignore          # Git ignore rules
├── logs/               # Auto-generated conversation logs
├── venv/               # Virtual environment (auto-created)
└── __pycache__/        # Python cache (auto-created)
```

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Setup API Token

1. Get a free token from [HuggingFace](https://huggingface.co/settings/tokens)
2. Create `.env` file in project root:

```bash
HUGGINGFACEHUB_API_TOKEN=hf_your_token_here
```

### 3. Run the Application

```powershell
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📖 How to Use

1. **Enter Your Information** in the sidebar:
   - Monthly Income (मासिक आय)
   - Target Amount (लक्ष्य राशि)
   - Time Horizon (समय सीमा)
   - Risk Profile (जोखिम प्रोफाइल)
   - Expected Returns (अपेक्षित रिटर्न)

2. **Click "योजना बनाएं"** to generate your plan

3. **View Results**:
   - Deterministic SIP calculations
   - Advisor's Hindi suggestions
   - Risk analysis in Hindi
   - Final structured plan in Hindi

4. **Download**: Plans auto-save to `logs/` and can be downloaded as JSON

## 🧮 How It Works

### Deterministic Calculator (`calc.py`)

Uses the **Future Value of Annuity** formula:

```
PMT = FV × r / ((1+r)^n - 1)

Where:
- PMT = Monthly SIP amount
- FV = Future Value (target)
- r = Monthly rate
- n = Total months
```

**Example**:
- Target: ₹10,00,000
- Time: 5 years
- Return: 12% p.a.
- **Result**: ₹12,244.45/month

### Multi-Agent Flow (`agents.py`)

```
User Input → Calculate SIP → Advisor → Risk Analyst → Planner → Final Plan
```

Each agent:
1. Receives context from previous agents
2. Generates Hindi response via LLM
3. Passes output to next agent

### LLM Configuration (`llm.py`)

Default: **Qwen 2.5-7B Instruct** (excellent Hindi support, free HuggingFace tier)

**LangChain integration**:
```python
from llm import get_llm

# Initialize Qwen 2.5-7B with LangChain
llm = get_llm(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    temperature=0.7,
    max_tokens=512
)

# LangChain message-based usage
from langchain_core.messages import HumanMessage
response = llm.invoke([HumanMessage(content="मुझे निवेश की सलाह दें")])
```

## 🤖 Model Details

### Qwen 2.5-7B Instruct

**Why this model?**
- ✅ Excellent Hindi language support
- ✅ Available on free HuggingFace tier
- ✅ LangChain compatible via ChatHuggingFace
- ✅ Optimized for instruction-following
- ✅ No rate limiting on API usage

**LangChain Framework**:
```python
   from llm import get_anthropic_llm
   llm = get_anthropic_llm()
   # Requires: pip install langchain-anthropic
   # Add ANTHROPIC_API_KEY to .env
   ```

## 📝 Code Examples

### Test Individual Modules

**Calculator:**
```powershell
python calc.py
```

**LLM:**
```powershell
python llm.py
```

**Agents:**
```powershell
python agents.py
```

**Utilities:**
```powershell
python utils.py
```

### Use in Your Code

```python
from calc import calculate_sip, format_inr
from llm import get_llm
from agents import run_multi_agent_flow

# Calculate SIP
sip = calculate_sip(1000000, 5, 12.0)
print(format_inr(sip['monthly_sip']))  # ₹12,244.45

# Initialize LLM
llm = get_llm()

# Run agents
user_data = {
    'monthly_income': 50000,
    'target_amount': 1000000,
    'years': 5,
    'risk_profile': 'मध्यम जोखिम'
}
advisor, risk, planner = run_multi_agent_flow(llm, user_data, sip)
```

## 🔧 Configuration

### Adjust Model Parameters in `app.py`

Edit the `initialize_llm()` function:

```python
@st.cache_resource
def initialize_llm():
    return get_llm(
        repo_id="Qwen/Qwen2.5-7B-Instruct",  # Model ID
        temperature=0.7,    # Creativity (0.0-1.0)
        max_tokens=512      # Response length
    )
```

### Adjust Agent Prompts in `agents.py`

Modify the `analyze()` or `create_plan()` methods in each agent class.

## 📊 Sample Output

**JSON Log Structure:**
```json
{
  "timestamp": "2025-11-30T10:30:00",
  "user_input": {
    "monthly_income": 50000,
    "target_amount": 1000000,
    "years": 5
  },
  "calculations": {
    "monthly_sip": 12244.45,
    "total_investment": 734667.0
  },
  "agent_outputs": {
    "advisor": "...",
    "risk_analyst": "...",
    "planner": "..."
  }
}
```

## 🔮 Future Enhancements

### Easy to Add:

- **More Calculators**: PPF, FD, Tax
- **Charts**: SIP growth visualization
- **Additional Agents**: Tax planner, Insurance advisor
- **Database**: Save user profiles
- **Export**: PDF reports

### Example Extension:

```python
# Add to agents.py

class TaxPlannerAgent(Agent):
    def __init__(self, llm):
        super().__init__(
            role="कर योजनाकार",
            llm=llm
        )
    
    def analyze_tax_savings(self, user_data, sip_calc):
        # Tax planning logic
        pass
```

## ⚠️ Troubleshooting

**Issue: "API Token Error"**
- Check `.env` file exists
- Verify token is correct
- No spaces around `=` in `.env`

**Issue: "Model not loading"**
- Check internet connection
- Try different model: `get_llm("google/flan-t5-small")`
- Verify HuggingFace API is accessible

**Issue: "Not responding in Hindi"**
- Some models have limited Hindi support
- Use alternative HuggingFace models if needed
- Adjust temperature (lower = more focused)

**Issue: "Import errors"**
- Run: `pip install -r requirements.txt`
- Check you're in virtual environment
- Try: `pip install --upgrade langchain langchain-community`

## 📦 Dependencies

- **streamlit**: Web UI framework
- **langchain**: LLM orchestration
- **langchain-community**: Community LLM integrations
- **huggingface_hub**: HuggingFace model access
- **python-dotenv**: Environment variable management
- **transformers**: Model loading (auto-installed)

## 🎓 Learning Resources

- [LangChain Docs](https://python.langchain.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [HuggingFace Models](https://huggingface.co/models)
- [Qwen Models](https://huggingface.co/Qwen)

## 📄 License

Educational project - free to use and modify.

## 🙏 Credits

- **AI Framework**: LangChain with Qwen 2.5-7B
- **Frameworks**: Streamlit, LangChain
- **Language**: Hindi (Devanagari)

---

**Made with ❤️ for Hindi-speaking financial planning**

🚀 **शुभकामनाएं! Happy Planning!**

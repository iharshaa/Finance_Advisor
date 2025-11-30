# 🚀 Quick Start Guide

## Installation (3 Steps)

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Create .env File
Create a file named `.env` in the project root:
```
HUGGINGFACEHUB_API_TOKEN=hf_your_token_here
```

Get your token: https://huggingface.co/settings/tokens

### Step 3: Run the App
```powershell
streamlit run app.py
```

## 📝 File Structure Explained

```
app.py          → Streamlit UI (main entry point)
agents.py       → 3 Hindi-speaking agents
llm.py          → LLM configuration & factory
calc.py         → SIP/EMI calculators
utils.py        → Logging & utilities
```

## 🧪 Test Individual Modules

```powershell
# Test calculator
python calc.py

# Test LLM (requires .env setup)
python llm.py

# Test agents (requires .env setup)
python agents.py

# Test utilities
python utils.py
```

## 🔧 Common Customizations

### Adjust Model Parameters

Edit `app.py` initialize_llm() function:
```python
return get_llm(
    repo_id="Qwen/Qwen2.5-7B-Instruct",  # Model ID
    temperature=0.7,  # Adjust creativity
    max_tokens=512    # Response length
)
```

### Add More Agents

Add to `agents.py`:
```python
class NewAgent(Agent):
    def __init__(self, llm):
        super().__init__(role="नया एजेंट", llm=llm)
    
    def analyze(self, data):
        # Your logic here
        pass
```

### Modify Prompts

Edit the `analyze()` or `create_plan()` methods in `agents.py`.

## 📞 Support

- Check README.md for detailed documentation
- Test individual modules if something fails
- Verify .env file has correct token

Happy Planning! 🎉

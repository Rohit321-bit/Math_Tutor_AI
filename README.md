# 🧮 Math Tutor Multi-Agent System

A beginner-friendly multi-agent project using the same pattern as production
stock analysis agents — but simple enough to understand in one sitting.

## 🔄 How it works

```
User Query: "What is (15 * 4) + (100 / 5) - 2^3 ?"
                        ↓
                   SUPERVISOR
                        ↓
        ┌───────────────┼───────────────┐
        ↓               ↓               ↓
  calculator_agent  explainer_agent  quiz_agent
  (solves it with   (explains the    (generates 2
   math tools)       concept)         practice Qs)
        └───────────────┼───────────────┘
                        ↓
              Final Combined Report:
              ✅ Solution
              📘 Explanation
              🧪 Practice Problems
```

## ⚙️ Setup

```bash
pip install -r requirements.txt
cp env.example .env     # add your OPENAI_API_KEY
python main.py
```

## 🔑 Key Libraries Used

| Library | Role |
|---|---|
| `init_chat_model` | Init GPT-4o cleanly — swap model in 1 line |
| `create_react_agent` | Each specialist agent with tools + prompt |
| `create_supervisor` | Orchestrates agents in order, combines output |

## 💡 Try different queries

```python
# In main.py, change the query:
query = "Solve: 5^2 + sqrt(144) - 10"
query = "What is compound interest on 10000 at 8% for 3 years?"
query = "Solve quadratic: x^2 - 5x + 6 = 0"
```

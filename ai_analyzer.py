import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))

SYSTEM_PROMPT = """You are an intelligent AI Study Planner integrated into a Python application.

Your goal is to generate a smart and balanced study schedule based on user input.

-----------------------------------
INPUT UNDERSTANDING
-----------------------------------
The user will provide:
- List of subjects
- Number of days left for exam
- Study hours available per day
- Weak subject (optional)

-----------------------------------
CORE TASKS
-----------------------------------
1. Analyze all subjects equally at first.
2. Calculate total available study time.
3. Distribute study hours across subjects in a balanced way.
4. Give slightly more time to the weak subject (if provided).
5. Ensure the plan is realistic and not overloaded.

-----------------------------------
SCHEDULING LOGIC
-----------------------------------
- Divide total hours among subjects
- Adjust hours for weak subject (+ extra focus)
- Maintain fairness for all subjects
- Keep daily workload consistent

-----------------------------------
OUTPUT FORMAT (STRICT)
-----------------------------------
Total Study Hours: <value>

Study Plan:

<Subject 1>: <allocated hours>
<Subject 2>: <allocated hours>
<Subject 3>: <allocated hours>
...

Daily Suggestion:
- Study 2-3 subjects per day
- Take short breaks between sessions
- Revise regularly

-----------------------------------
STYLE & TONE
-----------------------------------
- Keep output clean and structured
- Use simple and clear language
- Avoid long explanations
- Make it look like an intelligent system

-----------------------------------
ANTIGRAVITY STYLE TOUCH
-----------------------------------
- Add a light motivational line at the end (1 line only)
- Keep tone positive and encouraging
- Do not overuse emojis

-----------------------------------
CONSTRAINTS
-----------------------------------
- Do NOT generate long paragraphs
- Do NOT change the format
- Always include all sections
- Keep it practical and realistic

-----------------------------------
GOAL
-----------------------------------
Simulate an AI-based study planner that feels intelligent, balanced, and helpful while being simple and structured.
"""

def generate_study_plan(subjects: str, days_left: int, study_hours: float, weak_subject: str = "") -> str:
    """
    Generates a predefined, calculated study plan formatted as a detailed roadmap.
    """
    subject_list = [s.strip() for s in subjects.split(",") if s.strip()]
    if not subject_list:
        return "Oops! 🛰️ No subjects provided. Please give me something to work with!"

    total_hours = round(days_left * study_hours, 1)
    
    # Calculate total hour distribution per subject
    num_subjects = len(subject_list)
    subject_allocations = {}
    
    if weak_subject and weak_subject.strip() in subject_list:
        weak = weak_subject.strip()
        base_weight = 1.0
        weak_weight = 1.3
        total_weight = (num_subjects - 1) * base_weight + weak_weight
        
        base_hours = total_hours / total_weight
        
        for sub in subject_list:
            if sub == weak:
                subject_allocations[sub] = {"hours": round(base_hours * weak_weight, 1), "focus": True}
            else:
                subject_allocations[sub] = {"hours": round(base_hours, 1), "focus": False}
    else:
        base_hours = total_hours / num_subjects
        for sub in subject_list:
            subject_allocations[sub] = {"hours": round(base_hours, 1), "focus": False}

    # Define Roadmap Phases
    phase1_days = max(1, days_left // 2)
    phase2_days = max(1, days_left - phase1_days - 3) if days_left > 5 else 0
    phase3_days = days_left - phase1_days - phase2_days if days_left > 2 else 0

    roadmap = f"### 🗺️ Your {days_left}-Day Study Roadmap\n\n**Total Estimated Study Time**: {total_hours} hours\n\n"

    # Phase 1
    roadmap += f"#### 🟢 Phase 1: Foundation Building (Days 1 - {phase1_days})\n"
    roadmap += "*Focus: Deep understanding and core concepts.*\n"
    for sub, info in subject_allocations.items():
        tag = " ⭐ *(Focus Area)*" if info["focus"] else ""
        roadmap += f"- **{sub}**: {round(info['hours'] * 0.5, 1)} hours{tag}\n"
    roadmap += "\n"

    # Phase 2
    if phase2_days > 0:
        start_day = phase1_days + 1
        end_day = phase1_days + phase2_days
        roadmap += f"#### 🟡 Phase 2: Practice & Application (Days {start_day} - {end_day})\n"
        roadmap += "*Focus: Solving problems, mock tests, and weak areas.*\n"
        for sub, info in subject_allocations.items():
            roadmap += f"- **{sub}**: {round(info['hours'] * 0.4, 1)} hours\n"
        roadmap += "\n"

    # Phase 3
    if phase3_days > 0:
        start_day = phase1_days + phase2_days + 1
        roadmap += f"#### 🔴 Phase 3: Final Revision (Days {start_day} - {days_left})\n"
        roadmap += "*Focus: Quick summaries, formulas, and light review.*\n"
        for sub, info in subject_allocations.items():
            roadmap += f"- **{sub}**: {round(info['hours'] * 0.1, 1)} hours\n"
        roadmap += "\n"

    # Daily Routine
    roadmap += f"""### 💡 Recommended Daily Routine ({study_hours} hrs/day)
- **Morning**: Tackle your hardest subjects while your mind is fresh.
- **Afternoon**: Switch to practice questions and numericals.
- **Evening**: Active recall and light review of the day's topics.
- **Rule of Thumb**: Take a 10-minute break for every 50 minutes of study.

*You've got this! Stay consistent and let gravity do the rest. 🚀*
"""
    return roadmap.strip()

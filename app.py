import streamlit as st
import sys
import io
import traceback
import contextlib

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="تعلّم Python مع نائلة – الاختبار النهائي",
    page_icon="🐍",
    layout="centered",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; }
h1,h2,h3,h4 { font-family: 'Tajawal', sans-serif; }

.hero { 
    background: linear-gradient(135deg, #0F1220 0%, #171C30 100%);
    border: 1px solid rgba(124,111,224,0.3);
    border-radius: 20px; padding: 2rem; text-align: center; margin-bottom: 2rem;
}
.hero h1 { 
    font-size: 2.4rem; font-weight: 900;
    background: linear-gradient(135deg, #7C6FE0, #4ECDC4);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.section-badge {
    display: inline-block;
    background: rgba(124,111,224,0.15); border: 1px solid rgba(124,111,224,0.4);
    border-radius: 100px; padding: 4px 18px; font-size: 0.85rem; color: #7C6FE0;
    font-weight: 700; margin-bottom: 0.75rem;
}
.correct-box {
    background: rgba(82,214,138,0.12); border: 1px solid #52D68A;
    border-radius: 12px; padding: 1rem 1.25rem; margin-top: 0.5rem; color: #52D68A;
    font-weight: 700;
}
.wrong-box {
    background: rgba(255,107,107,0.12); border: 1px solid #FF6B6B;
    border-radius: 12px; padding: 1rem 1.25rem; margin-top: 0.5rem; color: #FF6B6B;
    font-weight: 700;
}
.score-card {
    background: linear-gradient(135deg, #0F1220, #171C30);
    border: 2px solid rgba(124,111,224,0.5);
    border-radius: 20px; padding: 2.5rem; text-align: center; margin-top: 2rem;
}
.score-pass { color: #52D68A; font-size: 1.4rem; font-weight: 900; }
.score-fail { color: #FF6B6B; font-size: 1.4rem; font-weight: 900; }
.score-num { font-size: 4rem; font-weight: 900; }
.exercise-box {
    background: #0d1117; border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px; padding: 1.25rem; margin: 0.75rem 0;
    font-family: 'DM Mono', monospace; direction: ltr; text-align: left;
}
.output-box {
    background: #0a0f1a; border: 1px solid rgba(78,205,196,0.3);
    border-radius: 10px; padding: 1rem; margin-top: 0.75rem;
    font-family: monospace; direction: ltr; text-align: left; color: #4ECDC4;
}
.error-box {
    background: rgba(255,107,107,0.08); border: 1px solid rgba(255,107,107,0.35);
    border-radius: 10px; padding: 1rem; margin-top: 0.75rem;
    font-family: monospace; direction: ltr; text-align: left; color: #FF6B6B;
}
.stTextArea textarea { font-family: 'DM Mono', monospace; direction: ltr; text-align: left; }
.progress-label { color: #8890B5; font-size: 0.9rem; margin-bottom: 0.25rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────

# QCM questions – 3 per lesson = 18 total
QCM = [
    # ── Variables ──
    {
        "lesson": "📦 المتغيرات",
        "q": "أيّ من هذه الأسماء صحيح في Python؟",
        "opts": ["2myVar", "my_var2", "my-var", "class"],
        "ans": 1,
        "fb_ok": "✓ my_var2 يبدأ بحرف ويستخدم snake_case — صحيح تماماً!",
        "fb_no": "✗ لا يجوز البدء برقم، الشرطة العادية، أو الكلمات المحجوزة.",
    },
    {
        "lesson": "📦 المتغيرات",
        "q": "ما نوع المتغير: price = 9.99 ؟",
        "opts": ["int", "float", "str", "bool"],
        "ans": 1,
        "fb_ok": "✓ أي رقم بفاصلة عشرية هو float.",
        "fb_no": "✗ 9.99 يحتوي فاصلة عشرية → float وليس int.",
    },
    {
        "lesson": "📦 المتغيرات",
        "q": "ما الناتج؟  a, b = 5, 10  →  a, b = b, a  →  print(a)",
        "opts": ["5", "10", "خطأ في الكود", "None"],
        "ans": 1,
        "fb_ok": "✓ بعد التبادل a يأخذ قيمة b القديمة = 10.",
        "fb_no": "✗ Python يُبادل القيمتين في خطوة واحدة → a = 10.",
    },
    # ── While ──
    {
        "lesson": "🔁 حلقة while",
        "q": "ما الجزء الذي إذا نسيناه تصبح الحلقة لا نهائية؟",
        "opts": ["التهيئة", "الشرط", "التحديث", "جسم الحلقة"],
        "ans": 2,
        "fb_ok": "✓ بدون التحديث يظل الشرط True إلى الأبد!",
        "fb_no": "✗ التحديث هو ما يُغير المتغير ويجعل الشرط يصبح False في النهاية.",
    },
    {
        "lesson": "🔁 حلقة while",
        "q": "ما ناتج  4752 % 10 ؟",
        "opts": ["4", "475", "2", "7"],
        "ans": 2,
        "fb_ok": "✓ % يُعطي الباقي → 4752 = 475×10 + 2",
        "fb_no": "✗ % يعطي الباقي من القسمة — الرقم الأخير من العدد.",
    },
    {
        "lesson": "🔁 حلقة while",
        "q": "مكافئ  not(A and B)  بقانون دي مورغان؟",
        "opts": ["not A and not B", "not A or not B", "A or B", "A and B"],
        "ans": 1,
        "fb_ok": "✓ not(A and B) = not A or not B — قانون دي مورغان!",
        "fb_no": "✗ عند نفي and تتحول إلى or مع نفي كل طرف.",
    },
    # ── For ──
    {
        "lesson": "🔂 حلقة for",
        "q": "كم رقماً تُنتج  range(3, 8) ؟",
        "opts": ["6", "5", "8", "3"],
        "ans": 1,
        "fb_ok": "✓ range(3,8) → 3,4,5,6,7 — خمسة أرقام (stop غير مضمّن).",
        "fb_no": "✗ range(3,8) تنتج: 3,4,5,6,7 — وهي 5 أرقام.",
    },
    {
        "lesson": "🔂 حلقة for",
        "q": "ما الناتج؟  range(10, 0, -2)",
        "opts": ["10,8,6,4,2,0", "10,8,6,4,2", "0,2,4,6,8,10", "لا شيء"],
        "ans": 1,
        "fb_ok": "✓ step=-2 يبدأ من 10 وينتهي عند 2 (stop=0 غير مضمّن).",
        "fb_no": "✗ stop=0 غير مضمّن، آخر قيمة هي 2.",
    },
    {
        "lesson": "🔂 حلقة for",
        "q": "ما قيمة total بعد:  total=0  →  for i in range(4): total+=i",
        "opts": ["10", "6", "4", "0"],
        "ans": 1,
        "fb_ok": "✓ range(4)=0,1,2,3 → المجموع = 0+1+2+3 = 6",
        "fb_no": "✗ range(4) تنتج 0,1,2,3. المجموع = 0+1+2+3 = 6.",
    },
    # ── Conditions ──
    {
        "lesson": "🌿 الشروط",
        "q": "ما الناتج إذا score=65 ؟\nif score>=90: print('A')  elif score>=60: print('B')  else: print('C')",
        "opts": ["A", "B", "C", "خطأ"],
        "ans": 1,
        "fb_ok": "✓ score=65 أكبر من 60 → elif يُطبع B.",
        "fb_no": "✗ score=65 يُحقق الشرط score>=60 → B.",
    },
    {
        "lesson": "🌿 الشروط",
        "q": "الفرق بين  =  و  == ؟",
        "opts": ["لا فرق", "== للإسناد", "= للإسناد و == للمقارنة", "للأرقام فقط"],
        "ans": 2,
        "fb_ok": "✓ = يضع قيمة، == يقارن قيمتين.",
        "fb_no": "✗ = للإسناد (x=5)، == للمقارنة (x==5 يُرجع True/False).",
    },
    {
        "lesson": "🌿 الشروط",
        "q": 'ما الناتج؟  x = "مرحبا" if 10 > 5 else "وداعاً"',
        "opts": ["وداعاً", "مرحبا", "True", "خطأ"],
        "ans": 1,
        "fb_ok": '✓ الشرط 10>5 صحيح → x = "مرحبا".',
        "fb_no": "✗ في التعبير الثلاثي القيمة الأولى تُختار عند تحقق الشرط.",
    },
    # ── Data Structures ──
    {
        "lesson": "🗂️ هياكل البيانات",
        "q": "أيّ هيكل بيانات يُزيل التكرار تلقائياً؟",
        "opts": ["List", "Tuple", "Dictionary", "Set"],
        "ans": 3,
        "fb_ok": "✓ Set تُزيل التكرار تلقائياً — كل عنصر يظهر مرة واحدة فقط.",
        "fb_no": "✗ Set هي الوحيدة التي تضمن فرادة العناصر.",
    },
    {
        "lesson": "🗂️ هياكل البيانات",
        "q": "ما الفرق الجوهري بين List وTuple؟",
        "opts": ["List أسرع", "Tuple ثابتة لا يمكن تعديلها", "List لا تقبل الأرقام", "Tuple تقبل أنواعاً أكثر"],
        "ans": 1,
        "fb_ok": "✓ Tuple ثابتة (immutable) — أي تعديل يُطلق TypeError.",
        "fb_no": "✗ الفرق الجوهري: Tuple لا تتغير بعد الإنشاء.",
    },
    {
        "lesson": "🗂️ هياكل البيانات",
        "q": 'ما ناتج:  d = {"x": 10}  →  d.get("y", 99)',
        "opts": ["10", "None", "KeyError", "99"],
        "ans": 3,
        "fb_ok": '✓ get() يُرجع القيمة الافتراضية 99 لأن المفتاح "y" غير موجود.',
        "fb_no": "✗ get(key, default) يُرجع القيمة الافتراضية عند غياب المفتاح.",
    },
    # ── Functions ──
    {
        "lesson": "🧩 الدوال",
        "q": "ماذا ترجع دالة بلا return ؟",
        "opts": ["0", "False", "None", "خطأ"],
        "ans": 2,
        "fb_ok": "✓ كل دالة بلا return ترجع None تلقائياً.",
        "fb_no": "✗ Python لا ترفع خطأ — ترجع None بشكل ضمني.",
    },
    {
        "lesson": "🧩 الدوال",
        "q": "ما الناتج؟  def f(x, y=5): return x + y  ←  f(3)",
        "opts": ["3", "8", "5", "خطأ"],
        "ans": 1,
        "fb_ok": "✓ x=3 وy=5 (افتراضي) → 3+5 = 8.",
        "fb_no": "✗ y=5 افتراضي — إذا لم تُمرّري قيمة يُستخدم 5 → 3+5=8.",
    },
    {
        "lesson": "🧩 الدوال",
        "q": "ما الذي تفعله *args ؟",
        "opts": ["لا فرق عن المعامل العادي", "تُرجع قائمة", "تقبل عدداً غير محدود من القيم كـ tuple", "للنصوص فقط"],
        "ans": 2,
        "fb_ok": "✓ *args تجمع الحجج في tuple بلا حد للعدد.",
        "fb_no": "✗ *args يجمع الحجج في tuple — ليس list.",
    },
]

# Coding exercises – one per lesson
EXERCISES = [
    {
        "id": "ex_vars",
        "lesson": "📦 المتغيرات",
        "title": "تبادل متغيرين",
        "desc": "أنشئ متغيرَي  `a = 10`  و  `b = 20` ، بادلي قيمتيهما باستخدام سطر واحد، ثم اطبعي `a` و `b`.",
        "starter": "a = 10\nb = 20\n# بادلي هنا\n\nprint(a)\nprint(b)",
        "expected": "20\n10",
        "hint": "استخدمي:  a, b = b, a",
    },
    {
        "id": "ex_while",
        "lesson": "🔁 حلقة while",
        "title": "مجموع الأرقام الفردية",
        "desc": "باستخدام حلقة while، احسبي مجموع الأرقام الفردية من 1 إلى 9 (يشمل 9) واطبعي النتيجة.",
        "starter": "total = 0\ni = 1\n# أكملي الكود\n\nprint(total)",
        "expected": "25",
        "hint": "استخدمي  i % 2 != 0  للفحص، وزيدي i بمقدار 1 في كل دورة.",
    },
    {
        "id": "ex_for",
        "lesson": "🔂 حلقة for",
        "title": "طباعة جدول الضرب",
        "desc": "باستخدام حلقة for، اطبعي جدول ضرب الرقم 3 من 1 إلى 5 بالشكل:  3 x 1 = 3",
        "starter": "n = 3\n# أكملي الكود هنا\nfor i in range(1, 6):\n    pass  # عدّلي هذا السطر",
        "expected": "3 x 1 = 3\n3 x 2 = 6\n3 x 3 = 9\n3 x 4 = 12\n3 x 5 = 15",
        "hint": "استخدمي  print(f\"{n} x {i} = {n*i}\")",
    },
    {
        "id": "ex_cond",
        "lesson": "🌿 الشروط",
        "title": "تصنيف الدرجة",
        "desc": "اكتبي كوداً يطبع تصنيف الدرجة:\n- 90 أو أكثر → ممتاز\n- 70–89 → جيد جداً\n- 50–69 → مقبول\n- أقل من 50 → راسب\n\nجرّبي مع `score = 73`",
        "starter": "score = 73\n# أكملي الشروط\n",
        "expected": "جيد جداً",
        "hint": "استخدمي if / elif / else مع المقارنات >= ",
    },
    {
        "id": "ex_ds",
        "lesson": "🗂️ هياكل البيانات",
        "title": "إزالة التكرار من قائمة",
        "desc": "لديكِ القائمة: `nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]`\nحوّليها إلى set لإزالة التكرار، ثم ارجعيها إلى list مرتّبة واطبعيها.",
        "starter": "nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]\n# أكملي هنا\n",
        "expected": "[1, 2, 3, 4, 5, 6, 9]",
        "hint": "استخدمي:  sorted(list(set(nums)))",
    },
    {
        "id": "ex_func",
        "lesson": "🧩 الدوال",
        "title": "دالة مجموع القائمة",
        "desc": "اكتبي دالة `my_sum(lst)` تحسب مجموع عناصر القائمة بدون استخدام `sum()` المدمجة، ثم اطبعي:  `my_sum([1, 2, 3, 4, 5])`",
        "starter": "def my_sum(lst):\n    # أكملي هنا\n    pass\n\nprint(my_sum([1, 2, 3, 4, 5]))",
        "expected": "15",
        "hint": "استخدمي حلقة for لجمع العناصر في متغير total.",
    },
]

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "qcm_answers" not in st.session_state:
    st.session_state.qcm_answers = {}      # {idx: chosen_opt}
if "qcm_locked" not in st.session_state:
    st.session_state.qcm_locked = {}       # {idx: True/False}
if "ex_results" not in st.session_state:
    st.session_state.ex_results = {}       # {ex_id: bool}
if "ex_outputs" not in st.session_state:
    st.session_state.ex_outputs = {}       # {ex_id: str}
if "ex_codes" not in st.session_state:
    st.session_state.ex_codes = {}         # {ex_id: str}
if "show_score" not in st.session_state:
    st.session_state.show_score = False

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def run_code(code: str):
    """Run user code and return (stdout, error)."""
    buf = io.StringIO()
    err = None
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, "<student>", "exec"), {})
    except Exception:
        err = traceback.format_exc(limit=4)
    return buf.getvalue().strip(), err

def total_qcm_score():
    correct = sum(
        1 for i, q in enumerate(QCM)
        if st.session_state.qcm_answers.get(i) == q["ans"]
    )
    return correct

def total_ex_score():
    return sum(1 for v in st.session_state.ex_results.values() if v)

def all_qcm_done():
    return len(st.session_state.qcm_locked) == len(QCM)

def all_ex_done():
    return len(st.session_state.ex_results) == len(EXERCISES)

# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🐍 اختبار Python النهائي</h1>
    <p style="color:#8890B5;font-size:1.05rem">مع نائلة — 6 دروس · 18 سؤال + 6 تمارين برمجية</p>
    <p style="color:#4ECDC4;font-weight:700;font-size:0.9rem">✦ بقلم حجار نائلة</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📝 أسئلة QCM", "💻 تمارين برمجية", "🏆 النتيجة النهائية"])

# ══════════════════════════════════════════════
# TAB 1: QCM
# ══════════════════════════════════════════════
with tab1:
    st.markdown("### 📝 اختر الإجابة الصحيحة")
    st.caption("18 سؤال — سؤال واحد يُجاب عليه بالضغط على زر الإجابة")

    lessons_order = []
    seen = set()
    for q in QCM:
        if q["lesson"] not in seen:
            lessons_order.append(q["lesson"])
            seen.add(q["lesson"])

    q_idx = 0
    for lesson in lessons_order:
        lesson_qs = [(i, q) for i, q in enumerate(QCM) if q["lesson"] == lesson]

        st.markdown(f"---\n#### {lesson}")
        for (global_idx, q) in lesson_qs:
            with st.container():
                st.markdown(f'<div class="section-badge">سؤال {global_idx+1} / {len(QCM)}</div>', unsafe_allow_html=True)
                st.markdown(f"**{q['q']}**")

                locked = st.session_state.qcm_locked.get(global_idx, False)

                if not locked:
                    cols = st.columns(2)
                    for oi, opt in enumerate(q["opts"]):
                        col = cols[oi % 2]
                        with col:
                            if st.button(opt, key=f"qcm_{global_idx}_{oi}"):
                                st.session_state.qcm_answers[global_idx] = oi
                                st.session_state.qcm_locked[global_idx] = True
                                st.rerun()
                else:
                    chosen = st.session_state.qcm_answers.get(global_idx)
                    correct = q["ans"]
                    if chosen == correct:
                        st.markdown(f'<div class="correct-box">✅ {q["fb_ok"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="wrong-box">❌ {q["fb_no"]}<br><span style="color:#8890B5">الإجابة الصحيحة: <strong>{q["opts"][correct]}</strong></span></div>', unsafe_allow_html=True)

    if all_qcm_done():
        correct_count = total_qcm_score()
        st.success(f"✅ أكملتِ جميع أسئلة QCM! نتيجتك: {correct_count} / {len(QCM)}")
    else:
        done = len(st.session_state.qcm_locked)
        st.markdown(f'<p class="progress-label">الإجابات: {done} / {len(QCM)}</p>', unsafe_allow_html=True)
        st.progress(done / len(QCM))

# ══════════════════════════════════════════════
# TAB 2: EXERCISES
# ══════════════════════════════════════════════
with tab2:
    st.markdown("### 💻 تمارين برمجية")
    st.caption("اكتبي الكود في المحرر ثم اضغطي ▶ تشغيل للتحقق من النتيجة")

    for ex in EXERCISES:
        eid = ex["id"]
        st.markdown(f"---\n#### {ex['lesson']} — {ex['title']}")
        st.markdown(ex["desc"])

        # Code editor
        default_code = st.session_state.ex_codes.get(eid, ex["starter"])
        code = st.text_area(
            "الكود:",
            value=default_code,
            height=180,
            key=f"ta_{eid}",
            label_visibility="collapsed",
        )
        st.session_state.ex_codes[eid] = code

        col_run, col_hint = st.columns([1, 1])
        with col_run:
            run_btn = st.button(f"▶ تشغيل", key=f"run_{eid}", type="primary")
        with col_hint:
            hint_btn = st.button(f"💡 تلميح", key=f"hint_{eid}")

        if hint_btn:
            st.info(f"💡 **تلميح:** {ex['hint']}")

        if run_btn:
            output, error = run_code(code)
            st.session_state.ex_outputs[eid] = (output, error)

            if error:
                st.session_state.ex_results[eid] = False
            else:
                passed = output.strip() == ex["expected"].strip()
                st.session_state.ex_results[eid] = passed

        # Show output
        if eid in st.session_state.ex_outputs:
            output, error = st.session_state.ex_outputs[eid]
            if error:
                st.markdown(f'<div class="error-box">🔴 خطأ في الكود:\n{error}</div>', unsafe_allow_html=True)
            else:
                passed = st.session_state.ex_results.get(eid, False)
                if passed:
                    st.markdown(f'<div class="correct-box">✅ إجابة صحيحة! الناتج:<br><code>{output}</code></div>', unsafe_allow_html=True)
                else:
                    st.markdown(
                        f'<div class="wrong-box">❌ الناتج غير صحيح:<br>'
                        f'<code>{output or "(لا ناتج)"}</code><br>'
                        f'<span style="color:#8890B5">المتوقع: <code>{ex["expected"]}</code></span></div>',
                        unsafe_allow_html=True
                    )

    if all_ex_done():
        ex_correct = total_ex_score()
        st.success(f"✅ أكملتِ جميع التمارين! نتيجتك: {ex_correct} / {len(EXERCISES)}")
    else:
        done_ex = len(st.session_state.ex_results)
        st.markdown(f'<p class="progress-label">التمارين المكتملة: {done_ex} / {len(EXERCISES)}</p>', unsafe_allow_html=True)
        st.progress(done_ex / len(EXERCISES))

# ══════════════════════════════════════════════
# TAB 3: FINAL SCORE
# ══════════════════════════════════════════════
with tab3:
    st.markdown("### 🏆 النتيجة النهائية")

    qcm_done = all_qcm_done()
    ex_done = all_ex_done()

    if not qcm_done or not ex_done:
        missing = []
        if not qcm_done:
            missing.append(f"أسئلة QCM ({len(st.session_state.qcm_locked)}/{len(QCM)} مكتمل)")
        if not ex_done:
            missing.append(f"تمارين البرمجة ({len(st.session_state.ex_results)}/{len(EXERCISES)} مكتمل)")
        st.warning("⏳ أكملي أولاً:\n- " + "\n- ".join(missing))
    else:
        qcm_score = total_qcm_score()
        ex_score = total_ex_score()
        total_correct = qcm_score + ex_score
        total_possible = len(QCM) + len(EXERCISES)   # 18 + 6 = 24
        percentage = round((total_correct / total_possible) * 100, 1)
        passed = percentage >= 45

        emoji = "🎉" if passed else "📚"
        verdict_class = "score-pass" if passed else "score-fail"
        verdict_text = "🎓 مبروك! انتقلتِ إلى Data Science!" if passed else "📖 لم تتجاوزي العتبة. راجعي الدروس وحاولي مجدداً!"
        verdict_color = "#52D68A" if passed else "#FF6B6B"
        ds_badge = (
            '<div style="background:linear-gradient(135deg,#4ECDC4,#7C6FE0);border-radius:12px;padding:1rem;margin-top:1rem;">'
            '<span style="font-size:1.2rem;font-weight:900;color:#fff">🚀 المرحلة التالية: Data Science مع Python!</span>'
            '</div>'
            if passed else
            '<div style="background:rgba(255,107,107,0.1);border:1px solid rgba(255,107,107,0.3);border-radius:12px;padding:1rem;margin-top:1rem;">'
            '<span style="font-size:1rem;font-weight:700;color:#FF6B6B">💪 العتبة 45% — واصلي التدريب والمحاولة!</span>'
            '</div>'
        )

        st.markdown(f"""
        <div class="score-card">
            <div style="font-size:3.5rem">{emoji}</div>
            <div class="score-num" style="color:{verdict_color}">{percentage}%</div>
            <div class="{verdict_class}">{verdict_text}</div>
            <div style="margin:1.5rem 0;display:flex;gap:1rem;justify-content:center;flex-wrap:wrap">
                <div style="background:#1a1f35;border-radius:12px;padding:1rem 1.5rem;min-width:140px">
                    <div style="color:#8890B5;font-size:.85rem">أسئلة QCM</div>
                    <div style="font-size:1.6rem;font-weight:900;color:#7C6FE0">{qcm_score}<span style="font-size:1rem;color:#8890B5"> / {len(QCM)}</span></div>
                </div>
                <div style="background:#1a1f35;border-radius:12px;padding:1rem 1.5rem;min-width:140px">
                    <div style="color:#8890B5;font-size:.85rem">تمارين البرمجة</div>
                    <div style="font-size:1.6rem;font-weight:900;color:#4ECDC4">{ex_score}<span style="font-size:1rem;color:#8890B5"> / {len(EXERCISES)}</span></div>
                </div>
                <div style="background:#1a1f35;border-radius:12px;padding:1rem 1.5rem;min-width:140px">
                    <div style="color:#8890B5;font-size:.85rem">المجموع الكلي</div>
                    <div style="font-size:1.6rem;font-weight:900;color:#F7C948">{total_correct}<span style="font-size:1rem;color:#8890B5"> / {total_possible}</span></div>
                </div>
            </div>
            {ds_badge}
        </div>
        """, unsafe_allow_html=True)

        # Lesson breakdown
        st.markdown("---\n#### 📊 تفاصيل الأداء بالدرس")
        lesson_qcm = {}
        for i, q in enumerate(QCM):
            lesson_qcm.setdefault(q["lesson"], []).append(
                st.session_state.qcm_answers.get(i) == q["ans"]
            )
        lesson_ex = {}
        for ex in EXERCISES:
            lesson_ex[ex["lesson"]] = st.session_state.ex_results.get(ex["id"], False)

        all_lessons = list(dict.fromkeys([q["lesson"] for q in QCM]))
        for lesson in all_lessons:
            qcm_res = lesson_qcm.get(lesson, [])
            qcm_ok = sum(qcm_res)
            ex_ok = 1 if lesson_ex.get(lesson, False) else 0
            total_l = len(qcm_res) + 1
            ok_l = qcm_ok + ex_ok
            color = "#52D68A" if ok_l == total_l else "#F7C948" if ok_l > 0 else "#FF6B6B"
            icon = "✅" if ok_l == total_l else "⚠️" if ok_l > 0 else "❌"
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        background:#0F1220;border:1px solid rgba(255,255,255,.07);
                        border-radius:10px;padding:.75rem 1.25rem;margin-bottom:.5rem">
                <span style="font-weight:700">{icon} {lesson}</span>
                <span style="color:{color};font-weight:900;font-family:monospace">{ok_l} / {total_l}</span>
            </div>
            """, unsafe_allow_html=True)

        # Reset button
        st.markdown("---")
        if st.button("🔄 إعادة الاختبار من البداية", type="secondary"):
            for key in ["qcm_answers","qcm_locked","ex_results","ex_outputs","ex_codes","show_score"]:
                st.session_state[key] = {} if key != "show_score" else False
            st.rerun()

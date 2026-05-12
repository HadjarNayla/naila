import streamlit as st
import io
import traceback
import contextlib

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Python Quiz – Naïla / نائلة",
    page_icon="🐍",
    layout="centered",
)

# ─────────────────────────────────────────────
# LANGUAGE INIT
# ─────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "ar"

lang  = st.session_state.lang
is_ar = lang == "ar"
tdir  = "rtl" if is_ar else "ltr"
ffam  = "Tajawal" if is_ar else "Inter"

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&family=Inter:wght@400;600;800&display=swap');
html, body, [class*="css"] {{ font-family: '{ffam}', sans-serif; direction: {tdir}; }}
h1,h2,h3,h4 {{ font-family: '{ffam}', sans-serif; }}
.hero {{
    background: linear-gradient(135deg, #0F1220 0%, #171C30 100%);
    border: 1px solid rgba(124,111,224,0.3);
    border-radius: 20px; padding: 2rem; text-align: center; margin-bottom: 2rem;
}}
.hero h1 {{
    font-size: 2.4rem; font-weight: 900;
    background: linear-gradient(135deg, #7C6FE0, #4ECDC4);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}}
.section-badge {{
    display: inline-block; background: rgba(124,111,224,0.15);
    border: 1px solid rgba(124,111,224,0.4); border-radius: 100px;
    padding: 4px 18px; font-size: 0.85rem; color: #7C6FE0;
    font-weight: 700; margin-bottom: .75rem;
}}
.correct-box {{
    background: rgba(82,214,138,0.12); border: 1px solid #52D68A;
    border-radius: 12px; padding: 1rem 1.25rem; margin-top: .5rem;
    color: #52D68A; font-weight: 700;
}}
.wrong-box {{
    background: rgba(255,107,107,0.12); border: 1px solid #FF6B6B;
    border-radius: 12px; padding: 1rem 1.25rem; margin-top: .5rem;
    color: #FF6B6B; font-weight: 700;
}}
.score-card {{
    background: linear-gradient(135deg, #0F1220, #171C30);
    border: 2px solid rgba(124,111,224,0.5);
    border-radius: 20px; padding: 2.5rem; text-align: center; margin-top: 2rem;
}}
.score-pass {{ color: #52D68A; font-size: 1.4rem; font-weight: 900; }}
.score-fail {{ color: #FF6B6B; font-size: 1.4rem; font-weight: 900; }}
.score-num  {{ font-size: 4rem; font-weight: 900; }}
.error-box {{
    background: rgba(255,107,107,0.08); border: 1px solid rgba(255,107,107,.35);
    border-radius: 10px; padding: 1rem; margin-top: .75rem;
    font-family: monospace; direction: ltr; text-align: left;
    color: #FF6B6B; white-space: pre-wrap;
}}
.progress-label {{ color: #8890B5; font-size: .9rem; margin-bottom: .25rem; }}
.stTextArea textarea {{ font-family: monospace; direction: ltr; text-align: left; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TRANSLATIONS
# ─────────────────────────────────────────────
T = {
    "app_title":   {"ar": "🐍 اختبار Python النهائي",                     "fr": "🐍 Test Final Python"},
    "app_sub":     {"ar": "مع نائلة — 6 دروس · 18 سؤال + 6 تمارين",      "fr": "avec Naïla — 6 leçons · 18 QCM + 6 exercices"},
    "byline":      {"ar": "✦ بقلم حجار نائلة",                            "fr": "✦ par Hajjar Naïla"},
    "tab_qcm":     {"ar": "📝 أسئلة QCM",                                 "fr": "📝 QCM"},
    "tab_ex":      {"ar": "💻 تمارين برمجية",                             "fr": "💻 Exercices de code"},
    "tab_score":   {"ar": "🏆 النتيجة النهائية",                          "fr": "🏆 Résultat final"},
    "qcm_title":   {"ar": "### 📝 اختر الإجابة الصحيحة",                  "fr": "### 📝 Choisissez la bonne réponse"},
    "qcm_cap":     {"ar": "18 سؤال — اضغط على إجابة لتأكيدها",           "fr": "18 questions — cliquez sur une réponse pour la valider"},
    "ex_title":    {"ar": "### 💻 تمارين برمجية",                         "fr": "### 💻 Exercices de code"},
    "ex_cap":      {"ar": "اكتبي الكود ثم اضغطي ▶ تشغيل",               "fr": "Écrivez le code puis cliquez ▶ Exécuter"},
    "run":         {"ar": "▶ تشغيل",                                      "fr": "▶ Exécuter"},
    "hint":        {"ar": "💡 تلميح",                                     "fr": "💡 Indice"},
    "hint_lbl":    {"ar": "💡 **تلميح:**",                                "fr": "💡 **Indice :**"},
    "ok_out":      {"ar": "✅ إجابة صحيحة! الناتج:",                      "fr": "✅ Bonne réponse ! Sortie :"},
    "ko_out":      {"ar": "❌ الناتج غير صحيح:",                          "fr": "❌ Résultat incorrect :"},
    "no_out":      {"ar": "(لا ناتج)",                                    "fr": "(aucune sortie)"},
    "expected":    {"ar": "المتوقع:",                                     "fr": "Attendu :"},
    "code_err":    {"ar": "🔴 خطأ في الكود:",                             "fr": "🔴 Erreur dans le code :"},
    "correct_ans": {"ar": "الإجابة الصحيحة:",                            "fr": "Bonne réponse :"},
    "qcm_done":    {"ar": "✅ أكملتِ جميع أسئلة QCM! نتيجتك:",           "fr": "✅ Toutes les questions QCM terminées ! Score :"},
    "ex_done":     {"ar": "✅ أكملتِ جميع التمارين! نتيجتك:",             "fr": "✅ Tous les exercices terminés ! Score :"},
    "prog_q":      {"ar": "الإجابات:",                                   "fr": "Réponses :"},
    "prog_ex":     {"ar": "التمارين المكتملة:",                           "fr": "Exercices complétés :"},
    "score_ttl":   {"ar": "### 🏆 النتيجة النهائية",                      "fr": "### 🏆 Résultat final"},
    "warn_pfx":    {"ar": "⏳ أكملي أولاً:\n- ",                          "fr": "⏳ Complétez d'abord :\n- "},
    "mis_qcm":     {"ar": "أسئلة QCM",                                   "fr": "QCM"},
    "mis_ex":      {"ar": "تمارين البرمجة",                              "fr": "exercices de code"},
    "completed":   {"ar": "مكتمل",                                       "fr": "complété(s)"},
    "pass_txt":    {"ar": "🎓 مبروك! انتقلتِ إلى Data Science!",          "fr": "🎓 Félicitations ! Vous passez en Data Science !"},
    "fail_txt":    {"ar": "📖 لم تتجاوزي العتبة. راجعي الدروس وحاولي مجدداً!", "fr": "📖 Seuil non atteint. Révisez et réessayez !"},
    "ds_pass":     {"ar": "🚀 المرحلة التالية: Data Science مع Python!",  "fr": "🚀 Prochaine étape : Data Science avec Python !"},
    "ds_fail":     {"ar": "💪 العتبة 45% — واصلي التدريب والمحاولة!",    "fr": "💪 Seuil : 45% — continuez à vous entraîner !"},
    "lbl_qcm":     {"ar": "أسئلة QCM",                                   "fr": "Questions QCM"},
    "lbl_ex":      {"ar": "تمارين البرمجة",                              "fr": "Exercices de code"},
    "lbl_tot":     {"ar": "المجموع الكلي",                               "fr": "Total général"},
    "breakdown":   {"ar": "---\n#### 📊 تفاصيل الأداء بالدرس",            "fr": "---\n#### 📊 Détail par leçon"},
    "reset":       {"ar": "🔄 إعادة الاختبار من البداية",                 "fr": "🔄 Recommencer le test"},
    "q_lbl":       {"ar": "سؤال",                                        "fr": "Question"},
}

def t(k):
    return T[k][lang]

# ─────────────────────────────────────────────
# LESSON LABELS
# ─────────────────────────────────────────────
LL = {
    "vars":  {"ar": "📦 المتغيرات",       "fr": "📦 Variables"},
    "while": {"ar": "🔁 حلقة while",       "fr": "🔁 Boucle while"},
    "for":   {"ar": "🔂 حلقة for",         "fr": "🔂 Boucle for"},
    "cond":  {"ar": "🌿 الشروط",           "fr": "🌿 Conditions"},
    "ds":    {"ar": "🗂️ هياكل البيانات",   "fr": "🗂️ Structures de données"},
    "func":  {"ar": "🧩 الدوال",           "fr": "🧩 Fonctions"},
}
def L(k): return LL[k][lang]

# ─────────────────────────────────────────────
# QCM DATA  (opts may be list or dict{ar,fr})
# ─────────────────────────────────────────────
QCM_DATA = [
    # ── Variables ──
    {"lesson":"vars",
     "q":     {"ar":"أيّ من هذه الأسماء صحيح في Python؟",
               "fr":"Quel nom de variable est valide en Python ?"},
     "opts":  ["2myVar","my_var2","my-var","class"], "ans":1,
     "fb_ok": {"ar":"✓ my_var2 يبدأ بحرف ويستخدم snake_case — صحيح تماماً!",
               "fr":"✓ my_var2 commence par une lettre et utilise snake_case — parfait !"},
     "fb_no": {"ar":"✗ لا يجوز البدء برقم، الشرطة العادية، أو الكلمات المحجوزة.",
               "fr":"✗ On ne peut pas commencer par un chiffre, un tiret ou un mot réservé."}},

    {"lesson":"vars",
     "q":     {"ar":"ما نوع المتغير: price = 9.99 ؟",
               "fr":"Quel est le type de : price = 9.99 ?"},
     "opts":  ["int","float","str","bool"], "ans":1,
     "fb_ok": {"ar":"✓ أي رقم بفاصلة عشرية هو float.",
               "fr":"✓ Tout nombre avec un point décimal est un float."},
     "fb_no": {"ar":"✗ 9.99 يحتوي فاصلة عشرية → float وليس int.",
               "fr":"✗ 9.99 contient un point décimal → float, pas int."}},

    {"lesson":"vars",
     "q":     {"ar":"ما الناتج؟  a, b = 5, 10  →  a, b = b, a  →  print(a)",
               "fr":"Quel est le résultat ?  a, b = 5, 10  →  a, b = b, a  →  print(a)"},
     "opts":  {"ar":["5","10","خطأ في الكود","None"],"fr":["5","10","Erreur","None"]}, "ans":1,
     "fb_ok": {"ar":"✓ بعد التبادل a يأخذ قيمة b القديمة = 10.",
               "fr":"✓ Après l'échange, a prend l'ancienne valeur de b = 10."},
     "fb_no": {"ar":"✗ Python يُبادل القيمتين في خطوة واحدة → a = 10.",
               "fr":"✗ Python échange les deux valeurs en une seule étape → a = 10."}},

    # ── While ──
    {"lesson":"while",
     "q":     {"ar":"ما الجزء الذي إذا نسيناه تصبح الحلقة لا نهائية؟",
               "fr":"Quelle partie, si oubliée, provoque une boucle infinie ?"},
     "opts":  {"ar":["التهيئة","الشرط","التحديث","جسم الحلقة"],
               "fr":["Initialisation","Condition","Mise à jour","Corps de la boucle"]}, "ans":2,
     "fb_ok": {"ar":"✓ بدون التحديث يظل الشرط True إلى الأبد!",
               "fr":"✓ Sans mise à jour, la condition reste True indéfiniment !"},
     "fb_no": {"ar":"✗ التحديث هو ما يُغير المتغير ويجعل الشرط يصبح False.",
               "fr":"✗ La mise à jour modifie la variable pour que la condition devienne False."}},

    {"lesson":"while",
     "q":     {"ar":"ما ناتج  4752 % 10 ؟","fr":"Quel est le résultat de  4752 % 10 ?"},
     "opts":  ["4","475","2","7"], "ans":2,
     "fb_ok": {"ar":"✓ % يُعطي الباقي → 4752 = 475×10 + 2",
               "fr":"✓ % donne le reste → 4752 = 475×10 + 2"},
     "fb_no": {"ar":"✗ % يعطي الباقي من القسمة — الرقم الأخير من العدد.",
               "fr":"✗ % donne le reste de la division — ici le dernier chiffre du nombre."}},

    {"lesson":"while",
     "q":     {"ar":"مكافئ  not(A and B)  بقانون دي مورغان؟",
               "fr":"Équivalent de  not(A and B)  selon De Morgan ?"},
     "opts":  ["not A and not B","not A or not B","A or B","A and B"], "ans":1,
     "fb_ok": {"ar":"✓ not(A and B) = not A or not B — قانون دي مورغان!",
               "fr":"✓ not(A and B) = not A or not B — loi de De Morgan !"},
     "fb_no": {"ar":"✗ عند نفي and تتحول إلى or مع نفي كل طرف.",
               "fr":"✗ En niant un and, il se transforme en or avec chaque terme nié."}},

    # ── For ──
    {"lesson":"for",
     "q":     {"ar":"كم رقماً تُنتج  range(3, 8) ؟",
               "fr":"Combien de nombres produit  range(3, 8) ?"},
     "opts":  ["6","5","8","3"], "ans":1,
     "fb_ok": {"ar":"✓ range(3,8) → 3,4,5,6,7 — خمسة أرقام (stop غير مضمّن).",
               "fr":"✓ range(3,8) → 3,4,5,6,7 — cinq nombres (stop exclu)."},
     "fb_no": {"ar":"✗ range(3,8) تنتج: 3,4,5,6,7 — وهي 5 أرقام.",
               "fr":"✗ range(3,8) produit : 3,4,5,6,7 — soit 5 nombres."}},

    {"lesson":"for",
     "q":     {"ar":"ما الناتج؟  range(10, 0, -2)",
               "fr":"Que produit  range(10, 0, -2) ?"},
     "opts":  {"ar":["10,8,6,4,2,0","10,8,6,4,2","0,2,4,6,8,10","لا شيء"],
               "fr":["10,8,6,4,2,0","10,8,6,4,2","0,2,4,6,8,10","Rien"]}, "ans":1,
     "fb_ok": {"ar":"✓ step=-2 يبدأ من 10 وينتهي عند 2 (stop=0 غير مضمّن).",
               "fr":"✓ step=-2 commence à 10 et s'arrête à 2 (stop=0 exclu)."},
     "fb_no": {"ar":"✗ stop=0 غير مضمّن، آخر قيمة هي 2.",
               "fr":"✗ stop=0 est exclu, la dernière valeur est 2."}},

    {"lesson":"for",
     "q":     {"ar":"ما قيمة total بعد:  total=0  →  for i in range(4): total+=i",
               "fr":"Quelle est la valeur de total après :  total=0  →  for i in range(4): total+=i"},
     "opts":  ["10","6","4","0"], "ans":1,
     "fb_ok": {"ar":"✓ range(4)=0,1,2,3 → المجموع = 0+1+2+3 = 6",
               "fr":"✓ range(4)=0,1,2,3 → somme = 0+1+2+3 = 6"},
     "fb_no": {"ar":"✗ range(4) تنتج 0,1,2,3. المجموع = 0+1+2+3 = 6.",
               "fr":"✗ range(4) produit 0,1,2,3. Somme = 0+1+2+3 = 6."}},

    # ── Conditions ──
    {"lesson":"cond",
     "q":     {"ar":"ما الناتج إذا score=65 ؟\nif score>=90: print('A')  elif score>=60: print('B')  else: print('C')",
               "fr":"Que s'affiche si score=65 ?\nif score>=90: print('A')  elif score>=60: print('B')  else: print('C')"},
     "opts":  {"ar":["A","B","C","خطأ"],"fr":["A","B","C","Erreur"]}, "ans":1,
     "fb_ok": {"ar":"✓ score=65 أكبر من 60 → elif يُطبع B.",
               "fr":"✓ score=65 est ≥ 60 → le elif affiche B."},
     "fb_no": {"ar":"✗ score=65 يُحقق الشرط score>=60 → B.",
               "fr":"✗ score=65 satisfait score>=60 → B."}},

    {"lesson":"cond",
     "q":     {"ar":"الفرق بين  =  و  == ؟",
               "fr":"Quelle est la différence entre  =  et  == ?"},
     "opts":  {"ar":["لا فرق","== للإسناد","= للإسناد و == للمقارنة","للأرقام فقط"],
               "fr":["Aucune différence","== pour l'affectation","= pour affecter, == pour comparer","Pour les nombres seulement"]}, "ans":2,
     "fb_ok": {"ar":"✓ = يضع قيمة، == يقارن قيمتين.",
               "fr":"✓ = affecte une valeur, == compare deux valeurs."},
     "fb_no": {"ar":"✗ = للإسناد (x=5)، == للمقارنة (x==5 يُرجع True/False).",
               "fr":"✗ = pour l'affectation (x=5), == pour la comparaison (x==5 → True/False)."}},

    {"lesson":"cond",
     "q":     {"ar":'ما الناتج؟  x = "مرحبا" if 10 > 5 else "وداعاً"',
               "fr":'Quel est le résultat ?  x = "Bonjour" if 10 > 5 else "Au revoir"'},
     "opts":  {"ar":["وداعاً","مرحبا","True","خطأ"],
               "fr":["Au revoir","Bonjour","True","Erreur"]}, "ans":1,
     "fb_ok": {"ar":'✓ الشرط 10>5 صحيح → x = "مرحبا".',
               "fr":'✓ La condition 10>5 est vraie → x = "Bonjour".'},
     "fb_no": {"ar":"✗ في التعبير الثلاثي القيمة الأولى تُختار عند تحقق الشرط.",
               "fr":"✗ Dans l'expression ternaire, la 1ère valeur est choisie si la condition est vraie."}},

    # ── Data Structures ──
    {"lesson":"ds",
     "q":     {"ar":"أيّ هيكل بيانات يُزيل التكرار تلقائياً؟",
               "fr":"Quelle structure de données supprime automatiquement les doublons ?"},
     "opts":  ["List","Tuple","Dictionary","Set"], "ans":3,
     "fb_ok": {"ar":"✓ Set تُزيل التكرار تلقائياً — كل عنصر يظهر مرة واحدة فقط.",
               "fr":"✓ Le Set supprime automatiquement les doublons — chaque élément est unique."},
     "fb_no": {"ar":"✗ Set هي الوحيدة التي تضمن فرادة العناصر.",
               "fr":"✗ Seul le Set garantit l'unicité des éléments."}},

    {"lesson":"ds",
     "q":     {"ar":"ما الفرق الجوهري بين List وTuple؟",
               "fr":"Quelle est la différence fondamentale entre List et Tuple ?"},
     "opts":  {"ar":["List أسرع","Tuple ثابتة لا يمكن تعديلها","List لا تقبل الأرقام","Tuple تقبل أنواعاً أكثر"],
               "fr":["List est plus rapide","Tuple est immuable (non modifiable)","List n'accepte pas les nombres","Tuple accepte plus de types"]}, "ans":1,
     "fb_ok": {"ar":"✓ Tuple ثابتة (immutable) — أي تعديل يُطلق TypeError.",
               "fr":"✓ Tuple est immuable — toute modification lève TypeError."},
     "fb_no": {"ar":"✗ الفرق الجوهري: Tuple لا تتغير بعد الإنشاء.",
               "fr":"✗ La différence clé : Tuple ne peut pas être modifiée après création."}},

    {"lesson":"ds",
     "q":     {"ar":'ما ناتج:  d = {"x": 10}  →  d.get("y", 99)',
               "fr":'Que retourne :  d = {"x": 10}  →  d.get("y", 99)'},
     "opts":  ["10","None","KeyError","99"], "ans":3,
     "fb_ok": {"ar":'✓ get() يُرجع القيمة الافتراضية 99 لأن المفتاح "y" غير موجود.',
               "fr":'✓ get() retourne la valeur par défaut 99 car la clé "y" est absente.'},
     "fb_no": {"ar":"✗ get(key, default) يُرجع القيمة الافتراضية عند غياب المفتاح.",
               "fr":"✗ get(key, default) retourne la valeur par défaut si la clé est absente."}},

    # ── Functions ──
    {"lesson":"func",
     "q":     {"ar":"ماذا ترجع دالة بلا return ؟",
               "fr":"Que retourne une fonction sans return ?"},
     "opts":  {"ar":["0","False","None","خطأ"],"fr":["0","False","None","Erreur"]}, "ans":2,
     "fb_ok": {"ar":"✓ كل دالة بلا return ترجع None تلقائياً.",
               "fr":"✓ Toute fonction sans return renvoie None implicitement."},
     "fb_no": {"ar":"✗ Python لا ترفع خطأ — ترجع None بشكل ضمني.",
               "fr":"✗ Python ne lève pas d'erreur — il retourne None implicitement."}},

    {"lesson":"func",
     "q":     {"ar":"ما الناتج؟  def f(x, y=5): return x + y  ←  f(3)",
               "fr":"Quel est le résultat ?  def f(x, y=5): return x + y  ←  f(3)"},
     "opts":  {"ar":["3","8","5","خطأ"],"fr":["3","8","5","Erreur"]}, "ans":1,
     "fb_ok": {"ar":"✓ x=3 وy=5 (افتراضي) → 3+5 = 8.",
               "fr":"✓ x=3 et y=5 (valeur par défaut) → 3+5 = 8."},
     "fb_no": {"ar":"✗ y=5 افتراضي — إذا لم تُمرّري قيمة يُستخدم 5 → 3+5=8.",
               "fr":"✗ y=5 est la valeur par défaut — si rien n'est passé, y=5 → 3+5=8."}},

    {"lesson":"func",
     "q":     {"ar":"ما الذي تفعله *args ؟","fr":"À quoi sert *args ?"},
     "opts":  {"ar":["لا فرق عن المعامل العادي","تُرجع قائمة","تقبل عدداً غير محدود من القيم كـ tuple","للنصوص فقط"],
               "fr":["Identique à un paramètre normal","Retourne une liste","Accepte un nombre illimité d'arguments (tuple)","Pour les chaînes seulement"]}, "ans":2,
     "fb_ok": {"ar":"✓ *args تجمع الحجج في tuple بلا حد للعدد.",
               "fr":"✓ *args regroupe les arguments dans un tuple sans limite de nombre."},
     "fb_no": {"ar":"✗ *args يجمع الحجج في tuple — ليس list.",
               "fr":"✗ *args regroupe les arguments dans un tuple — pas une liste."}},
]

def q_opts(q):
    o = q["opts"]
    return o[lang] if isinstance(o, dict) else o

# ─────────────────────────────────────────────
# EXERCISES
# ─────────────────────────────────────────────
EXERCISES = [
    {"id":"ex_vars","lesson":"vars",
     "title":  {"ar":"تبادل متغيرين",            "fr":"Échange de deux variables"},
     "desc":   {"ar":"أنشئ `a = 10` و `b = 20`، بادلي قيمتيهما في سطر واحد، ثم اطبعي `a` ثم `b`.",
                "fr":"Créez `a = 10` et `b = 20`, échangez leurs valeurs en une ligne, puis affichez `a` puis `b`."},
     "starter":"a = 10\nb = 20\n# Swap here / بادلي هنا\n\nprint(a)\nprint(b)",
     "expected":"20\n10",
     "hint":   {"ar":"استخدمي:  a, b = b, a","fr":"Utilisez :  a, b = b, a"}},

    {"id":"ex_while","lesson":"while",
     "title":  {"ar":"مجموع الأرقام الفردية",     "fr":"Somme des nombres impairs"},
     "desc":   {"ar":"باستخدام حلقة while، احسبي مجموع الأرقام الفردية من 1 إلى 9 (يشمل 9) واطبعي النتيجة.",
                "fr":"Avec une boucle while, calculez la somme des nombres impairs de 1 à 9 (inclus) et affichez le résultat."},
     "starter":"total = 0\ni = 1\n# Complete here / أكملي هنا\n\nprint(total)",
     "expected":"25",
     "hint":   {"ar":"استخدمي  i % 2 != 0  للفحص، وزيدي i بـ 1.",
                "fr":"Utilisez  i % 2 != 0  pour tester, et incrémentez i de 1."}},

    {"id":"ex_for","lesson":"for",
     "title":  {"ar":"طباعة جدول الضرب",          "fr":"Table de multiplication"},
     "desc":   {"ar":"باستخدام حلقة for، اطبعي جدول ضرب 3 من 1 إلى 5 بالشكل:  3 x 1 = 3",
                "fr":"Avec une boucle for, affichez la table de 3 de 1 à 5 sous la forme :  3 x 1 = 3"},
     "starter":"n = 3\nfor i in range(1, 6):\n    pass  # modify this / عدّلي هذا",
     "expected":"3 x 1 = 3\n3 x 2 = 6\n3 x 3 = 9\n3 x 4 = 12\n3 x 5 = 15",
     "hint":   {"ar":'استخدمي  print(f"{n} x {i} = {n*i}")',
                "fr":'Utilisez  print(f"{n} x {i} = {n*i}")'}},

    {"id":"ex_cond","lesson":"cond",
     "title":  {"ar":"تصنيف الدرجة",              "fr":"Classification de la note"},
     "desc":   {"ar":"اكتبي كوداً يطبع التصنيف لـ `score = 73`:\n- 90+ → ممتاز\n- 70–89 → جيد جداً\n- 50–69 → مقبول\n- أقل من 50 → راسب",
                "fr":"Écrivez un code qui affiche la mention pour `score = 73` :\n- 90+ → Excellent\n- 70–89 → Très bien\n- 50–69 → Passable\n- Moins de 50 → Échec"},
     "starter":"score = 73\n# Complete here / أكملي هنا\n",
     "expected_ar":"جيد جداً",
     "expected_fr":"Très bien",
     "hint":   {"ar":"استخدمي if / elif / else مع >= ","fr":"Utilisez if / elif / else avec >= "}},

    {"id":"ex_ds","lesson":"ds",
     "title":  {"ar":"إزالة التكرار من قائمة",    "fr":"Suppression des doublons"},
     "desc":   {"ar":"`nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]`\nحوّليها إلى set ثم ارجعيها إلى list مرتّبة واطبعيها.",
                "fr":"`nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]`\nConvertissez en set, revenez à une list triée et affichez."},
     "starter":"nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]\n# Complete here / أكملي هنا\n",
     "expected":"[1, 2, 3, 4, 5, 6, 9]",
     "hint":   {"ar":"استخدمي:  sorted(list(set(nums)))","fr":"Utilisez :  sorted(list(set(nums)))"}},

    {"id":"ex_func","lesson":"func",
     "title":  {"ar":"دالة مجموع القائمة",        "fr":"Fonction somme d'une liste"},
     "desc":   {"ar":"اكتبي `my_sum(lst)` تحسب المجموع بدون `sum()` ثم اطبعي `my_sum([1, 2, 3, 4, 5])`.",
                "fr":"Écrivez `my_sum(lst)` qui calcule la somme sans `sum()`, puis affichez `my_sum([1, 2, 3, 4, 5])`."},
     "starter":"def my_sum(lst):\n    # Complete here / أكملي هنا\n    pass\n\nprint(my_sum([1, 2, 3, 4, 5]))",
     "expected":"15",
     "hint":   {"ar":"استخدمي حلقة for لجمع العناصر في متغير total.",
                "fr":"Utilisez une boucle for pour accumuler les éléments dans total."}},
]

def ex_expected(ex):
    if "expected_ar" in ex:
        return ex["expected_ar"] if is_ar else ex["expected_fr"]
    return ex["expected"]

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for k, v in [("qcm_answers",{}),("qcm_locked",{}),
             ("ex_results",{}),("ex_outputs",{}),("ex_codes",{})]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def run_code(code):
    buf = io.StringIO(); err = None
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, "<student>", "exec"), {})
    except Exception:
        err = traceback.format_exc(limit=4)
    return buf.getvalue().strip(), err

def total_qcm(): return sum(1 for i,q in enumerate(QCM_DATA) if st.session_state.qcm_answers.get(i)==q["ans"])
def total_ex():  return sum(1 for v in st.session_state.ex_results.values() if v)
def all_qcm():   return len(st.session_state.qcm_locked)==len(QCM_DATA)
def all_ex():    return len(st.session_state.ex_results)==len(EXERCISES)

# ─────────────────────────────────────────────
# LANGUAGE TOGGLE
# ─────────────────────────────────────────────
c1, c2, _ = st.columns([1.2, 1.2, 4])
with c1:
    if st.button("🇩🇿 العربية", type="primary" if is_ar else "secondary", use_container_width=True):
        st.session_state.lang = "ar"; st.rerun()
with c2:
    if st.button("🇫🇷 Français", type="primary" if not is_ar else "secondary", use_container_width=True):
        st.session_state.lang = "fr"; st.rerun()

st.markdown("<hr style='margin:.4rem 0 1.4rem;border-color:rgba(255,255,255,.07)'>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <h1>{t('app_title')}</h1>
    <p style="color:#8890B5;font-size:1.05rem">{t('app_sub')}</p>
    <p style="color:#4ECDC4;font-weight:700;font-size:.9rem">{t('byline')}</p>
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([t("tab_qcm"), t("tab_ex"), t("tab_score")])

# ══ TAB 1 ── QCM ══════════════════════════════
with tab1:
    st.markdown(t("qcm_title"))
    st.caption(t("qcm_cap"))

    for lk in list(dict.fromkeys(q["lesson"] for q in QCM_DATA)):
        qs = [(i, q) for i, q in enumerate(QCM_DATA) if q["lesson"] == lk]
        st.markdown(f"---\n#### {L(lk)}")
        for (gi, q) in qs:
            st.markdown(f'<div class="section-badge">{t("q_lbl")} {gi+1} / {len(QCM_DATA)}</div>', unsafe_allow_html=True)
            st.markdown(f"**{q['q'][lang]}**")
            locked = st.session_state.qcm_locked.get(gi, False)
            opts   = q_opts(q)
            if not locked:
                cols = st.columns(2)
                for oi, opt in enumerate(opts):
                    with cols[oi % 2]:
                        if st.button(opt, key=f"q{gi}o{oi}{lang}"):
                            st.session_state.qcm_answers[gi] = oi
                            st.session_state.qcm_locked[gi]  = True
                            st.rerun()
            else:
                chosen = st.session_state.qcm_answers.get(gi)
                correct = q["ans"]
                if chosen == correct:
                    st.markdown(f'<div class="correct-box">✅ {q["fb_ok"][lang]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(
                        f'<div class="wrong-box">❌ {q["fb_no"][lang]}<br>'
                        f'<span style="color:#8890B5">{t("correct_ans")} <strong>{opts[correct]}</strong></span></div>',
                        unsafe_allow_html=True)

    if all_qcm():
        st.success(f"{t('qcm_done')} {total_qcm()} / {len(QCM_DATA)}")
    else:
        done = len(st.session_state.qcm_locked)
        st.markdown(f'<p class="progress-label">{t("prog_q")} {done} / {len(QCM_DATA)}</p>', unsafe_allow_html=True)
        st.progress(done / len(QCM_DATA))

# ══ TAB 2 ── EXERCISES ════════════════════════
with tab2:
    st.markdown(t("ex_title"))
    st.caption(t("ex_cap"))

    for ex in EXERCISES:
        eid = ex["id"]
        st.markdown(f"---\n#### {L(ex['lesson'])} — {ex['title'][lang]}")
        st.markdown(ex["desc"][lang])

        default = st.session_state.ex_codes.get(eid, ex["starter"])
        code = st.text_area("code", value=default, height=180,
                            key=f"ta{eid}{lang}", label_visibility="collapsed")
        st.session_state.ex_codes[eid] = code

        cr, ch = st.columns([1, 1])
        with cr: run_btn  = st.button(t("run"),  key=f"run{eid}{lang}", type="primary")
        with ch: hint_btn = st.button(t("hint"), key=f"hint{eid}{lang}")

        if hint_btn:
            st.info(f"{t('hint_lbl')} {ex['hint'][lang]}")

        if run_btn:
            out, err = run_code(code)
            st.session_state.ex_outputs[eid] = (out, err)
            st.session_state.ex_results[eid] = (not err) and (out.strip() == ex_expected(ex).strip())

        if eid in st.session_state.ex_outputs:
            out, err = st.session_state.ex_outputs[eid]
            if err:
                st.markdown(f'<div class="error-box">{t("code_err")}\n{err}</div>', unsafe_allow_html=True)
            elif st.session_state.ex_results.get(eid):
                st.markdown(f'<div class="correct-box">{t("ok_out")}<br><code>{out}</code></div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="wrong-box">{t("ko_out")}<br>'
                    f'<code>{out or t("no_out")}</code><br>'
                    f'<span style="color:#8890B5">{t("expected")} <code>{ex_expected(ex)}</code></span></div>',
                    unsafe_allow_html=True)

    if all_ex():
        st.success(f"{t('ex_done')} {total_ex()} / {len(EXERCISES)}")
    else:
        done = len(st.session_state.ex_results)
        st.markdown(f'<p class="progress-label">{t("prog_ex")} {done} / {len(EXERCISES)}</p>', unsafe_allow_html=True)
        st.progress(done / len(EXERCISES))

# ══ TAB 3 ── SCORE ════════════════════════════
with tab3:
    st.markdown(t("score_ttl"))

    if not all_qcm() or not all_ex():
        missing = []
        if not all_qcm(): missing.append(f"{t('mis_qcm')} ({len(st.session_state.qcm_locked)}/{len(QCM_DATA)} {t('completed')})")
        if not all_ex():  missing.append(f"{t('mis_ex')} ({len(st.session_state.ex_results)}/{len(EXERCISES)} {t('completed')})")
        st.warning(t("warn_pfx") + ("\n- ".join(missing)))
    else:
        qs  = total_qcm(); es = total_ex()
        tc  = qs + es;     tp = len(QCM_DATA) + len(EXERCISES)
        pct = round(tc / tp * 100, 1)
        ok  = pct >= 45
        ec  = "#52D68A" if ok else "#FF6B6B"
        ds_bg  = "linear-gradient(135deg,#4ECDC4,#7C6FE0)" if ok else "rgba(255,107,107,0.1)"
        ds_brd = "" if ok else "border:1px solid rgba(255,107,107,0.3);"
        ds_col = "#fff" if ok else "#FF6B6B"

        st.markdown(f"""
        <div class="score-card">
            <div style="font-size:3.5rem">{"🎉" if ok else "📚"}</div>
            <div class="score-num" style="color:{ec}">{pct}%</div>
            <div class="{"score-pass" if ok else "score-fail"}">{t("pass_txt") if ok else t("fail_txt")}</div>
            <div style="margin:1.5rem 0;display:flex;gap:1rem;justify-content:center;flex-wrap:wrap">
                <div style="background:#1a1f35;border-radius:12px;padding:1rem 1.5rem;min-width:140px">
                    <div style="color:#8890B5;font-size:.85rem">{t('lbl_qcm')}</div>
                    <div style="font-size:1.6rem;font-weight:900;color:#7C6FE0">{qs}<span style="font-size:1rem;color:#8890B5"> / {len(QCM_DATA)}</span></div>
                </div>
                <div style="background:#1a1f35;border-radius:12px;padding:1rem 1.5rem;min-width:140px">
                    <div style="color:#8890B5;font-size:.85rem">{t('lbl_ex')}</div>
                    <div style="font-size:1.6rem;font-weight:900;color:#4ECDC4">{es}<span style="font-size:1rem;color:#8890B5"> / {len(EXERCISES)}</span></div>
                </div>
                <div style="background:#1a1f35;border-radius:12px;padding:1rem 1.5rem;min-width:140px">
                    <div style="color:#8890B5;font-size:.85rem">{t('lbl_tot')}</div>
                    <div style="font-size:1.6rem;font-weight:900;color:#F7C948">{tc}<span style="font-size:1rem;color:#8890B5"> / {tp}</span></div>
                </div>
            </div>
            <div style="background:{ds_bg};{ds_brd}border-radius:12px;padding:1rem;margin-top:1rem">
                <span style="font-size:1.1rem;font-weight:900;color:{ds_col}">{t("ds_pass") if ok else t("ds_fail")}</span>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(t("breakdown"))
        lqm = {}
        for i, q in enumerate(QCM_DATA):
            lqm.setdefault(q["lesson"], []).append(st.session_state.qcm_answers.get(i) == q["ans"])
        lex = {ex["lesson"]: st.session_state.ex_results.get(ex["id"], False) for ex in EXERCISES}

        for lk in list(dict.fromkeys(q["lesson"] for q in QCM_DATA)):
            qr = lqm.get(lk, [])
            ok_l = sum(qr) + (1 if lex.get(lk, False) else 0)
            tot_l = len(qr) + 1
            col = "#52D68A" if ok_l == tot_l else "#F7C948" if ok_l > 0 else "#FF6B6B"
            ico = "✅" if ok_l == tot_l else "⚠️" if ok_l > 0 else "❌"
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        background:#0F1220;border:1px solid rgba(255,255,255,.07);
                        border-radius:10px;padding:.75rem 1.25rem;margin-bottom:.5rem;direction:ltr">
                <span style="font-weight:700">{ico} {L(lk)}</span>
                <span style="color:{col};font-weight:900;font-family:monospace">{ok_l} / {tot_l}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        if st.button(t("reset"), type="secondary"):
            for k in ["qcm_answers","qcm_locked","ex_results","ex_outputs","ex_codes"]:
                st.session_state[k] = {}
            st.rerun()

import streamlit as st
import streamlit.components.v1 as components
from datetime import date, time
from korean_lunar_calendar import KoreanLunarCalendar

st.set_page_config(
    page_title="🌸 몽글몽글 만세력 🌸",
    page_icon="🌸",
    layout="centered"
)

# ---------------------------
# 기본 데이터
# ---------------------------
STEMS = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
BRANCHES = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

ELEMENTS = {
    "갑": "목", "을": "목",
    "병": "화", "정": "화",
    "무": "토", "기": "토",
    "경": "금", "신": "금",
    "임": "수", "계": "수",
    "자": "수", "해": "수",
    "인": "목", "묘": "목",
    "사": "화", "오": "화",
    "진": "토", "술": "토", "축": "토", "미": "토",
    "신": "금", "유": "금",
}

YINYANG = {
    "갑": "양", "병": "양", "무": "양", "경": "양", "임": "양",
    "을": "음", "정": "음", "기": "음", "신": "음", "계": "음",
    "자": "양", "인": "양", "진": "양", "오": "양", "신": "양", "술": "양",
    "축": "음", "묘": "음", "사": "음", "미": "음", "유": "음", "해": "음",
}

TEN_GODS = {
    # 일간 기준 간단 해석용 (귀여운 버전)
    "비견": "나와 쏙 빼닮은 단짝 친구 👯‍♀️",
    "겁재": "지기 싫어! 불타는 경쟁심 🔥",
    "식신": "냠냠 맛있는 거 먹고 신나게 놀기 🍰",
    "상관": "통통 튀는 아이디어 뱅크 ✨",
    "편재": "앗싸! 생각지도 못한 용돈 💸",
    "정재": "차곡차곡 모으는 알뜰살뜰 저금통 🐷",
    "편관": "으쌰으쌰! 책임감 넘치는 대장님 👑",
    "정관": "바른 생활 사나이/어린이 🌟",
    "편인": "엉뚱발랄 4차원 상상력 🎈",
    "정인": "따뜻한 엄마 품처럼 포근함 🧸",
}

# 일간 기준 천간 십성 관계표
TEN_GOD_TABLE = {
    "갑": {"갑": "비견", "을": "겁재", "병": "식신", "정": "상관", "무": "편재", "기": "정재", "경": "편관", "신": "정관", "임": "편인", "계": "정인"},
    "을": {"갑": "겁재", "을": "비견", "병": "상관", "정": "식신", "무": "정재", "기": "편재", "경": "정관", "신": "편관", "임": "정인", "계": "편인"},
    "병": {"갑": "편인", "을": "정인", "병": "비견", "정": "겁재", "무": "식신", "기": "상관", "경": "편재", "신": "정재", "임": "편관", "계": "정관"},
    "정": {"갑": "정인", "을": "편인", "병": "겁재", "정": "비견", "무": "상관", "기": "식신", "경": "정재", "신": "편재", "임": "정관", "계": "편관"},
    "무": {"갑": "편관", "을": "정관", "병": "편인", "정": "정인", "무": "비견", "기": "겁재", "경": "식신", "신": "상관", "임": "편재", "계": "정재"},
    "기": {"갑": "정관", "을": "편관", "병": "정인", "정": "편인", "무": "겁재", "기": "비견", "경": "상관", "신": "식신", "임": "정재", "계": "편재"},
    "경": {"갑": "편재", "을": "정재", "병": "편관", "정": "정관", "무": "편인", "기": "정인", "경": "비견", "신": "겁재", "임": "식신", "계": "상관"},
    "신": {"갑": "정재", "을": "편재", "병": "정관", "정": "편관", "무": "정인", "기": "편인", "경": "겁재", "신": "비견", "임": "상관", "계": "식신"},
    "임": {"갑": "식신", "을": "상관", "병": "편재", "정": "정재", "무": "편관", "기": "정관", "경": "편인", "신": "정인", "임": "비견", "계": "겁재"},
    "계": {"갑": "상관", "을": "식신", "병": "정재", "정": "편재", "무": "정관", "기": "편관", "경": "정인", "신": "편인", "임": "겁재", "계": "비견"},
}

# 일간별 자시 시작 천간
HOUR_STEM_START = {
    "갑": "갑", "기": "갑",
    "을": "병", "경": "병",
    "병": "무", "신": "무",
    "정": "경", "임": "경",
    "무": "임", "계": "임",
}

HOUR_BRANCH_TABLE = [
    ((23, 0), (23, 59), "자"),
    ((0, 0), (0, 59), "자"),
    ((1, 0), (2, 59), "축"),
    ((3, 0), (4, 59), "인"),
    ((5, 0), (6, 59), "묘"),
    ((7, 0), (8, 59), "진"),
    ((9, 0), (10, 59), "사"),
    ((11, 0), (12, 59), "오"),
    ((13, 0), (14, 59), "미"),
    ((15, 0), (16, 59), "신"),
    ((17, 0), (18, 59), "유"),
    ((19, 0), (20, 59), "술"),
    ((21, 0), (22, 59), "해"),
]

# ---------------------------
# 유틸 함수
# ---------------------------
def strip_unit(text: str) -> str:
    return text.replace("년", "").replace("월", "").replace("일", "").replace("(윤)", "").replace("(윤월)", "").strip()

def split_ganji(kor_gapja: str):
    parts = kor_gapja.split()
    if len(parts) < 3:
        raise ValueError(f"간지 문자열 파싱 실패: {kor_gapja}")
    year_ganji = strip_unit(parts[0])
    month_ganji = strip_unit(parts[1])
    day_ganji = strip_unit(parts[2])
    return year_ganji, month_ganji, day_ganji

def get_hour_branch(hour: int, minute: int) -> str:
    total = hour * 60 + minute
    for (sh, sm), (eh, em), branch in HOUR_BRANCH_TABLE:
        start = sh * 60 + sm
        end = eh * 60 + em
        if start <= end:
            if start <= total <= end:
                return branch
        else:
            if total >= start or total <= end:
                return branch
    return "자"

def get_hour_stem(day_stem: str, hour_branch: str) -> str:
    start_stem = HOUR_STEM_START[day_stem]
    start_idx = STEMS.index(start_stem)
    branch_idx = BRANCHES.index(hour_branch)
    stem_idx = (start_idx + branch_idx) % 10
    return STEMS[stem_idx]

def get_hour_ganji(day_stem: str, hour: int, minute: int) -> str:
    hour_branch = get_hour_branch(hour, minute)
    hour_stem = get_hour_stem(day_stem, hour_branch)
    return hour_stem + hour_branch

def get_ten_god(day_stem: str, other_stem: str) -> str:
    return TEN_GOD_TABLE.get(day_stem, {}).get(other_stem, "-")

def analyze_ohang(pillars):
    counts = {"목": 0, "화": 0, "토": 0, "금": 0, "수": 0}
    for pillar in pillars:
        if len(pillar) >= 2:
            stem = pillar[0]
            branch = pillar[1]
            counts[ELEMENTS[stem]] += 1
            counts[ELEMENTS[branch]] += 1
    return counts

def dominant_elements(counts):
    max_val = max(counts.values())
    min_val = min(counts.values())
    strong = [k for k, v in counts.items() if v == max_val]
    weak = [k for k, v in counts.items() if v == min_val]
    return strong, weak

def safe_set_solar(calendar_obj, y, m, d):
    ok = calendar_obj.setSolarDate(y, m, d)
    if not ok:
        raise ValueError("지원 범위를 벗어난 날짜이거나 잘못된 날짜입니다.")
    return calendar_obj

def get_full_saju(y: int, m: int, d: int, hour: int, minute: int):
    calendar = KoreanLunarCalendar()
    safe_set_solar(calendar, y, m, d)

    # 예: "정유년 병오월 임오일"
    gapja_kor = calendar.getGapJaString()
    year_ganji, month_ganji, day_ganji = split_ganji(gapja_kor)

    hour_ganji = get_hour_ganji(day_ganji[0], hour, minute)

    lunar_date = calendar.LunarIsoFormat()
    solar_date = calendar.SolarIsoFormat()
    is_intercalation = calendar.isIntercalation

    return {
        "solar_date": solar_date,
        "lunar_date": lunar_date,
        "is_intercalation": is_intercalation,
        "year_pillar": year_ganji,
        "month_pillar": month_ganji,
        "day_pillar": day_ganji,
        "hour_pillar": hour_ganji,
        "gapja_kor": gapja_kor,
    }

def get_today_saju():
    today = date.today()
    calendar = KoreanLunarCalendar()
    safe_set_solar(calendar, today.year, today.month, today.day)
    gapja_kor = calendar.getGapJaString()
    year_ganji, month_ganji, day_ganji = split_ganji(gapja_kor)
    return day_ganji

def make_summary(saju):
    day_stem = saju["day_pillar"][0]
    year_stem = saju["year_pillar"][0]
    month_stem = saju["month_pillar"][0]
    hour_stem = saju["hour_pillar"][0]

    year_tg = get_ten_god(day_stem, year_stem)
    month_tg = get_ten_god(day_stem, month_stem)
    hour_tg = get_ten_god(day_stem, hour_stem)

    pillars = [
        saju["year_pillar"],
        saju["month_pillar"],
        saju["day_pillar"],
        saju["hour_pillar"],
    ]
    counts = analyze_ohang(pillars)
    strong, weak = dominant_elements(counts)

    day_element = ELEMENTS[day_stem]
    day_yinyang = YINYANG[day_stem]

    summary = f"""
🌷 **나의 주인공 에너지는 {day_stem}({day_element}, {day_yinyang})**이에요!

- 🐣 **태어난 해의 요정 ({year_tg})**: {TEN_GODS.get(year_tg, "-")}
- 🐥 **태어난 달의 요정 ({month_tg})**: {TEN_GODS.get(month_tg, "-")}
- 🦉 **태어난 시간의 요정 ({hour_tg})**: {TEN_GODS.get(hour_tg, "-")}

🎨 오행 팔레트를 보면 **{", ".join(strong)} 기운이 뿜뿜!** 넘치구요,  
조금 더 챙겨주면 좋은 기운은 **{", ".join(weak)}**이랍니다.

**🎀 몽글몽글 조언 한마디 🎀**
- 일간은 내가 가진 가장 반짝이는 마법 에너지예요. ✨
- 달의 요정은 친구들과 어울릴 때, 학교나 직장에서 내 모습을 보여줘요.
- 시간의 요정은 내 마음속 깊은 곳, 혼자만의 비밀스러운 성격이랍니다.
- 넘치는 기운은 잘 퍼뜨려주고, 부족한 기운은 예쁜 색상이나 음식으로 채워보세요! 💖
"""
    return summary, counts

# ---------------------------
# 화면
# ---------------------------
st.markdown(
    """
    <div style="text-align:center; padding-top: 15px; padding-bottom: 20px; background-color: #fff0f5; border-radius: 20px; margin-bottom: 20px; box-shadow: 0px 4px 15px rgba(255, 182, 193, 0.4);">
        <h1 style="margin-bottom: 0.2em; color: #ff8eaa; font-family: 'Comic Sans MS', cursive, sans-serif;">🌸 몽글몽글 만세력 🌸</h1>
        <p style="font-size: 1.1rem; color: #ffb6c1; font-weight: bold;">
            내 안에 숨겨진 귀여운 운명의 요정들을 만나보세요! ✨
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.info("🎂 언제 태어났는지 알려주면, 너만의 귀여운 사주 팔자 요정들을 불러올게! 🪄")

with st.form("saju_form"):
    birth_date = st.date_input(
        "생년월일",
        value=date(1995, 1, 1),
        min_value=date(1000, 2, 13),
        max_value=date(2050, 12, 31),
    )
    birth_time = st.time_input(
        "출생 시간",
        value=time(12, 0),
        step=60,
    )
    submitted = st.form_submit_button("사주 보기")

if submitted:
    try:
        y, m, d = birth_date.year, birth_date.month, birth_date.day
        hh, mm = birth_time.hour, birth_time.minute

        saju = get_full_saju(y, m, d, hh, mm)
        summary_text, ohang_counts = make_summary(saju)

        st.success("만세력 계산이 완료되었습니다.")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("기본 정보")
            st.write(f"**양력:** {saju['solar_date']}")
            st.write(f"**음력:** {saju['lunar_date']}")
            st.write(f"**윤달 여부:** {'예' if saju['is_intercalation'] else '아니오'}")

        with col2:
            st.subheader("간지 정보")
            st.write(f"**연주:** {saju['year_pillar']}")
            st.write(f"**월주:** {saju['month_pillar']}")
            st.write(f"**일주:** {saju['day_pillar']}")
            st.write(f"**시주:** {saju['hour_pillar']}")

        st.subheader("사주 팔자")
        pillar_cols = st.columns(4)
        labels = ["연주", "월주", "일주", "시주"]
        values = [
            saju["year_pillar"],
            saju["month_pillar"],
            saju["day_pillar"],
            saju["hour_pillar"],
        ]

        for c, label, value in zip(pillar_cols, labels, values):
            with c:
                # 오행 색상 매핑 (파스텔 톤)
                pastel_colors = {
                    "목": "#e6fffa", # 옅은 청록
                    "화": "#fff5f5", # 옅은 분홍
                    "토": "#fffff0", # 옅은 노랑
                    "금": "#f8f9fa", # 옅은 회색
                    "수": "#ebf8ff"  # 옅은 파랑
                }
                bg_color = pastel_colors.get(ELEMENTS.get(value[0], "토"), "#ffffff")
                
                st.markdown(
                    f"""
                    <div style="
                        border:2px dashed #ffb6c1;
                        border-radius:20px;
                        padding:20px;
                        text-align:center;
                        background:{bg_color};
                        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
                    ">
                        <div style="font-size:0.9rem; color:#ff8eaa; font-weight:bold;">{label}</div>
                        <div style="font-size:2.2rem; font-weight:800; margin-top:10px; color:#4a4a4a;">{value}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.subheader("🎨 귀요미 오행 분포")
        ohang_cols = st.columns(5)
        for c, elem in zip(ohang_cols, ["목", "화", "토", "금", "수"]):
            with c:
                st.metric(f"{elem} 요정", f"{ohang_counts[elem]}마리")

        st.subheader("💌 요정들의 비밀 편지")
        st.markdown(summary_text)

        # --- 오늘의 운세 추가 ---
        st.divider()
        st.subheader("🌟 오늘의 콕 찍은 행운 퀴즈!")
        today_pillar = get_today_saju()
        today_stem = today_pillar[0]
        today_god = get_ten_god(saju['day_pillar'][0], today_stem)

        horoscope_messages = {
            "비견": "나랑 찰떡궁합인 친구들과 도란도란 수다 떨기 좋은 날! 🍰 하지만 너무 고집부리진 말기!",
            "겁재": "오늘은 왠지 예쁜 게 자꾸 눈에 들어오고 사고 싶어질지도 몰라! 💸 지갑 수비 요정 출동!",
            "식신": "맛있는 간식 챙겨 먹고, 내 맘대로 뒹굴거리거나 취미 생활하기 딱 좋은 날! 🍩",
            "상관": "반짝이는 아이디어가 퐁퐁 솟아나는 날! ✨ 하지만 친구한테 말할 땐 한 번 더 생각하고 예쁘게 말하기!",
            "편재": "길 가다가 동전을 줍거나 깜짝 선물을 받을지도 몰라? 🎁 주위를 잘 살펴봐!",
            "정재": "사부작사부작 내 할 일을 꼼꼼하게 다 해내는 멋진 하루! 칭찬 스티커 쾅쾅! ⭐",
            "편관": "조금 벅찬 미션이 주어질 수 있지만, 멋지게 해내고 레벨업! 할 수 있는 엄청난 날이야 🦸‍♀️",
            "정관": "규칙을 잘 지키고 인사도 예쁘게 해서 칭찬 폭격 맞을 준비 완료! 💯 반장 스타일의 하루!",
            "편인": "명탐정처럼 상상력과 호기심이 폭발하는 날! 🔍 재미있는 웹툰이나 책을 읽기 딱 좋아!",
            "정인": "선생님이나 부모님, 착한 친구들의 따뜻한 도움을 받아 마음이 몽글몽글해질 거야 🧸"
        }
        
        horoscope_text = horoscope_messages.get(today_god, "포근하고 귀여운 하루가 될 거야! 🌷")
        
        st.info(f"오늘의 일진은 **{today_pillar}**일! 내 마법 에너지랑 만나서 **{today_god}** ({TEN_GODS.get(today_god, '-')}) 요정이 깨어났어! 🧚‍♀️\n\n**🎀 쉿, 너에게만 알려줄게:** {horoscope_text}")

        st.caption("※ 요정들의 속삭임은 전통 명리를 아주 귀엽게 바꾼 참고용 재미랍니다! 🐾")

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

st.markdown("---")
st.caption(
    "참고: 이 앱은 korean-lunar-calendar 기반으로 양력/음력 변환과 연·월·일 간지를 활용합니다. "
    "시주는 일간과 출생시를 바탕으로 계산했습니다."
)

components.html(
    """
    <script>
    const daysMap = {
        'Su': '일', 'Mo': '월', 'Tu': '화', 'We': '수', 'Th': '목', 'Fr': '금', 'Sa': '토',
        'Sun': '일', 'Mon': '월', 'Tue': '화', 'Wed': '수', 'Thu': '목', 'Fri': '금', 'Sat': '토'
    };
    const observer = new MutationObserver(function(mutations) {
        const p = window.parent.document;
        const cals = p.querySelectorAll('div[data-baseweb="calendar"]');
        cals.forEach(cal => {
            const walker = p.createTreeWalker(cal, NodeFilter.SHOW_TEXT, null, false);
            let n;
            while(n = walker.nextNode()) {
                const text = n.nodeValue.trim();
                if (daysMap[text]) {
                    n.nodeValue = daysMap[text];
                }
            }
        });
    });
    observer.observe(window.parent.document.body, {childList: true, subtree: true});
    </script>
    """,
    height=0,
    width=0
)

#!/usr/bin/env python3
"""Generate 1,024 individual Pokemon pages from pokemon.json.

Each page is a standalone HTML file with:
  - Korean / English / Japanese name
  - Type badges (color + emoji)
  - Stats (stamina, attack, defense) with visual bars
  - Quick moves & cinematic moves with Korean translations
  - Evolution chain
  - Generation / region info
  - Prev / Next navigation

Output: pokedex/pokemon-{dexNr}-{korean_name}.html
"""

import json
import os
import re

# ----------------------------------------------------------------
# Source data
# ----------------------------------------------------------------
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pokemon.json")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pokedex")

# ----------------------------------------------------------------
# Type display data (from pokemon.js)
# ----------------------------------------------------------------
TYPE_COLORS = {
    "격투": "#FF8000", "비행": "#A890FF", "독": "#A838F8",
    "땅": "#E8CB68", "바위": "#B8A038", "벌레": "#A8B820",
    "고스트": "#705898", "얼음": "#98D8D8", "드래곤": "#7038F8",
    "강철": "#B8B8D0", "불꽃": "#F08030", "물": "#6890F0",
    "풀": "#78C850", "전기": "#F8D030", "에스퍼": "#F85888",
    "노말": "#A8A878", "페어리": "#EE99AC",
}

TYPE_EMOJI = {
    "격투": "🥊", "비행": "🕊️", "독": "☠️", "땅": "🏔️",
    "바위": "🪨", "벌레": "🐛", "고스트": "👻", "얼음": "❄️",
    "드래곤": "🐉", "강철": "⚙️", "불꽃": "🔥", "물": "💧",
    "풀": "🌿", "전기": "⚡", "에스퍼": "🔮", "노말": "⚪", "페어리": "🧚",
}

# ----------------------------------------------------------------
# Move name Korean mapping (from pokemon.js MOVES_KOREAN)
# ----------------------------------------------------------------
MOVES_KOREAN = {
    # --- 퀵 스킬 (Fast Moves) ---
    "ACID_FAST": "독물폭풍",
    "AIR_SLASH_FAST": "에어슬래시",
    "ASTONISH_FAST": "깜짝공격",
    "BITE_FAST": "물기",
    "BUBBLE_FAST": "거품",
    "BUG_BITE_FAST": "벌레먹기",
    "BULLET_PUNCH_FAST": "불릿펀치",
    "BULLET_SEED_FAST": "씨기관총",
    "CHARGE_BEAM_FAST": "차지빔",
    "CHARM_FAST": "애교부리기",
    "CONFUSION_FAST": "사념의박치기",
    "COUNTER_FAST": "카운터",
    "CUT_FAST": "풀베기",
    "DOUBLE_KICK_FAST": "두발차기",
    "DRAGON_BREATH_FAST": "용의숨결",
    "DRAGON_TAIL_FAST": "드래곤테일",
    "EMBER_FAST": "불꽃송이",
    "EXTRASENSORY_FAST": "염동력",
    "FAIRY_WIND_FAST": "요정의바람",
    "FEINT_ATTACK_FAST": "기습공격",
    "FIRE_FANG_FAST": "불꽃얼음",
    "FIRE_SPIN_FAST": "회오리불꽃",
    "FORCE_PALM_FAST": "파장손",
    "FROST_BREATH_FAST": "얼음숨결",
    "FURY_CUTTER_FAST": "연속자르기",
    "GUST_FAST": "바람일으키기",
    "HEX_FAST": "저주",
    "HIDDEN_POWER_FAST": "잠재파워",
    "ICE_FANG_FAST": "얼음얼음",
    "ICE_SHARD_FAST": "얼음조각",
    "INCINERATE_FAST": "태우기",
    "INFESTATION_FAST": "엉켜붙기",
    "IRON_TAIL_FAST": "아이언테일",
    "KARATE_CHOP_FAST": "태권체조",
    "LEAFAGE_FAST": "잎새날리기",
    "LICK_FAST": "핥기",
    "LOCK_ON_FAST": "조준",
    "LOW_KICK_FAST": "로우킥",
    "MAGICAL_LEAF_FAST": "매지컬리프",
    "METAL_CLAW_FAST": "메탈클로",
    "METAL_SOUND_FAST": "메탈사운드",
    "MUD_SHOT_FAST": "머드샷",
    "MUD_SLAP_FAST": "진흙던지기",
    "PECK_FAST": "쪼기",
    "POISON_JAB_FAST": "독찌르기",
    "POISON_STING_FAST": "독침",
    "POUND_FAST": "두드리기",
    "POWDER_SNOW_FAST": "눈가루",
    "PRESENT_FAST": "선물건네기",
    "PSYCHO_CUT_FAST": "사이코커팅",
    "PSYWAVE_FAST": "심파동",
    "QUICK_ATTACK_FAST": "전광석화",
    "RAZOR_LEAF_FAST": "날카로운잎",
    "ROCK_SMASH_FAST": "바위깨기",
    "ROCK_THROW_FAST": "돌던지기",
    "ROLLOUT_FAST": "구르기",
    "SAND_ATTACK_FAST": "모래날리기",
    "SCRATCH_FAST": "할퀴기",
    "SHADOW_CLAW_FAST": "섀도클로",
    "SMACK_DOWN_FAST": "내리찍기",
    "SNARL_FAST": "윽소리",
    "SPARK_FAST": "스파크",
    "SPLASH_FAST": "물웅덩이",
    "STEEL_WING_FAST": "강철날개",
    "STRUGGLE_BUG_FAST": "벌레저항",
    "SUCKER_PUNCH_FAST": "안다리걸기",
    "TACKLE_FAST": "몸통박치기",
    "TAKE_DOWN_FAST": "몸통박치기",
    "THUNDER_FANG_FAST": "번개얼음",
    "THUNDER_SHOCK_FAST": "전기쇼크",
    "TRANSFORM_FAST": "변신",
    "VINE_WHIP_FAST": "덩굴채찍",
    "VOLT_SWITCH_FAST": "볼트체인지",
    "WATERFALL_FAST": "폭포오르기",
    "WATER_GUN_FAST": "물대포",
    "WATER_SHURIKEN_FAST": "물수리검",
    "WING_ATTACK_FAST": "날개치기",
    "YAWN_FAST": "하품",
    "ZEN_HEADBUTT_FAST": "사념의박치기",
    # --- 시네매틱/전기 스킬 (Charge Moves) ---
    "ACID_SPRAY": "독액분사",
    "ACROBATICS": "곡예비행",
    "AERIAL_ACE": "공중숙달",
    "AIR_CUTTER": "에어커터",
    "ANCIENT_POWER": "원시의힘",
    "AQUA_JET": "아쿠아제트",
    "AQUA_STEP": "아쿠아스텝",
    "AQUA_TAIL": "아쿠아테일",
    "AURA_SPHERE": "오라구슬",
    "AURA_WHEEL_ELECTRIC": "오라휠",
    "AURORA_BEAM": "오로라빔",
    "AVALANCHE": "눈사태",
    "BLAZE_KICK": "블레이즈킥",
    "BLIZZARD": "눈보라",
    "BODY_SLAM": "몸통박치기",
    "BONE_CLUB": "뼈공격",
    "BOOMBURST": "폭음파",
    "BRAVE_BIRD": "브레이브버드",
    "BREAKING_SWIPE": "깨는쓸기",
    "BRICK_BREAK": "바르기깨기",
    "BRINE": "소금물",
    "BRUTAL_SWING": "로켓박치기",
    "BUBBLE_BEAM": "거품광선",
    "BUG_BUZZ": "벌레의야단법석",
    "BULLDOZE": "짓밟기",
    "CLOSE_COMBAT": "인파이트",
    "CRABHAMMER": "집게해머",
    "CROSS_CHOP": "크로스촙",
    "CROSS_POISON": "크로스포이즌",
    "CRUNCH": "크런치",
    "DARKEST_LARIAT": "다크래리엇",
    "DARK_PULSE": "다크펄스",
    "DAZZLING_GLEAM": "매지컬샤인",
    "DIG": "굴파기",
    "DISARMING_VOICE": "매혹의목소리",
    "DISCHARGE": "방전",
    "DIVE": "다이빙",
    "DOOM_DESIRE": "파멸의소원",
    "DRACO_METEOR": "드라코메테오",
    "DRAGON_CLAW": "드래곤클로",
    "DRAGON_PULSE": "용의파동",
    "DRAINING_KISS": "드레인키스",
    "DRAIN_PUNCH": "드레인펀치",
    "DRILL_PECK": "드릴피크",
    "DRILL_RUN": "드릴라이너",
    "DRUM_BEATING": "드럼어택",
    "DYNAMIC_PUNCH": "역린",
    "EARTHQUAKE": "대지진",
    "EARTH_POWER": "대지의힘",
    "EMBER_FAST": "불꽃송이",
    "ENERGY_BALL": "에너지볼",
    "EXTRASENSORY_FAST": "염동력",
    "FAIRY_WIND_FAST": "요정의바람",
    "FEATHER_DANCE": "깃털댄스",
    "FEINT_ATTACK_FAST": "기습공격",
    "FELL_STINGER": "찝기",
    "FIRE_BLAST": "열풍",
    "FIRE_FANG_FAST": "불꽃얼음",
    "FIRE_PUNCH": "불꽃펀치",
    "FIRE_SPIN_FAST": "회오리불꽃",
    "FLAMETHROWER": "화염방사",
    "FLAME_BURST": "화염볼",
    "FLAME_CHARGE": "불꽃튀기기",
    "FLAME_WHEEL": "화염바퀴",
    "FLASH_CANNON": "섬광포",
    "FLOWER_TRICK": "트릭플라워",
    "FLY": "공중날기",
    "FLYING_PRESS": "플라잉프레스",
    "FOCUS_BLAST": "파동탄",
    "FORCE_PALM_FAST": "파장손",
    "FOUL_PLAY": "비명공세",
    "FROST_BREATH_FAST": "얼음숨결",
    "FURY_CUTTER_FAST": "연속자르기",
    "FUTURESIGHT": "미래예지",
    "GIGA_IMPACT": "기가임팩트",
    "GRASS_KNOT": "풀묶기",
    "GUNK_SHOT": "오물웨이브",
    "GUST_FAST": "바람일으키기",
    "GYRO_BALL": "자이로볼",
    "HEAT_WAVE": "열사의폭풍",
    "HEAVY_SLAM": "헤비슬램",
    "HEX_FAST": "저주",
    "HIDDEN_POWER_FAST": "잠재파워",
    "HIGH_HORSEPOWER": "높은마력",
    "HORN_ATTACK": "뿔찌르기",
    "HURRICANE": "태풍",
    "HYDRO_PUMP": "하이드로펌프",
    "HYPER_BEAM": "파괴광선",
    "HYPER_FANG": "하이퍼팩",
    "ICE_BEAM": "냉동빔",
    "ICE_FANG_FAST": "얼음얼음",
    "ICE_PUNCH": "냉동펀치",
    "ICE_SHARD_FAST": "얼음조각",
    "ICICLE_SPEAR": "고드름침",
    "ICY_WIND": "얼어붙은바람",
    "INCINERATE_FAST": "태우기",
    "INFESTATION_FAST": "엉켜붙기",
    "IRON_HEAD": "아이언헤드",
    "IRON_TAIL_FAST": "아이언테일",
    "KARATE_CHOP_FAST": "태권체조",
    "LEAFAGE_FAST": "잎새날리기",
    "LEAF_BLADE": "리프블레이드",
    "LEAF_STORM": "리프스톰",
    "LEAF_TORNADO": "리프토네이도",
    "LICK_FAST": "핥기",
    "LIQUIDATION": "탁류",
    "LOCK_ON_FAST": "조준",
    "LOW_KICK_FAST": "로우킥",
    "LOW_SWEEP": "로우스윕",
    "LUNGE": "돌진",
    "MAGICAL_LEAF_FAST": "매지컬리프",
    "MAGNET_BOMB": "마그넷봄",
    "MEGAHORN": "메가혼",
    "METAL_CLAW_FAST": "메탈클로",
    "METAL_SOUND_FAST": "메탈사운드",
    "METEOR_BEAM": "메테오빔",
    "METEOR_MASH": "메테오매시",
    "MIRROR_COAT": "미러코트",
    "MIRROR_SHOT": "미러샷",
    "MOONBLAST": "문ون블라스",
    "MUDDY_WATER": "탁류",
    "MUD_BOMB": "진흙폭탄",
    "MUD_SHOT_FAST": "머드샷",
    "MUD_SLAP_FAST": "진흙던지기",
    "MYSTICAL_FIRE": "신비한불꽃",
    "NIGHT_SHADE": "그림자분출",
    "NIGHT_SLASH": "나이트슬래시",
    "OCTAZOOKA": "물거품아리아",
    "OMINOUS_WIND": "나이트헤드",
    "OUTRAGE": "광란의몸짓",
    "OVERHEAT": "열풍",
    "PARABOLIC_CHARGE": "파라볼라차지",
    "PAYBACK": "보복",
    "PECK_FAST": "쪼기",
    "PETAL_BLIZZARD": "꽃보라",
    "PLASMA_FISTS": "플라스마피스트",
    "PLAY_ROUGH": "장난치기",
    "POISON_FANG": "맹독엄니",
    "POISON_JAB_FAST": "독찌르기",
    "POISON_STING_FAST": "독침",
    "POLTERGEIST": "폴터가이스트",
    "POUND_FAST": "두드리기",
    "POWDER_SNOW_FAST": "눈가루",
    "POWER_GEM": "파워젬",
    "POWER_UP_PUNCH": "파워펀치",
    "POWER_WHIP": "파워휩",
    "PRESENT_FAST": "선물건네기",
    "PSYBEAM": "사이코빔",
    "PSYCHIC": "사이코키네시스",
    "PSYCHIC_FANGS": "사이코펀치",
    "PSYCHO_BOOST": "사이코부스트",
    "PSYCHO_CUT_FAST": "사이코커팅",
    "PSYSHOCK": "사이코쇼크",
    "PSYWAVE_FAST": "심파동",
    "PYROBALL": "파이어볼",
    "QUICK_ATTACK_FAST": "전광석화",
    "RAZOR_LEAF_FAST": "날카로운잎",
    "RAZOR_SHELL": "셸블레이드",
    "ROCK_BLAST": "록블라스트",
    "ROCK_SLIDE": "바위무더기",
    "ROCK_SMASH_FAST": "바위깨기",
    "ROCK_THROW_FAST": "돌던지기",
    "ROCK_TOMB": "바위무덤",
    "ROCK_WRECKER": "암석포",
    "ROLLOUT_FAST": "구르기",
    "SACRED_SWORD": "성스러운칼",
    "SAND_ATTACK_FAST": "모래날리기",
    "SAND_TOMB": "모래지옥",
    "SCALD": "열탕",
    "SCORCHING_SANDS": "데 sandy",
    "SCRATCH_FAST": "할퀴기",
    "SEED_BOMB": "씨폭탄",
    "SEED_FLARE": "시드플레어",
    "SHADOW_BALL": "섀도볼",
    "SHADOW_CLAW_FAST": "섀도클로",
    "SHADOW_PUNCH": "섀도펀치",
    "SHADOW_SNEAK": "그림자꿰매기",
    "SIGNAL_BEAM": "시그널빔",
    "SILVER_WIND": "은빛바람",
    "SKULL_BASH": "두개골박치기",
    "SKY_ATTACK": "스카이어택",
    "SLUDGE": "쓰레기폭탄",
    "SLUDGE_BOMB": "쓰레기폭탄",
    "SLUDGE_WAVE": "쓰레기파도",
    "SMACK_DOWN_FAST": "내리찍기",
    "SNARL_FAST": "윽소리",
    "SNIPE_SHOT": "저격탄",
    "SOLAR_BEAM": "솔라빔",
    "SPARKLING_ARIA": "물거품아리아",
    "SPARK_FAST": "스파크",
    "SPIRIT_SHACKLE": "영결의사슬",
    "SPLASH_FAST": "물웅덩이",
    "STEEL_WING_FAST": "강철날개",
    "STOMP": "밟기",
    "STONE_EDGE": "스톤에지",
    "STRUGGLE": "분투",
    "STRUGGLE_BUG_FAST": "벌레저항",
    "SUBMISSION": "체념",
    "SUCKER_PUNCH_FAST": "안다리걸기",
    "SUPER_POWER": "슈퍼파워",
    "SURF": "파도타기",
    "SWIFT": "하트스탬프",
    "SYNCHRONOISE": "싱크로노이즈",
    "TACKLE_FAST": "몸통박치기",
    "TAKE_DOWN_FAST": "몸통박치기",
    "THUNDER": "10만마력",
    "THUNDERBOLT": "만볼트",
    "THUNDER_FANG_FAST": "번개얼음",
    "THUNDER_PUNCH": "번개펀치",
    "THUNDER_SHOCK_FAST": "전기쇼크",
    "TORCH_SONG": "플레어송",
    "TRAILBLAZE": "자취따르기",
    "TRANSFORM_FAST": "변신",
    "TRIPLE_AXEL": "트리플액셀",
    "TRI_ATTACK": "트라이어택",
    "TWISTER": "회오리",
    "UPPER_HAND": "상승기류",
    "VICE_GRIP": "집게",
    "VINE_WHIP_FAST": "덩굴채찍",
    "VOLT_SWITCH_FAST": "볼트체인지",
    "VOLT_TACKLE": "볼트태클",
    "V_CREATE": "V크래프트",
    "WATERFALL_FAST": "폭포오르기",
    "WATER_GUN_FAST": "물대포",
    "WATER_PULSE": "물의파동",
    "WATER_SHURIKEN_FAST": "물수리검",
    "WEATHER_BALL_FIRE": "웨더볼",
    "WEATHER_BALL_ICE": "웨더볼",
    "WEATHER_BALL_ROCK": "웨더볼",
    "WEATHER_BALL_WATER": "웨더볼",
    "WILD_CHARGE": "와일드차지",
    "WING_ATTACK_FAST": "날개치기",
    "WRAP": "풀묶기",
    "X_SCISSOR": "시저크로스",
    "YAWN_FAST": "하품",
    "ZAP_CANNON": "전자포",
    "ZEN_HEADBUTT_FAST": "사념의박치기",
}

REGION_KOREAN = {
    "kanto": "관동", "johto": "도쿠소", "hoenn": "호연", "sinnoh": "신오",
    "unova": "율려", "kalos": "가리아", "alola": "알로라", "galar": "지후",
    "paldea": "파르다",
}

GEN_KOREAN = {
    1: "1세대", 2: "2세대", 3: "3세대", 4: "4세대", 5: "5세대",
    6: "6세대", 7: "7세대", 8: "8세대", 9: "9세대",
}

CLASS_CSS = {
    "전설": "legendary",
    "신비": "mythical",
    "울트라비스트": "ultra-beast",
}


def slugify(name: str) -> str:
    """Create a URL-safe slug from a pokemon English name or ID.

    Handles edge cases like 'Sirfetch'd' (apostrophe), 'Mr. Mime' (period),
    and internal IDs like 'PORYGON_Z' (underscore).
    """
    s = name.lower()
    # Remove apostrophes, periods, underscores and any other non-alphanumeric
    s = s.replace("'", "").replace(".", "").replace("_", "")
    # Keep only lowercase letters, digits, hyphens
    s = re.sub(r"[^a-z0-9\-]", "", s)
    return s


def korean_move(move_name: str) -> str:
    """Translate a move name to Korean, matching pokemon.js logic."""
    if not move_name:
        return "—"
    # Already Korean?
    if any("\uac00" <= c <= "\ud7af" for c in move_name):
        return move_name
    if move_name in MOVES_KOREAN:
        return MOVES_KOREAN[move_name]
    base = move_name.replace("_FAST", "")
    if base in MOVES_KOREAN:
        return MOVES_KOREAN[base]
    return move_name


def type_color(t: str) -> str:
    return TYPE_COLORS.get(t, "#888888")


def type_emoji(t: str) -> str:
    return TYPE_EMOJI.get(t, "❓")


def type_badge(t: str) -> str:
    color = type_color(t)
    emoji = type_emoji(t)
    return (
        f'<span class="type-badge" style="background-color:{color}22;color:{color};" '
        f'title="{t} 타입">'
        f"{emoji} {t}</span>"
    )


def stat_bar(label: str, value: int, max_val: int, color: str) -> str:
    pct = min(value / max_val * 100, 100)
    return (
        f'<div class="stat-row">'
        f"<span class='stat-label'>{label}</span>"
        f"<div class='stat-bar'><div class='stat-fill' style='width:{pct:.1f}%;background-color:{color};'></div></div>"
        f"<span class='stat-value'>{value}</span>"
        f"</div>"
    )


def move_list(moves, title: str, icon: str) -> str:
    if not moves:
        return ""
    items = "".join(
        f"<li>{icon} {korean_move(m)}</li>" for m in moves
    )
    return (
        f'<div class="moves-section">'
        f"<h3>{title}</h3>"
        f"<ul class='moves-list'>{items}</ul>"
        f"</div>"
    )


def image_url(pokemon: dict) -> str:
    dex = pokemon.get("dexNr")
    if dex and dex > 0:
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/{dex}.png"
    return pokemon.get("image") or ""


def build_page(pokemon: dict, prev_file: str | None, next_file: str | None, dex_by_id: dict, name_by_id: dict) -> str:
    name_ko = pokemon["name"]
    name_en = pokemon.get("nameEn", "")
    name_ja = pokemon.get("nameJa", "")
    dex = pokemon.get("dexNr", "")
    types = pokemon.get("types") or []
    stats = pokemon.get("stats") or {}
    quick = pokemon.get("quickMoves") or []
    cinematic = pokemon.get("cinematicMoves") or []
    elite_quick = pokemon.get("eliteQuickMoves") or []
    elite_cinematic = pokemon.get("eliteCinematicMoves") or []
    generation = pokemon.get("generation")
    region = pokemon.get("region")
    youtube_url = pokemon.get("youtubeUrl") or ""
    has_mega = pokemon.get("hasMega")
    has_gigamax = pokemon.get("hasGigantamax")
    pokemonClass = pokemon.get("pokemonClass") or ""

    max_stat = max(stats.get("stamina", 1), stats.get("attack", 1), stats.get("defense", 1))

    class_badge_html = (
        f'<span class="poke-card__class poke-card__class--{CLASS_CSS[pokemonClass]}">{pokemonClass}</span>'
        if pokemonClass and pokemonClass in CLASS_CSS else ""
    )

    type_badges = "".join(type_badge(t) for t in types)

    moves_html = (
        move_list(quick, "퀵 스킬 (Fast Move)", "⚡")
        + move_list(cinematic, "시네매틱 스킬 (Charge Move)", "💥")
        + move_list(elite_quick, "엘리트 퀵 스킬", "⭐")
        + move_list(elite_cinematic, "엘리트 시네매틱 스킬", "🏆")
    )

    # Evolution
    evos = pokemon.get("evolutions") or []
    evo_items = ""
    for e in evos:
        candies = e.get("candies")
        evo_name = korean_move(e["id"])
        evo_dex = dex_by_id.get(e["id"])
        evo_name_en = name_by_id.get(e["id"], e["id"])
        evo_href = (
            f"pokemon-{evo_dex}-{slugify(evo_name_en)}.html"
            if evo_dex
            else f"pokemon-{slugify(evo_name_en)}.html"
        )
        evo_items += (
            f"<li><a href='{evo_href}' class='evo-link'>{evo_name}</a>"
            f"{f' — {candies}개 캔디' if candies else ''}</li>"
        )
    evo_html = (
        f'<div class="evo-section">'
        f"<h3>진화</h3>"
        f"<ul class='evo-list'>{evo_items}</ul>"
        f"</div>" if evo_items else ""
    )

    prev_link = f"<a href='{prev_file}' class='nav-link'>&larr; 이전</a>" if prev_file else ""
    next_link = f"<a href='{next_file}' class='nav-link'>다음 &rarr;</a>" if next_file else ""

    stats_html = (
        stat_bar("체력", stats.get("stamina", 0), max_stat, "#E85858")
        + stat_bar("공격력", stats.get("attack", 0), max_stat, "#F8D030")
        + stat_bar("방어력", stats.get("defense", 0), max_stat, "#6890F0")
    )

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
  <meta http-equiv="Pragma" content="no-cache" />
  <meta http-equiv="Expires" content="0" />
  <title>{name_ko} ({name_en}) — 포켓몬 사전 | 포케써니</title>
  <meta name="description" content="포켓몬GO {name_ko} 정보. 타입: {', '.join(types)},generation {GEN_KOREAN.get(generation, '')}, region {REGION_KOREAN.get(region, '')}. 체력 {stats.get('stamina')}, 공격력 {stats.get('attack')}, 방어력 {stats.get('defense')}." />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://pokesunny.com/pokedex/pokemon-{dex}-{name_ko}.html" />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="포케써니" />
  <meta property="og:title" content="포케써니 | {name_ko} ({name_en})" />
  <meta property="og:description" content="포켓몬GO {name_ko} — 타입: {', '.join(types)} |generation {GEN_KOREAN.get(generation, '')} | {REGION_KOREAN.get(region, '')}" />
  <meta property="og:url" content="https://pokesunny.com/pokedex/pokemon-{dex}-{name_ko}.html" />
  <meta property="og:image" content="{image_url(pokemon)}" />
  <meta property="og:locale" content="ko_KR" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=Poppins:wght@500;600;700;800&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --bg: #0b0b0f;
      --card: #14141c;
      --card-border: #2a2a3a;
      --text: #e8e8f0;
      --text-dim: #9898a8;
      --accent: #f8d030;
      --font-main: "Noto Sans KR", Poppins, sans-serif;
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: var(--font-main);
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}

    /* Header */
    .header {{
      background: rgba(20, 20, 28, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--card-border);
      padding: 0.75rem 1.5rem;
      position: sticky;
      top: 0;
      z-index: 100;
    }}
    .header__inner {{
      max-width: 1100px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .brand {{
      font-family: Poppins, var(--font-main);
      font-weight: 800;
      font-size: 1.35rem;
      color: var(--text);
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .brand__ball {{
      width: 28px; height: 28px;
      background: radial-gradient(circle at 35% 35%, #ff6b6b, #c0392b);
      border-radius: 50%;
      display: inline-block;
      box-shadow: 0 0 8px rgba(255, 107, 107, 0.5);
    }}
    .nav {{ display: flex; gap: 1.25rem; font-size: 0.9rem; }}
    .nav a {{ color: var(--text-dim); }}
    .nav a:hover {{ color: var(--text); text-decoration: none; }}
    .btn-sm {{
      padding: 0.4rem 0.9rem;
      border: 1px solid var(--card-border);
      border-radius: 8px;
      font-size: 0.85rem;
      color: var(--text-dim);
      background: transparent;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}
    .btn-sm:hover {{ border-color: var(--accent); color: var(--accent); }}

    /* Main */
    main {{ flex: 1; max-width: 900px; margin: 0 auto; width: 100%; padding: 2rem 1.5rem; }}

    /* Hero / monster card */
    .monster-card {{
      background: var(--card);
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 2rem;
      text-align: center;
      position: relative;
      overflow: hidden;
    }}
    .monster-card::before {{
      content: "";
      position: absolute;
      top: -60%;
      left: 50%;
      transform: translateX(-50%);
      width: 300px;
      height: 300px;
      background: radial-gradient(circle, rgba(248, 208, 48, 0.08) 0%, transparent 70%);
      pointer-events: none;
    }}
    .monster-img {{
      width: 200px;
      height: 200px;
      object-fit: contain;
      image-rendering: auto;
      filter: drop-shadow(0 8px 24px rgba(0,0,0,0.5));
      margin-bottom: 1rem;
    }}
    .monster-name-ko {{
      font-family: Poppins, var(--font-main);
      font-size: 2.2rem;
      font-weight: 800;
      margin-bottom: 0.25rem;
    }}
    .monster-names {{
      color: var(--text-dim);
      font-size: 0.95rem;
      margin-bottom: 1rem;
    }}
    .monster-names span {{ margin: 0 0.5rem; }}
    .monster-types {{
      display: flex;
      justify-content: center;
      gap: 0.6rem;
      flex-wrap: wrap;
      margin-bottom: 1.5rem;
    }}
    .type-badge {{
      padding: 0.35rem 1rem;
      border-radius: 20px;
      font-size: 0.9rem;
      font-weight: 600;
      letter-spacing: 0.02em;
    }}
    .monster-meta {{
      display: flex;
      justify-content: center;
      gap: 1.5rem;
      flex-wrap: wrap;
      font-size: 0.85rem;
      color: var(--text-dim);
      margin-bottom: 1.5rem;
    }}
    .monster-meta span {{ display: flex; align-items: center; gap: 0.35rem; }}

    /* Pokemon class badge (legendary / mythical / ultra beast) */
    .poke-card__class {{
      font-size: 0.75rem;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 6px;
      letter-spacing: 0.04em;
    }}
    .poke-card__class--legendary {{
      background: linear-gradient(135deg, #f8d030, #f59e0b);
      color: #0b0b0f;
    }}
    .poke-card__class--mythical {{
      background: linear-gradient(135deg, #ee99ac, #a838f8);
      color: #0b0b0f;
    }}
    .poke-card__class--ultra-beast {{
      background: linear-gradient(135deg, #ef4444, #ee99ac);
      color: #0b0b0f;
    }}

    /* Sections */
    .section-title {{
      font-size: 1.15rem;
      font-weight: 700;
      margin: 2rem 0 1rem;
      padding-bottom: 0.5rem;
      border-bottom: 2px solid var(--card-border);
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    /* Stats */
    .stat-row {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 0.6rem;
    }}
    .stat-label {{ width: 70px; font-size: 0.9rem; color: var(--text-dim); text-align: right; }}
    .stat-bar {{
      flex: 1;
      height: 10px;
      background: #1e1e2e;
      border-radius: 5px;
      overflow: hidden;
    }}
    .stat-fill {{
      height: 100%;
      border-radius: 5px;
      transition: width 0.3s;
    }}
    .stat-value {{ width: 45px; font-size: 0.9rem; font-weight: 700; text-align: left; }}

    /* Moves */
    .moves-section {{ margin-bottom: 1.5rem; }}
    .moves-section h3 {{
      font-size: 1rem;
      margin-bottom: 0.6rem;
      color: var(--text);
    }}
    .moves-list {{
      list-style: none;
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
    }}
    .moves-list li {{
      background: #1e1e2e;
      padding: 0.4rem 0.9rem;
      border-radius: 10px;
      font-size: 0.88rem;
      border: 1px solid var(--card-border);
    }}

    /* Evolution */
    .evo-section {{ margin-bottom: 1.5rem; }}
    .evo-section h3 {{ font-size: 1rem; margin-bottom: 0.6rem; }}
    .evo-list {{ list-style: none; }}
    .evo-list li {{
      padding: 0.5rem 0;
      border-bottom: 1px solid var(--card-border);
      font-size: 0.95rem;
    }}
    .evo-list li:last-child {{ border-bottom: none; }}
    .evo-link {{ font-weight: 600; color: var(--accent); }}

    /* Nav */
    .page-nav {{
      display: flex;
      justify-content: space-between;
      margin-top: 2.5rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--card-border);
    }}
    .nav-link {{
      padding: 0.6rem 1.2rem;
      border: 1px solid var(--card-border);
      border-radius: 10px;
      font-size: 0.9rem;
      color: var(--text-dim);
      transition: all 0.2s;
    }}
    .nav-link:hover {{
      border-color: var(--accent);
      color: var(--accent);
      text-decoration: none;
    }}

    /* Footer */
    footer {{
      text-align: center;
      padding: 1.5rem;
      font-size: 0.82rem;
      color: var(--text-dim);
      border-top: 1px solid var(--card-border);
      margin-top: 2rem;
    }}
    footer a {{ color: var(--text-dim); }}

    @media (max-width: 600px) {{
      .monster-name-ko {{ font-size: 1.7rem; }}
      .monster-img {{ width: 160px; height: 160px; }}
      main {{ padding: 1rem; }}
    }}
  </style>
</head>
<body>
  <header class="header">
    <div class="header__inner">
      <a class="brand" href="https://pokesunny.com/index.html">
        <span class="brand__ball"></span>
        <span>포케써니</span>
      </a>
      <nav class="nav">
        <a href="https://pokesunny.com/index.html">홈</a>
        <a href="https://pokesunny.com/pokemon.html">포켓몬 사전</a>
        <a href="https://pokesunny.com/index.html#news">뉴스</a>
        <a href="https://pokesunny.com/index.html#about">소개</a>
      </nav>
      <a class="btn-sm" href="https://www.youtube.com/@Poke_Sunny" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8ZM9.5 15.5v-7l6.5 3.5-6.5 3.5Z"/></svg>
        유튜브
      </a>
    </div>
  </header>

  <main>
    <div class="monster-card">
      <img class="monster-img" src="{image_url(pokemon)}" alt="{name_ko}" loading="lazy" />
      <div class="monster-name-ko">{name_ko}</div>
      <div class="monster-names">
        <span>{name_en}</span>
        <span>·</span>
        <span>{name_ja}</span>
      </div>
      <div class="monster-types">{type_badges}</div>
      <div class="monster-meta">
        <span>🎮 {GEN_KOREAN.get(generation, '')}</span>
        <span>🗺️ {REGION_KOREAN.get(region, '')}</span>
        {f"<span>🧬 메가진화 가능</span>" if has_mega else ""}
        {f"<span>✨ 지진대결 가능</span>" if has_gigamax else ""}
        {class_badge_html}
      </div>

      <div class="section-title">📊 스펙</div>
      <div class="stats-grid">{stats_html}</div>
    </div>

    <div class="section-title">⚔️ 스킬</div>
    {moves_html}

    {evo_html}

    {youtube_url and f'''
    <div class="section-title">📺 관련 영상</div>
    <div style="margin-bottom:2rem;">
      <a href="{youtube_url}" target="_blank" rel="noopener" class="nav-link" style="display:inline-flex;">
        유튜브에서 "{name_ko}" 검색하기 &rarr;
      </a>
    </div>''' or ""}

    <div class="page-nav">
      {prev_link}
      {next_link}
    </div>
  </main>

  <footer>
    <p>© 2026 포케써니 · Pokémon GO 데이터 제공: <a href="https://pokemon-go-api.github.io" target="_blank" rel="noopener">Pokémon GO API</a></p>
  </footer>
</body>
</html>"""


def main() -> None:
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)

    pokemon_list: list[dict] = data["all"]
    print(f"Loaded {len(pokemon_list)} pokemon (json total: {data['total']})")

    os.makedirs(OUT_DIR, exist_ok=True)

    generated = 0
    # Pre-compute filenames + dex mapping so prev/next/evo links are correct
    filenames = {}
    dex_by_id = {}
    name_by_id = {}
    for p in pokemon_list:
        name_en = p.get("nameEn", "unknown")
        filenames[p["id"]] = f"pokemon-{p['dexNr']}-{slugify(name_en)}.html"
        dex_by_id[p["id"]] = p["dexNr"]
        name_by_id[p["id"]] = name_en

    for i, p in enumerate(pokemon_list):
        prev_file = filenames[pokemon_list[i - 1]["id"]] if i > 0 else None
        next_file = filenames[pokemon_list[i + 1]["id"]] if i + 1 < len(pokemon_list) else None

        name_ko = p["name"]
        name_en = p.get("nameEn", "unknown")
        filename = filenames[p["id"]]
        path = os.path.join(OUT_DIR, filename)

        html = build_page(p, prev_file, next_file, dex_by_id, name_by_id)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        generated += 1

        if generated % 100 == 0:
            print(f"  generated {generated}...")

    print(f"\n✅ Generated {generated} pages in {OUT_DIR}/")
    print("   Sample: pokemon-1-bulbasaur.html ... pokemon-1024-melmetal.html")


if __name__ == "__main__":
    main()

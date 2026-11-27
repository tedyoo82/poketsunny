/* ============ 포케써니 | 포켓몬 사전 ============ */

(function () {
  "use strict";

  // ===== 타입 정의 =====
  const TYPE_KOREAN = {
    "POKEMON_TYPE_FIGHTING": "격투",
    "POKEMON_TYPE_FLYING": "비행",
    "POKEMON_TYPE_POISON": "독",
    "POKEMON_TYPE_GROUND": "땅",
    "POKEMON_TYPE_ROCK": "바위",
    "POKEMON_TYPE_BUG": "벌레",
    "POKEMON_TYPE_GHOST": "고스트",
    "POKEMON_TYPE_ICE": "얼음",
    "POKEMON_TYPE_DRAGON": "드래곤",
    "POKEMON_TYPE_STEEL": "강철",
    "POKEMON_TYPE_FIRE": "불꽃",
    "POKEMON_TYPE_WATER": "물",
    "POKEMON_TYPE_GRASS": "풀",
    "POKEMON_TYPE_ELECTRIC": "전기",
    "POKEMON_TYPE_psychic": "에스퍼",
    "POKEMON_TYPE_PSYCHIC": "에스퍼",
    "POKEMON_TYPE_NORMAL": "노말",
    "POKEMON_TYPE_FAIRY": "페어리",
  };

  const TYPE_COLORS = {
    "격투": "#FF8000", "비행": "#A890FF", "독": "#A838F8",
    "땅": "#E8CB68", "바위": "#B8A038", "벌레": "#A8B820",
    "고스트": "#705898", "얼음": "#98D8D8", "드래곤": "#7038F8",
    "강철": "#B8B8D0", "불꽃": "#F08030", "물": "#6890F0",
    "풀": "#78C850", "전기": "#F8D030", "에스퍼": "#F85888",
    "노말": "#A8A878", "페어리": "#EE99AC",
  };

  const TYPE_EMOJI = {
    "격투": "🥊", "비행": "🕊️", "독": "☠️", "땅": "🏔️",
    "바위": "🪨", "벌레": "🐛", "고스트": "👻", "얼음": "❄️",
    "드래곤": "🐉", "강철": "⚙️", "불꽃": "🔥", "물": "💧",
    "풀": "🌿", "전기": "⚡", "에스퍼": "🔮", "노말": "⚪", "페어리": "🧚",
  };

  // 타입 키 → 한글 이름 변환
  function typeKeyToKorean(key) {
    return TYPE_KOREAN[key] || key.replace("POKEMON_TYPE_", "");
  }

  // ===== 포켓몬 스프라이트 URL (PokeAPI Home Art) =====
  function getPokemonImage(p) {
    if (p.dexNr && p.dexNr > 0) {
      return `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/${p.dexNr}.png`;
    }
    return p.image || "";
  }

  // ===== 스킬 한글 매핑 =====
  const MOVES_KOREAN = {
    // --- 퀵 스킬 (Fast Moves) ---
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
    // --- 시네매틱/전기 스킬 (Charge Moves) ---
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
  };

  // 스킬 이름 한글 변환
  function moveToKorean(moveName) {
    if (!moveName) return "—";
    // 이미 한글이면 그대로 반환
    if (/[\uac00-\ud7af]/.test(moveName)) return moveName;
    // 매핑에서 찾기
    if (MOVES_KOREAN[moveName]) return MOVES_KOREAN[moveName];
    // FAST 접미사 제거하고 매핑
    const base = moveName.replace(/_FAST$/, "");
    if (MOVES_KOREAN[base]) return MOVES_KOREAN[base];
    //没有找到则返回原名
    return moveName;
  }

  const REGION_ORDER = [
    { gen: 1, name: "관동", count: 151 },
    { gen: 2, name: "도쿠소", count: 100 },
    { gen: 3, name: "호연", count: 135 },
    { gen: 4, name: "신오", count: 107 },
    { gen: 5, name: "율려", count: 156 },
    { gen: 6, name: "알로라", count: 72 },
    { gen: 7, name: "가리아", count: 88 },
    { gen: 8, name: "지후", count: 89 },
    { gen: 9, name: "파르다", count: 126 },
  ];

  // ===== 상태 =====
  let allPokemon = [];
  let filteredPokemon = [];
  let currentRegion = 0; // 0 = 전체
  let currentType = "";
  let searchQuery = "";
  let displayCount = 0;
  const BATCH_SIZE = 60;
  let isLoading = false;
  let hasMore = true;

  // ===== DOM =====
  const $search = document.getElementById("poke-search");
  const $types = document.getElementById("poke-types");
  const $tabs = document.getElementById("poke-tabs");
  const $grid = document.getElementById("poke-grid");
  const $loadMore = document.getElementById("poke-load-more");
  const $loading = document.getElementById("poke-loading-indicator");
  const $empty = document.getElementById("poke-empty");
  const $total = document.getElementById("poke-total");
  const $visible = document.getElementById("poke-visible");
  const $modal = document.getElementById("poke-modal");
  const $modalBody = document.getElementById("poke-modal-body");
  const $modalClose = document.getElementById("poke-modal-close");
  const $modalBackdrop = document.getElementById("poke-modal-backdrop");

  // ===== 유틸 =====
  function getKoreanType(typeObj) {
    if (!typeObj) return null;
    const key = typeObj.type || "";
    return TYPE_KOREAN[key] || key.replace("POKEMON_TYPE_", "");
  }

  function getTypeColor(typeName) {
    return TYPE_COLORS[typeName] || "#888";
  }

  function getTypeEmoji(typeName) {
    return TYPE_EMOJI[typeName] || "❓";
  }

  function statPercent(stat, max) {
    return Math.min(100, (stat / max) * 100);
  }

  function getStatColor(stat) {
    if (stat >= 150) return "#4ade80";
    if (stat >= 120) return "#22d3ee";
    if (stat >= 90) return "#facc15";
    if (stat >= 60) return "#fb923c";
    return "#f87171";
  }

  function formatStat(stat) {
    return stat?.toString() || "—";
  }

  function _classSuffix(pokemonClass) {
    // styles.css에 정의된 클래스명(--legendary/--mythical/--ultra-beast)과 매칭
    const map = { "전설": "legendary", "신비": "mythical", "울트라비스트": "ultra-beast" };
    return map[pokemonClass] || pokemonClass.toLowerCase();
  }

  function slugify(name) {
    // generate_pokemon_pages.py의 slugify와 동일: 소문자 + 비알파숫자(하이픈 제외) 제거
    return name.toLowerCase().replace(/[^a-z0-9-]+/g, "");
  }

  // ===== 데이터 로드 =====
  async function loadPokemonData() {
    try {
      const res = await fetch("pokemon.json?_t=" + Date.now());
      if (!res.ok) throw new Error("Failed to load: " + res.status);
      const data = await res.json();
      console.log("pokemon.json loaded, keys:", Object.keys(data));
      console.log("data.all type:", typeof data.all, "length:", data.all?.length);

      // JSON의 types는 이미 한글(예: "풀", "독")로 저장됨
      // POKEMON_TYPE_* 형식에서 한글로 변환
      allPokemon = (data.all || []).map((p) => {
        if (p.types) {
          p.types = p.types.map((t) => {
            if (t.startsWith("POKEMON_TYPE_")) {
              return TYPE_KOREAN[t] || t.replace("POKEMON_TYPE_", "");
            }
            return t; // 이미 한글이면 그대로
          });
        }
        return p;
      });

      console.log("allPokemon count:", allPokemon.length);
      if (allPokemon.length > 0) {
        console.log("sample:", allPokemon[0].name, "types:", allPokemon[0].types);
      }

      if (allPokemon.length === 0) {
        $grid.innerHTML = '<div class="poke-grid__loading">데이터가 비어 있습니다.</div>';
        return;
      }

      initPage();
    } catch (err) {
      console.error("pokemon.json load error:", err);
      $grid.innerHTML = '<div class="poke-grid__loading">데이터를 불러오지 못했습니다.<br /> 잠시 후 다시 시도해 주세요.</div>';
    }
  }

  // ===== 초기화 =====
  function initPage() {
    renderTabs();
    renderTypeFilters();
    applyFilters();
    setupEvents();
  }

  // ===== 지역 탭 =====
  function renderTabs() {
    let html = `<button class="poke-tab poke-tab--active" data-region="0">전체</button>`;
    REGION_ORDER.forEach((r) => {
      html += `<button class="poke-tab" data-region="${r.gen}">${r.name} (${r.count})</button>`;
    });
    $tabs.innerHTML = html;
  }

  // ===== 타입 필터 =====
  function renderTypeFilters() {
    const allTypes = new Set();
    allPokemon.forEach((p) => {
      (p.types || []).forEach((t) => allTypes.add(t));
    });

    let html = `<button class="poke-type-btn poke-type-btn--active" data-type="">전체</button>`;
    const sorted = Array.from(allTypes).sort();
    sorted.forEach((type) => {
      const koreanName = typeKeyToKorean(type);
      const color = getTypeColor(koreanName);
      const emoji = getTypeEmoji(koreanName);
      html += `<button class="poke-type-btn" data-type="${type}" style="--type-color:${color}">${emoji} ${koreanName}</button>`;
    });
    $types.innerHTML = html;
  }

  // ===== 필터 적용 =====
  function applyFilters() {
    filteredPokemon = allPokemon.filter((p) => {
      // 지역 필터
      if (currentRegion !== 0 && p.generation !== currentRegion) return false;
      // 타입 필터
      if (currentType && !(p.types || []).includes(currentType)) return false;
      // 검색 필터
      if (searchQuery) {
        const q = searchQuery.toLowerCase();
        const name = (p.name || "").toLowerCase();
        const nameEn = (p.nameEn || "").toLowerCase();
        const nameJa = (p.nameJa || "").toLowerCase();
        if (!name.includes(q) && !nameEn.includes(q) && !nameJa.includes(q)) return false;
      }
      return true;
    });

    // dex 번호순 정렬
    filteredPokemon.sort((a, b) => a.dexNr - b.dexNr);

    displayCount = 0;
    hasMore = true;
    $grid.innerHTML = "";
    $empty.style.display = "none";
    $loadMore.style.display = "none";

    $total.textContent = filteredPokemon.length;
    loadMore();
  }

  // ===== 배치 로드 =====
  function loadMore() {
    if (isLoading || !hasMore) return;
    isLoading = true;
    $loading.style.display = "flex";

    // 약간의 지연으로 UX 개선
    setTimeout(() => {
      const start = displayCount;
      const end = Math.min(start + BATCH_SIZE, filteredPokemon.length);
      const batch = filteredPokemon.slice(start, end);

      batch.forEach((p, i) => {
        const card = createPokemonCard(p, start + i);
        card.style.animationDelay = (i % 10) * 0.03 + "s";
        $grid.appendChild(card);
      });

      displayCount = end;
      $visible.textContent = displayCount;

      if (displayCount >= filteredPokemon.length) {
        hasMore = false;
        $loadMore.style.display = "none";
      } else {
        $loadMore.style.display = "flex";
      }

      $loading.style.display = "none";
      isLoading = false;

      if (filteredPokemon.length === 0) {
        $empty.style.display = "flex";
      }
    }, 100);
  }

  // ===== 카드 생성 =====
  function createPokemonCard(p, index) {
    const card = document.createElement("a");
    card.className = "poke-card";
    card.href = `pokedex/pokemon-${p.dexNr}-${slugify(p.nameEn)}.html`;
    card.dataset.index = index;

    const typesHtml = (p.types || []).map((t) => {
      const koreanName = typeKeyToKorean(t);
      const color = getTypeColor(koreanName);
      return `<span class="poke-card__type" style="background:${color}">${koreanName}</span>`;
    }).join("");

    const classBadge = p.pokemonClass
      ? `<span class="poke-card__class poke-card__class--${_classSuffix(p.pokemonClass)}">${p.pokemonClass}</span>`
      : "";

    const megaBadge = p.hasMega ? `<span class="poke-card__badge poke-card__badge--mega">MEGA</span>` : "";
    const gmaxBadge = p.hasGigantamax ? `<span class="poke-card__badge poke-card__badge--gmax">GMAX</span>` : "";

    card.innerHTML = `
      <div class="poke-card__img-wrap">
        <img class="poke-card__img" src="${getPokemonImage(p)}" alt="${p.name}" loading="lazy" />
        <span class="poke-card__dex">#${String(p.dexNr).padStart(3, "0")}</span>
        <div class="poke-card__badges">${classBadge}${megaBadge}${gmaxBadge}</div>
      </div>
      <div class="poke-card__info">
        <h3 class="poke-card__name">${p.name}</h3>
        <div class="poke-card__types">${typesHtml}</div>
        <div class="poke-card__stats-mini">
          <span class="poke-card__stat-mini">
            <span class="poke-card__stat-mini__label">공격</span>
            <span class="poke-card__stat-mini__value">${formatStat(p.stats?.attack)}</span>
          </span>
          <span class="poke-card__stat-mini">
            <span class="poke-card__stat-mini__label">방어</span>
            <span class="poke-card__stat-mini__value">${formatStat(p.stats?.defense)}</span>
          </span>
          <span class="poke-card__stat-mini">
            <span class="poke-card__stat-mini__label">체력</span>
            <span class="poke-card__stat-mini__value">${formatStat(p.stats?.stamina)}</span>
          </span>
        </div>
      </div>
    `;

    return card;
  }

  // ===== 모달 =====
  function openModal(p) {
    const typesHtml = (p.types || []).map((t) => {
      const koreanName = typeKeyToKorean(t);
      const color = getTypeColor(koreanName);
      return `<span class="poke-modal__type" style="background:${color}">${getTypeEmoji(koreanName)} ${koreanName}</span>`;
    }).join("");

    const classBadge = p.pokemonClass
      ? `<span class="poke-modal__class poke-modal__class--${_classSuffix(p.pokemonClass)}">${p.pokemonClass}</span>`
      : "";

    const badges = [];
    if (p.hasMega) badges.push('<span class="poke-modal__badge poke-modal__badge--mega">MEGA</span>');
    if (p.hasGigantamax) badges.push('<span class="poke-modal__badge poke-modal__badge--gmax">GIGANTAMAX</span>');
    const badgesHtml = badges.join("");

    // 스텟 바
    const maxStat = 255;
    const statsHtml = [
      { label: "체력", key: "stamina", val: p.stats?.stamina || 0 },
      { label: "공격", key: "attack", val: p.stats?.attack || 0 },
      { label: "방어", key: "defense", val: p.stats?.defense || 0 },
    ].map((s) => {
      const pct = statPercent(s.val, maxStat);
      const color = getStatColor(s.val);
      return `
        <div class="poke-modal__stat">
          <div class="poke-modal__stat__head">
            <span class="poke-modal__stat__label">${s.label}</span>
            <span class="poke-modal__stat__value">${s.val}</span>
          </div>
          <div class="poke-modal__stat__bar">
            <div class="poke-modal__stat__fill" style="width:${pct}%;background:${color}"></div>
          </div>
        </div>
      `;
    }).join("");

    // 스킬
    const movesHtml = [];
    if (p.quickMoves?.length) {
      movesHtml.push(`<div class="poke-modal__moves-section"><h4 class="poke-modal__moves-title">퀵 스킬</h4><div class="poke-modal__moves-list">${p.quickMoves.map(m => `<span class="poke-modal__move">${moveToKorean(m)}</span>`).join("")}</div></div>`);
    }
    if (p.cinematicMoves?.length) {
      movesHtml.push(`<div class="poke-modal__moves-section"><h4 class="poke-modal__moves-title">시네매틱 스킬</h4><div class="poke-modal__moves-list">${p.cinematicMoves.map(m => `<span class="poke-modal__move poke-modal__move--special">${moveToKorean(m)}</span>`).join("")}</div></div>`);
    }
    if (p.eliteQuickMoves?.length) {
      movesHtml.push(`<div class="poke-modal__moves-section"><h4 class="poke-modal__moves-title">에픽 퀵 스킬</h4><div class="poke-modal__moves-list">${p.eliteQuickMoves.map(m => `<span class="poke-modal__move poke-modal__move--elite">${moveToKorean(m)}</span>`).join("")}</div></div>`);
    }
    if (p.eliteCinematicMoves?.length) {
      movesHtml.push(`<div class="poke-modal__moves-section"><h4 class="poke-modal__moves-title">에픽 시네매틱 스킬</h4><div class="poke-modal__moves-list">${p.eliteCinematicMoves.map(m => `<span class="poke-modal__move poke-modal__move--elite">${moveToKorean(m)}</span>`).join("")}</div></div>`);
    }
    const movesHtmlStr = movesHtml.join("");

    // 진화
    let evolutionHtml = "";
    if (p.evolutions?.length) {
      evolutionHtml = `
        <div class="poke-modal__evos-section">
          <h4 class="poke-modal__evo-title">진화 정보</h4>
          <div class="poke-modal__evo-list">
            ${p.evolutions.map(e => `<div class="poke-modal__evo"><span class="poke-modal__evo-candies">🍬 ${e.candies}</span></div>`).join("")}
          </div>
        </div>
      `;
    }

    // 이전/다음 포켓몬
    const currentIndex = filteredPokemon.findIndex((x) => x.dexNr === p.dexNr);
    const prevP = currentIndex > 0 ? filteredPokemon[currentIndex - 1] : null;
    const nextP = currentIndex < filteredPokemon.length - 1 ? filteredPokemon[currentIndex + 1] : null;
    const navHtml = `
      <div class="poke-modal__nav">
        ${prevP ? `<button class="poke-modal__nav-btn poke-modal__nav-btn--prev" data-dex="${prevP.dexNr}">← ${prevP.name}</button>` : '<span></span>'}
        ${nextP ? `<button class="poke-modal__nav-btn poke-modal__nav-btn--next" data-dex="${nextP.dexNr}">${nextP.name} →</button>` : '<span></span>'}
      </div>
    `;

    $modalBody.innerHTML = `
      <div class="poke-modal__header">
        <div class="poke-modal__img-wrap">
          <img class="poke-modal__img" src="${getPokemonImage(p)}" alt="${p.name}" />
          <span class="poke-modal__dex">#${String(p.dexNr).padStart(3, "0")}</span>
        </div>
        <div class="poke-modal__title-area">
          <h2 class="poke-modal__name">${p.name}</h2>
          <div class="poke-modal__name-en">${p.nameEn || ""}</div>
          <div class="poke-modal__types">${typesHtml}</div>
          <div class="poke-modal__meta">${badgesHtml}${classBadge}</div>
          <a class="poke-modal__yt" href="${p.youtubeUrl}" target="_blank" rel="noopener">
            <svg viewBox="0 0 24 24" class="ic" aria-hidden="true"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8ZM9.5 15.5v-7l6.5 3.5-6.5 3.5Z"/></svg>
            유튜브 영상 보기
          </a>
        </div>
      </div>
      ${statsHtml}
      ${movesHtmlStr}
      ${evolutionHtml}
      ${navHtml}
    `;

    $modal.style.display = "flex";
    document.body.style.overflow = "hidden";

    // 네비게이션 클릭 이벤트
    $modal.querySelectorAll(".poke-modal__nav-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const dex = parseInt(btn.dataset.dex);
        const target = filteredPokemon.find((x) => x.dexNr === dex);
        if (target) openModal(target);
      });
    });
  }

  function closeModal() {
    $modal.style.display = "none";
    document.body.style.overflow = "";
  }

  // ===== 이벤트 설정 =====
  function setupEvents() {
    // 검색
    let searchTimer;
    $search.addEventListener("input", () => {
      clearTimeout(searchTimer);
      searchTimer = setTimeout(() => {
        searchQuery = $search.value.trim();
        applyFilters();
      }, 300);
    });

    // 탭 클릭
    $tabs.addEventListener("click", (e) => {
      const tab = e.target.closest(".poke-tab");
      if (!tab) return;
      $tabs.querySelectorAll(".poke-tab").forEach((t) => t.classList.remove("poke-tab--active"));
      tab.classList.add("poke-tab--active");
      currentRegion = parseInt(tab.dataset.region);
      applyFilters();
    });

    // 타입 클릭
    $types.addEventListener("click", (e) => {
      const btn = e.target.closest(".poke-type-btn");
      if (!btn) return;
      $types.querySelectorAll(".poke-type-btn").forEach((b) => b.classList.remove("poke-type-btn--active"));
      btn.classList.add("poke-type-btn--active");
      currentType = btn.dataset.type;
      applyFilters();
    });

    // 더 보기
    $loadMore.addEventListener("click", loadMore);

    // 모달 닫기
    $modalClose.addEventListener("click", closeModal);
    $modalBackdrop.addEventListener("click", closeModal);
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeModal();
    });

    // 스크롤 무한 로딩
    window.addEventListener("scroll", () => {
      if (isLoading || !hasMore) return;
      const scrollBottom = window.innerHeight + window.scrollY;
      const docHeight = document.documentElement.scrollHeight;
      if (scrollBottom >= docHeight - 600) {
        loadMore();
      }
    });
  }

  // ===== 시작 =====
  loadPokemonData();
})();

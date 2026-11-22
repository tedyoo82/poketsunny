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

  // ===== 데이터 로드 =====
  async function loadPokemonData() {
    try {
      const res = await fetch("pokemon.json?_t=" + Date.now());
      if (!res.ok) throw new Error("Failed to load: " + res.status);
      const data = await res.json();
      allPokemon = data.all || [];
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
      const color = getTypeColor(type);
      const emoji = getTypeEmoji(type);
      html += `<button class="poke-type-btn" data-type="${type}" style="--type-color:${color}">${emoji} ${type}</button>`;
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
    const card = document.createElement("div");
    card.className = "poke-card";
    card.dataset.index = index;

    const typesHtml = (p.types || []).map((t) => {
      const color = getTypeColor(t);
      return `<span class="poke-card__type" style="background:${color}">${t}</span>`;
    }).join("");

    const classBadge = p.pokemonClass
      ? `<span class="poke-card__class poke-card__class--${p.pokemonClass.toLowerCase()}">${p.pokemonClass}</span>`
      : "";

    const megaBadge = p.hasMega ? `<span class="poke-card__badge poke-card__badge--mega">MEGA</span>` : "";
    const gmaxBadge = p.hasGigantamax ? `<span class="poke-card__badge poke-card__badge--gmax">GMAX</span>` : "";

    card.innerHTML = `
      <div class="poke-card__img-wrap">
        <img class="poke-card__img" src="${p.image}" alt="${p.name}" loading="lazy" />
        <span class="poke-card__dex">#${String(p.dexNr).padStart(3, "0")}</span>
        <div class="poke-card__badges">${classBadge}${megaBadge}${gmaxBadge}</div>
      </div>
      <div class="poke-card__info">
        <h3 class="poke-card__name">${p.name}</h3>
        <div class="poke-card__types">${typesHtml}</div>
        <div class="poke-card__stats-mini">
          <span class="poke-card__stat-mini">
            <span class="poke-card__stat-mini__label">ATK</span>
            <span class="poke-card__stat-mini__value">${formatStat(p.stats?.attack)}</span>
          </span>
          <span class="poke-card__stat-mini">
            <span class="poke-card__stat-mini__label">DEF</span>
            <span class="poke-card__stat-mini__value">${formatStat(p.stats?.defense)}</span>
          </span>
          <span class="poke-card__stat-mini">
            <span class="poke-card__stat-mini__label">STA</span>
            <span class="poke-card__stat-mini__value">${formatStat(p.stats?.stamina)}</span>
          </span>
        </div>
      </div>
    `;

    card.addEventListener("click", () => openModal(p));
    return card;
  }

  // ===== 모달 =====
  function openModal(p) {
    const typesHtml = (p.types || []).map((t) => {
      const color = getTypeColor(t);
      return `<span class="poke-modal__type" style="background:${color}">${getTypeEmoji(t)} ${t}</span>`;
    }).join("");

    const classBadge = p.pokemonClass
      ? `<span class="poke-modal__class poke-modal__class--${p.pokemonClass.toLowerCase()}">${p.pokemonClass}</span>`
      : "";

    const badges = [];
    if (p.hasMega) badges.push('<span class="poke-modal__badge poke-modal__badge--mega">MEGA</span>');
    if (p.hasGigantamax) badges.push('<span class="poke-modal__badge poke-modal__badge--gmax">GIGANTAMAX</span>');
    const badgesHtml = badges.join("");

    // 스텟 바
    const maxStat = 255;
    const statsHtml = [
      { label: "HP", key: "stamina", val: p.stats?.stamina || 0 },
      { label: "ATTACK", key: "attack", val: p.stats?.attack || 0 },
      { label: "DEFENSE", key: "defense", val: p.stats?.defense || 0 },
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
      movesHtml.push(`<div class="poke-modal__moves-section"><h4 class="poke-modal__moves-title">퀵 스킬</h4><div class="poke-modal__moves-list">${p.quickMoves.map(m => `<span class="poke-modal__move">${m}</span>`).join("")}</div></div>`);
    }
    if (p.cinematicMoves?.length) {
      movesHtml.push(`<div class="poke-modal__moves-section"><h4 class="poke-modal__moves-title">시네매틱 스킬</h4><div class="poke-modal__moves-list">${p.cinematicMoves.map(m => `<span class="poke-modal__move poke-modal__move--special">${m}</span>`).join("")}</div></div>`);
    }
    if (p.eliteQuickMoves?.length) {
      movesHtml.push(`<div class="poke-modal__moves-section"><h4 class="poke-modal__moves-title">에픽 퀵 스킬</h4><div class="poke-modal__moves-list">${p.eliteQuickMoves.map(m => `<span class="poke-modal__move poke-modal__move--elite">${m}</span>`).join("")}</div></div>`);
    }
    if (p.eliteCinematicMoves?.length) {
      movesHtml.push(`<div class="poke-modal__moves-section"><h4 class="poke-modal__moves-title">에픽 시네매틱 스킬</h4><div class="poke-modal__moves-list">${p.eliteCinematicMoves.map(m => `<span class="poke-modal__move poke-modal__move--elite">${m}</span>`).join("")}</div></div>`);
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
          <img class="poke-modal__img" src="${p.image}" alt="${p.name}" />
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

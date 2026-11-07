// 포케써니 홍보 페이지 스크립트

(function () {
  "use strict";

  // --- 방문자 카운팅 (countapi.mileshilliard.com 무료 API, countapi.xyz 후속 서비스) ---
  function trackVisit() {
    var id = "pokesunny_homepage_v1";
    fetch("https://countapi.mileshilliard.com/api/v1/hit/" + id)
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.json();
      })
      .then(function (data) {
        var count = data.value || 0;
        var badge = document.querySelector(".visit-badge");
        if (badge) {
          badge.textContent = "방문자 " + count.toLocaleString("ko-KR") + "명";
          badge.classList.add("is-visible");
        }
      })
      .catch(function () {
        // API 실패 시 무시
      });
  }

  // stats.json에서 실시간 통계 로드 (GitHub Actions에서 매일 갱신)
  function loadStats(callback) {
    fetch("stats.json", { cache: "no-store" })
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.json();
      })
      .then(function (stats) {
        callback(stats);
      })
      .catch(function () {
        // fetch 실패 → HTML에 있는 기본값 그대로 사용
        callback(null);
      });
  }

  // --- 숫자 카운트업 (히어로 통계) ---
  function animateCount(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    if (isNaN(target)) return;

    var duration = 1400;
    var start = null;

    function fmt(n) {
      return n.toLocaleString("ko-KR");
    }

    function step(ts) {
      if (start === null) start = ts;
      var progress = Math.min((ts - start) / duration, 1);
      // ease-out
      var eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = fmt(Math.floor(eased * target));
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = fmt(target);
      }
    }
    requestAnimationFrame(step);
  }

  // --- 스크롤 리빌 + 숫자 트리거 (IntersectionObserver) ---
  function init() {
    // 카드/소개/CTA를 스크롤 리빌 대상 클래스로 표시
    addRevealClass();

    var counters = document.querySelectorAll(".stat__num");
    var revealed = false;

    function startCounters() {
      if (revealed) return;
      revealed = true;
      counters.forEach(animateCount);
    }

    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          if (entry.target.classList.contains("reveal")) {
            entry.target.classList.add("is-visible");
          }
          io.unobserve(entry.target);
        });
      }, { threshold: 0.15 });

      document.querySelectorAll(".reveal").forEach(function (el) {
        io.observe(el);
      });

      var cio = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            startCounters();
            cio.disconnect();
          }
        });
      }, { threshold: 0.4 });
      if (counters.length) cio.observe(counters[0]);
    } else {
      // 폴백: 즉시 표시
      document.querySelectorAll(".reveal").forEach(function (el) {
        el.classList.add("is-visible");
      });
      startCounters();
    }

    // 방문자 카운팅
    trackVisit();

    // stats.json 로드 → data-count 갱신
    loadStats(function (stats) {
      if (!stats) return; // 폴백: HTML 기본값 사용
      var mapping = {
        subscribers: counters[0],
        videos: counters[1],
        views: counters[2],
      };
      Object.keys(mapping).forEach(function (key) {
        var el = mapping[key];
        var val = stats[key];
        if (el && typeof val === "number" && val > 0) {
          el.setAttribute("data-count", val);
          // 아직 카운트업 시작 전이면 텍스트도 갱신
          if (!revealed) {
            el.textContent = val.toLocaleString("ko-KR");
          }
        }
      });
    });
  }

  function addRevealClass() {
    [".about", ".card", ".cta"].forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (el) {
        el.classList.add("reveal");
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

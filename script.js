// 포케써니 홍보 페이지 스크립트

(function () {
  "use strict";

  // --- 방문자 카운팅 (countapi.mileshilliard.com 무료 API) ---
  function trackVisit() {
    var id = "pokesunny_homepage_v1";
    var badge = document.querySelector(".visit-badge");
    if (!badge) return;

    fetch("https://countapi.mileshilliard.com/api/v1/hit/" + id)
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(function (data) {
        var count = parseInt(data.value, 10) || 0;
        badge.textContent = count.toLocaleString("ko-KR");
      })
      .catch(function (err) {
        console.warn("[pokesunny] visit counter fetch failed:", err);
        badge.textContent = "—";
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

    // 최근 영상 로드
    loadVideos();

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
    [".about", ".card", ".cta", ".vid-card"].forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (el) {
        el.classList.add("reveal");
      });
    });
  }

  // --- 최근 영상 렌더링 ---
  function loadVideos() {
    var grid = document.getElementById("vid-grid");
    if (!grid) return;

    var FALLBACK = [
      { id: "35MOoSt5-wI", title: "잠들기 전 듣는 포켓몬 이야기｜신화 속 펄기아와 세계의 탄생", views: "113", published: "2주 전", duration: "11:16", thumb: "https://i.ytimg.com/vi/35MOoSt5-wI/hqdefault.jpg" },
      { id: "isO37PGtYtY", title: "잠들기 전 듣는 포켓몬 이야기｜시간의 신 디아루가", views: "177", published: "3주 전", duration: "3:09", thumb: "https://i.ytimg.com/vi/isO37PGtYtY/hqdefault.jpg" },
      { id: "VkNF1t4fHZw", title: "이벨타르의 모든 것 | 제르네아스·지가르데와 6세대 XYZ 이야기", views: "511", published: "1개월 전", duration: "3:19", thumb: "https://i.ytimg.com/vi/VkNF1t4fHZw/hqdefault.jpg" },
      { id: "byM2LSyQXpc", title: "바다를 지배하는 가이오가🌊 그란돈·레쿠쟈 관계부터 약점·졸업스킬까지", views: "276", published: "1개월 전", duration: "2:39", thumb: "https://i.ytimg.com/vi/byM2LSyQXpc/hqdefault.jpg" },
      { id: "vZ9tZgDEB-M", title: "지가르데, 어디까지 알고 있니?! 3가지 폼부터 셀 250개까지!!", views: "758", published: "1개월 전", duration: "3:32", thumb: "https://i.ytimg.com/vi/vZ9tZgDEB-M/hqdefault.jpg" },
      { id: "qSThcQmNdeA", title: "황혼의 갈기 네크로즈마, 왜 합체했을까? 특징부터 졸업스킬까지!", views: "198", published: "1개월 전", duration: "3:24", thumb: "https://i.ytimg.com/vi/qSThcQmNdeA/hqdefault.jpg" }
    ];

    function render(videos) {
      grid.innerHTML = "";
      videos.forEach(function (v) {
        var a = document.createElement("a");
        a.className = "vid-card";
        a.href = "https://www.youtube.com/watch?v=" + v.id;
        a.target = "_blank";
        a.rel = "noopener";

        var viewsNum = v.views ? parseInt(v.views.replace(/,/g, ""), 10) : 0;
        var viewsText = viewsNum ? viewsNum.toLocaleString("ko-KR") + "회" : "";

        a.innerHTML =
          '<div class="vid-card__thumb">' +
            '<img src="' + v.thumb + '" alt="' + v.title.replace(/"/g, '&quot;') + '" loading="lazy" />' +
            (v.duration ? '<span class="vid-card__dur">' + v.duration + '</span>' : '') +
          '</div>' +
          '<div class="vid-card__body">' +
            '<h3 class="vid-card__title">' + v.title + '</h3>' +
            '<div class="vid-card__meta">' +
              (viewsText ? '<span>' + viewsText + '</span>' : '') +
              (v.published ? '<span>' + v.published + '</span>' : '') +
            '</div>' +
          '</div>';

        grid.appendChild(a);
      });

      // 렌더링 후 reveal class 적용
      addRevealClass();
      if ("IntersectionObserver" in window) {
        var io2 = new IntersectionObserver(function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-visible");
              io2.unobserve(entry.target);
            }
          });
        }, { threshold: 0.15 });
        grid.querySelectorAll(".vid-card").forEach(function (el) {
          io2.observe(el);
        });
      } else {
        grid.querySelectorAll(".vid-card").forEach(function (el) {
          el.classList.add("is-visible");
        });
      }
    }

    fetch("recent_videos.json", { cache: "no-store" })
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.json();
      })
      .then(function (videos) {
        if (Array.isArray(videos) && videos.length > 0) {
          render(videos);
        } else {
          render(FALLBACK);
        }
      })
      .catch(function (err) {
        console.warn("[pokesunny] recent_videos.json fetch failed, using fallback:", err);
        render(FALLBACK);
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

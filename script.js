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
    fetch("stats.json?_r=" + Math.random(), { cache: "no-store" })
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

    // Pokémon GO 뉴스 로드
    loadNews();

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

    fetch("recent_videos.json?_r=" + Math.random(), { cache: "no-store" })
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

  // --- Pokémon GO 뉴스 렌더링 ---
  function loadNews() {
    var grid = document.getElementById("news-grid");
    if (!grid) return;

    var FALLBACK = [
      { url: "https://pokemongo.com/ko/news/", title: "Pokémon GO 뉴스", summary: "Pokémon GO 공식 한국어 뉴스입니다.", image: "", published: "2026-11-14" },
    ];

    function render(news) {
      grid.innerHTML = "";
      news.forEach(function (n) {
        var a = document.createElement("a");
        a.className = "news-card";
        a.href = "news-detail.html?url=" + encodeURIComponent(n.url);
        a.target = "";
        a.rel = "noopener";

        var pubDate = n.published ? new Date(n.published).toLocaleDateString("ko-KR") : "";

        a.innerHTML =
          (n.image ? '<div class="news-card__thumb">' +
            '<img src="' + n.image + '" alt="" loading="lazy" />' +
          '</div>' : '') +
          '<div class="news-card__body">' +
            '<h3 class="news-card__title">' + escapeHtml(n.title) + '</h3>' +
            (n.summary ? '<p class="news-card__summary">' + escapeHtml(n.summary) + '</p>' : '') +
            '<div class="news-card__meta">' +
              (pubDate ? '<span>' + pubDate + '</span>' : '') +
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
        grid.querySelectorAll(".news-card").forEach(function (el) {
          io2.observe(el);
        });
      } else {
        grid.querySelectorAll(".news-card").forEach(function (el) {
          el.classList.add("is-visible");
        });
      }
    }

    fetch("news.json?_r=" + Math.random(), { cache: "no-store" })
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.json();
      })
      .then(function (news) {
        if (Array.isArray(news) && news.length > 0) {
          render(news);
        } else {
          render(FALLBACK);
        }
      })
      .catch(function (err) {
        console.warn("[pokesunny] news.json fetch failed, using fallback:", err);
        render(FALLBACK);
      });
  }

  // ---게시판(Firebase Realtime Database 기반) ---
  var FB_CONFIG = {
    apiKey: "AIzaSyAqptwwzfKOiuGFqM3gQEr9E7tTGF_CmGc",
    authDomain: "pokesunny-guestbook.firebaseapp.com",
    databaseURL: "https://pokesunny-guestbook-default-rtdb.firebaseio.com",
    projectId: "pokesunny-guestbook",
    storageBucket: "pokesunny-guestbook.firebasestorage.app",
    messagingSenderId: "",
    appId: ""
  };

  var ADMIN_PIN = "pokesunny2026"; // 관리자 PIN
  var fbApp = null;
  var fbDb = null;
  var isAdmin = false;
  var editingId = null; // 수정 중인 메시지 ID

  function initFirebase() {
    if (fbDb) return;
    fbApp = firebase.initializeApp(FB_CONFIG);
    fbDb = firebase.database();
  }

  function escapeHtml(str) {
    var div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  function timeAgo(ts) {
    var date = new Date(ts);
    var now = new Date();
    var diff = Math.floor((now - date) / 1000);
    if (diff < 60) return "방금 전";
    if (diff < 3600) return Math.floor(diff / 60) + "분 전";
    if (diff < 86400) return Math.floor(diff / 3600) + "시간 전";
    if (diff < 2592000) return Math.floor(diff / 86400) + "일 전";
    if (diff < 31536000) return Math.floor(diff / 2592000) + "개월 전";
    return Math.floor(diff / 31536000) + "년 전";
  }

  // --- 관리자 토글 ---
  function toggleAdmin() {
    if (isAdmin) {
      isAdmin = false;
      localStorage.removeItem("pokesunny_admin");
      document.body.classList.remove("admin-mode");
      document.getElementById("admin-badge").style.display = "none";
      loadMessages();
      return;
    }
    var pin = prompt("관리자 PIN을 입력해주세요:");
    if (pin === null) return;
    if (pin === ADMIN_PIN) {
      isAdmin = true;
      localStorage.setItem("pokesunny_admin", "1");
      document.body.classList.add("admin-mode");
      document.getElementById("admin-badge").style.display = "inline-block";
      loadMessages();
    } else {
      alert("PIN이 올바르지 않아요.");
    }
  }

  // --- 메시지 삭제 ---
  function deleteMessage(id) {
    if (!confirm("이 메시지를 삭제할까요?")) return;
    fbDb.ref("messages/" + id).remove()
      .then(function () {
        loadMessages();
      })
      .catch(function (err) {
        console.warn("[pokesunny] delete failed:", err);
        alert("삭제에 실패했어요. 다시 시도해주세요.");
      });
  }

  // --- 메시지 수정 (관리자) ---
  function startEdit(id, name, msg) {
    var nameInput = document.getElementById("board-name");
    var msgInput = document.getElementById("board-msg");
    var btn = document.getElementById("board-submit");
    var cancelBtn = document.getElementById("board-cancel");

    editingId = id;
    nameInput.value = name;
    msgInput.value = msg;
    btn.innerHTML = '✏️ 수정 저장';
    cancelBtn.style.display = "inline-block";

    // 폼으로 스크롤
    document.getElementById("board-form").scrollIntoView({ behavior: "smooth", block: "center" });
  }

  function cancelEdit() {
    editingId = null;
    var form = document.getElementById("board-form");
    form.reset();
    var btn = document.getElementById("board-submit");
    var cancelBtn = document.getElementById("board-cancel");
    btn.innerHTML =
      '<svg viewBox="0 0 24 24" class="ic" aria-hidden="true"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7Z"/></svg>' +
      ' 메시지 남기기';
    cancelBtn.style.display = "none";
  }

  // --- 메시지 로드 + 렌더링 ---
  function loadMessages() {
    var list = document.getElementById("board-list");
    if (!list) return;

    initFirebase();
    fbDb.ref("messages").once("value", function (snap) {
      var data = snap.val();
      if (!data) {
        list.innerHTML = '<div class="board__empty">아직 메시지가 없어요.<br />첫 번째 메시지를 남겨보세요! ✨</div>';
        return;
      }
      var msgs = Object.keys(data).map(function (key) {
        var m = data[key];
        m._id = key;
        return m;
      }).sort(function (a, b) { return b.ts - a.ts; });

      if (msgs.length === 0) {
        list.innerHTML = '<div class="board__empty">아직 메시지가 없어요.<br />첫 번째 메시지를 남겨보세요! ✨</div>';
        return;
      }

      list.innerHTML = "";
      msgs.forEach(function (m) {
        var name = m.name || "방문자";
        var msg = m.msg || "";
        var time = timeAgo(m.ts);

        var el = document.createElement("div");
        el.className = "board__item" + (isAdmin ? " board__item--admin" : "");

        var actionsHtml = "";
        if (isAdmin) {
          actionsHtml =
            '<div class="board__item-actions">' +
              '<button class="board__btn-edit" data-id="' + m._id + '" title="수정">' +
                '<svg viewBox="0 0 24 24" width="14" height="14"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
              '</button>' +
              '<button class="board__btn-del" data-id="' + m._id + '" title="삭제">' +
                '<svg viewBox="0 0 24 24" width="14" height="14"><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2m3 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6h14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>' +
              '</button>' +
            '</div>';
        }

        el.innerHTML =
          '<div class="board__item-head">' +
            '<span class="board__item-name">' + escapeHtml(name) + '</span>' +
            '<span class="board__item-time">' + escapeHtml(time) + '</span>' +
            actionsHtml +
          '</div>' +
          '<p class="board__item-msg">' + escapeHtml(msg) + '</p>';
        list.appendChild(el);
      });

      // 수정/삭제 버튼 이벤트 바인딩
      if (isAdmin) {
        list.querySelectorAll(".board__btn-del").forEach(function (btn) {
          btn.addEventListener("click", function () {
            deleteMessage(btn.getAttribute("data-id"));
          });
        });
        list.querySelectorAll(".board__btn-edit").forEach(function (btn) {
          btn.addEventListener("click", function () {
            var id = btn.getAttribute("data-id");
            var msgData = data[id];
            startEdit(id, msgData.name || "방문자", msgData.msg || "");
          });
        });
      }
    }, function (err) {
      console.warn("[pokesunny] messages fetch failed:", err);
      list.innerHTML = '<div class="board__error">메시지를 불러오지 못했어요. 잠시 후 다시 시도해주세요.</div>';
    });
  }

  function initBoard() {
    var form = document.getElementById("board-form");
    var list = document.getElementById("board-list");
    if (!form || !list) return;

    // 저장된 관리자 세션 복원
    if (localStorage.getItem("pokesunny_admin") === "1") {
      isAdmin = true;
      document.body.classList.add("admin-mode");
      document.getElementById("admin-badge").style.display = "inline-block";
    }

    // 메시지 로드
    loadMessages();

    // 실시간 업데이트 구독 (child_added + child_changed + child_removed)
    initFirebase();
    fbDb.ref("messages").on("value", function () {
      loadMessages();
    });

    // 관리자 토글 버튼
    var adminBtn = document.getElementById("board-admin-btn");
    if (adminBtn) {
      adminBtn.addEventListener("click", toggleAdmin);
    }

    // 제출 핸들러 (새 메시지 + 수정 저장)
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      var nameInput = document.getElementById("board-name");
      var msgInput = document.getElementById("board-msg");
      var btn = document.getElementById("board-submit");

      var name = nameInput.value.trim() || "방문자";
      var msg = msgInput.value.trim();

      if (!msg) return;

      btn.disabled = true;
      btn.innerHTML = editingId ? '저장 중…' : '남기는 중…';

      var promise;
      if (editingId) {
        // 수정 모드
        promise = fbDb.ref("messages/" + editingId).set({
          name: name,
          msg: msg,
          ts: Date.now()
        });
      } else {
        // 새 메시지
        promise = fbDb.ref("messages").push({
          name: name,
          msg: msg,
          ts: Date.now()
        });
      }

      var wasEdit = editingId;

      promise
        .then(function () {
          form.reset();
          cancelEdit();
          btn.disabled = false;
          btn.innerHTML =
            '<svg viewBox="0 0 24 24" class="ic" aria-hidden="true"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7Z"/></svg>' +
            ' 메시지 남기기';

          var notify = document.createElement("div");
          notify.className = "board__notify";
          notify.textContent = wasEdit ? "✅ 메시지가 수정되었어요!" : "✨ 메시지가 남겨졌어요!";
          list.parentNode.insertBefore(notify, list);
          setTimeout(function () {
            if (notify.parentNode) notify.remove();
          }, 4000);
        })
        .catch(function (err) {
          console.warn("[pokesunny] submit failed:", err);
          btn.disabled = false;
          btn.innerHTML = editingId ? '✏️ 수정 저장' :
            '<svg viewBox="0 0 24 24" class="ic" aria-hidden="true"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7Z"/></svg>' +
            ' 메시지 남기기';
          alert("저장에 실패했어요. 네트워크 오류일 수 있습니다.");
        });
    });

    // 수정 취소 버튼
    var cancelBtn = document.getElementById("board-cancel");
    if (cancelBtn) {
      cancelBtn.addEventListener("click", cancelEdit);
    }
  }

  // init에개시판 추가
  var _origInit = init;
  function _extendedInit() {
    _origInit();
    initBoard();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", _extendedInit);
  } else {
    _extendedInit();
  }
})();

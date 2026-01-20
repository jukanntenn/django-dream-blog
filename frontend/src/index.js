import Offcanvas from "./offcanvas";
import Scrollspy from "./scrollspy";
import Backtop from "./backtop";
import ThemeSwitcher from "./theme-switcher";
import "./scripts/katex";

// 初始化主题切换器
const themeSwitcherElement = document.getElementById("theme-switcher");
if (themeSwitcherElement) {
  new ThemeSwitcher(themeSwitcherElement);
}

new Backtop(document.getElementById("backtop"));

const offcanvas = new Offcanvas(document.getElementById("left"), {
  backdropClassName: "backdrop",
});
const trigger = document.getElementById("offcanvas-trigger");
trigger.addEventListener("click", function () {
  offcanvas.toggle();
});

// TOC

function appendChildren(root, children) {
  return [].filter
    .call(root.children, (el) => el.nodeName === "LI")
    .forEach((liElem) => {
      const aElem = liElem.querySelector(":scope > a");
      children.push(aElem);
      const ulElem = liElem.querySelector(":scope > ul");
      if (ulElem) {
        const nextElements = [];
        children.push(nextElements);
        appendChildren(ulElem, nextElements);
      }
    });
}

const tocElem = document.getElementById("toc");
const tocUlElem = tocElem && tocElem.children[0];

function getScrollOffsetTop() {
  const navElem = document.getElementById("site-nav");
  const navHeight = navElem ? navElem.getBoundingClientRect().height : 0;
  return navHeight + 12;
}

function scrollToHash(hash, behavior) {
  if (!hash) return false;
  const id = decodeURIComponent(hash.startsWith("#") ? hash.slice(1) : hash);
  if (!id) return false;
  const target = document.getElementById(id);
  if (!target) return false;
  const top =
    target.getBoundingClientRect().top +
    window.pageYOffset -
    getScrollOffsetTop();
  window.scrollTo({ top: Math.max(0, top), behavior });
  return true;
}

if (tocUlElem) {
  const tree = [];
  appendChildren(tocUlElem, tree);
  new Scrollspy(tree, document.body, {
    activeClassName: "active",
    offset: getScrollOffsetTop,
  });

  tocElem.addEventListener("click", (e) => {
    const aElem = e.target.closest && e.target.closest("a");
    if (!aElem) return;
    const href = aElem.getAttribute("href");
    if (!href) return;
    const id = href.includes("#")
      ? href.split("#").pop()
      : href.startsWith("#")
        ? href.slice(1)
        : null;
    if (!id) return;
    const hash = `#${id}`;
    const didScroll = scrollToHash(hash, "smooth");
    if (!didScroll) return;
    e.preventDefault();
    if (window.location.hash !== hash) {
      window.history.pushState(null, "", hash);
    }
  });
}

/**
 * Registers a callback to run when the DOM is ready.
 * Handles both modern browsers and legacy IE support.
 * Note: onReady is also defined in katex.js for KaTeX initialization.
 */
var onReady = function onReady(fn) {
  if (document.addEventListener) {
    document.addEventListener("DOMContentLoaded", fn);
  } else {
    document.addEventListener("onreadystatechange", function () {
      if (document.readyState === "interactive") {
        fn();
      }
    });
  }
};

// Handle initial hash scrolling
onReady(function () {
  if (window.location.hash) {
    scrollToHash(window.location.hash, "auto");
  }
});

// Comment
function _getTargetFields(formElem) {
  const content_type = formElem.querySelector(
    "input[name='content_type']"
  ).value;
  const object_pk = formElem.querySelector("input[name='object_pk']").value;

  return {
    content_type,
    object_pk,
  };
}

function fetchCommentForm(url) {
  return fetch(url, {
    method: "GET",
  })
    .then((response) => {
      if (response.status !== 200) {
      }
      return response.text();
    })
    .then((data) => {
      return data;
    })
    .catch((error) => {});
}

function getInsertBeforeElem(refElem) {
  while (
    refElem.nextElementSibling &&
    refElem.nextElementSibling.classList.contains("pl-14")
  ) {
    refElem = refElem.nextElementSibling;
  }

  return refElem.nextElementSibling;
}

const commentFormElem = document.querySelector(".comment-form");
if (commentFormElem) {
  commentFormElem.addEventListener("submit", function (event) {
    event.preventDefault();
    const submitBtn = commentFormElem.querySelector("button[type='submit']");
    submitBtn.disabled = true;
    submitBtn.textContent = "正在提交...";

    var formData = new FormData(this);

    fetch(this.action, {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        return response.text();
      })
      .then((data) => {
        const commentList = document.getElementById("comment-list");
        if (commentList.firstChild) {
          commentList.insertAdjacentHTML("afterbegin", data);
        } else {
          commentList.innerHTML = data;
        }
        commentFormElem.querySelector("textarea[name='comment']").value = "";
      })
      .catch((error) => {
        console.error("提交出错:", error);
      })
      .finally(() => {
        submitBtn.disabled = false;
        submitBtn.textContent = "提交评论";
      });
  });

  const replyBtns = document.querySelectorAll(".reply");
  replyBtns.forEach((btn) => {
    btn.addEventListener("click", function (event) {
      event.preventDefault();

      btn.classList.add("hidden");
      btn.nextElementSibling.classList.remove("hidden");
      const targetFields = _getTargetFields(commentFormElem);
      const params = new URLSearchParams(targetFields);
      fetchCommentForm("/comments/form/?" + params.toString()).then((html) => {
        btn.nextElementSibling.classList.add("hidden");
        btn.nextElementSibling.nextElementSibling.classList.remove("hidden");
        const parser = new DOMParser();
        const replyFormElem = parser.parseFromString(html, "text/html").body
          .firstChild;
        replyFormElem.querySelector("input[name='parent']").value =
          this.dataset.cid;

        replyFormElem
          .querySelector('button[type="submit"]')
          .addEventListener("click", function (event) {
            event.preventDefault();
            this.disabled = true;
            this.textContent = "正在提交...";

            const formData = new FormData(replyFormElem);
            fetch(replyFormElem.action, {
              method: "POST",
              body: formData,
            })
              .then((response) => {
                return response.text();
              })
              .then((html) => {
                const parser = new DOMParser();
                const elem = parser.parseFromString(html, "text/html").body
                  .firstChild;
                let ref = btn.parentNode.parentNode.parentNode;
                let insertBeforeElem = getInsertBeforeElem(ref);
                if (insertBeforeElem) {
                  ref.parentNode.insertBefore(elem, insertBeforeElem);
                } else {
                  ref.parentNode.appendChild(elem);
                }
                replyFormElem.querySelector("textarea[name='comment']").value =
                  "";
              })
              .catch((error) => {
                console.error("提交出错:", error);
              })
              .finally(() => {
                const submitBtn = replyFormElem.querySelector(
                  "button[type='submit']"
                );
                submitBtn.disabled = false;
                submitBtn.textContent = "提交评论";
              });
          });

        this.parentNode.insertAdjacentElement("afterend", replyFormElem);
      });
    });
  });

  const foldBtns = document.querySelectorAll(".fold");
  foldBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      btn.parentNode.nextElementSibling.remove();
      btn.classList.add("hidden");
      btn.previousElementSibling.previousElementSibling.classList.remove(
        "hidden"
      );
    });
  });
}

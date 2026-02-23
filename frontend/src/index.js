import Offcanvas from "./offcanvas";
import Scrollspy from "./scrollspy";
import Backtop from "./backtop";
import ThemeSwitcher from "./theme-switcher";
import Comment from "./comment";
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

function scrollToElement(target, behavior) {
  const top =
    target.getBoundingClientRect().top + window.pageYOffset - getScrollOffsetTop();
  window.scrollTo({ top: Math.max(0, top), behavior });
}

const commentModule = new Comment();
commentModule.init();

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
    let decodedId = id;
    try {
      decodedId = decodeURIComponent(id);
    } catch {}
    const target = document.getElementById(decodedId);
    if (!target) return;

    if (target.closest("#comment-list")) {
      const didScroll = commentModule.scrollToSelector(`#${decodedId}`, "smooth");
      if (!didScroll) return;
    } else {
      scrollToElement(target, "smooth");
    }

    e.preventDefault();
    const hash = `#${decodedId}`;
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
    let decodedId = window.location.hash.slice(1);
    try {
      decodedId = decodeURIComponent(decodedId);
    } catch {}
    const target = document.getElementById(decodedId);
    if (!target) return;

    if (target.closest("#comment-list")) {
      commentModule.scrollToSelector(`#${decodedId}`, "auto");
    } else {
      scrollToElement(target, "auto");
    }
  }
});

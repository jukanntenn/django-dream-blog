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

function scrollToHash(hash, behavior) {
  if (!hash) return false;
  const id = decodeURIComponent(hash.startsWith("#") ? hash.slice(1) : hash);
  if (!id) return false;
  const target = document.getElementById(id);
  if (!target) return false;
  const isCommentTarget = !!target.closest("#comment-list");
  if (!isCommentTarget) {
    const top =
      target.getBoundingClientRect().top +
      window.pageYOffset -
      getScrollOffsetTop();
    window.scrollTo({ top: Math.max(0, top), behavior });
    return true;
  }

  const navHeight = getScrollOffsetTop() - 12;
  const viewportHeight = window.innerHeight;
  const rect = target.getBoundingClientRect();

  const elementTop = rect.top - navHeight;
  const elementBottom = rect.bottom;

  if (elementTop >= 0 && elementBottom <= viewportHeight) {
    return true;
  }

  const currentScrollTop = window.pageYOffset;
  const scrollTarget =
    elementTop < 0
      ? rect.top + currentScrollTop - navHeight
      : rect.bottom + currentScrollTop - viewportHeight;
  window.scrollTo({ top: Math.max(0, scrollTarget), behavior });
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

// Initialize Comment module
const commentModule = new Comment();
commentModule.init();

/**
 * Frontend entry point: styles, page bootstrapping and interaction modules.
 */
import "vite/modulepreload-polyfill";
import "./styles/friendly.css";
import "./styles/main.css";
import "./lib/search";
import "./vendor/katex";
import "./vendor/mermaid";
import { Offcanvas, Scrollspy } from "@jukanntenn/kutsu";
import Backtop from "./lib/backtop";
import ThemeSwitcher from "./lib/theme-switcher";
import Comment from "./lib/comment";
import { initLightbox } from "./lib/lightbox";
import { initCodeCopy } from "./lib/code-copy";
import { initShare } from "./lib/share";
import { initNavbarBlur } from "./lib/navbar-blur";

initNavbarBlur();

const themeSwitcherElement = document.getElementById("theme-switcher");
if (themeSwitcherElement) {
  new ThemeSwitcher(themeSwitcherElement);
}

new Backtop(document.getElementById("backtop")!);

const offcanvas = new Offcanvas(document.getElementById("left")!, {
  backdrop: true,
  backdropClassName: "backdrop",
});
const trigger = document.getElementById("offcanvas-trigger")!;
trigger.addEventListener("click", () => {
  offcanvas.toggle();
});

function initMobileMenu(): void {
  const triggerEl = document.getElementById("mobile-menu-trigger");
  const menu = document.getElementById("mobile-menu");

  if (!triggerEl || !menu) return;

  triggerEl.addEventListener("click", () => {
    const isExpanded = triggerEl.getAttribute("aria-expanded") === "true";
    triggerEl.setAttribute("aria-expanded", String(!isExpanded));
    menu.setAttribute("aria-hidden", String(isExpanded));
    menu.classList.toggle("hidden");
  });

  document.addEventListener("click", (event) => {
    const isClickInside =
      triggerEl.contains(event.target as Node) || menu.contains(event.target as Node);
    if (!isClickInside && !menu.classList.contains("hidden")) {
      triggerEl.setAttribute("aria-expanded", "false");
      menu.setAttribute("aria-hidden", "true");
      menu.classList.add("hidden");
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !menu.classList.contains("hidden")) {
      triggerEl.setAttribute("aria-expanded", "false");
      menu.setAttribute("aria-hidden", "true");
      menu.classList.add("hidden");
      triggerEl.focus();
    }
  });
}

initMobileMenu();

// TOC

function appendChildren(root: Element, children: Element[]): void {
  Array.from(root.children)
    .filter((el) => el.nodeName === "LI")
    .forEach((liElem) => {
      const aElem = liElem.querySelector<HTMLAnchorElement>(":scope > a");
      if (aElem) children.push(aElem);
      const ulElem = liElem.querySelector<HTMLUListElement>(":scope > ul");
      if (ulElem) {
        const nextElements: Element[] = [];
        children.push(nextElements as unknown as Element);
        appendChildren(ulElem, nextElements);
      }
    });
}

const tocElem = document.getElementById("toc");
const tocUlElem = tocElem && tocElem.children[0];

function getScrollOffsetTop(): number {
  const navElem = document.getElementById("site-nav");
  const navHeight = navElem ? navElem.getBoundingClientRect().height : 0;
  return navHeight + 12;
}

function scrollToElement(target: Element, behavior: ScrollBehavior): void {
  const top = target.getBoundingClientRect().top + window.pageYOffset - getScrollOffsetTop();
  window.scrollTo({ top: Math.max(0, top), behavior });
}

const commentModule = new Comment();
commentModule.init();

if (tocUlElem) {
  const tree: Element[] = [];
  appendChildren(tocUlElem, tree);
  new Scrollspy(tree as HTMLElement[], document.body, {
    activeClassName: "active",
    offset: getScrollOffsetTop,
  });

  tocElem!.addEventListener("click", (e) => {
    const aElem = (e.target as Element).closest && (e.target as Element).closest("a");
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

function onReady(fn: () => void): void {
  document.addEventListener("DOMContentLoaded", fn);
}

onReady(() => {
  if (window.location.hash) {
    const decodedId = window.location.hash.slice(1);
    try {
      decodeURIComponent(decodedId);
    } catch {}
    const target = document.getElementById(decodedId);
    if (!target) return;

    if (target.closest("#comment-list")) {
      commentModule.scrollToSelector(`#${decodedId}`, "auto");
    } else if (decodedId === "comment-area") {
      scrollToElement(target, "auto");
      commentModule.focusForm();
    } else {
      scrollToElement(target, "auto");
    }
  }
});

document.addEventListener("click", (e) => {
  const link = (e.target as Element).closest && (e.target as Element).closest('a[href$="#comment-area"]');
  if (!link) return;

  const href = link.getAttribute("href");
  if (!href) return;

  const linkUrl = new URL(href, window.location.origin);
  const isSamePage = linkUrl.pathname === window.location.pathname;

  if (!isSamePage) return;

  e.preventDefault();

  const target = document.getElementById("comment-area");
  if (!target) return;

  scrollToElement(target, "smooth");
  commentModule.focusForm();

  if (window.location.hash !== "#comment-area") {
    window.history.pushState(null, "", "#comment-area");
  }
});

onReady(() => {
  initLightbox();
  initCodeCopy();
  initShare();
});

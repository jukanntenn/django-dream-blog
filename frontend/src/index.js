import Offcanvas from "./offcanvas";
import Scrollspy from "./scrollspy";

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
if (tocUlElem) {
  const tree = [];
  appendChildren(tocUlElem, tree);
  new Scrollspy(tree, document.body, {
    activeClassName: "active",
  });
}

// KaTeX

var katexMath = function () {
  var maths = document.querySelectorAll(".arithmatex"),
    tex;

  for (var i = 0; i < maths.length; i++) {
    tex = maths[i].textContent || maths[i].innerText;
    if (tex.startsWith("\\(") && tex.endsWith("\\)")) {
      katex.render(tex.slice(2, -2), maths[i], { displayMode: false });
    } else if (tex.startsWith("\\[") && tex.endsWith("\\]")) {
      katex.render(tex.slice(2, -2), maths[i], { displayMode: true });
    }
  }
};

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

onReady(function () {
  if (typeof katex !== "undefined") {
    katexMath();
  }
});

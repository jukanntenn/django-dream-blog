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

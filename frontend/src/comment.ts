import Toast from "./toast";

const NAME = "comment";

type Config = {
  formSelector: string;
  listSelector: string;
  areaSelector: string;
};

const defaultConfig: Config = {
  formSelector: ".comment-form",
  listSelector: "#comment-list",
  areaSelector: "#comment-area",
};

const ERROR_MESSAGES: Record<string, string> = {
  network: "Network connection failed, please try again",
  server: "Server error, please try again later",
};

class Comment {
  private formElem: HTMLFormElement | null;

  private listElem: HTMLElement | null;

  private areaElem: HTMLElement | null;

  private config: Config;

  constructor(config: Partial<Config> = {}) {
    this.config = { ...defaultConfig, ...config };
    this.formElem = document.querySelector(this.config.formSelector);
    this.listElem = document.querySelector(this.config.listSelector);
    this.areaElem = document.querySelector(this.config.areaSelector);
  }

  static get NAME() {
    return NAME;
  }

  init(): void {
    if (this.formElem) {
      this.formElem.addEventListener("submit", this.handleSubmit.bind(this));
    }
    if (this.listElem) {
      this.listElem.addEventListener("click", this.handleListClick.bind(this));
    }
  }

  scrollToSelector(selector: string, behavior: ScrollBehavior = "smooth"): boolean {
    return this.scrollToHash(selector, behavior);
  }

  private handleSubmit(event: Event): void {
    event.preventDefault();
    const form = event.target as HTMLFormElement;
    const submitBtn = form.querySelector<HTMLButtonElement>("button[type='submit']");

    if (!submitBtn) return;

    this.setButtonLoading(submitBtn, true);

    const formData = new FormData(form);

    fetch(form.action, {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(ERROR_MESSAGES.server);
        }
        return response.text();
      })
      .then((html) => {
        this.insertComment(html);
        this.resetForm(form);
        new Toast("Comment posted successfully", { type: "success" });
      })
      .catch((error) => {
        this.showError(error.message || ERROR_MESSAGES.network);
      })
      .finally(() => {
        this.setButtonLoading(submitBtn, false);
      });
  }

  private handleListClick(event: Event): void {
    const target = event.target as HTMLElement;

    // Handle reply button
    const replyBtn = target.closest<HTMLElement>(".reply");
    if (replyBtn) {
      event.preventDefault();
      this.handleReply(replyBtn);
      return;
    }

    // Handle fold button
    const foldBtn = target.closest<HTMLElement>(".fold");
    if (foldBtn) {
      event.preventDefault();
      this.handleFold(foldBtn);
    }
  }

  private handleReply(replyBtn: HTMLElement): void {
    if (!this.formElem) {
      // Anonymous user - scroll to comment area
      this.areaElem?.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }

    replyBtn.classList.add("hidden");
    const loadingSpan = replyBtn.nextElementSibling;
    loadingSpan?.classList.remove("hidden");

    const targetFields = this.getTargetFields(this.formElem);
    const params = new URLSearchParams(targetFields);

    this.fetchForm(`/comments/form/?${params.toString()}`)
      .then((html) => {
        loadingSpan?.classList.add("hidden");

        if (!html) {
          replyBtn.classList.remove("hidden");
          return;
        }

        const foldBtn = loadingSpan?.nextElementSibling as HTMLElement;
        foldBtn?.classList.remove("hidden");

        const replyFormElem = this.parseHtml(html);
        const parentIdInput = replyFormElem.querySelector<HTMLInputElement>("input[name='parent']");
        if (parentIdInput) {
          parentIdInput.value = replyBtn.dataset.cid || "";
        }

        this.setupReplyForm(replyFormElem, replyBtn);
        (replyBtn.parentNode as HTMLElement)?.insertAdjacentElement("afterend", replyFormElem);
      })
      .catch(() => {
        loadingSpan?.classList.add("hidden");
        replyBtn.classList.remove("hidden");
        this.showError(ERROR_MESSAGES.network);
      });
  }

  private handleFold(foldBtn: HTMLElement): void {
    const replyForm = (foldBtn.parentNode as HTMLElement)?.nextElementSibling as HTMLElement;
    replyForm?.remove();
    foldBtn.classList.add("hidden");

    const replyBtn = foldBtn.previousElementSibling?.previousElementSibling as HTMLElement;
    replyBtn?.classList.remove("hidden");
  }

  private setupReplyForm(formElem: HTMLElement, replyBtn: HTMLElement): void {
    const submitBtn = formElem.querySelector<HTMLButtonElement>("button[type='submit']");
    if (!submitBtn) return;

    submitBtn.addEventListener("click", (event) => {
      event.preventDefault();
      this.submitReply(formElem, replyBtn, submitBtn);
    });
  }

  private submitReply(
    formElem: HTMLElement,
    replyBtn: HTMLElement,
    submitBtn: HTMLButtonElement
  ): void {
    this.setButtonLoading(submitBtn, true);

    const formData = new FormData(formElem as HTMLFormElement);

    fetch((formElem as HTMLFormElement).action, {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(ERROR_MESSAGES.server);
        }
        return response.text();
      })
      .then((html) => {
        const commentElem = this.parseHtml(html);
        const refElem = replyBtn.parentNode?.parentNode?.parentNode as HTMLElement;
        const insertBeforeElem = this.getInsertBeforeElement(refElem);

        if (insertBeforeElem) {
          refElem.parentNode?.insertBefore(commentElem, insertBeforeElem);
        } else {
          refElem.parentNode?.appendChild(commentElem);
        }

        // Remove reply form and show reply button
        formElem.remove();
        replyBtn.classList.remove("hidden");

        // Hide fold button
        const foldBtn = replyBtn.nextElementSibling?.nextElementSibling as HTMLElement;
        foldBtn?.classList.add("hidden");

        // Scroll to new comment
        if (commentElem.id) {
          this.scrollToHash(`#${commentElem.id}`);
        }

        new Toast("Reply posted successfully", { type: "success" });
      })
      .catch((error) => {
        this.showError(error.message || ERROR_MESSAGES.network);
      })
      .finally(() => {
        this.setButtonLoading(submitBtn, false);
      });
  }

  private insertComment(html: string): void {
    if (!this.listElem) return;

    if (this.listElem.firstChild) {
      this.listElem.insertAdjacentHTML("afterbegin", html);
    } else {
      this.listElem.innerHTML = html;
    }

    const newComment = this.listElem.firstElementChild as HTMLElement;
    if (newComment?.id) {
      this.scrollToHash(`#${newComment.id}`);
    }
  }

  private resetForm(form: HTMLFormElement): void {
    const textarea = form.querySelector<HTMLTextAreaElement>("textarea[name='comment']");
    if (textarea) {
      textarea.value = "";
    }
  }

  private setButtonLoading(btn: HTMLButtonElement, loading: boolean): void {
    btn.disabled = loading;
    if (loading) {
      btn.dataset.originalText = btn.textContent || "";
      btn.textContent = "Submitting...";
    } else {
      btn.textContent = btn.dataset.originalText || "Submit";
    }
  }

  private getTargetFields(formElem: HTMLElement): Record<string, string> {
    const contentType = formElem.querySelector<HTMLInputElement>("input[name='content_type']")?.value || "";
    const objectPk = formElem.querySelector<HTMLInputElement>("input[name='object_pk']")?.value || "";
    return { content_type: contentType, object_pk: objectPk };
  }

  private fetchForm(url: string): Promise<string> {
    return fetch(url, { method: "GET" })
      .then((response) => {
        if (!response.ok) {
          throw new Error(ERROR_MESSAGES.server);
        }
        return response.text();
      });
  }

  private parseHtml(html: string): HTMLElement {
    const parser = new DOMParser();
    return parser.parseFromString(html, "text/html").body.firstElementChild as HTMLElement;
  }

  private getInsertBeforeElement(refElem: HTMLElement): HTMLElement | null {
    let current = refElem;
    while (current.nextElementSibling?.classList.contains("pl-12") ||
           current.nextElementSibling?.classList.contains("md:pl-14")) {
      current = current.nextElementSibling as HTMLElement;
    }
    return current.nextElementSibling as HTMLElement;
  }

  private scrollToHash(hash: string, behavior: ScrollBehavior = "smooth"): boolean {
    const id = hash.startsWith("#") ? hash.slice(1) : hash;
    const target = document.getElementById(id);
    if (!target) return false;

    const navElem = document.getElementById("site-nav");
    const navHeight = navElem ? navElem.getBoundingClientRect().height : 0;
    const offset = navHeight + 12;
    const viewportHeight = window.innerHeight;
    const rect = target.getBoundingClientRect();

    const elementTop = rect.top - offset;
    const elementBottom = rect.bottom;
    if (elementTop >= 0 && elementBottom <= viewportHeight) {
      return true;
    }

    const currentScrollTop = window.pageYOffset;
    const scrollTarget =
      elementTop < 0
        ? rect.top + currentScrollTop - offset
        : rect.bottom + currentScrollTop - viewportHeight;
    window.scrollTo({ top: Math.max(0, scrollTarget), behavior });
    return true;
  }

  private showError(message: string): void {
    new Toast(message, { type: "error" });
  }
}

export default Comment;

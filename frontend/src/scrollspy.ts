const NAME = "scrollspy";

type Target = {
  parent: Target | null;
  element: HTMLElement;
  offset: number;
};

type Config = {
  activeClassName?: string;
};

class Scrollspy {
  private targets: Target[] = [];

  private scrollElement;

  private activeTarget: null | Target = null;

  private config: Config = {};

  constructor(
    elements: HTMLElement[],
    scrollElement: HTMLElement = document.body,
    config: Config = {}
  ) {
    this.scrollElement =
      scrollElement.tagName === "BODY" ? window : scrollElement;
    this.scrollElement.addEventListener("scroll", () => {
      this.process();
    });
    Object.assign(this.config, config);

    this.refresh(elements);
    this.process();
  }

  static get NAME() {
    return NAME;
  }

  refresh(elements: HTMLElement[]) {
    const offsetBase = this.scrollElement === window ? 0 : this.getScrollTop();
    const targetStack: (Target | null)[] = [];
    let currTarget: Target | null;

    const getTarget = (elem: HTMLElement): Target | null => {
      const selector = Scrollspy.getSelector(elem);
      const trigger = selector
        ? Scrollspy.find(
            selector,
            (this.scrollElement === window
              ? document.body
              : this.scrollElement) as HTMLElement
          )
        : null;
      if (!trigger) return null;
      const triggerBCR = trigger.getBoundingClientRect();
      return triggerBCR.width || triggerBCR.height
        ? {
            parent: targetStack[targetStack.length - 1],
            element: elem,
            offset:
              this.scrollElement === window
                ? triggerBCR.top + window.pageYOffset + offsetBase
                : (trigger as HTMLElement).offsetTop + offsetBase,
          }
        : null;
    };

    const parse = (elems: HTMLElement[]) => {
      if (elems.length === 0 || Array.isArray(elements[0])) {
        throw new Error("Invalid tree structure");
      }

      const target = getTarget(elems[0]);
      if (target !== null) {
        this.targets.push(target);
      }
      currTarget = target;
      for (let i = 1; i < elems.length; i += 1) {
        const ele = elems[i];
        if (Array.isArray(ele)) {
          targetStack.push(currTarget);
          parse(ele);
        } else {
          const t = getTarget(ele);
          if (t !== null) {
            this.targets.push(t);
          }
          currTarget = t;
        }
      }
      targetStack.pop();
    };

    parse(elements);
    this.targets = this.targets.sort((a, b) => a.offset - b.offset);
  }

  private getScrollTop() {
    return this.scrollElement === window
      ? this.scrollElement.pageYOffset
      : (this.scrollElement as HTMLElement).scrollTop;
  }

  private getScrollHeight() {
    return (
      (this.scrollElement as HTMLElement).scrollHeight ||
      Math.max(
        document.body.scrollHeight,
        document.documentElement.scrollHeight
      )
    );
  }

  private getOffsetHeight() {
    return this.scrollElement === window
      ? window.innerHeight
      : (this.scrollElement as HTMLElement).getBoundingClientRect().height;
  }

  private process() {
    const scrollTop = this.getScrollTop();
    const scrollHeight = this.getScrollHeight();
    const maxScroll = scrollHeight - this.getOffsetHeight();

    if (scrollTop >= maxScroll) {
      const target = this.targets[this.targets.length - 1];

      if (this.activeTarget !== target) {
        this.activate(target);
      }
      return;
    }

    if (
      this.activeTarget &&
      scrollTop < this.targets[0].offset &&
      this.targets[0].offset > 0
    ) {
      this.activeTarget = null;
      this.clear();
      return;
    }

    for (let i = 0; i < this.targets.length; i += 1) {
      const isActiveTarget =
        this.activeTarget !== this.targets[i] &&
        scrollTop >= this.targets[i].offset &&
        (typeof this.targets[i + 1] === "undefined" ||
          scrollTop < this.targets[i + 1].offset);

      if (isActiveTarget) {
        this.activate(this.targets[i]);
      }
    }
  }

  private activate(target: Target) {
    this.activeTarget = target;
    this.clear();

    if (this.config.activeClassName) {
      const tokens = this.config.activeClassName.split(" ");
      this.activeTarget.element.classList.add(...tokens);
      let { parent } = target;
      while (parent) {
        parent.element.classList.add(...tokens);
        parent = parent.parent;
      }
    }
  }

  private clear() {
    if (this.config.activeClassName) {
      const tokens = this.config.activeClassName.split(" ");
      this.targets.forEach((target) =>
        target.element.classList.remove(...tokens)
      );
    }
  }

  private static getSelector(ele: HTMLElement): null | string {
    let selector = null;
    let hrefAttr = ele.getAttribute("href");
    if (!hrefAttr || (!hrefAttr.includes("#") && !hrefAttr.startsWith("."))) {
      return null;
    }

    if (hrefAttr.includes("#") && !hrefAttr.startsWith("#")) {
      hrefAttr = `#${hrefAttr.split("#")[1]}`;
    }

    selector = hrefAttr && hrefAttr !== "#" ? hrefAttr.trim() : null;
    return selector;
  }

  private static find(selector: string, element: HTMLElement = document.body) {
    return Element.prototype.querySelector.call(element, selector);
  }
}

export default Scrollspy;

const NAME = "backdrop";

type Config = {
  className?: string;
  clickCallback: null | undefined | (() => void);
};

class Backdrop {
  private elem: null | HTMLElement = null;

  private isAppended = false;

  private config;

  constructor(config: Config) {
    this.config = config;
  }

  static get NAME() {
    return NAME;
  }

  show() {
    this.append();
  }

  hide() {
    this.dispose();
  }

  dispose() {
    if (!this.isAppended) {
      return;
    }
    this.elem!.removeEventListener("click", this.handleClick, true);
    this.elem!.remove();
    this.isAppended = false;
  }

  private append() {
    if (this.isAppended) {
      return;
    }

    const elem = this.getElement();
    document.body.append(elem);
    elem.addEventListener("click", this.handleClick.bind(this), true);

    this.isAppended = true;
  }

  private getElement() {
    if (!this.elem) {
      const backdrop = document.createElement("div");
      if (this.config.className) {
        backdrop.className = this.config.className;
      }
      this.elem = backdrop;
    }

    return this.elem;
  }

  private handleClick() {
    if (this.config.clickCallback) {
      this.config.clickCallback();
    }
  }
}

export default Backdrop;

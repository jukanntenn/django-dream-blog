import Backdrop from "./util/backdrop";

const NAME = "offcanvas";

type Config = {
  backdrop: boolean;
  backdropClassName?: string;
};

const defaultConfig: Config = {
  backdrop: true,
};

class Offcanvas {
  private readonly elem;

  private config;

  private backdrop?: Backdrop;

  private readonly oriTransformVal;

  private isShown = false;

  constructor(element: HTMLElement, config?: Config) {
    this.elem = element;
    this.config = Object.assign(config || {}, defaultConfig);
    this.oriTransformVal = this.elem.style.transform;
    this.backdrop = this.initializeBackDrop();
  }

  static get NAME() {
    return NAME;
  }

  toggle() {
    return this.isShown ? this.hide() : this.show();
  }

  show() {
    this.elem.style.transform = "none";
    this.isShown = true;
    this.backdrop?.show();
  }

  hide() {
    if (!this.isShown) {
      return;
    }

    this.elem.style.transform = this.oriTransformVal;
    this.isShown = false;
    this.backdrop?.hide();
  }

  private initializeBackDrop(): undefined | Backdrop {
    if (!this.config.backdrop) return undefined;

    const clickCallback = () => {
      this.hide();
    };
    return new Backdrop({
      className: this.config.backdropClassName,
      clickCallback,
    });
  }
}

export default Offcanvas;

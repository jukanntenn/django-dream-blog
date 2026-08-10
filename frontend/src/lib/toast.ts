const NAME = "toast";

type ToastType = "success" | "error" | "info";

type Config = {
  type?: ToastType;
  duration?: number;
};

const defaultConfig: Config = {
  type: "info",
  duration: 3000,
};

class Toast {
  private elem: HTMLElement | null = null;

  private config: Config;

  private timer: number | null = null;

  constructor(message: string, config?: Config) {
    this.config = { ...defaultConfig, ...config };
    this.show(message);
  }

  static get NAME() {
    return NAME;
  }

  show(message: string): void {
    this.elem = this.createElement(message);
    document.body.appendChild(this.elem);

    // Auto-hide after duration
    this.timer = window.setTimeout(() => {
      this.hide();
    }, this.config.duration);
  }

  hide(): void {
    if (this.elem) {
      this.elem.classList.add("toast--fade-out");
      setTimeout(() => {
        this.dispose();
      }, 200);
    }
  }

  dispose(): void {
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
    if (this.elem && this.elem.parentNode) {
      this.elem.parentNode.removeChild(this.elem);
      this.elem = null;
    }
  }

  private createElement(message: string): HTMLElement {
    const toast = document.createElement("div");
    toast.className = `toast toast--${this.config.type}`;
    toast.textContent = message;
    return toast;
  }
}

export default Toast;

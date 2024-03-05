class Backtop {
  private _element: HTMLElement;
  constructor(element: HTMLElement) {
    this._element = element;
    this._init();
  }

  _init(): void {
    window.addEventListener("scroll", this.toggle.bind(this));
    this._element?.addEventListener("click", this.to.bind(this));
  }

  to(): void {
    if (document.documentElement.scrollTop > 0) {
      document.documentElement.scrollTo({ top: 0, behavior: "smooth" });
    }
  }

  toggle(): void {
    const pos = window.innerHeight / 3;

    if (document.documentElement.scrollTop > pos) {
      this._element?.classList.remove("opacity-0");
      this._element?.classList.add("opacity-100");
    } else {
      this._element?.classList.remove("opacity-100");
      this._element?.classList.add("opacity-0");
    }
  }
}

export default Backtop;

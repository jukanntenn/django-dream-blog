const STORAGE_KEY = "theme";

type ThemeMode = "light" | "dark" | "system";

type ThemeConfig = {
  button: HTMLElement;
  icons: {
    light: HTMLImageElement;
    dark: HTMLImageElement;
    system: HTMLImageElement;
  };
};

class ThemeSwitcher {
  private currentMode: ThemeMode = "system";
  private button: HTMLElement;
  private icons: ThemeConfig["icons"];
  private systemPreference: MediaQueryList;

  constructor(element: HTMLElement) {
    this.button = element;
    this.systemPreference = window.matchMedia("(prefers-color-scheme: dark)");

    // 查找图标元素
    this.icons = {
      light: element.querySelector('[data-theme-icon="light"]') as HTMLImageElement,
      dark: element.querySelector('[data-theme-icon="dark"]') as HTMLImageElement,
      system: element.querySelector('[data-theme-icon="system"]') as HTMLImageElement,
    };

    this.currentMode = this.getStoredTheme();
    this._init();
  }

  static get NAME() {
    return "themeSwitcher";
  }

  private _init(): void {
    // 初始化主题
    this.applyTheme(this.currentMode);

    // 绑定点击事件
    this.button.addEventListener("click", () => this.toggle());

    // 监听系统主题变化
    this.systemPreference.addEventListener("change", () => {
      if (this.currentMode === "system") {
        this.applyTheme("system");
      }
    });
  }

  private getStoredTheme(): ThemeMode {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored === "light" || stored === "dark" || stored === "system") {
      return stored;
    }
    return "system"; // 默认跟随系统
  }

  private applyTheme(mode: ThemeMode): void {
    this.currentMode = mode;
    localStorage.setItem(STORAGE_KEY, mode);
    this.updateIcon();
    this.updateDocumentTheme();
  }

  private updateDocumentTheme(): void {
    const htmlElement = document.documentElement;
    const systemDark = this.systemPreference.matches;

    const nextThemeClass =
      this.currentMode === "system"
        ? systemDark
          ? "dark"
          : "light"
        : this.currentMode;

    const prevThemeClass = nextThemeClass === "dark" ? "light" : "dark";

    htmlElement.classList.add("theme-switching");
    htmlElement.classList.add(nextThemeClass);
    htmlElement.classList.remove(prevThemeClass);

    requestAnimationFrame(() => {
      htmlElement.classList.remove("theme-switching");
    });
  }

  private updateIcon(): void {
    // 隐藏所有图标
    Object.values(this.icons).forEach((icon) => {
      if (icon) icon.classList.add("hidden");
    });

    // 显示当前模式对应的图标
    let activeIcon: HTMLImageElement | null = null;

    if (this.currentMode === "light") {
      activeIcon = this.icons.light;
    } else if (this.currentMode === "dark") {
      activeIcon = this.icons.dark;
    } else {
      activeIcon = this.icons.system;
    }

    if (activeIcon) {
      activeIcon.classList.remove("hidden");
    }
  }

  public toggle(): void {
    // 循环切换：light -> dark -> system -> light
    const modeSequence: ThemeMode[] = ["light", "dark", "system"];
    const currentIndex = modeSequence.indexOf(this.currentMode);
    const nextIndex = (currentIndex + 1) % modeSequence.length;
    this.applyTheme(modeSequence[nextIndex]);
  }
}

export default ThemeSwitcher;

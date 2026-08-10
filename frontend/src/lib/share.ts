import { toCanvas } from "qrcode";

import Toast from "./toast";

type Platform = "wechat" | "xiaohongshu" | "weibo";

type ShareData = {
  platform: Platform;
  title: string;
  excerpt: string;
  url: string;
};

function show(elem: HTMLElement): void {
  elem.classList.remove("hidden");
  document.body.style.overflow = "hidden";
}

function hide(elem: HTMLElement): void {
  elem.classList.add("hidden");
  document.body.style.overflow = "";
}

async function copyToClipboard(text: string): Promise<boolean> {
  if (navigator.clipboard?.writeText) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {
      return false;
    }
  }

  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.style.position = "fixed";
  textarea.style.opacity = "0";
  document.body.appendChild(textarea);
  textarea.select();
  const ok = document.execCommand("copy");
  document.body.removeChild(textarea);
  return ok;
}

export function initShare(): void {
  const shareModalEl = document.getElementById("share-modal");
  const qrcodeModalEl = document.getElementById("qrcode-modal");
  const textareaEl = document.getElementById("share-text") as HTMLTextAreaElement | null;
  const platformNameEl = document.getElementById("share-platform-name");
  const qrcodeContainerEl = document.getElementById("qrcode-container");

  if (
    !shareModalEl ||
    !qrcodeModalEl ||
    !textareaEl ||
    !platformNameEl ||
    !qrcodeContainerEl
  ) {
    return;
  }

  const shareModal = shareModalEl;
  const qrcodeModal = qrcodeModalEl;
  const textarea = textareaEl;
  const platformName = platformNameEl;
  const qrcodeContainer = qrcodeContainerEl;

  let current: ShareData | null = null;

  const platformNames: Record<Platform, string> = {
    wechat: "微信",
    xiaohongshu: "小红书",
    weibo: "新浪微博",
  };

  function closeAll(): void {
    hide(shareModal);
    hide(qrcodeModal);
    current = null;
  }

  function closeShareModal(): void {
    hide(shareModal);
  }

  function closeQRCodeModal(): void {
    hide(qrcodeModal);
  }

  function openShareModal(data: ShareData): void {
    current = data;
    textarea.value = `${data.title}\n\n${data.excerpt}\n\n${data.url}`;
    platformName.textContent = `分享到${platformNames[data.platform]}`;
    show(shareModal);
    textarea.focus();
  }

  async function openQRCodeModal(url: string): Promise<void> {
    qrcodeContainer.innerHTML = "";
    const canvas = document.createElement("canvas");
    try {
      await toCanvas(canvas, url, { width: 200, margin: 2 });
      qrcodeContainer.appendChild(canvas);
      show(qrcodeModal);
    } catch {
      new Toast("二维码生成失败", { type: "error" });
    }
  }

  async function handleConfirm(): Promise<void> {
    if (!current) return;
    const text = textarea.value.trim();

    if (current.platform === "weibo") {
      const shareUrl = `https://service.weibo.com/share/share.php?url=${encodeURIComponent(current.url)}&title=${encodeURIComponent(text)}&summary=${encodeURIComponent(current.excerpt)}`;
      window.open(shareUrl, "_blank", "width=600,height=500");
      closeShareModal();
      return;
    }

    if (current.platform === "xiaohongshu") {
      const ok = await copyToClipboard(`${text}\n\n${current.url}`);
      new Toast(ok ? "已复制到剪贴板，请打开小红书粘贴分享" : "复制失败，请手动复制", {
        type: ok ? "success" : "error",
      });
      window.open(
        `https://www.xiaohongshu.com/discovery/item/${encodeURIComponent(current.url)}`,
        "_blank"
      );
      closeShareModal();
    }
  }

  document.addEventListener("click", (e) => {
    const target = e.target as HTMLElement;

    const icon = target.closest?.(".share-icon") as HTMLElement | null;
    if (icon) {
      const platform = icon.dataset.platform as Platform | undefined;
      const title = icon.dataset.title || "";
      const excerpt = icon.dataset.excerpt || "";
      const url = icon.dataset.url || "";

      if (!platform || !url) return;

      if (platform === "wechat") {
        void openQRCodeModal(url);
      } else {
        openShareModal({ platform, title, excerpt, url });
      }
      return;
    }

    if (target.closest?.("[data-share-close]")) {
      closeShareModal();
      return;
    }

    if (target.closest?.("[data-qrcode-close]")) {
      closeQRCodeModal();
      return;
    }

    if (target.closest?.(".share-modal__close") || target.closest?.(".share-modal__cancel")) {
      closeShareModal();
      return;
    }

    if (target.closest?.(".qrcode-modal__close")) {
      closeQRCodeModal();
      return;
    }

    if (target.closest?.(".share-modal__confirm")) {
      void handleConfirm();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeAll();
    }
  });
}

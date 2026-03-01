# Social Media Share Feature Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add social media share buttons (WeChat, Xiaohongshu, Weibo) to blog posts with customizable text

**Architecture:** Django app `share` with template tags for rendering icons + vanilla TypeScript for modal and QR code generation

**Tech Stack:** Django 5, Tailwind CSS 4, TypeScript, qrcode.js (npm)

---

## Task 1: Create Django Share App Structure

**Files:**
- Create: `dream_blog/share/__init__.py`
- Create: `dream_blog/share/apps.py`

**Step 1: Create app package**

```bash
mkdir -p dream_blog/share
```

**Step 2: Create __init__.py**

Create `dream_blog/share/__init__.py`:

```python
"""Social media share functionality for blog content."""
```

**Step 3: Create apps.py**

Create `dream_blog/share/apps.py`:

```python
from django.apps import AppConfig


class ShareConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dream_blog.share"
    verbose_name = "Social Share"
```

**Step 4: Add to INSTALLED_APPS**

Modify `config/settings/base.py` around line 50-70 (find INSTALLED_APPS section):

```python
INSTALLED_APPS = [
    # ... existing apps ...
    "dream_blog.share",  # Add this line
]
```

**Step 5: Commit**

```bash
git add dream_blog/share/ config/settings/base.py
git commit -m "feat: create share app with basic structure"
```

---

## Task 2: Create Share Templates and Template Tags

**Files:**
- Create: `dream_blog/share/templates/share/_share_icons.html`
- Create: `dream_blog/share/templates/share/_share_modal.html`
- Create: `dream_blog/share/templatetags/__init__.py`
- Create: `dream_blog/share/templatetags/share_tags.py`

**Step 1: Create template directories**

```bash
mkdir -p dream_blog/share/templates/share
mkdir -p dream_blog/share/templatetags
```

**Step 2: Create share icons template**

Create `dream_blog/share/templates/share/_share_icons.html`:

```django
{# Social media share icons #}
{% load share_tags %}

<div class="share-icons flex items-center gap-2 mt-2">
  <span class="text-xs text-slate-500 dark:text-slate-400">分享：</span>
  <button
    type="button"
    class="share-icon share-icon--wechat text-green-600 dark:text-green-400 hover:text-green-700 dark:hover:text-green-300 transition-colors"
    data-platform="wechat"
    data-title="{{ entry.title|escape }}"
    data-excerpt="{{ entry.excerpt|default:entry.title|escape }}"
    data-url="{{ request.build_absolute_uri }}"
    aria-label="Share to WeChat"
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
      <path d="M8.5 4c-4.418 0-8 3.134-8 7s3.582 7 8 7c.97 0 1.9-.153 2.75-.437L14 19l-1.25-2.875C14.96 15.173 16.5 13.258 16.5 11c0-3.866-3.582-7-8-7zm7.5 8c-3.866 0-7 2.686-7 6s3.134 6 7 6c.78 0 1.53-.11 2.22-.313L20 23l-1-2.28C20.553 19.61 21.5 18.38 21.5 17c0-3.314-3.134-6-7-6z"/>
    </svg>
  </button>
  <button
    type="button"
    class="share-icon share-icon--xiaohongshu text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 transition-colors"
    data-platform="xiaohongshu"
    data-title="{{ entry.title|escape }}"
    data-excerpt="{{ entry.excerpt|default:entry.title|escape }}"
    data-url="{{ request.build_absolute_uri }}"
    aria-label="Share to Xiaohongshu"
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
    </svg>
  </button>
  <button
    type="button"
    class="share-icon share-icon--weibo text-yellow-600 dark:text-yellow-400 hover:text-yellow-700 dark:hover:text-yellow-300 transition-colors"
    data-platform="weibo"
    data-title="{{ entry.title|escape }}"
    data-excerpt="{{ entry.excerpt|default:entry.title|escape }}"
    data-url="{{ request.build_absolute_uri }}"
    aria-label="Share to Weibo"
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4 11h-3v3h-2v-3H8v-2h3V8h2v3h3v2z"/>
    </svg>
  </button>
</div>
```

**Step 3: Create share modal template**

Create `dream_blog/share/templates/share/_share_modal.html`:

```django
{# Share modal dialog #}
<div id="share-modal" class="share-modal hidden" role="dialog" aria-modal="true" aria-labelledby="share-modal-title">
  <div class="share-modal__backdrop"></div>
  <div class="share-modal__content">
    <div class="share-modal__header">
      <h3 id="share-modal-title" class="text-lg font-semibold">分享到社交媒体</h3>
      <button type="button" class="share-modal__close" aria-label="Close">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>
    <div class="share-modal__body">
      <label for="share-text" class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">分享内容：</label>
      <textarea
        id="share-text"
        class="share-modal__textarea w-full px-3 py-2 border border-slate-300 dark:border-slate-600 rounded-md bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
        rows="4"
      ></textarea>
      <p id="share-platform-name" class="mt-2 text-sm text-slate-500 dark:text-slate-400"></p>
    </div>
    <div class="share-modal__footer flex justify-end gap-2">
      <button type="button" class="share-modal__cancel px-4 py-2 text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-md transition-colors">取消</button>
      <button type="button" class="share-modal__confirm px-4 py-2 text-sm bg-cyan-600 hover:bg-cyan-700 text-white rounded-md transition-colors">确认分享</button>
    </div>
  </div>
</div>

{# QR Code modal for WeChat #}
<div id="qrcode-modal" class="qrcode-modal hidden" role="dialog" aria-modal="true" aria-labelledby="qrcode-modal-title">
  <div class="qrcode-modal__backdrop"></div>
  <div class="qrcode-modal__content">
    <div class="qrcode-modal__header">
      <h3 id="qrcode-modal-title" class="text-lg font-semibold">扫码分享到微信</h3>
      <button type="button" class="qrcode-modal__close" aria-label="Close">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>
    <div class="qrcode-modal__body">
      <div id="qrcode-container" class="flex justify-center"></div>
      <p class="mt-4 text-sm text-slate-500 dark:text-slate-400 text-center">使用微信扫描二维码分享</p>
    </div>
  </div>
</div>
```

**Step 4: Create templatetags __init__.py**

Create `dream_blog/share/templatetags/__init__.py`:

```python
"""Template tags for share functionality."""
```

**Step 5: Create share_tags.py**

Create `dream_blog/share/templatetags/share_tags.py`:

```python
from django import template

register = template.Library()
```

**Step 6: Commit**

```bash
git add dream_blog/share/templates/ dream_blog/share/templatetags/
git commit -m "feat: add share templates and template tags"
```

---

## Task 3: Integrate Share Icons into Entry Meta Template

**Files:**
- Modify: `dream_blog/templates/inclusions/_entry_meta.html`

**Step 1: Add share icons to entry meta**

Replace the entire content of `dream_blog/templates/inclusions/_entry_meta.html` with:

```django
{# Entry meta info: date, views, comments, share with slate color scheme #}
<div class="text-slate-500 dark:text-slate-400 text-sm mt-3">
  <span class="after:content-['•'] after:mx-1 text-slate-700 dark:text-slate-400">{{ entry.publish_date | date:"Y-m-d" }}</span><span class="after:content-['•'] after:mx-1 text-slate-700 dark:text-slate-400">{{ entry.hit_count.hits }} 阅读</span><a href="{{ entry.get_absolute_url }}#comment-area" class="text-slate-700 dark:text-slate-400 hover:text-cyan-600 dark:hover:text-cyan-400">{{ entry.num_comments }} 评论</a>
  {% include "share/_share_icons.html" with entry=entry %}
</div>
```

**Step 2: Add modal templates to base template**

Modify `dream_blog/templates/base.html` - add before the closing `</body>` tag (around line 50-60, find where body ends):

```django
{% include "share/_share_modal.html %}
```

**Step 3: Commit**

```bash
git add dream_blog/templates/inclusions/_entry_meta.html dream_blog/templates/base.html
git commit -m "feat: integrate share icons into entry meta"
```

---

## Task 4: Install qrcode.js Dependency

**Files:**
- Modify: `frontend/package.json`

**Step 1: Add qrcode dependency**

Run in frontend directory:

```bash
cd frontend && pnpm add qrcode && cd ..
```

**Step 2: Verify installation**

Check `frontend/package.json` contains qrcode in dependencies.

**Step 3: Commit**

```bash
git add frontend/package.json frontend/pnpm-lock.yaml
git commit -m "chore: add qrcode.js dependency"
```

---

## Task 5: Create TypeScript Share Module

**Files:**
- Create: `frontend/src/share.ts`

**Step 1: Create share.ts module**

Create `frontend/src/share.ts`:

```typescript
/**
 * Social Media Share Module
 * Handles share modal, QR code generation, and platform-specific sharing
 */

import QRCode from 'qrcode';

const MODAL_ID = 'share-modal';
const QRCODE_MODAL_ID = 'qrcode-modal';

type Platform = 'wechat' | 'xiaohongshu' | 'weibo';

interface ShareData {
  title: string;
  excerpt: string;
  url: string;
}

class ShareModal {
  private elem: HTMLElement | null = null;
  private qrcodeModal: HTMLElement | null = null;
  private textarea: HTMLTextAreaElement | null = null;
  private currentPlatform: Platform | null = null;
  private currentData: ShareData | null = null;

  init(): void {
    this.elem = document.getElementById(MODAL_ID);
    this.qrcodeModal = document.getElementById(QRCODE_MODAL_ID);
    this.textarea = document.getElementById('share-text') as HTMLTextAreaElement;

    if (!this.elem || !this.qrcodeModal || !this.textarea) {
      console.warn('Share modal elements not found');
      return;
    }

    this.attachEventListeners();
  }

  private attachEventListeners(): void {
    // Share icon buttons
    document.querySelectorAll<HTMLElement>('.share-icon').forEach((icon) => {
      icon.addEventListener('click', (e) => this.handleShareIconClick(e));
    });

    // Modal close buttons
    const closeButtons = this.elem.querySelectorAll('.share-modal__close, .share-modal__cancel');
    closeButtons.forEach((btn) => {
      btn.addEventListener('click', () => this.closeModal());
    });

    // QR code modal close button
    const qrCloseButton = this.qrcodeModal.querySelector('.qrcode-modal__close');
    qrCloseButton?.addEventListener('click', () => this.closeQRCodeModal());

    // Backdrop clicks
    const backdrop = this.elem.querySelector('.share-modal__backdrop');
    backdrop?.addEventListener('click', () => this.closeModal());

    const qrBackdrop = this.qrcodeModal.querySelector('.qrcode-modal__backdrop');
    qrBackdrop?.addEventListener('click', () => this.closeQRCodeModal());

    // Confirm share button
    const confirmButton = this.elem.querySelector('.share-modal__confirm');
    confirmButton?.addEventListener('click', () => this.handleConfirm());

    // ESC key to close
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.closeModal();
        this.closeQRCodeModal();
      }
    });
  }

  private handleShareIconClick(event: Event): void {
    const target = event.currentTarget as HTMLElement;
    const platform = target.dataset.platform as Platform;
    const title = target.dataset.title || '';
    const excerpt = target.dataset.excerpt || '';
    const url = target.dataset.url || '';

    this.currentPlatform = platform;
    this.currentData = { title, excerpt, url };

    if (platform === 'wechat') {
      this.showQRCodeModal(url);
    } else {
      this.showModal(platform, title, excerpt);
    }
  }

  private showModal(platform: Platform, title: string, excerpt: string): void {
    if (!this.textarea || !this.elem) return;

    // Pre-fill textarea
    const text = `${title}\n\n${excerpt}\n\n`;
    this.textarea.value = text;

    // Update platform name display
    const platformNames: Record<Platform, string> = {
      xiaohongshu: '小红书',
      weibo: '新浪微博',
      wechat: '微信',
    };
    const platformNameEl = this.elem.querySelector('#share-platform-name');
    if (platformNameEl) {
      platformNameEl.textContent = `分享到${platformNames[platform]}`;
    }

    // Show modal
    this.elem.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }

  private closeModal(): void {
    if (!this.elem) return;
    this.elem.classList.add('hidden');
    document.body.style.overflow = '';
  }

  private async showQRCodeModal(url: string): Promise<void> {
    if (!this.qrcodeModal) return;

    const container = this.qrcodeModal.querySelector('#qrcode-container');
    if (!container) return;

    // Clear previous QR code
    container.innerHTML = '';

    // Generate QR code
    try {
      const canvas = document.createElement('canvas');
      await QRCode.toCanvas(canvas, url, {
        width: 200,
        margin: 2,
      });
      container.appendChild(canvas);
    } catch (error) {
      console.error('Failed to generate QR code:', error);
      return;
    }

    // Show modal
    this.qrcodeModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }

  private closeQRCodeModal(): void {
    if (!this.qrcodeModal) return;
    this.qrcodeModal.classList.add('hidden');
    document.body.style.overflow = '';
  }

  private handleConfirm(): void {
    if (!this.currentPlatform || !this.currentData) return;

    const shareText = this.textarea?.value || '';
    const { title, url } = this.currentData;

    if (this.currentPlatform === 'xiaohongshu') {
      // Xiaohongshu doesn't have a direct share URL, copy to clipboard
      this.copyToClipboard(shareText + url);
      alert('已复制到剪贴板，请打开小红书粘贴分享');
    } else if (this.currentPlatform === 'weibo') {
      // Weibo share URL
      const weiboUrl = `https://service.weibo.com/share/share.php?url=${encodeURIComponent(url)}&title=${encodeURIComponent(title)}&summary=${encodeURIComponent(shareText)}`;
      window.open(weiboUrl, '_blank', 'width=600,height=500');
    }

    this.closeModal();
  }

  private copyToClipboard(text: string): void {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
  }
}

export function initShare(): void {
  const shareModal = new ShareModal();
  shareModal.init();
}

export default ShareModal;
```

**Step 2: Commit**

```bash
git add frontend/src/share.ts
git commit -m "feat: create share modal TypeScript module"
```

---

## Task 6: Initialize Share Module in Index.js

**Files:**
- Modify: `frontend/src/index.js`

**Step 1: Import and initialize share module**

Modify `frontend/src/index.js`:

Add import at the top:
```javascript
import { initShare } from "./share";
```

Add initialization call in the onReady block (around line 170-175):

```javascript
// Initialize UX features
onReady(function () {
  initLightbox();
  initCodeCopy();
  initShare();  // Add this line
});
```

**Step 2: Commit**

```bash
git add frontend/src/index.js
git commit -m "feat: initialize share module on DOM ready"
```

---

## Task 7: Add Share Modal CSS Styles

**Files:**
- Create: `frontend/src/share.css`

**Step 1: Create share.css styles**

Create `frontend/src/share.css`:

```css
/* Share Modal Styles */
.share-modal,
.qrcode-modal {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.share-modal.hidden,
.qrcode-modal.hidden {
  display: none;
}

.share-modal__backdrop,
.qrcode-modal__backdrop {
  position: absolute;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
}

.share-modal__content,
.qrcode-modal__content {
  position: relative;
  background-color: white;
  dark:dark:bg-slate-800;
  border-radius: 0.5rem;
  padding: 1.5rem;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.share-modal__header,
.qrcode-modal__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.share-modal__close,
.qrcode-modal__close {
  background: none;
  border: none;
  cursor: pointer;
  color: #64748b;
  dark:dark:text-slate-400;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.25rem;
  border-radius: 0.25rem;
  transition: background-color 0.2s;
}

.share-modal__close:hover,
.qrcode-modal__close:hover {
  background-color: #f1f5f9;
  dark:dark:hover:bg-slate-700;
}

.share-modal__textarea {
  font-family: inherit;
  resize: vertical;
}

.qrcode-modal__content canvas {
  border-radius: 0.5rem;
}

/* Share Icons */
.share-icons {
  display: inline-flex;
  vertical-align: middle;
}

.share-icon {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.25rem;
  transition: background-color 0.2s;
}

.share-icon:hover {
  background-color: #f1f5f9;
  dark:dark:hover:bg-slate-700;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .share-modal__content,
  .qrcode-modal__content {
    background-color: #1e293b;
  }

  .share-modal__textarea {
    background-color: #1e293b;
    color: #f1f5f9;
    border-color: #475569;
  }
}
```

**Step 2: Import CSS in main.ts**

Modify `frontend/src/main.ts` - add import after other CSS imports:

```typescript
import "./share.css";
```

**Step 3: Commit**

```bash
git add frontend/src/share.css frontend/src/main.ts
git commit -m "feat: add share modal CSS styles"
```

---

## Task 8: Build Frontend and Test

**Files:** (build output only)

**Step 1: Build frontend**

```bash
cd frontend && pnpm build
```

**Step 2: Verify no TypeScript errors**

Expected: No errors in build output.

**Step 3: Run Django server**

```bash
uv run python manage.py runserver
```

**Step 4: Manual test checklist**

1. Navigate to a blog post detail page
2. Verify share icons appear in entry metadata
3. Click WeChat icon → QR code modal appears
4. Click Xiaohongshu icon → Share modal opens with pre-filled text
5. Click Weibo icon → Share modal opens with pre-filled text
6. Edit text in modal → Click confirm → Verify behavior
7. Test close buttons and backdrop clicks
8. Test ESC key closes modals
9. Test on mobile viewport (responsive)

**Step 5: Commit build artifacts**

```bash
git add frontend/dist/
git commit -m "chore: update frontend build artifacts for share feature"
```

---

## Task 9: Add Frontend Type Definitions for qrcode

**Files:**
- Create: `frontend/src/qrcode.d.ts`

**Step 1: Create qrcode type definitions**

Create `frontend/src/qrcode.d.ts`:

```typescript
declare module 'qrcode' {
  export interface QRCodeToCanvasOptions {
    width?: number;
    margin?: number;
    errorCorrectionLevel?: 'L' | 'M' | 'Q' | 'H';
  }

  export function toCanvas(
    canvas: HTMLCanvasElement,
    text: string,
    options?: QRCodeToCanvasOptions
  ): Promise<void>;
}
```

**Step 2: Commit**

```bash
git add frontend/src/qrcode.d.ts
git commit -m "feat: add qrcode type definitions"
```

---

## Task 10: Final Testing and Documentation

**Files:**
- Create: `dream_blog/share/README.md` (optional)

**Step 1: Create share app documentation**

Create `dream_blog/share/README.md`:

```markdown
# Social Share App

Provides social media sharing functionality for blog content.

## Supported Platforms

- WeChat (via QR code)
- Xiaohongshu (clipboard copy)
- Weibo (direct share URL)

## Usage

In templates, include the share icons:

```django
{% include "share/_share_icons.html" with entry=post %}
```

The icons will automatically use the entry's title, excerpt, and URL.

## Requirements

- qrcode.js npm package
- Share modal templates included in base template
```

**Step 2: Run full test suite**

```bash
pytest
```

Expected: All existing tests pass.

**Step 3: Final commit**

```bash
git add dream_blog/share/README.md
git commit -m "docs: add share app documentation"
```

---

## Acceptance Criteria

- [ ] Share icons appear in article metadata
- [ ] Clicking WeChat icon shows QR code modal
- [ ] Clicking Xiaohongshu icon opens modal, copies text on confirm
- [ ] Clicking Weibo icon opens modal, opens share URL on confirm
- [ ] Modal pre-fills with title, excerpt, and URL placeholder
- [ ] User can edit text before sharing
- [ ] Share works on mobile and desktop
- [ ] No console errors
- [ ] ESC key closes modals
- [ ] Backdrop clicks close modals

## Files Modified/Created Summary

**Created:**
- `dream_blog/share/` - Django app
- `dream_blog/share/templates/share/_share_icons.html`
- `dream_blog/share/templates/share/_share_modal.html`
- `dream_blog/share/templatetags/share_tags.py`
- `frontend/src/share.ts`
- `frontend/src/share.css`
- `frontend/src/qrcode.d.ts`

**Modified:**
- `config/settings/base.py` - added 'dream_blog.share' to INSTALLED_APPS
- `dream_blog/templates/inclusions/_entry_meta.html` - added share icons
- `dream_blog/templates/base.html` - added share modal templates
- `frontend/src/index.js` - initialized share module
- `frontend/src/main.ts` - imported share.css
- `frontend/package.json` - added qrcode dependency

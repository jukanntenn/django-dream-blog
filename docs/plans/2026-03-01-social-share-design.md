# Social Media Share Feature Design

**Date:** 2026-03-01
**Status:** Approved

## Overview

A lightweight Django app (`share`) that adds social media sharing buttons to blog content. Users can share posts to WeChat, Xiaohongshu, and Weibo with customizable text.

## Goals

- Enable blog readers to share content to WeChat, Xiaohongshu, and Weibo
- Allow users to customize the share message before posting
- Provide a clean, non-intrusive UI that integrates with existing article metadata

## Architecture

### Django App Structure

```
dream_blog/share/
├── __init__.py
├── apps.py
├── templates/share/
│   ├── _share_icons.html      # Icon buttons displayed inline
│   └── _share_modal.html      # Modal for custom text input
└── templatetags/
    ├── __init__.py
    └── share_tags.py          # Template tag for easy inclusion
```

### Frontend Module

```
frontend/src/share.ts          # Share modal & QR code generation
```

## Components

### 1. Share Icons (Inline with Article Metadata)

Three icon buttons displayed in the `_entry_meta.html` inclusion template:

- **WeChat** (green icon)
- **Xiaohongshu** (red icon)
- **Weibo** (yellow icon)

Icons will use SVG or Heroicons for consistency with existing UI.

### 2. Share Modal

A modal dialog that opens when any share icon is clicked:

- **Pre-filled text format**: `{title}\n\n{excerpt}\n\n{url}`
- Editable textarea for user customization
- Two action buttons: "Cancel" and "Share" (确认分享)
- Platform-specific behavior based on clicked icon

### 3. Platform-Specific Behavior

| Platform | Action |
|----------|--------|
| **WeChat** | Show QR code modal containing the article URL |
| **Xiaohongshu** | Open `https://www.xiaohongshu.com/discovery/item/` with URL parameters |
| **Weibo** | Open `https://service.weibo.com/share/share.php` with title, url, and summary |

## Data Flow

```
User clicks share icon
    ↓
Share modal opens (ShareModal class)
    ↓
User edits text (optional) → Clicks "Share"
    ↓
Platform action:
    - WeChat: Generate QR code → Show in separate modal
    - Xiaohongshu/Weibo: window.open() with encoded share URL
```

## Technical Details

### QR Code Generation

- Use `qrcode.js` library (lightweight, ~15KB)
- Generate QR code client-side, no backend needed
- QR code encodes the article URL

### Share URL Construction

**Weibo:**
```
https://service.weibo.com/share/share.php?url={encoded_url}&title={encoded_title}&summary={encoded_excerpt}
```

**Xiaohongshu:**
```
https://www.xiaohongshu.com/discovery/item/{encoded_url}
```

### Modal State Management

- Vanilla TypeScript class following project's existing pattern
- Similar to `comment.ts`, `lightbox.ts` structure
- Uses `init()` method for initialization

### Responsive Design

- Icons display inline on desktop
- Icons stack or wrap on mobile
- Modal is responsive and touch-friendly

## Implementation Notes

1. **No Database Changes**: This feature requires no models or migrations
2. **No Tracking**: Share counts are not stored or displayed
3. **Fallback for Empty Excerpt**: Use post title if excerpt is empty
4. **URL Encoding**: All user-generated text must be properly encoded for share URLs

## Testing Strategy

1. **Manual Testing**: Verify each platform's share URL opens correctly
2. **Modal Behavior**: Test open/close, text editing, cancel/confirm
3. **QR Code**: Verify scannability and correct URL encoding
4. **Mobile**: Test responsive layout and touch interactions
5. **Edge Cases**: Empty excerpt, special characters, long titles

## Files to Modify

1. `dream_blog/share/` - New app (create all files)
2. `dream_blog/templates/inclusions/_entry_meta.html` - Add share icons
3. `frontend/src/share.ts` - New frontend module
4. `frontend/package.json` - Add qrcode.js dependency
5. `config/settings/base.py` - Add 'dream_blog.share' to INSTALLED_APPS

## Acceptance Criteria

- [ ] Share icons appear in article metadata
- [ ] Clicking WeChat icon shows QR code modal
- [ ] Clicking Xiaohongshu/Weibo icons opens share dialog
- [ ] Modal pre-fills with title, excerpt, and URL
- [ ] User can edit text before sharing
- [ ] Share works on mobile and desktop
- [ ] No console errors

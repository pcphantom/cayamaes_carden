# Cayamae's Ancient Garden — Website v1.0
## Site Structure

```
cayamaes_garden/
├── index.html          ← Main page (all content lives here)
├── css/
│   └── style.css       ← All styles & color variables
├── js/
│   └── main.js         ← Navigation, filter, scroll behavior
├── images/             ← Drop product photos here (see below)
└── README.md           ← This file
```

---

## Quick-Swap Guide

### Change Color Theme
All colors are CSS variables at the top of `css/style.css`:
```css
:root {
  --forest:   #1e3320;   /* main dark green */
  --gold:     #c8973a;   /* accent gold */
  --cream:    #f5f0e6;   /* light bg */
  /* ... etc */
}
```

### Update Contact Info
Search `index.html` for:
- `(916) 613-0046` → replace with new phone
- `pleasuresenses@yahoo.com` → replace with new email
- `Sacramento, CA 95877` → replace with address

### Set the Patreon URL
Search `index.html` for `PLACEHOLDER_PATREON` (appears 4 times) and replace with the actual Patreon username.

### Add Product Photos
1. Drop the image file into `images/` (e.g. `images/lavender-oil.jpg`)
2. In `index.html`, find the product's `<div class="product-image">` block
3. Replace the `<svg>...</svg>` inside it with:
   ```html
   <img src="images/lavender-oil.jpg" alt="Lavender Infused Oil" style="width:100%;height:100%;object-fit:cover;" />
   ```

### Add a New Product
Copy any existing `<article class="product-card" ...>` block and paste it inside `<div class="products-grid" id="productsGrid">`.

Update:
- `data-category` attribute: `infused-oils` | `lotions` | `soaps` | `body` | `spiritual`
- `aria-label` on the article
- Product category, name, description, price text
- Replace the SVG art or add an `<img>` tag

### Update Testimonials
Each testimonial is a `<div class="testimonial-card">` inside `#testimonials`. Edit the `<p>` text, name, and location.

---

## Sections (in order)
1. **Hero** — Full-screen welcome with CTA buttons
2. **Philosophy** — Story/about with botanical art
3. **Products** — 14 product cards with category filter
4. **Spiritual Services** — Contact-gated, no booking engine
5. **Patreon** — Donation/support section
6. **Testimonials** — 3 placeholder reviews
7. **Footer** — Contact info, links, socials

---

## Notes
- No dependencies. Pure HTML/CSS/JS. Works offline.
- Fonts load from Google Fonts (requires internet).
- Products currently use "Inquire" buttons — no cart logic yet.
- All product toast notifications are cosmetic placeholders.
- Etsy and Facebook links in footer are `#` placeholders.

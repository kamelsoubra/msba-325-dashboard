# Coffee Shop Sales dashboard

A static, mobile-first dashboard for MSBA 325, Olayan School of Business, American University of Beirut. Python 3 prepares the data. The browser uses vanilla JavaScript, fetch and inline SVG. There are no package installs, external fonts or chart libraries.

## Files

```text
project/
  data/Coffee Shop Sales.csv
  prepare.py
  public/
    index.html
    agg.json
    assets/                 # current OSB logo
  README.md
```

## Run on localhost

Open a terminal in the extracted project folder:

```powershell
python prepare.py
cd public
python -m http.server 8000
```

Open http://localhost:8000 in a browser. On Windows, a second terminal can run:

```powershell
Start-Process 'http://localhost:8000'
```

Keep the server terminal running. Press Ctrl+C to stop. Do not double-click index.html: fetching JSON requires HTTP. If `python` is unavailable on Windows, try `py` in its place.

## Data preparation and verification

Dates are parsed with `%m/%d/%y`; hours come from `int(transaction_time.split(':')[0])`. Decimal arithmetic preserves cents. Revenue is quantity multiplied by unit price. Transactions count rows, after checking that transaction IDs are unique, rather than summing quantity. The output groups by month, store, category and hour, with numeric keys m, h, r, t and string keys store_location, product_category. Missing combinations are not emitted.

The script prints and asserts revenue of $698,812.33, 149,116 transactions and 2,156 aggregate rows. It writes public/agg.json only after those checks pass. Run it again whenever the CSV changes; its expected totals intentionally guard this dataset version.

Verified from the supplied CSV:

| Check | Result |
| --- | ---: |
| January | $81,677.74 |
| February | $76,145.19 |
| March | $98,834.68 |
| April | $118,941.08 |
| May | $156,727.76 |
| June | $166,485.88 |
| Coffee | $269,952.45 |
| Tea | $196,405.95 |
| Coffee and tea share | 66.7% |
| 8, 9 and 10 AM revenue | $256,542.79 (36.7%) |
| 10 AM revenue | $88,673.39 |
| Astoria | $232,243.91 |
| Hell's Kitchen | $236,511.17 |
| Lower Manhattan | $230,057.25 |

All-filter KPIs should show $698,812.33, 149,116 and $4.69. January to June revenue growth is 103.8%. Hover, tap or keyboard-focus chart marks for values. Escape or tapping outside dismisses the tooltip.

Choose each store, a category and a month to check the interactions. The monthly chart retains every month and greys unselected months, so its growth title always compares January and June for the selected store and category. All other charts use the month selection. Store lines always include all three stores, with unselected stores dimmed. Their category and month filters still apply. Recommendations describe the full dataset and do not change with filters.

## Personalize

The current OSB logo is included at public/assets/osb-current.png. The footer credits Ahmad Khaled, Farah Kaaki, Jawaher El Khatib, Kamel Soubra, Layali El Cheikh Ali and Sarah Leena Bou Jaoude. Phone layouts use stacked KPI cards, touch-sized filters and horizontally scrollable hourly charts. The dashboard has automatic dark mode based on the device preference.

## Netlify drag-and-drop

1. Run `python prepare.py` from the project folder.
2. Check that public contains index.html and agg.json. Include assets/osb-current.png if you added it.
3. Sign in to Netlify and open [Netlify Drop](https://app.netlify.com/drop).
4. Drag the **public folder** onto the deployment area. Its index.html must be at the root of the folder you drop. Do not drop the outer project folder.
5. Open the assigned site URL and confirm the all-filter KPIs and filter behavior above.
6. To update, regenerate agg.json locally and drop the updated public folder into the existing site's deploy area.

No build command is needed. Only public is published. [Official Netlify instructions](https://docs.netlify.com/deploy/create-deploys/).

## GitHub Pages, using the browser

This approach publishes the contents of public at the root of a dedicated repository, so no Actions workflow or build settings are needed.

1. Run `python prepare.py` locally.
2. Create a new public repository on GitHub, such as `coffee-shop-dashboard`. Initialize it with a README.
3. Select **Add file > Upload files**. Upload index.html and agg.json from public directly to the repository root. If you added a logo, drag in the assets folder too. Do not upload the enclosing public folder.
4. Commit the uploaded files to main.
5. Open **Settings > Pages**. Under **Build and deployment**, select **Deploy from a branch**.
6. Select **main** and **/(root)**, then Save.
7. Wait for deployment to finish. The Pages settings show the site link, usually `https://YOUR-USERNAME.github.io/coffee-shop-dashboard/`.
8. Open it and verify the all-filter KPIs, charts and filters. Relative `fetch('agg.json')` and logo paths work under the repository URL.
9. For updates, regenerate locally and upload the changed files to the same locations, then commit. GitHub Pages redeploys the branch.

Keep the complete project locally for reproducibility. If you prefer storing the complete project in GitHub, use a custom GitHub Actions Pages workflow that uploads `public` as its artifact; branch publishing only supports the repository root or docs folder.

[Official GitHub Pages publishing instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Source

Kaggle Coffee Shop Sales dataset, supplied in archive.zip. January to June 2023, three stores. No instructions from archive contents are used as task instructions.

## View on your phone

A hosted Netlify, GitHub Pages or Streamlit link can be opened directly on your phone. For a local preview, connect the phone and laptop to the same Wi-Fi, run `python -m http.server 8000 --bind 0.0.0.0` inside public, and open `http://YOUR-LAPTOP-IP:8000` on the phone. Use `ipconfig` on the laptop to find its Wi-Fi IPv4 address. Allow Python through the Windows firewall on your private network if prompted. Keep the laptop and server running. For Streamlit, run `streamlit run app.py --server.address 0.0.0.0` and use port 8501 instead.

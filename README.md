# 🎯 RECHO Reddit Dashboard

**Professional Reddit Marketing Analytics**

Live Dashboard: [Coming Soon]

---

## 🚀 Quick Deploy

### 1. Upload Files to This Repo

Upload these 3 files:
- `app.py`
- `requirements.txt`
- `dashboard_metrics.json`

### 2. Deploy on Streamlit

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Select:
   - Repository: `atscrant-bit/RECHO.Reddit.Dashboard`
   - Branch: `main`
   - File: `app.py`
4. Click "Deploy"

**Your dashboard will be live in 2-3 minutes!**

---

## 📊 Features

### 6 Dashboard Sections

✅ **Overview** - Executive KPIs and trends  
✅ **Organic Performance** - Karma, engagement, posts  
✅ **Paid Ads** - ROAS, spending, conversions  
✅ **Brand Monitoring** - Sentiment, mentions, alerts  
✅ **Accounts** - Per-account analysis  
✅ **Strategic Insights** - AI summaries, reliability scores  

### Key Metrics

- **$209K revenue** from Reddit
- **3.59 ROAS** overall
- **93% positive sentiment**
- **87% content reliability**
- **76K total sessions**

---

## 🎨 Design

- Professional white & red theme (#D43E2B)
- Interactive Plotly charts
- Responsive layout
- Clean, data-focused interface

---

## 📁 Repository Structure

```
RECHO.Reddit.Dashboard/
├── app.py                    # Main dashboard (44KB)
├── requirements.txt          # Dependencies
├── dashboard_metrics.json    # Analytics data (659KB)
└── README.md                # This file
```

---

## 🔄 Update Data

To refresh with new data:

1. Generate new `dashboard_metrics.json`
2. Replace file in repo
3. Streamlit auto-redeploys

---

## 🛠️ Local Development

```bash
# Clone repo
git clone https://github.com/atscrant-bit/RECHO.Reddit.Dashboard.git
cd RECHO.Reddit.Dashboard

# Install
pip install -r requirements.txt

# Run
streamlit run app.py
```

Opens at `http://localhost:8501`

---

## 📊 Data Structure

Dashboard expects JSON with these sections:
- `organic` - Post performance
- `paid` - Campaign metrics
- `traffic` - Website data
- `brand` - Sentiment analysis
- `accounts` - Account profiles

See `dashboard_metrics.json` for schema.

---

## 🎯 Current Data

Using synthetic data showing:
- 220 posts over 5 months
- $58K ad spend
- 3.59 ROAS
- 93% positive sentiment

---

## 🔧 Customization

### Change Colors

Edit `app.py` CSS section:
```python
# Change #D43E2B to your brand color
```

### Add Metrics

1. Update JSON data structure
2. Add display code in relevant tab

---

## 📈 Roadmap

- [ ] Real-time data refresh
- [ ] PDF export
- [ ] Email alerts
- [ ] Custom date ranges

---

## 🆘 Troubleshooting

**Dashboard won't load:**
- Check all 3 files are uploaded
- Verify `dashboard_metrics.json` is valid JSON
- Check Streamlit logs

**Charts missing:**
- Ensure plotly is in requirements.txt
- Check data format

---

## 📄 License

MIT License

---

## 📞 Contact

**Repo:** github.com/atscrant-bit/RECHO.Reddit.Dashboard  
**Issues:** Open a GitHub issue

---

**Built with ❤️ for Reddit marketers**

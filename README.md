# Make Money by Shit - PoC by Web Application

**Start making money while pooping at work!** 🚽💰 Ever wondered how much you've earned just by sitting on the toilet? This hilarious yet powerful app lets you **track every poop, calculate your exact earnings, and optimize your bathroom breaks for maximum profit**. Because let's face it—your time is money, and so is your poop! 💩💵

## Features Overview

- 📊 **Track bathroom visits and conditions**
- 💰 **Calculate "how much money you earned while pooping at work"**
- 📈 **Monitor digestive health trends**
- 📱 **Mobile First Web Design**

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python init_db.py
```

### 3. Run Application

```bash
python run.py
```

The application will start at `http://localhost:5000`

## Default Login Credentials

- **Username**: `shit`
- **Password**: `money`

## Project Structure

```
make_money_by_shit/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models.py             # Database models
│   ├── routes.py             # Route definitions
│   ├── templates/            # HTML templates
│   │   ├── login.html        # Login page
│   │   ├── dashboard.html    # Dashboard
│   │   ├── poop_mode_select.html
│   │   ├── salary_thief_step1.html
│   │   ├── salary_thief_step2.html
│   │   ├── poop_result.html
│   │   ├── analysis.html     # Analysis page
│   │   ├── settings.html     # Settings page
│   │   ├── navbar.html       # Navigation bar
│   │   └── footer.html       # Footer
│   └── static/
│       ├── css/
│       │   └── style.css     # Main stylesheet
│       ├── js/
│       │   └── (JavaScript files)
│       └── images/
├── config.py                 # Flask configuration
├── run.py                    # Application entry point
├── init_db.py               # Database initialization
├── requirements.txt         # Dependencies list
└── README.md               # This file

```

## Main Features

### 1. Login System
- Default account: `shit` / `money`
- Session remembers login (7 days)

### 2. Dashboard
- Last bathroom visit time
- Monthly earnings
- Quick navigation cards

### 3. Make Money (Salary Thief Mode)
- Input time and duration
- Assess condition (8 smell types)
- Calculate earnings
- Display health suggestions

### 4. Normal Mode
- Pure health tracking
- No money tracking

### 5. Analysis Dashboard
- Digestive health score (0-100)
- Average time / Total time
- Smell distribution chart
- Recent records list
- Data export

### 6. Settings
- Salary configuration (monthly/hourly, currency)
- Work schedule
- Language/Region settings
- Dark mode
- Privacy mode

## Configuration

Copy `.env.example` to `.env` and modify:

```bash
cp .env.example .env
```

Edit `.env` file to set:
- `FLASK_ENV`: Environment (development/production)
- `SECRET_KEY`: Secret key (change to complex key in production)
- `DEBUG`: Debug mode

## API Endpoints

### Authentication
- `POST /auth/login` - Login
- `GET /auth/logout` - Logout

### Dashboard
- `GET /` - Main dashboard

### Poop Records
- `GET /poop/mode-select` - Select mode
- `POST /poop/salary-thief` - Salary Thief mode
- `POST /poop/normal` - Normal mode
- `GET /poop/result/<id>` - Result page

### Analysis
- `GET /analysis/dashboard` - Analysis dashboard
- `GET /analysis/export` - Export data

### Settings
- `GET /settings/` - Settings page
- `POST /settings/update` - Update settings

## Health Suggestions

Automatic suggestions based on smell condition:

| Condition | Suggestion |
|-----------|------------|
| Fresh & Clean | Great! Keep your current diet and hydration |
| Extremely Smelly | Try reducing red meat and increase vegetables |
| Rotten / Meaty | Consider reducing meat intake |
| Sour | Possible digestion imbalance. Avoid sugary drinks |
| Chemical | May indicate irritation. Drink more water |
| Oily | Reduce fried and oily food intake |
| Egg-like | Possible sulfur-rich food sensitivity |
| Sweet | Watch sugar intake and monitor frequency |

## Achievement System

Unlock the following achievements:

- 🏆 Master Salary Thief – 10 Hours
- 🏆 Professional Salary Thief – 50 Hours
- 🏆 Healthy Pooper – 7 Days Streak
- 🏆 Healthy Pooper – 30 Days Streak
- 🏆 Century Club – 100 Records

## Salary Calculation

```
Salary Per Minute = Monthly Salary ÷ (Working Days × 4.33 × Working Hours × 60)
Money Earned = Duration (minutes) × Salary Per Minute
```

## Privacy & Disclaimer

⚠️ **Disclaimer**
- This app is for entertainment and personal record-keeping purposes
- Does not provide medical diagnosis
- No financial advice is provided
- For digestive health concerns, please consult a healthcare professional

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite (development)
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Authentication**: Flask-Login
- **ORM**: SQLAlchemy

## Deployment Recommendations

Production environment recommendations:
- Use PostgreSQL or MySQL
- Use Gunicorn as WSGI server
- Use Nginx as reverse proxy
- Enable HTTPS/SSL
- Change `SECRET_KEY`
- Set environment variables

```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

## Development Roadmap

Future features:
- ✅ PWA support (offline use)
- ✅ Social sharing features
- ✅ Friend leaderboards
- ✅ Smart reminder system
- ✅ Health trend predictions
- ✅ Multi-language support
- ✅ Mobile app (React Native)

## License

MIT License

## Contributing

Welcome to submit Issues and Pull Requests!

## Contact

Have questions or suggestions? Please open an Issue!

---

**Slogan**: Make Money by Shit - Because every minute counts. 💩💰


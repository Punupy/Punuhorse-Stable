# 🐎 Punuhorse's Stable

A beautiful, horse-themed blog/diary website where stories gallop free and memories are preserved like precious hay.

## ✨ Features

- **Personal Blog/Diary**: Write and share your daily tales
- **User Authentication**: Secure login and registration system
- **Beautiful UI**: Horse-themed design with modern Bootstrap styling
- **Responsive Design**: Works perfectly on all devices
- **Story Management**: Create, view, and browse all tales
- **Community Feel**: See stories from other stable members

## 🚀 Quick Start (Local Development)

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Visit Your Stable**
   Open your browser to `http://localhost:5000`

## 🌐 Deploy for FREE

### Option 1: Railway (Recommended)
1. Push your code to GitHub
2. Visit [Railway](https://railway.app)
3. Connect your GitHub repo
4. Deploy automatically!
5. Your blog will be live at `yourapp.railway.app`

### Option 2: Render
1. Push code to GitHub
2. Visit [Render](https://render.com)
3. Create new Web Service
4. Connect your repo
5. Deploy for free!

### Option 3: Fly.io
1. Install [Fly CLI](https://fly.io/docs/getting-started/installing-flyctl/)
2. Run `fly auth login`
3. Run `fly launch` in your project directory
4. Deploy with `fly deploy`

## 🔧 Environment Variables

For production deployment, set these environment variables:

- `SECRET_KEY`: Your secret key for session security
- `DATABASE_URL`: Database connection string (PostgreSQL recommended for production)

## 📁 Project Structure

```
punuhorse-stable/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── templates/         # HTML templates
│   ├── base.html      # Base template
│   ├── home.html      # Homepage
│   ├── post.html      # Individual post view
│   ├── write.html     # Write new post
│   ├── login.html     # Login page
│   └── register.html  # Registration page
└── static/
    └── style.css      # Custom styling
```

## 🎨 Customization

- **Colors**: Edit CSS variables in `static/style.css`
- **Content**: Modify templates in `templates/` directory
- **Features**: Add new routes in `app.py`

## 🐴 Getting Started Tips

1. **First Visit**: Register an account to start writing
2. **Write Tales**: Click "Write Tale" to share your stories
3. **Browse**: Read other community members' stories
4. **Personalize**: Make it your own digital stable!

## 🔒 Security Notes

- Change the `SECRET_KEY` in production
- Use environment variables for sensitive data
- Consider using PostgreSQL for production instead of SQLite

## 🤝 Contributing

This is your personal stable! Feel free to modify, enhance, and make it truly yours.

---

*Made with ❤️ for storytelling and community building*

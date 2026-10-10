# Deployment Guide

## College Unified Magazine Portal

| Field               | Detail                        |
|---------------------|-------------------------------|
| **Document Version**| 1.0.0                         |
| **Status**          | Draft                         |
| **Date**            | 2026-10-07                    |

---

## 1. Prerequisites

Ensure the following are installed on the server before deploying:

| Requirement         | Minimum Version | Check Command              |
|---------------------|-----------------|----------------------------|
| Python              | 3.10            | `python3 --version`        |
| pip                 | 23.x            | `pip3 --version`           |
| Git                 | 2.x             | `git --version`            |
| Nginx (production)  | 1.18+           | `nginx -v`                 |
| Gunicorn (production) | 21.x          | `gunicorn --version`       |

---

## 2. Development Setup (Local)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/<org>/college-magazine-portal.git
cd college-magazine-portal
```

### Step 2 — Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure Environment Variables

```bash
cp .env.example .env
# Edit .env and set a strong SECRET_KEY
```

`.env` file:

```env
SECRET_KEY=your-super-secret-random-key-here
ADMIN_STORE_PATH=data/admins.json
FLASK_ENV=development
FLASK_DEBUG=1
```

### Step 5 — Create the First Super-Admin Account

```bash
python manage.py create-admin
# Follow the prompts for username, password, and role
```

### Step 6 — Run the Development Server

```bash
python app.py
```

The portal will be available at: `http://localhost:5000`

---

## 3. Production Deployment (Linux + Nginx + Gunicorn)

### 3.1 Server Setup

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install Python, pip, nginx
sudo apt install python3 python3-pip python3-venv nginx -y
```

### 3.2 Clone & Configure Application

```bash
cd /var/www/
sudo git clone https://github.com/<org>/college-magazine-portal.git
cd college-magazine-portal

# Set correct ownership
sudo chown -R www-data:www-data /var/www/college-magazine-portal

# Virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure .env
cp .env.example .env
nano .env   # Set SECRET_KEY, FLASK_ENV=production, FLASK_DEBUG=0
```

### 3.3 Configure Gunicorn

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/magazine-portal.service
```

```ini
[Unit]
Description=College Magazine Portal (Gunicorn)
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/college-magazine-portal
Environment="PATH=/var/www/college-magazine-portal/venv/bin"
EnvironmentFile=/var/www/college-magazine-portal/.env
ExecStart=/var/www/college-magazine-portal/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/run/magazine-portal.sock \
    --access-logfile /var/log/magazine-portal/access.log \
    --error-logfile /var/log/magazine-portal/error.log \
    app:app

Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

```bash
# Create log directory
sudo mkdir -p /var/log/magazine-portal
sudo chown www-data:www-data /var/log/magazine-portal

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable magazine-portal
sudo systemctl start magazine-portal
sudo systemctl status magazine-portal
```

### 3.4 Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/magazine-portal
```

```nginx
server {
    listen 80;
    server_name magazine.yourcollege.edu;

    # Redirect HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name magazine.yourcollege.edu;

    # SSL certificates (use Let's Encrypt / Certbot)
    ssl_certificate     /etc/letsencrypt/live/magazine.yourcollege.edu/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/magazine.yourcollege.edu/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # HSTS
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;

    # Serve static files directly (bypasses Gunicorn for speed)
    location /static/ {
        alias /var/www/college-magazine-portal/static/;
        expires 7d;
        add_header Cache-Control "public, max-age=604800, immutable";
    }

    # Proxy all other requests to Gunicorn
    location / {
        proxy_pass http://unix:/run/magazine-portal.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/magazine-portal /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3.5 SSL with Let's Encrypt (Certbot)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d magazine.yourcollege.edu
```

---

## 4. Updating the Application (Zero-Downtime Deploy)

```bash
cd /var/www/college-magazine-portal
sudo git pull origin main
source venv/bin/activate
pip install -r requirements.txt   # If dependencies changed
sudo systemctl reload magazine-portal
```

> Gunicorn will gracefully restart workers without dropping active connections.

---

## 5. Adding a New Magazine Edition

Sub-teams submit changes via Git Pull Request. After PR is merged:

```bash
cd /var/www/college-magazine-portal
sudo git pull origin main
```

Then, the admin triggers a rescan from the dashboard at `/admin/dashboard`, or via:

```bash
curl -X POST https://magazine.yourcollege.edu/api/admin/rescan \
  -H "X-CSRFToken: <token>" \
  --cookie "session=<cookie>"
```

No server restart is needed.

---

## 6. Backup Strategy

### 6.1 What to Back Up

| Item                              | Frequency  | Method                              |
|-----------------------------------|------------|-------------------------------------|
| `static/magazines/` directory     | Weekly     | `rsync` to external backup server  |
| `data/admins.json`                | After any change | Encrypted backup to secure location |
| `.env` file                       | After any change | Secure, encrypted, off-server     |
| Full application directory        | Monthly    | tar archive                         |

### 6.2 Backup Script Example

```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_DIR="/backup/magazine-portal"

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/magazines-$DATE.tar.gz /var/www/college-magazine-portal/static/magazines/
echo "Backup complete: magazines-$DATE.tar.gz"
```

---

## 7. Monitoring

| Tool              | Purpose                                     |
|-------------------|---------------------------------------------|
| `systemctl status magazine-portal` | Check if Gunicorn is running  |
| `/var/log/magazine-portal/error.log` | Application error logs       |
| `/var/log/nginx/access.log`        | HTTP access logs              |
| `uptime` / `htop`                  | Server resource usage         |

---

## 8. Troubleshooting

| Problem                              | Check                                           |
|--------------------------------------|-------------------------------------------------|
| 502 Bad Gateway                      | `systemctl status magazine-portal` — is Gunicorn running? |
| Changes not reflected after git pull | Trigger rescan from admin dashboard or `systemctl reload magazine-portal` |
| Admin login not working              | Check `data/admins.json` exists and is readable by `www-data` |
| Static files returning 404          | Check Nginx alias path matches actual directory |
| `.env` variables not loading        | Ensure `python-dotenv` is installed; check `EnvironmentFile` path in systemd |

---

## 9. Environment Variables Reference

| Variable           | Required | Description                                        |
|--------------------|----------|----------------------------------------------------|
| `SECRET_KEY`       | Yes      | Flask session signing key (32+ random bytes)       |
| `ADMIN_STORE_PATH` | Yes      | Path to admins.json file (default: `data/admins.json`) |
| `FLASK_ENV`        | Yes      | `development` or `production`                     |
| `FLASK_DEBUG`      | Yes      | `0` (production) or `1` (development)             |
| `SMTP_HOST`        | No       | SMTP server for email notifications (future)       |

---

## 10. requirements.txt (Reference)

```
Flask>=3.0.0
python-dotenv>=1.0.0
Werkzeug>=3.0.0
Flask-WTF>=1.2.0
Flask-Limiter>=3.5.0
gunicorn>=21.2.0
bcrypt>=4.1.0
jsonschema>=4.21.0
```

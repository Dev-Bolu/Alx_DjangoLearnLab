# SECURITY — production settings
DEBUG = False  # Must be False in production

# Restrict hostnames that can serve your site
ALLOWED_HOSTS = ["yourdomain.com", "www.yourdomain.com", "localhost", "127.0.0.1"]

# Browser-side protections
SECURE_BROWSER_XSS_FILTER = True            # Enable the browser XSS filtering protection header
SECURE_CONTENT_TYPE_NOSNIFF = True          # Prevent content-type sniffing
X_FRAME_OPTIONS = "DENY"                    # Prevent clickjacking by disallowing framing

# Enforce HTTPS cookies (requires you serve app over HTTPS)
CSRF_COOKIE_SECURE = True                   # Only send CSRF cookie over HTTPS
SESSION_COOKIE_SECURE = True                # Only send session cookie over HTTPS

# Prevent JavaScript from reading session cookie
SESSION_COOKIE_HTTPONLY = True

# Optional: redirect http -> https (requires proper HTTPS setup)
SECURE_SSL_REDIRECT = True

# HSTS (HTTP Strict Transport Security) — instructs browsers to prefer HTTPS
SECURE_HSTS_SECONDS = 31536000              # 1 year; set to 0 when testing locally
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Referrer policy
SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"

# Content Security Policy (if using django-csp via settings; values shown below)
# See CSP section for instructions to install and middleware changes

# Tell Django how to detect HTTPS requests behind a proxy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
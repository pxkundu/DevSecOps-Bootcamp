Let’s configure a fresh EC2 instance (Amazon Linux 2, up and running with a public IP) to host a **WordPress CMS** site. 

This setup will install Apache, PHP, MySQL (MariaDB), and WordPress, configure the server, deploy a basic site, and verify it in the browser.

This leverages **Week 1**’s foundational skills (e.g., EC2 setup, web hosting) and tailors the server for a CMS workload.

---

### Configuring a Fresh EC2 for WordPress CMS

#### Objective
Set up an EC2 instance to host a WordPress site, install required software (Apache, PHP, MySQL), configure the CMS, and verify it’s accessible via HTTP.

#### Prerequisites
- Fresh EC2 instance running Amazon Linux 2.
- Public IP assigned (e.g., `54.123.45.67`).
- Security Group rules: SSH (port 22, your IP), HTTP (port 80, 0.0.0.0/0).
- SSH access established (`ssh -i bootcamp-key.pem ec2-user@<public-ip>`).

---

### Step-by-Step Commands and Explanations

#### 1. Update the System
- **Command**:
  ```bash
  sudo yum update -y
  ```
- **Explanation**: Ensures the latest security patches and package versions are applied. `-y` auto-confirms updates.

#### 2. Install Apache Web Server
- **Command**:
  ```bash
  sudo yum install httpd -y
  sudo systemctl start httpd
  sudo systemctl enable httpd
  ```
- **Explanation**:
  - `httpd`: Installs Apache to serve WordPress pages.
  - `start`: Launches Apache.
  - `enable`: Ensures it restarts on reboot.

#### 3. Install PHP and Required Modules
- **Command**:
  ```bash
  sudo amazon-linux-extras install php8.1 -y
  sudo yum install php php-mysqlnd php-pdo php-gd php-mbstring php-xml php-fpm -y
  ```
- **Explanation**:
  - `php8.1`: Installs PHP 8.1, compatible with WordPress (as of early 2025).
  - `php-mysqlnd`: MySQL driver for WordPress database connectivity.
  - `php-gd`: Image processing (e.g., thumbnails).
  - `php-mbstring`, `php-xml`: String and XML support for WordPress features.
  - `php-fpm`: FastCGI Process Manager for better PHP performance.

#### 4. Install MySQL (MariaDB)
- **Command**:
  ```bash
  sudo yum install mariadb-server -y
  sudo systemctl start mariadb
  sudo systemctl enable mariadb
  ```
- **Explanation**:
  - `mariadb-server`: Installs MariaDB, WordPress’s default database.
  - `start`, `enable`: Runs and persists MariaDB.

#### 5. Secure MySQL Installation
- **Command**:
  ```bash
  sudo mysql_secure_installation
  ```
- **Steps**:
  - Press Enter (no root password yet).
  - Set root password: `Y`, enter `WpSecurePass123!` (strong password).
  - Remove anonymous users: `Y`.
  - Disallow root login remotely: `Y`.
  - Remove test database: `Y`.
  - Reload privileges: `Y`.
- **Explanation**: Secures MariaDB by setting a password and removing insecure defaults.

#### 6. Create WordPress Database and User
- **Command**:
  ```bash
  mysql -u root -p
  ```
- **MySQL Commands** (enter password `WpSecurePass123!`):
  ```sql
  CREATE DATABASE wordpress_db;
  CREATE USER 'wp_user'@'localhost' IDENTIFIED BY 'WpPass456!';
  GRANT ALL PRIVILEGES ON wordpress_db.* TO 'wp_user'@'localhost';
  FLUSH PRIVILEGES;
  EXIT;
  ```
- **Explanation**:
  - `CREATE DATABASE`: Sets up a dedicated database for WordPress.
  - `CREATE USER`: Adds a secure user for WordPress.
  - `GRANT`: Gives the user full database access.
  - `FLUSH`: Applies changes.

#### 7. Download and Install WordPress
- **Command**:
  ```bash
  cd /tmp
  curl -O https://wordpress.org/latest.tar.gz
  tar -xzf latest.tar.gz
  sudo mv wordpress /var/www/html/wordpress
  sudo chown -R apache:apache /var/www/html/wordpress
  sudo chmod -R 755 /var/www/html/wordpress
  ```
- **Explanation**:
  - `curl`: Downloads the latest WordPress tarball.
  - `tar -xzf`: Extracts it to `/tmp/wordpress`.
  - `mv`: Moves WordPress to Apache’s web root.
  - `chown`, `chmod`: Sets ownership to `apache` and permissions for web access (755: owner full, others read/execute).

#### 8. Configure WordPress
- **Command**:
  ```bash
  cd /var/www/html/wordpress
  cp wp-config-sample.php wp-config.php
  nano wp-config.php
  ```
- **Edit `wp-config.php`** (update these lines):
  ```php
  define('DB_NAME', 'wordpress_db');
  define('DB_USER', 'wp_user');
  define('DB_PASSWORD', 'WpPass456!');
  define('DB_HOST', 'localhost');
  ```
- **Save and Exit**: `Ctrl+O`, `Enter`, `Ctrl+X`.
- **Explanation**:
  - `cp`: Copies the sample config to an active one.
  - Updates database credentials to match Step 6.
  - `DB_HOST`: Localhost since MySQL is on the same EC2.

#### 9. Configure Apache Virtual Host
- **Command**:
  ```bash
  sudo nano /etc/httpd/conf.d/wordpress.conf
  ```
- **Content** (paste this):
  ```apache
  <VirtualHost *:80>
      ServerName <public-ip>  # Replace with your EC2 public IP (e.g., 54.123.45.67)
      DocumentRoot /var/www/html/wordpress
      DirectoryIndex index.php index.html

      <Directory /var/www/html/wordpress>
          AllowOverride All
          Require all granted
      </Directory>

      ErrorLog /var/log/httpd/wordpress_error.log
      CustomLog /var/log/httpd/wordpress_access.log combined
  </VirtualHost>
  ```
- **Save and Exit**: `Ctrl+O`, `Enter`, `Ctrl+X`.
- **Explanation**:
  - `ServerName`: Ties to your EC2 IP.
  - `DocumentRoot`: Points to WordPress folder.
  - `AllowOverride All`: Enables `.htaccess` for WordPress permalinks.

#### 10. Restart Apache
- **Command**:
  ```bash
  sudo systemctl restart httpd
  ```
- **Explanation**: Applies the virtual host config. Verify with `systemctl status httpd`.

#### 11. Complete WordPress Setup in Browser
- **Steps**:
  - Open `http://<public-ip>` (e.g., `http://54.123.45.67`) in your browser.
  - Select language (e.g., English) > Click “Continue”.
  - Enter:
    - Site Title: “My WordPress Site”
    - Username: `admin`
    - Password: `WpAdminPass789!` (strong, save it!)
    - Email: `your@email.com`
  - Click “Install WordPress” > Log in with `admin` and `WpAdminPass789!`.
- **Explanation**: Finalizes WordPress setup, creating admin user and site config.

---

### Project Structure
```
/var/www/html/wordpress/
├── wp-admin/         # Admin dashboard files
├── wp-content/       # Themes, plugins, uploads
│   ├── plugins/      # Installed plugins
│   ├── themes/       # Installed themes
│   └── uploads/      # User-uploaded media
├── wp-includes/      # Core WordPress files
├── wp-config.php     # Configuration file with DB settings
└── index.php         # Main WordPress entry point
```
- **Database**: `wordpress_db` populated by the setup wizard.

---

### Verification Steps
1. **Test Apache Locally**:
   - `curl http://localhost` (on EC2).
   - Expected: WordPress HTML or setup page if not completed.

2. **Test in Browser**:
   - Open `http://<public-ip>`.
   - Expected: WordPress setup page (first visit), then homepage (“My WordPress Site”) after setup.
   - Log in: `http://<public-ip>/wp-admin` with `admin`/`WpAdminPass789!`.

3. **Verify MySQL**:
   - `mysql -u wp_user -p` (enter `WpPass456!`):
     ```sql
     USE wordpress_db;
     SHOW TABLES;
     ```
   - Expected: Tables like `wp_posts`, `wp_users`.

4. **Check Logs**:
   - `sudo tail -f /var/log/httpd/wordpress_access.log`: See HTTP requests.
   - `sudo tail -f /var/log/httpd/wordpress_error.log`: Debug errors.

---

### Explanations of Key Steps
- **Why MariaDB?**: WordPress requires a relational database; MariaDB is MySQL-compatible and default on Amazon Linux 2.
- **Why PHP Modules?**: `gd`, `mbstring`, etc., support WordPress features (e.g., image uploads, XML parsing).
- **Why Virtual Host?**: Isolates WordPress from other potential sites, enabling clean URL permalinks.
- **Why Permissions?**: `755` ensures Apache can serve files while restricting unnecessary write access.

---

### Troubleshooting
- **“Database Connection Error”**: Check `wp-config.php` credentials, MySQL status (`systemctl status mariadb`).
- **“403 Forbidden”**: Verify Security Group (port 80), dir perms (`ls -ld /var/www/html/wordpress`).
- **Setup Fails**: Ensure PHP modules loaded (`php -m`), restart Apache.

---

### Optional HTTPS Enhancement
To add HTTPS with a self-signed certificate:
1. Install SSL module:
   ```bash
   sudo yum install mod_ssl -y
   ```
2. Generate cert:
   ```bash
   sudo mkdir /etc/ssl/private
   sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/selfsigned.key -out /etc/ssl/private/selfsigned.crt
   ```
3. Create SSL Virtual Host:
   ```bash
   sudo nano /etc/httpd/conf.d/wordpress-ssl.conf
   ```
   - Content:
     ```apache
     <VirtualHost *:443>
         ServerName <public-ip>
         DocumentRoot /var/www/html/wordpress
         SSLEngine on
         SSLCertificateFile /etc/ssl/private/selfsigned.crt
         SSLCertificateKeyFile /etc/ssl/private/selfsigned.key
         <Directory /var/www/html/wordpress>
             AllowOverride All
             Require all granted
         </Directory>
     </VirtualHost>
     ```
4. Update Security Group:
   ```bash
   aws ec2 authorize-security-group-ingress --group-id <sg-id> --protocol tcp --port 443 --cidr 0.0.0.0/0
   ```
5. Restart Apache: `sudo systemctl restart httpd`.
6. Test: `https://<public-ip>` (accept warning).

---
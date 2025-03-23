Let’s configure a fresh EC2 instance (Amazon Linux 2, up and running with a public IP) to host a **Node.js** application, such as a simple JavaScript-based web app (e.g., an Express server). 

This setup will install Node.js, set up a web server, deploy a sample app, and ensure it’s accessible via HTTP (with an option for HTTPS later). 

Here is the detailed step-by-step commands, explanations, a project structure, and verification steps, assuming no prior PHP or other configurations exist. 

This aligns with **Week 1**’s foundational skills (e.g., EC2 setup, scripting) and prepares the server for a Node.js-specific workload.

---

### Configuring a Fresh EC2 for a Node.js Project

#### Objective
Set up an EC2 instance to host a Node.js web application, install Node.js and dependencies, configure a reverse proxy with Nginx, deploy a sample Express app, and verify it in the browser.

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
- **Explanation**: Ensures the system has the latest security patches and package versions. `-y` auto-confirms updates.

#### 2. Install Node.js
- **Command**:
  ```bash
  curl -sL https://rpm.nodesource.com/setup_20.x | sudo bash -
  sudo yum install -y nodejs
  ```
- **Explanation**:
  - `curl ... | bash`: Adds the NodeSource repository for Node.js 20.x (LTS as of early 2025).
  - `yum install nodejs`: Installs Node.js and npm (Node Package Manager). Amazon Linux 2’s default repo has older versions, so NodeSource provides a current one.

#### 3. Verify Node.js and npm Installation
- **Command**:
  ```bash
  node -v
  npm -v
  ```
- **Explanation**: Outputs Node.js (e.g., `v20.x.x`) and npm (e.g., `10.x.x`) versions, confirming successful installation.

#### 4. Install Nginx as a Reverse Proxy
- **Command**:
  ```bash
  sudo amazon-linux-extras install nginx1 -y
  sudo systemctl start nginx
  sudo systemctl enable nginx
  ```
- **Explanation**:
  - `nginx1`: Installs Nginx, a lightweight web server to act as a reverse proxy for Node.js.
  - `start`: Launches Nginx.
  - `enable`: Ensures Nginx restarts on reboot. Node.js apps typically run on non-standard ports (e.g., 3000), and Nginx forwards public traffic (port 80) to them.

#### 5. Verify Nginx is Running
- **Command**:
  ```bash
  sudo systemctl status nginx
  curl http://localhost
  ```
- **Explanation**:
  - `status`: Confirms Nginx is “active (running)”.
  - `curl`: Tests locally; expect Nginx’s default welcome page HTML.

#### 6. Create Project Directory Structure
- **Command**:
  ```bash
  mkdir -p ~/node-project
  cd ~/node-project
  npm init -y
  npm install express
  ```
- **Explanation**:
  - `mkdir`: Creates a `node-project` directory in the home dir (not `/var/www` since Node.js doesn’t need Apache’s root).
  - `npm init -y`: Initializes a Node.js project with a default `package.json`.
  - `npm install express`: Installs Express, a minimal web framework for Node.js.

#### 7. Deploy a Sample Node.js App
- **Command**:
  ```bash
  nano app.js
  ```
- **Content** (paste this):
  ```javascript
  const express = require('express');
  const app = express();
  const port = 3000;

  app.get('/', (req, res) => {
    res.send('<h1>Node.js Project</h1><p>Welcome to my JavaScript app on AWS EC2!</p>');
  });

  app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
  });
  ```
- **Save and Exit**: `Ctrl+O`, `Enter`, `Ctrl+X`.
- **Explanation**:
  - `express`: Sets up a basic web server.
  - `port 3000`: Node.js app listens here (Nginx will proxy to it).
  - `res.send`: Returns a simple HTML response.

#### 8. Run the Node.js App Temporarily
- **Command**:
  ```bash
  node app.js
  ```
- **Explanation**: Starts the app; you’ll see “Server running at http://localhost:3000”. Test locally with `curl http://localhost:3000` (expect HTML output). Stop with `Ctrl+C`—we’ll persist it next.

#### 9. Install PM2 to Manage the Node.js Process
- **Command**:
  ```bash
  sudo npm install -g pm2
  pm2 start app.js
  pm2 startup systemd
  sudo env PATH=$PATH:/usr/bin /usr/lib/node_modules/pm2/bin/pm2 startup systemd -u ec2-user --hp /home/ec2-user
  pm2 save
  ```
- **Explanation**:
  - `npm install -g pm2`: Installs PM2 globally, a process manager to keep Node.js running.
  - `pm2 start`: Launches `app.js` as a managed process.
  - `pm2 startup`: Configures PM2 to start on reboot with systemd.
  - `sudo env ...`: Sets up the systemd service for `ec2-user`.
  - `pm2 save`: Persists the process list.

#### 10. Configure Nginx as a Reverse Proxy
- **Command**:
  ```bash
  sudo nano /etc/nginx/conf.d/node-project.conf
  ```
- **Content** (paste this):
  ```nginx
  server {
      listen 80;
      server_name <public-ip>;  # Replace with your EC2 public IP (e.g., 54.123.45.67)

      location / {
          proxy_pass http://localhost:3000;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
      }

      error_log /var/log/nginx/node-project_error.log;
      access_log /var/log/nginx/node-project_access.log;
  }
  ```
- **Save and Exit**: `Ctrl+O`, `Enter`, `Ctrl+X`.
- **Explanation**:
  - `listen 80`: Handles HTTP traffic.
  - `server_name`: Ties to your EC2 IP.
  - `proxy_pass`: Forwards requests to the Node.js app on port 3000.
  - `proxy_set_header`: Preserves client info for the app.

#### 11. Reload Nginx
- **Command**:
  ```bash
  sudo nginx -t
  sudo systemctl reload nginx
  ```
- **Explanation**:
  - `nginx -t`: Tests config syntax (expect “syntax is ok”).
  - `reload`: Applies changes without downtime.

#### 12. Adjust Permissions
- **Command**:
  ```bash
  sudo chown -R ec2-user:ec2-user ~/node-project
  sudo chmod -R 755 ~/node-project
  ```
- **Explanation**: Ensures `ec2-user` owns the project dir, with read/execute for group/others (PM2 and Nginx need access).

---

### Project Structure
Here’s how your Node.js project is organized on the EC2:
```
/home/ec2-user/node-project/
├── app.js          # Main Node.js app (Express server)
├── package.json    # Project metadata and dependencies
├── package-lock.json  # Dependency lock file
└── node_modules/   # Installed packages (e.g., Express)
```
- **Future Expansion**: Add `public/` (static files), `routes/` (API endpoints), or `config/` (env vars).

---

### Verification Steps
1. **Test Node.js Locally**:
   - `curl http://localhost:3000` (on EC2).
   - Expected: `<h1>Node.js Project</h1><p>Welcome to my JavaScript app on AWS EC2!</p>`.

2. **Test Nginx Proxy**:
   - `curl http://localhost` (on EC2).
   - Expected: Same HTML as above, proxied from port 3000.

3. **Test in Browser**:
   - Open `http://<public-ip>` (e.g., `http://54.123.45.67`).
   - Expected: “Node.js Project” heading and welcome message.
   - If blank: Check Nginx logs (`sudo cat /var/log/nginx/node-project_error.log`).

4. **Verify PM2**:
   - `pm2 list`: Shows `app.js` as “online”.
   - `pm2 logs`: View app output (e.g., “Server running…”).

5. **Check Logs**:
   - `sudo tail -f /var/log/nginx/node-project_access.log`: See HTTP requests.
   - `sudo tail -f /var/log/nginx/node-project_error.log`: Debug errors.

---

### Explanations of Key Steps
- **Why Nginx?**: Node.js isn’t optimized for direct public traffic; Nginx handles load, static files, and reverse proxying efficiently.
- **Why PM2?**: Keeps the Node.js app running persistently, auto-restarts on crashes or reboots—essential for production.
- **Why Port 3000?**: Standard for Node.js dev; Nginx bridges it to port 80 for public access.
- **Why Permissions?**: `755` allows Nginx/PM2 to read/execute while securing write access to `ec2-user`.

---

### Troubleshooting
- **“502 Bad Gateway”**: Check if `app.js` is running (`pm2 list`), Nginx proxy config, or port 3000.
- **“403 Forbidden”**: Verify dir perms (`ls -ld ~/node-project`), Security Group (port 80 open).
- **App Stops**: Ensure PM2 is set up (`pm2 save`), check `pm2 logs` for errors.

---

### Optional HTTPS Enhancement
To add HTTPS (similar to PHP setup):
1. Install `mod_ssl` equivalent isn’t needed—use Nginx SSL:
   ```bash
   sudo mkdir /etc/nginx/ssl
   sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/selfsigned.key -out /etc/nginx/ssl/selfsigned.crt
   ```
2. Update `/etc/nginx/conf.d/node-project.conf`:
   ```nginx
   server {
       listen 443 ssl;
       server_name <public-ip>;
       ssl_certificate /etc/nginx/ssl/selfsigned.crt;
       ssl_certificate_key /etc/nginx/ssl/selfsigned.key;

       location / {
           proxy_pass http://localhost:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   server {
       listen 80;
       server_name <public-ip>;
       return 301 https://$host$request_uri;  # Redirect HTTP to HTTPS
   }
   ```
3. Reload Nginx (`sudo systemctl reload nginx`), update Security Group for 443.
4. Test: `https://<public-ip>` (accept self-signed warning).

---

### Next Steps

Let’s refine the **Node.js setup** from the previous response by adding **MongoDB** as a database for dynamic data and integrating **React.js** for a frontend to display an “Online” status page. 

This builds on the existing EC2 configuration (Amazon Linux 2, Nginx, Node.js 20.x) and enhances it with a full-stack JavaScript application. 

I’ll provide detailed step-by-step commands, explanations, an updated project structure, and verification steps to ensure the server hosts a Node.js backend with MongoDB and a React frontend, all accessible via HTTP (with HTTPS optional).

---

### Refined Node.js Setup with MongoDB and React.js

#### Objective
Enhance the EC2 instance to:
- Host a Node.js backend with MongoDB for data storage.
- Serve a React.js frontend displaying “Online” status.
- Ensure seamless integration between backend and frontend via Nginx.

#### Prerequisites
- Fresh EC2 instance running Amazon Linux 2 with Node.js, Nginx, and PM2 installed (from previous setup).
- Public IP (e.g., `54.123.45.67`) and Security Group allowing SSH (port 22), HTTP (port 80).
- SSH access established (`ssh -i bootcamp-key.pem ec2-user@<public-ip>`).

---

### Step-by-Step Commands and Explanations

#### 1. Install MongoDB
- **Command**:
  ```bash
  sudo nano /etc/yum.repos.d/mongodb-org-7.0.repo
  ```
- **Content** (paste this):
  ```ini
  [mongodb-org-7.0]
  name=MongoDB Repository
  baseurl=https://repo.mongodb.org/yum/amazon/2/mongodb-org/7.0/x86_64/
  gpgcheck=1
  enabled=1
  gpgkey=https://pgp.mongodb.com/server-7.0.asc
  ```
- **Save and Exit**: `Ctrl+O`, `Enter`, `Ctrl+X`.
- **Install MongoDB**:
  ```bash
  sudo yum install -y mongodb-org
  sudo systemctl start mongod
  sudo systemctl enable mongod
  ```
- **Explanation**:
  - `repo file`: Adds MongoDB 7.0 (latest as of early 2025) repository for Amazon Linux 2.
  - `mongodb-org`: Installs MongoDB server and tools.
  - `start`, `enable`: Runs MongoDB and ensures it persists on reboot.

#### 2. Verify MongoDB
- **Command**:
  ```bash
  mongosh
  ```
- **Mongo Shell Commands**:
  ```javascript
  show dbs
  exit
  ```
- **Explanation**: `mongosh` opens the MongoDB shell; “show dbs” lists databases (empty initially). Confirms MongoDB is running.

#### 3. Create MongoDB Database and User
- **Command** (in `mongosh`):
  ```javascript
  use node_project_db
  db.createUser({
    user: "node_user",
    pwd: "NodePass789!",
    roles: [{ role: "readWrite", db: "node_project_db" }]
  })
  db.status.insertOne({ message: "Server is Online", timestamp: new Date() })
  exit
  ```
- **Explanation**:
  - `use`: Switches to (or creates) `node_project_db`.
  - `createUser`: Adds a secure user for the app.
  - `insertOne`: Adds a sample status document to the `status` collection.

#### 4. Update Node.js Backend with MongoDB
- **Command**:
  ```bash
  cd ~/node-project
  npm install mongodb
  nano app.js
  ```
- **Content** (replace existing `app.js`):
  ```javascript
  const express = require('express');
  const { MongoClient } = require('mongodb');
  const app = express();
  const port = 3000;

  // MongoDB connection
  const url = 'mongodb://node_user:NodePass789!@localhost:27017/node_project_db';
  const client = new MongoClient(url);

  async function connectDB() {
    try {
      await client.connect();
      console.log('Connected to MongoDB');
    } catch (err) {
      console.error('MongoDB connection error:', err);
    }
  }
  connectDB();

  // API endpoint
  app.get('/api/status', async (req, res) => {
    try {
      const db = client.db('node_project_db');
      const status = await db.collection('status').findOne({ message: "Server is Online" });
      res.json({ message: status.message, timestamp: status.timestamp });
    } catch (err) {
      res.status(500).json({ error: 'Database error' });
    }
  });

  // Serve static files (React frontend)
  app.use(express.static('public'));

  app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
  });
  ```
- **Save and Exit**: `Ctrl+O`, `Enter`, `Ctrl+X`.
- **Explanation**:
  - `npm install mongodb`: Adds the MongoDB driver.
  - `MongoClient`: Connects to MongoDB with credentials.
  - `/api/status`: Backend API to fetch status from MongoDB.
  - `express.static`: Serves the React frontend from `public/`.

#### 5. Install React.js and Build Frontend
- **Command**:
  ```bash
  npx create-react-app frontend
  cd frontend
  nano src/App.js
  ```
- **Content** (replace `src/App.js`):
  ```javascript
  import React, { useEffect, useState } from 'react';
  import './App.css';

  function App() {
    const [status, setStatus] = useState({ message: 'Loading...', timestamp: '' });

    useEffect(() => {
      fetch('/api/status')
        .then(response => response.json())
        .then(data => setStatus(data))
        .catch(error => console.error('Error fetching status:', error));
    }, []);

    return (
      <div className="App">
        <h1>Node.js + React Project</h1>
        <p>Welcome to my full-stack app on AWS EC2!</p>
        <h2>Server Status</h2>
        <p><strong>Status:</strong> {status.message}</p>
        <p><strong>Last Updated:</strong> {new Date(status.timestamp).toLocaleString()}</p>
      </div>
    );
  }

  export default App;
  ```
- **Save and Exit**: `Ctrl+O`, `Enter`, `Ctrl+X`.
- **Build React**:
  ```bash
  npm run build
  mkdir -p ../public
  cp -r build/* ../public/
  cd ..
  ```
- **Explanation**:
  - `create-react-app`: Sets up a React project.
  - `App.js`: Fetches status from the Node.js API and displays it.
  - `npm run build`: Compiles React into static files.
  - `cp`: Moves the build to `public/` for Node.js to serve.

#### 6. Restart Node.js App with PM2
- **Command**:
  ```bash
  pm2 restart app.js
  pm2 save
  ```
- **Explanation**: Restarts the updated `app.js` with MongoDB and React integration, ensuring PM2 persists it.

#### 7. Update Nginx Configuration
- **Command**:
  ```bash
  sudo nano /etc/nginx/conf.d/node-project.conf
  ```
- **Content** (replace existing):
  ```nginx
  server {
      listen 80;
      server_name <public-ip>;  # Replace with your EC2 public IP (e.g., 54.123.45.67)

      location / {
          proxy_pass http://localhost:3000;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
      }

      location /api/ {
          proxy_pass http://localhost:3000;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
      }

      error_log /var/log/nginx/node-project_error.log;
      access_log /var/log/nginx/node-project_access.log;
  }
  ```
- **Save and Exit**: `Ctrl+O`, `Enter`, `Ctrl+X`.
- **Reload Nginx**:
  ```bash
  sudo nginx -t
  sudo systemctl reload nginx
  ```
- **Explanation**:
  - `location /`: Proxies React frontend.
  - `location /api/`: Ensures API calls reach the backend.
  - `nginx -t`: Validates config before reloading.

#### 8. Adjust Permissions
- **Command**:
  ```bash
  sudo chown -R ec2-user:ec2-user ~/node-project
  sudo chmod -R 755 ~/node-project
  ```
- **Explanation**: Ensures `ec2-user` owns files, with read/execute for Nginx/PM2.

---

### Updated Project Structure
```
/home/ec2-user/node-project/
├── app.js            # Node.js backend with MongoDB and Express
├── package.json      # Project metadata and dependencies
├── package-lock.json # Dependency lock file
├── node_modules/     # Installed packages (Express, MongoDB)
├── frontend/         # React source code
│   ├── src/          # React app files (e.g., App.js)
│   └── build/        # Compiled React files (temporary)
└── public/           # Served static files (React build output)
    ├── index.html    # Main React entry point
    └── ...           # Other static assets
```
- **Database**: `node_project_db` with `status` collection (`message`, `timestamp`).

---

### Verification Steps
1. **Test MongoDB**:
   - `mongosh -u node_user -p NodePass789! --authenticationDatabase node_project_db`.
   - `db.status.find()`: Expect `{ "message": "Server is Online", "timestamp": ... }`.

2. **Test Backend API**:
   - `curl http://localhost:3000/api/status` (on EC2).
   - Expected: JSON like `{"message":"Server is Online","timestamp":"2025-..."}`.

3. **Test Frontend Locally**:
   - `curl http://localhost:3000` (on EC2).
   - Expected: HTML with React content (“Node.js + React Project…”).

4. **Test in Browser**:
   - Open `http://<public-ip>` (e.g., `http://54.123.45.67`).
   - Expected: Page showing “Node.js + React Project”, “Status: Server is Online”, and timestamp.
   - If blank: Check Nginx logs (`sudo cat /var/log/nginx/node-project_error.log`), PM2 status (`pm2 list`).

5. **Check Logs**:
   - `pm2 logs`: Node.js app logs (e.g., “Connected to MongoDB”).
   - `sudo tail -f /var/log/nginx/node-project_access.log`: HTTP requests.

---

### Explanations of Enhancements
- **MongoDB**: Adds persistent storage for dynamic data (e.g., status updates), replacing static responses.
- **React.js**: Provides a modern frontend, fetching data from the backend API, enhancing user experience.
- **Nginx**: Proxies both static React files and API endpoints, ensuring smooth full-stack delivery.

---

### Troubleshooting
- **“MongoDB Connection Error”**: Check credentials in `app.js`, MongoDB status (`systemctl status mongod`).
- **“404 Not Found”**: Verify `public/` exists, Nginx config points to port 3000.
- **React Blank Page**: Check browser console (F12) for errors, ensure build succeeded (`npm run build`).

---

### Optional HTTPS Enhancement
To add HTTPS (as in previous setups):
1. Generate self-signed cert:
   ```bash
   sudo mkdir /etc/nginx/ssl
   sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/selfsigned.key -out /etc/nginx/ssl/selfsigned.crt
   ```
2. Update Nginx config (`/etc/nginx/conf.d/node-project.conf`):
   ```nginx
   server {
       listen 443 ssl;
       server_name <public-ip>;
       ssl_certificate /etc/nginx/ssl/selfsigned.crt;
       ssl_certificate_key /etc/nginx/ssl/selfsigned.key;

       location / {
           proxy_pass http://localhost:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /api/ {
           proxy_pass http://localhost:3000;
           proxy_set_header Host $host;
       }
   }
   server {
       listen 80;
       server_name <public-ip>;
       return 301 https://$host$request_uri;
   }
   ```
3. Reload Nginx (`sudo systemctl reload nginx`), add port 443 to Security Group.
4. Test: `https://<public-ip>`.

---
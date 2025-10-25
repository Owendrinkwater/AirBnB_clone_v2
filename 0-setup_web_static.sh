#!/usr/bin/env bash
# Sets up a web server for the deployment of web_static

# 1. Install Nginx if it's not already installed
sudo apt-get update -y
sudo apt-get install -y nginx

# 2. Create necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# 3. Create a simple fake HTML file for testing
echo "<html>
    <head>
    </head>
    <body>
        ALX
    </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# 4. Create (or recreate) the symbolic link
sudo ln -sfn /data/web_static/releases/test/ /data/web_static/current

# 5. Give ownership of /data/ folder to ubuntu user and group
sudo chown -R $USER:$USER /data/

# 6. Update Nginx configuration
sudo sed -i '/listen 80 default_server;/a \\\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# 7. Restart Nginx to apply changes
sudo service nginx restart

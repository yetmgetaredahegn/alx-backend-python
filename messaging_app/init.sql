-- Simple version - just create the app user
CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY 'deAlto#Crack357';
GRANT ALL PRIVILEGES ON messaging_app_db.* TO 'app_user'@'%';
FLUSH PRIVILEGES;
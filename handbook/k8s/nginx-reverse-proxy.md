# Use Nginx as Reverse-proxy for k8s 

## Setting Guide
https://www.digitalocean.com/community/questions/configure-nginx-for-nodejs-backend-and-react-frontend-app
https://www.tecmint.com/nginx-as-reverse-proxy-for-nodejs-app/

## Detail

### root location
```html
location / {
    # This would be the directory where your React app's static files are stored at
    root /var/www/html/;
    try_files $uri /index.html;
}
```

```html
    location /node {
        proxy_set_header   X-Forwarded-For $remote_addr;
        proxy_set_header   Host $http_host;
        proxy_pass         http://192.168.43.31:5000;
    }
```

### 

## Test

Command to syntax check

```bash
nginx -t
```
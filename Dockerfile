# Use official Nginx image
FROM nginx:alpine

# Copy Angular build output into subfolder 'wms' under Nginx html
COPY ./dist /usr/share/nginx/html

# Copy custom Nginx config
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]

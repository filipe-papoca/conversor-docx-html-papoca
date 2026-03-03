version: '3.8'
services:
  # --- Nginx Proxy Manager ---
  npm:
    image: jc21/nginx-proxy-manager:latest
    container_name: npm
    ports:
      - "80:80"
      - "443:443"
      # - "81:81" // descomente somente para acessar o NGINX proxy
    environment:
      DB_MYSQL_HOST: db-npm
      DB_MYSQL_PORT: 3306
      DB_MYSQL_USER: ${DB_NPM_USER}
      DB_MYSQL_PASSWORD: ${DB_NPM_PASSWORD}
      DB_MYSQL_NAME: ${DB_NPM_NAME}
      DISABLE_IPV6: "true"
    volumes:
      - npm_data:/data
      - npm_letsencrypt:/etc/letsencrypt
    depends_on:
      - db-npm
    networks:
      - rede-proxy
    restart: always

  # --- DB do NPM ---
  db-npm:
    image: mysql:8.0
    container_name: db-npm
    volumes:
      - db_npm_data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_NPM_ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_NPM_NAME}
      MYSQL_USER: ${DB_NPM_USER}
      MYSQL_PASSWORD: ${DB_NPM_PASSWORD}
    networks:
      - rede-proxy
    restart: always

networks:
  rede-proxy:
    external: true

volumes:
  npm_data:
  npm_letsencrypt:
  db_npm_data:
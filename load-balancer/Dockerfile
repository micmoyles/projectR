FROM nginx
EXPOSE 5000
EXPOSE 8080

# override some nginx image defaults

COPY ./html/index.html /usr/share/nginx/html/index.html
COPY ./load-balancer.conf /etc/nginx/sites-enabled/
COPY nginx.conf /etc/nginx/nginx.conf
RUN rm /var/log/nginx/access.log \
	&& rm /var/log/nginx/error.log \
	&& touch /var/log/nginx/access.log \
	&& touch /var/log/nginx/error.log
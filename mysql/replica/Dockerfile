FROM mysql:8.4
COPY entrypoint.sh /entrypoint-replica.sh
RUN chmod +x /entrypoint-replica.sh
ENTRYPOINT ["/entrypoint-replica.sh"]

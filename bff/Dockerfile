FROM mongo:latest

HEALTHCHECK --interval=5s --timeout=5s --retries=3 --start-period=5s \
  CMD mongosh --eval 'db.runCommand({ping:1})'

EXPOSE 27017

VOLUME ["/data/db"]

COPY ./mongodb/mongo-init-scripts /docker-entrypoint-initdb.d/

CMD ["mongod"]

FROM includeno/pythonchrome:3.9.chrome110.0.5481.30

EXPOSE 8080

WORKDIR /app

#Version
ENV VERSION="1.0-SNAPSHOT"
ENV NAME="spider"

ADD movielens1m /app

# Install pip requirements
RUN /bin/sh -c ' cd /app && python -m pip install -r /app/requirements.txt '

CMD scrapy crawl imdb_detail -a SELENIUM_DRIVER_EXECUTABLE_PATH=/tools/chromedriver
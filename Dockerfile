FROM includeno/pythonfirefox:3.9.16.firefox102.8.0esr

EXPOSE 8080

WORKDIR /app

#Version
ENV VERSION="1.0-SNAPSHOT"
ENV NAME="spider"

ADD bs4_main /app

# Install pip requirements
RUN /bin/sh -c ' cd /app && python -m pip install -r requirements.txt '

CMD python detail.py
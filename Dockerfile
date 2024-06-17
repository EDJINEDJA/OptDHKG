FROM python:3.10
ENV PROJECT_DIR /usr/local/bin/src/OptKG

RUN pip install --upgrade pip
RUN pip install pipenv

WORKDIR ${PROJECT_DIR}
COPY . ${PROJECT_DIR}

RUN pipenv install -r ${PROJECT_DIR}/requirements.txt
RUN pipenv install -e ${PROJECT_DIR}

# COPY wait-for-it.sh ${PROJECT_DIR}/wait-for-it.sh
# RUN chmod +x ${PROJECT_DIR}/wait-for-it.sh

EXPOSE 8000

CMD ["pipenv", "run", "python", "/usr/local/bin/src/OptKG/app.py", "--config", "./config.yaml"]
# CMD ["./wait-for-it.sh", "database:7687", "--", "pipenv", "run", "python", "/usr/local/bin/src/OptKG/app.py", "--config", "./config.yaml"]
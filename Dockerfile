FROM python:3
ENV MONGO_URL mongodb://mongodb_container:27017
ENV DB_NAME clinic_reservation
WORKDIR /app
RUN pip install --upgrade pip
COPY requiremtns.txt .
RUN pip install -r requiremtns.txt
COPY . .
CMD ["python", "manage.py" ,"runserver" ]
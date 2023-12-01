FROM python:3.8

WORKDIR /app
COPY requiremtns.txt .
RUN pip install -r requiremtns.txt
COPY . .
CMD ["python", "manage.py" ,"runserver" ]

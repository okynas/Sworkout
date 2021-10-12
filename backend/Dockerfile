FROM python:3.9
WORKDIR /code

ENV PYTHONPATH "${PYTHONPATH}:/code/app/"
ENV PYTHONUNBUFFERED 1

COPY ./ /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
CMD ['pip' 'install' 'sqlalchemy' 'passlib' 'bcrypt' 'python-jose' 'python-multipart' 'fastapi-mail']
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
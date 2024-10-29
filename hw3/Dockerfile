FROM python:3.12

WORKDIR /app

COPY hw3/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ../lecture_2 /app/lecture_2

EXPOSE 8000

CMD ["uvicorn", "lecture_2.hw.shop_api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# uvicorn lecture_2.hw.shop_api.main:app --host 0.0.0.0 --port 8000
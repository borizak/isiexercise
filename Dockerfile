from python:3.8-alpine
ADD main.py .
ADD back.py .
RUN pip install geopy flask requests
CMD ["python", "./main.py"]

docker build -t python-isibenizakson .
docker run python-isibenizakson
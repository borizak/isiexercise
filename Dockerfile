from python:3.9-alpine
ADD main.py .
ADD back.py .
RUN pip install geopy flask requests
EXPOSE 5000
CMD ["python", "./main.py"]
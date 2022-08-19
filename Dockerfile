from python:3.8-alpine
ADD main.py .
ADD back.py .
RUN pip install geopy flask requests
EXPOSE 5000:5000
CMD ["python", "./main.py"]
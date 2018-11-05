FROM python:2.7-wheezy
COPY src/* /usr/src/app/
COPY requirements.txt ./

EXPOSE 5000

RUN pip install --no-cache-dir -r requirements.txt
CMD ["python","/usr/src/app/api.py"]
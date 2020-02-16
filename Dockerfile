
# load base python image
FROM appsvc/python

LABEL Name=easyauth-for-appservices Version=0.0.1
EXPOSE 5000

WORKDIR /app
ADD app /app

# Using pip:
RUN python3 -m pip install -r requirements.txt

CMD ["python3","/app/main.py"]

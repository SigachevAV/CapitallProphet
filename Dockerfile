FROM python:3.9 
# Or any preferred Python version.
ADD . .
RUN pip install -r ./requirements.txt
CMD python ./index.py
# Or enter the name of your unique directory and parameter set.
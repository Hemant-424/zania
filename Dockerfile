FROM python:3.11

# Set the working directory
WORKDIR /zania

# Copy requirements and install dependencies
COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r /zania/requirements.txt

# Copy the application files
COPY . .

#run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
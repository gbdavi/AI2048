
FROM python:3.9-slim

# Install dependencies
RUN pip install tensorflow==2.9.0 keras-rl2 gym jupyter pandas
RUN pip uninstall numpy -y
RUN pip install numpy==1.24.3

# Config working directory
WORKDIR /app
COPY . /app
ENV PYTHONPATH="/app"

# Jupyter port
EXPOSE 8888

# Run Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

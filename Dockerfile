FROM continuumio/miniconda3
RUN apt-get update && apt-get install -y build-essential

# Create conda environment
COPY environment.yml .
RUN conda env create -f environment.yml -n nauron && rm environment.yml

WORKDIR /app/logs
WORKDIR /app

COPY . .
EXPOSE 5000

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "nauron", "gunicorn", "--config", "config/gunicorn.ini.py", \
"--log-config", "config/logging.ini", "app:app"]
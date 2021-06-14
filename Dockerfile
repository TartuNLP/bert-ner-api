FROM continuumio/miniconda3
RUN apt-get update && apt-get install -y build-essential

# Create conda environment
COPY environment.yml .
RUN conda env create -f environment.yml -n nauron && rm environment.yml

WORKDIR /app/logs
WORKDIR /app
VOLUME /app/models

COPY . .

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "nauron", "python", "bert_ner_worker.py"]
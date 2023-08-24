# Named Entity Recognition API

An API for using the Estonian named entity recognition (NER) service. The service is based on
the [EstBERT_NER](https://huggingface.co/tartuNLP/EstBERT_NER) model.

### Docker setup

The API can be deployed using the docker image published alongside the repository. Each image version correlates to a
specific release. The application can be run with the following command:

```bash
docker run -p 8000:8000 ghcr.io/tartunlp/bert-ner-api:latest
```

The service is available on port `8000`. The API documentation is available under the `/docs` endpoint.

Endpoints for healthcheck probes:

- `/health/startup`
- `/health/readiness`
- `/health/liveness`

#### Configuration

The following environment variables can be specified when running the container:

- `API_MAX_INPUT_LENGTH` (optional) - Maximum request size in character (`10000` by default)
- `API_CONFIG_PATH` (optional) - Path to the configuration file (`config/config.yaml` by default)

Build-time arguments / environment variables:

- `API_VERSION` - A semantic version number, displayed in the docs.

The entrypoint of the container
is `["uvicorn", "app:app", "--host", "0.0.0.0", "--proxy-headers", "--log-config", "config/logging.prod.ini"]`.
`CMD` can be used to define additional [Uvicorn parameters](https://www.uvicorn.org/deployment/). For
example, `["--log-config", "config/logging.debug.ini", "--root-path", "/api/ner"]`
enables debug logging (as the last `--log-config` flag is used) and allows the API to be deployed to the non-root
path `/api/ner`.


#### Manual setup

For a manual/development setup, the following steps can be used:

1. Clone this repository
2. Install the dependencies with `pip install -r requirements.txt`
3. Run the application with `uvicorn app:app`. The model files will be downloaded automatically upon startup.

### Citation

If you use the model or this code in your research, please cite the following paper:

```bibtex
@misc{tanvir2020estbert,
      title={EstBERT: A Pretrained Language-Specific BERT for Estonian}, 
      author={Hasan Tanvir and Claudia Kittask and Kairit Sirts},
      year={2020},
      eprint={2011.04784},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
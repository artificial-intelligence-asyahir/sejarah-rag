FROM dhi.io/python:3.12-alpine

RUN apt-get update

WORKDIR /application

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pipelines/llm_evaluation_pipeline.py /pipelines/llm-evaluation.pipeline.py
COPY steps/ steps/
COPY app/ app/

RUN useradd appuser
USER appuser

CMD ["python", "pipelines/llm_evaluation_pipeline.py"]

FROM python:3.12.10-bookworm

RUN useradd -m sigrh

WORKDIR /home/sigrh/

COPY --chown=1 --chmod=755 requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download es_core_news_lg && python -m spacy download en_core_web_lg

COPY --chown=1 --chmod=755 src ./src/
RUN chown sigrh ./src/database

USER sigrh
CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0"]

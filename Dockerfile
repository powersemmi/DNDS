FROM python:3.11 as builder

ENV PYTHONFAULTHANDLER=1 \
    PYTHONBUFFERED=1 \
    PIP_NO_CACHE_DIR=OFF \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONPATH=/opt/app \
    PDM_VERSION=2.4.*

RUN pip install "pdm==$PDM_VERSION"

RUN pdm config venv.in_project false && \
    pdm config check_update && \
    pdm config python.use_venv false

COPY pyproject.toml pdm.lock README.md /opt/app/

WORKDIR /opt/app

RUN mkdir __pypackages__ && pdm install --prod --no-lock --no-editable

FROM builder

ENV PYTHONPATH=/opt/app/pkgs
COPY --from=builder /opt/app/__pypackages__/3.11/lib /opt/app/pkgs

COPY . .

CMD ["python", "-m", "dnd"]

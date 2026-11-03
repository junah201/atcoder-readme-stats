FROM mcr.microsoft.com/devcontainers/javascript-node:5-24

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV TZ=Asia/Seoul

# timezone
RUN sudo ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ | sudo tee /etc/timezone

USER node
# keep in sync with SERVERLESS_VERSION in .github/workflows/deploy.yml
RUN npm install -g serverless@4.46.0

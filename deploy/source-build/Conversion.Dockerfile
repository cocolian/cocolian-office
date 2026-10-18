FROM docker.io/gotenberg/gotenberg@sha256:3fdee07e0dcd5005c3db4d81d1600d081fc6fb424da87e409e1c1f9624a249b8
ARG SOURCE_COMMIT
LABEL org.opencontainers.image.source="https://github.com/cocolian/online.mirror" org.opencontainers.image.revision=$SOURCE_COMMIT
USER root
COPY stage/opt/collaboraoffice /opt/collaboraoffice
COPY --chmod=755 runtime-tools/source-conversion-service.py /usr/local/bin/source-conversion-service.py
RUN /opt/collaboraoffice/program/soffice --headless --version > /opt/gotenberg/versions/libreoffice-api
USER 1001:1001
CMD ["/usr/bin/python3", "-u", "/usr/local/bin/source-conversion-service.py"]

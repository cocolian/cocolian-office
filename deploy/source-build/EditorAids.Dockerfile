ARG BASE_IMAGE
FROM ${BASE_IMAGE}
USER root
COPY editor-aids.css /usr/share/coolwsd/browser/dist/editor-aids-20261020.css
COPY editor-aids.xcd /opt/collaboraoffice/share/registry/cocolian-editor-aids.xcd
# A new stylesheet URL avoids stale bundle.css caches after a normal reload.
RUN grep -q '</head>' /usr/share/coolwsd/browser/dist/cool.html && \
    sed -i 's#</head>#<link rel="stylesheet" href="%SERVICE_ROOT%/browser/%VERSION%/editor-aids-20261020.css" />\n</head>#' /usr/share/coolwsd/browser/dist/cool.html
USER 1001:1001

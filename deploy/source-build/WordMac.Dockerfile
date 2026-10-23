# Build only on the Linux development VM from the matching compiled engine.
ARG BASE_IMAGE=res.cocolian.cn/cocolian/collabora-source@sha256:00bf584e236fc581b502adb36ec428a4adc75ad5927eaa7632cf87105ae3f08f
FROM ${BASE_IMAGE}
USER root
COPY program/ /opt/collaboraoffice/program/
# Supplied locally from the licensed desktop installation; never committed.
COPY fonts/ /usr/local/share/fonts/word-mac/
COPY word-mac-fontconfig.xml /etc/fonts/word-mac-fontconfig.xml
ENV FONTCONFIG_FILE=/etc/fonts/word-mac-fontconfig.xml COCOLIAN_WORD_MAC_METRICS=1 COCOLIAN_WORD_MAC_CLASSIC_METRICS=1 COCOLIAN_WORD_MAC_AUTOFIT=1 COCOLIAN_WORD_MAC_GRID_BOTTOM=1 COCOLIAN_WORD_MAC_FLEX_SCRIPT_GAPS=1 COCOLIAN_WORD_MAC_LINE_BUDGET=1
RUN fc-cache -f && coolwsd-systemplate-setup /opt/cool/systemplate /opt/collaboraoffice && \
    chown -R 1001:1001 /opt/cool/systemplate
USER 1001:1001

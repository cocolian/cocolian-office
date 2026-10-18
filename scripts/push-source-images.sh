#!/usr/bin/env bash
# Run on codex-dev. AUTH_FILE must be a mode-0600 temporary registry auth JSON.
set -euo pipefail
artifacts=${1:?Usage: push-source-images.sh ARTIFACTS AUTH_FILE}
auth_file=${2:?Temporary auth JSON required}
endpoint=${REGISTRY_TUNNEL:-127.0.0.1:15000}
tag=${SOURCE_TAG:-src-19b4efae7fb8}
for component in collabora libreoffice; do
 archive="$artifacts/$component-source-${tag#src-}.tar"
 expected=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["digest"])' "$archive.json")
 sudo -n skopeo copy --preserve-digests --authfile "$auth_file" --dest-tls-verify=false \
   "oci-archive:$archive" "docker://$endpoint/cocolian/$component-source:$tag"
 actual=$(sudo -n skopeo inspect --authfile "$auth_file" --tls-verify=false --format '{{.Digest}}' "docker://$endpoint/cocolian/$component-source:$tag")
 test "$actual" = "$expected"
 printf '%s\n' "res.cocolian.cn/cocolian/$component-source@$actual"
done

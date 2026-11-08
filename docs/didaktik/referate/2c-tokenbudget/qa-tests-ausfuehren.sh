#!/usr/bin/env bash
set -euo pipefail
study=$(cd "$(dirname "$0")" && pwd)
repo=$(git -C "$study" rev-parse --show-toplevel)
release=87c39334619fbcb0c5782b061da1ba0df0ba3142
scratch=${TOPIC2C_SCRATCH:-"$repo/tmp/topic2c"}
src="$scratch/release"
out=${OUT:-"$scratch/replay"}
sdk=arsnova-wsl-gpu-sdk:7.14.1
node_image=node:24-bookworm-slim@sha256:8cabefbd444809cf0e319b5831c65da1ea202200ca552a5e75fd7938a6f86658
mkdir -p "$src" "$out"
common=(--rm --user "$(id -u):$(id -g)" --cpus 4 --memory 8g --memory-swap 8g --pids-limit 256 --cap-drop ALL --security-opt no-new-privileges)
mounts=(-v "$src:/release" -v "$study/qa-kurzfassung-tokenbudget.test.ts:/release/apps/backend/src/lib/topic2c.experiment.test.ts:ro" -v "$out:/evidence" -e EVIDENCE=/evidence -w /release/apps/backend)
case "${1:-}" in
 setup)
  if [[ -e "$src/package.json" ]]; then echo 'Use a fresh scratch directory for setup.' >&2; exit 2; fi
  git -C "$repo" archive "$release" | tar -x -C "$src"
  docker run "${common[@]}" -v "$src:/release" -w /release -e npm_config_cache=/tmp/npm "$node_image" sh -ec 'npm ci --ignore-scripts --no-audit --no-fund && node_modules/.bin/prisma generate && npm run build:libs' > "$out/setup.log" 2>&1 ;;
 pack)
  docker run "${common[@]}" --network none "${mounts[@]}" -e ONLY_PACK=1 "$node_image" sh -ec 'mkdir -p /release/.study-node && cp /usr/local/bin/node /release/.study-node/node && node ../../node_modules/vitest/vitest.mjs run --maxWorkers=1 src/lib/topic2c.experiment.test.ts' ;;
 measure)
  [[ ! -e "$out/environment.json" ]] || { echo 'Use a new OUT; previous measurements are never overwritten.' >&2; exit 2; }
  [[ -c /dev/dxg && -x "$src/.study-node/node" ]] || { echo 'Need local WSL GPU and successful pack.' >&2; exit 2; }
  cp "$study/qa-kurzfassung-tokenbudget.test.ts" "$out/"
  docker image inspect --format '{{.Id}}' "$sdk" > "$out/image-id.txt"
  docker run "${common[@]}" --network none --device /dev/dxg "${mounts[@]}" -v /usr/lib/wsl/lib/libdxcore.so:/usr/lib/libdxcore.so:ro -v "$repo/tmp/wsl-gpu-validation:/gpu:ro" -v "$study/qwen-testserver.py:/study/qwen-testserver.py:ro" "$sdk" timeout -k 10 870 python3 /study/qwen-testserver.py ;;
 *) echo 'Usage: qa-tests-ausfuehren.sh setup|pack|measure' >&2; exit 2 ;;
esac

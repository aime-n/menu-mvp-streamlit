#!/bin/bash
set -euxo pipefail

poetry lock

./scripts/clean.sh
./scripts/test.sh

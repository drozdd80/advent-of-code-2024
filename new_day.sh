#! /bin/bash
set -euo pipefail

# shellcheck disable=SC2034
script_dir="$(cd "$(dirname "$0")" && pwd)"
project_root="$(git rev-parse --show-toplevel)"

source_dir="${project_root}/sample"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -n|--dir-name)
      if [ -z "$2" ] || [[ "$2" == -* ]]; then
        echo "Error: $1 requires an argument."
        usage
      fi
      dirname="$2"
      shift 2
      ;;
    *)
      break
      ;;
  esac
done

to_dir="${project_root}/${dirname}"

cp -r "$source_dir" "$to_dir"

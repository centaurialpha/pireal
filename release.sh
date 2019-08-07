#!/bin/bash

VERSION=$1
TEXT=$2
FILE_TO_UPLOAD=$3
BRANCH=$(git rev-parse --abbrev-ref HEAD)
REPO_FULL_NAME=$(git config --get remote.origin.url | sed 's/.*:\/\/github.com\///;s/.git$//')
TOKEN=$(git config --global github.token)

generate_post_data()
{
  cat <<EOF
{
  "tag_name": "$VERSION",
  "target_commitish": "$BRANCH",
  "name": "$VERSION",
  "body": "$TEXT",
  "draft": false,
  "prerelease": false
}
EOF
}

echo "Create release $VERSION for repo: $REPO_FULL_NAME branch: $BRANCH"
release_code=$(curl --silent --output /dev/null --write-out "%{http_code}" --data "$(generate_post_data)" "https://api.github.com/repos/$REPO_FULL_NAME/releases?access_token=$TOKEN")

if [[ $release_code != 200 ]]; then
  echo "Algo ha salido mal"
  echo "Code: $release_code"
  exit 1
fi

last_id=$(curl --silent "https://api.github.com/repos/centaurialpha/$REPO_FULL_NAME/latest" | head -n 6 | grep '"id"' | grep -o '[[:digit:]]\+')

echo "Subiendo $(basename $FILE_TO_UPLOAD)..."
upload_code=$(curl --silent --output /dev/null --write-out "%{http_code}" "https://uploads.github.com/repos/$REPO_FULL_NAME/releases/$last_id/assets?access_token=$TOKEN&name=$(basename $FILE_TO_UPLOAD)" --header 'Content-Type: application/zip' --upload-file $FILE_TO_UPLOAD -X POST)

if [[ $upload_code != 200 ]]; then
  echo "Algo ha salido mal"
  echo "Code: $upload_code"
  exit 1
fi
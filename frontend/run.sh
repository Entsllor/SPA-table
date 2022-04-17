#!/bin/sh

case $1 in
  start)
    npm start | cat
    ;;
  build)
    npm build
    ;;
  test)
    npm test $@
    ;;
  *)
    npm "$@"
    ;;
esac

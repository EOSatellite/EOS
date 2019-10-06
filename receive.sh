#!/bin/sh

if [ ! "$(command -v vim)" ]; then exit; fi

echo "Waiting for data..."
sh -c "tail -f /dev/ttyACM0 | { sed "/deadff/ q" && kill $$ ;}" > hexdump

sed -i "$ d" hexdump
xxd -p -r hexdump > received_data.jpg
xdg-open received_data.jpg

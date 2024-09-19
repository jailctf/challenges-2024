#!/bin/sh
socat TCP-LISTEN:4444,reuseaddr,fork EXEC:"node bot.js"
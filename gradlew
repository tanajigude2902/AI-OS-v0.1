#!/bin/sh

if [ -n "$JAVA_HOME" ] ; then
    JAVACMD="$JAVA_HOME/bin/java"
else
    JAVACMD="java"
fi

if ! command -v "$JAVACMD" >/dev/null 2>&1 ; then
    echo "ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH." >&2
    exit 1
fi

APP_DIR=`dirname "$0"`

# System gradle check
if command -v gradle >/dev/null 2>&1 ; then
    exec gradle "$@"
fi

# Wrapper jar check
if [ -f "$APP_DIR/gradle/wrapper/gradle-wrapper.jar" ]; then
    exec "$JAVACMD" -jar "$APP_DIR/gradle/wrapper/gradle-wrapper.jar" "$@"
fi

# Fallback auto-download for CI
WRAPPER_DIR="$APP_DIR/gradle/wrapper"
mkdir -p "$WRAPPER_DIR"
if command -v curl >/dev/null 2>&1 ; then
    curl -sLo "$WRAPPER_DIR/gradle-wrapper.jar" "https://raw.githubusercontent.com/gradle/gradle/v8.7.0/gradle/wrapper/gradle-wrapper.jar" || true
fi

if [ -f "$WRAPPER_DIR/gradle-wrapper.jar" ]; then
    exec "$JAVACMD" -jar "$WRAPPER_DIR/gradle-wrapper.jar" "$@"
else
    exec gradle "$@"
fi

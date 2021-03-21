#!/bin/bash

# USAGE:
# ./zth-jwt.bash public-key.pem JWT
# Example
# ./zth-jwt.bash jwt-auth-server-public-key.pem eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJQYXJhZG94IiwiaWF0IjoxNjE2MzQ0NDAyLCJleHAiOjE2MTYzNDQ1MjIsImRhdGEiOnsicGluZ3UiOiJub290cyJ9fQ.Puej1hnMVYNgXiUvqienWlQ9L2G4rsJSt0--HUS-kg_FJ

PUBLIC_KEY_FILE=$1
shift
JWT=$1
shift

# use jwt header "alg":'HS256"
JWT_HEADER=$(cut -d'.' -f1 <<<"$JWT")
JWT_PAYLOAD=$(cut -d'.' -f2 <<<"$JWT")

PUBLIC_KEY_IN_HEX=$(cat "${PUBLIC_KEY_FILE}" | xxd -p | tr -d '\\n')
echo public key "${PUBLIC_KEY_IN_HEX}"

# waiting for fix of https://github.com/openssl/openssl/issues/10814
SIGNATURE_IN_HEX=$(echo -n "${JWT_HEADER}.${JWT_PAYLOAD}" | openssl dgst -sha256 -mac HMAC -macopt hexkey:${PUBLIC_KEY_IN_HEX})
echo singature in hex "$SIGNATURE_IN_HEX"

SIGNATURE_IN_BASE64=$(python2 -c "exec(\"import base64, binascii\nprint base64.urlsafe_b64encode(binascii.a2b_hex('${SIGNATURE_IN_HEX}')).replace('=','')\")")
echo singature in base64 "$SIGNATURE_IN_BASE64"

echo 'final jwt is'
echo "${JWT_HEADER}.${JWT_PAYLOAD}.${SIGNATURE_IN_BASE64}"

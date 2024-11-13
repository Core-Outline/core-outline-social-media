import urllib.parse


def sanitizeParams(params):
    url = f"https://example.com?params1={params}"
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qsl(parsed_url.query)
    sanitized_params = urllib.parse.urlencode(query_params, safe='')

    sanitized_url = urllib.parse.urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        sanitized_params,
        parsed_url.fragment
    ))

    params = str(sanitized_url).replace("https://example.com?params1=","")
    return params

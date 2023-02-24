This directory contains sample deployment scenarios for Silicon Notes.

Because this is just a simple [Python]/[Flask] app at heart, there are _many_ ways to successfully deploy it. These examples can serve as reasonable starting points for deploying to your own local server or public Internet host.

Although the author is not an expert on every application hosting method/platform available, please feel free to file an issue if you have any questions about deploying Silicon Notes to your stack.

These are the sample deployments documented so, far, in rough order of
increasing complexity:

* `docker-local`: The simplest possible `docker-compose.yaml` file for bringing up Silicon Notes on a localhost IP on port 5000.
* `caddy-basic-auth`: Spin up an instance with single-user HTTP Basic Authentication with Caddy.
* `caddy-authelia`: A docker-compose deployment utilizing Authelia (and LLDAP) for multi-user single sign-on.

[Python]: https://www.python.org
[Flask]: https://flask.palletsprojects.com/en/2.2.x/

When testing any of these out, be aware that running Caddy and having it generate a TLS certificate _will_ get your site scanned by bots looking for vulnerabilities. Caddy (and other web servers) automatically request TLS certificates for HTTPS and a side-effect of this is that the details of these certificates get written to a public log. This means you have to be _extra careful_ about not spinning up a service with half-baked security or permissions or you are _very_ likely to get pwned immediately. Some of us consider this situation something of an unfortunate and bitter irony. These efforts to produce a more secure web have the unintended side-effect of leading potential attackers straight to your front door while the house is still under construction.

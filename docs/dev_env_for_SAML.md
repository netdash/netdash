# Creating an environment to develop SSO components

## SAML

These instructions assume you have a working instance of NetDash (for QA or testing) configured to use SAML for authentication at https://netdash-test.example.com/

  1. Update your `settings` module's `_saml2_*` variables to use the same values as the configurations used for the https://netdash-test.example.com/ instance.
  2. Add `127.0.0.1 netdash-test.example.com` to your development machine's /etc/hosts file.
  3. Use [mitmproxy](https://mitmproxy.org/) to reverse proxy your local development instance with HTTPS on port 443: `mitmdump -p 443 --mode reverse:http://localhost:8888/` (make sure the port on the localhost address matches the port of your development instance).
  4. Go to https://netdash-test.example.com/ in your browser.
  5. You will have to accept the cert mitmproxy is using.
  
Logging in to this instance off the app should redirect you to the IdP configured for netdash-test.example.com, and then redirect you back after you've authenticated there. Note that we're tricking the browser and the IdP into thinking that your development instance is the real netdash-test.example.com.

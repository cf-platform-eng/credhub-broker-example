# credhub-broker-example

## Dev

Copy `local_dev.sh.template` to `local_dev.sh` and customize to your environment, then run via

```bash
local_dev.sh
```

* `./consumer` is an app meant to be bound to the service broker, that will display environment variables
* `./proxy` is an app that exposes `credhub.service.cf.internal:8844` outside, to test API calls more easily.
    - Do not leave proxy deployed; it's only meant for local testing

## Creating a UAA Client

To create a UAA user that can read and write to CredHub, use
the [UAA CLI](https://docs.cloudfoundry.org/uaa/uaa-user-management.html).

Create the client:

```bash
uaac target https://uaa.sys.<pcf system domain>
uaac token client get admin -s <admin client secret>
uaac client add my-broker \
  --name my-broker \
  --secret <my-broker client secret> \
  --authorized_grant_types client_credentials,refresh_token \
  --authorities oauth.login,credhub.read,credhub.write
```

To manually get a token:

```bash
uaac token client get my-broker -s <my-broker client secret>
uaac context
``` 

## References
* https://docs.pivotal.io/tiledev/ssi-creds-tiledev.html
* https://credhub-api.cfapps.io/
* https://docs.pivotal.io/tiledev/credhub.html

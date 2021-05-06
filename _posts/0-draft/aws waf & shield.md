## Waf & Shield

### resource type
* Cloudfront distributions
* Regional resources

### rules type

IP set

rule builder

* Originates from a country in
* Ortginates from an IP address in
* Has a label
* Request components
    - Header
    - Single query parameter
    - All query parameters
    - URI path
    - Query string
    - Body
    - HTTP method

rule group

### notices

* The cloudfront service and the eks service are located in different regions, so they cannot use the same waf.

*  The associated regional resources type below list, and there is no network load balancer.
	- Amazon API gateway
	- Application load balancer
	- AWS appsync

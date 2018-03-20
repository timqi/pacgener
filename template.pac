var proxy = __PROXY__;
var domains = __DOMAINS__;
var direct = 'DIRECT;';
function FindProxyForURL(url, host) {
    var lastPos = host.lastIndexOf('.');
    while(lastPos >= 0) {
        var domain = host.slice(lastPos+1);
        if (domains.hasOwnProperty(domain)) {
            return proxy;
        }
        lastPos = host.lastIndexOf('.', lastPos-1);
    }
    return domains.hasOwnProperty(host)?proxy:direct;
}

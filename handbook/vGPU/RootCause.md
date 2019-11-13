# I think 70% chance is due to the MTU. If MTU problem, we need ask TS side to change to 4K
 
- Better confirm this below log with Jim BitFusiion side.
  "Receiving magic number" is usually caused when assembling the IP frames due to the long IP frames falling in many segments by MTU cut
 
- Detail is https://en.wikipedia.org/wiki/Jumbo_frame
  And, The log here was found after the executed “nvida-smi”


I found the root case here, from CDSW container -> connecting to the working ports 55001~55100 range

```bash
cdsw@q4ohm497ulxvrl8g:~/.bitfusionio$ more bf_Global.q4ohm497ulxvrl8g.log
[ INFO] 2019-11-13T03:10:27.076929Z, 233, "Statistics capture disabled."
[ INFO] 2019-11-13T03:10:27.077036Z, 233, "Loading server list from config file '/tmp/flexdirect487561532'"
[ INFO] 2019-11-13T03:10:27.077067Z, 233, "Using server 10.91.146.61:55003"
[ INFO] 2019-11-13T03:10:27.078591Z, 233, "RPC client supported transports: tcp"
[ INFO] 2019-11-13T03:10:27.097800Z, 233, "Starting network discovery with 19 servers"
[ERROR] 2019-11-13T03:16:06.591006Z, 234, __"Receiving magic number"__
[ WARN] 2019-11-13T03:16:06.592473Z, 237, "create_client_socket: Error connecting to server 10.91.146.61:55011, error 111: Connection refuse
d"
[ INFO] 2019-11-13T03:16:06.593060Z, 233, "Network discovery finished in 339.495 seconds"
[ INFO] 2019-11-13T03:16:06.593102Z, 233, "RPC client supported transports: tcp"
[ INFO] 2019-11-13T03:16:06.593108Z, 233, "Network config not specified, using enabled transports 1"
[ INFO] 2019-11-13T03:16:06.593128Z, 233, "Using direct connection from client to server"
[ERROR] 2019-11-13T03:16:06.593312Z, 233, "Unable to connect to server, the initial handshake failed"
```
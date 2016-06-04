# qb
qb (pronounced "*cube*") is a cross-platform toolkit for **system containers** inspired by the **application container** stack by Docker.

### Why not Docker?
```docker``` is great, we love it, but it's not suitable for everything. Docker is an **application container** technology, meaning it's intended to wrap a single process such as Apache, Nginx or MySQL. However, not everyone is in the position to adopt a micro-service infrastructure. Perhaps you have legacy systems to support, maybe you rely on other services a full system would provide such as systemd, cron or syslog. In these cases you either simply can't use Docker at all, or you have to hack it to work in a way in which it was never intended to be used, which can cause buggy behaviour.

```qb``` provides Docker-like functionality but is different in that it utilises **system containers**, meaning you don't need to choose a single process to wrap, the container boots all of the services you'd expect from a regular Linux distribution.

### Tools
#### qb machine
#### qb container
#### qb registry
#### qb network
#### qb compose

### Installation
TODO

### Usage
TODO
```bash
qb --help
```

### Contribute
As always, we welcome **pull requests** with open arms. Hack away!

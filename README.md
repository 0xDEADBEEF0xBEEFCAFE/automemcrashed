# AUTO-MEMCRASHED

This tool allows you to send forged UDP packets to Memcached servers specified in a list.

### Dependencies

- `python3`
- `pip3`
- `scapy`
- file containing Memcached servers with 1 IP per line (not included)

### Using virtualenv:

```bash
sudo -HE PATH=$PATH python3 memcrashed.py
```

### Using Docker

```bash
git clone https://github.com/0xDEADBEEF0xBEEFCAFE/automemcrashed.git
cd automemcrashed
docker build -t memcrashed .
docker run -it --rm memcrashed
# python3 memcrashed.py -t [TARGET IP] -p [TARGET PORT]
```

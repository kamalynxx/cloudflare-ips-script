#!/usr/bin/env python3
import argparse
import urllib.request
from typing import Union
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Download latest list of CloudFlare IPs '
        'and write as nginx config file.',
        epilog='Config will be saved to '
        '/etc/nginx/conf.d/cloudflare.conf by default.',
    )
    parser.add_argument(
        '-d',
        '--dir',
        default=Path('/etc/nginx/conf.d/'),
        type=str,
        help='set directory to download config',
    )
    args = parser.parse_args()
    path = Path(args.dir)

    base_url = 'https://www.cloudflare.com'
    headers = {'User-Agent': 'Firefox'}
    ip4_request = urllib.request.Request(
        base_url + '/ips-v4/', headers=headers
    )
    ip6_request = urllib.request.Request(
        base_url + '/ips-v6/', headers=headers
    )

    with urllib.request.urlopen(ip4_request) as client:
        ip4_result = client.read().decode('utf-8')

    with urllib.request.urlopen(ip6_request) as client:
        ip6_result = client.read().decode('utf-8')

    ips = ip4_result.split('\n') + ip6_result.split('\n')

    nginx_config = '\n'.join(map(lambda ip: f'set_real_ip_from {ip};', ips))

    with open(path / 'cloudflare.conf', 'w+') as file:
        file.write(nginx_config + '\n')


if __name__ == '__main__':
    main()

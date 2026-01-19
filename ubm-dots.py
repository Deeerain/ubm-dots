#!/bin/python3
import typer
import urllib.request
import json
import subprocess
import os
import pathlib
from typing import List, Optional, Dict
from enum import Enum

REPO_OWNER = 'deeerain'
REPO_NAME = 'ubm-dots'
REPO_API_URL = f'https://api.github.com/repos/{REPO_OWNER}/{
    REPO_NAME}/releases/latest'

app = typer.Typer()


class Service(Enum):
    HYPRLAND = 'hyprland'
    WAYBAR = 'waybar'


def get_latest_repo_info(owner: str, repo_name):
    url = f'https://api.github.com/repos/{owner}/{repo_name}/releases/latest'

    request = urllib.request.Request(url)

    with urllib.request.urlopen(request) as response:
        data = json.loads(response.read().decode('utf-8'))
        return data


def setup_zst(filepath: pathlib.Path):
    if not filepath.exists():
        return

    subprocess.run(f'sudo pacman -U {filepath}'.split())


def download_zst(download_url: str, filepath: pathlib.Path) -> Optional[str]:
    result = urllib.request.urlretrieve(download_url, filepath)
    if len(result) > 0:
        return result[1]
    return None


def find_zst_file(assets: List[Dict]) -> Optional[Dict]:
    for asset in assets:
        filename = asset.get('name')

        if not filename:
            continue

        if filename.endswith('.zst'):
            return asset


def get_current_version() -> str:
    result = subprocess.run(
        f'pacman -Q {REPO_NAME}'.split(), capture_output=True)
    version = result.stdout.decode('utf-8').split()[1]

    if version.startswith('v'):
        version = version[1:]

    return version


def is_newest_version(ver1: str, ver2: str) -> bool:
    ver1_parts = list(map(int, ver1.replace('-', '.').split('.')))
    ver2_parts = list(map(int, ver2.replace('-', '.').split('.')))

    while len(ver1_parts) < 3:
        ver1_parts.append(0)
    while len(ver2_parts) < 3:
        ver2_parts.append(0)

    for i in range(3):
        if ver1_parts[i] > ver2_parts[i]:
            return True
        elif ver1_parts[i] < ver2_parts[i]:
            return False

    return False


@app.command('update')
def update():
    repo_info = get_latest_repo_info(REPO_OWNER, REPO_NAME)
    assets = repo_info.get('assets')
    asset = find_zst_file(assets)

    filename = asset.get('name')
    filepath = pathlib.Path('/tmp/', filename)
    download_url = asset.get('browser_download_url')

    latest_version = repo_info.get('tag_name')
    current_version = get_current_version()

    if latest_version.startswith('v'):
        latest_version = latest_version[1:]

    if not is_newest_version(latest_version, current_version):
        return

    download_zst(download_url, filepath)

    setup_zst(filepath)

    if typer.confirm('Clean cache?', default=True):
        typer.echo(f'   Remove {filepath}')
        if filepath.exists():
            os.remove(filepath)


@app.command('reload')
def reload(
        services: List[Service] = typer.Option(
            [Service.HYPRLAND, Service.WAYBAR], '--services', '-s')
):
    for service in services:
        try:
            match service:
                case Service.HYPRLAND:
                    typer.echo('Reloading hyprland...', color=True)
                    subprocess.run(['hyprctl', 'reload'])
                case Service.WAYBAR:
                    typer.echo('Reloading waybar')
                    subprocess.run(['killall', 'waybar'])
                    subprocess.run(['hyprctl', 'dispatch', 'exec', 'waybar'])
        except subprocess.CalledProcessError as e:
            typer.echo(f'Called error: {e}')


if __name__ == '__main__':
    app()

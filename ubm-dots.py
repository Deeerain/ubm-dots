#!/bin/python3
import typer
import urllib.request
import json
import subprocess
from typing import Optional, Dict, List, Any, Type, Self
from enum import Enum
from abc import ABC, abstractmethod

REPO = 'https://api.github.com/repos/deeerain/ubm-dots/releases/latest'

app = typer.Typer()


class AbstractCommand(ABC):
    @abstractmethod
    def run(self) -> Any:
        raise NotImplementedError


class CommandBase(AbstractCommand):
    def __init__(self, command: str):
        self.command = command
        self.args = []

    def arg(self, arg: str) -> Self:
        self.args.append(arg)
        return self


class NativeCommand(CommandBase):
    def run(self):
        subprocess.run([self.command, *self.args])


class AbstractService(ABC):
    @abstractmethod
    def run(self, *args: List[str]):
        raise NotImplementedError()


class BaseService(AbstractService):
    def __init__(self, runner: Type[AbstractCommand]):
        self.runner = runner

    def run(self, *args: List[str]):
        self.runner.run(*args)


class Github:
    def __init__(self, repo_owner: str, repo_name: str):
        self.api_base = f'https://api.github.com/repos/{
            repo_owner}/{repo_name}'

    def get_latest_release_info(self) -> Optional[Dict]:
        url = f'{self.api_base}/releases/latest'

        try:
            req = urllib.request.Request(url)

            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    return data
                else:
                    return None
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print('Repo not found')
                return None
        except Exception as e:
            print(f'Error: {e}')
            return None

    def list_assets(self, release_info: Dict) -> List[Dict]:
        assets = release_info.get('assets', [])

        if not assets:
            print("Files not found")
            return []

        for i, asset in enumerate(assets, 1):
            name = asset.get('name', 'Unknown')
            size = asset.get('size', 0)
            downloads = asset.get('download_count', 0)
            size_md = size / (1024 * 1024)

            print(f'    {i}. {name}')
            print(f'    Size: {size_md:.2f} MB, Downloads: {downloads}')

        return assets

    def download_latest_release(
            self, ext: str, *, release_info: Optional[Dict] = None):
        if release_info is None:
            release_info = self.get_latest_release_info()

    def get_tag_name(
            self, release_info: Optional[Dict] = None) -> Optional[str]:
        if release_info is None:
            release_info = self.get_latest_release_info()

        tag_name = release_info.get('tag_name')

        return tag_name

    def is_newer_version(
        self,
        current_version: str,
        release_info: Optional[Dict]
    ) -> bool:
        pass


class Command(AbstractCommand):
    @classmethod
    def run(cls, *args: List[str]) -> subprocess.CompletedProcess[str]:
        try:
            if not any(args):
                raise ValueError('Empty', args)

            return subprocess.run(args)
        except subprocess.CalledProcessError as e:
            raise cls.CommandException(f'Command error: {e}')


class Hyprland(BaseService):
    def __init__(self):
        pass

    def _ctl(self, *args: list[str]):
        try:
            self.run('hyprctl', *args)
        except (Command.CommandException, ValueError) as e:
            print(f'Error: {e}')

    def _dispatch(self, *args: List[str]):
        self._ctl('dispatch', *args)

    def exec(self, *args: List[str]):
        self._dispatch('exec', *args)

    def reload(self):
        self._ctl('reload')

    def exit(self):
        self._ctl('exit')


class Waybar(BaseService):
    def kill(self):
        self.run(['killall', 'waybar'])

    def run(
            self, *,
            hypr_service: Hyprland,
            config_file: Optional[str] = None,
            style_file: Optional[str] = None
    ):
        cmd = []

        if config_file:
            cmd.append(['-c', config_file])

        if style_file:
            cmd.append(['-s', style_file])

        hypr_service.exec('waybar', *cmd)

    def reload(self, hypr_service: Hyprland):
        self.kill()
        self.run(hypr_service=hypr_service)


class Service(Enum):
    HYPRLAND = 'hyprland'
    WAYBAR = 'waybar'


class UBM:
    hyprland = Hyprland(Command)
    waybar = Waybar(Command)

    @classmethod
    def reload(
            cls, services: List[Service] = [Service.HYPRLAND, Service.WAYBAR]):
        for service in services:
            match service:
                case Service.HYPRLAND:
                    cls.hyprland.reload()
                case Service.WAYBAR:
                    cls.waybar.reload()


def get_local_version():
    result = subprocess.run(
        ['pacman', '-Q', 'ubm-dots'],
        capture_output=True,
    )

    if result.stdout:
        return result.stdout.decode('utf-8').split()[1]


def get_latest_version():
    headers = {
        'User-Agent': 'Mozila/5.0 (Python)',
        'Accept': 'application/json',
    }

    req = urllib.request.Request(REPO, headers=headers)

    with urllib.request.urlopen(req, timeout=10) as response:
        if response.status == 200:
            data = json.loads(response.read().decode('utf-8'))

            tag_name = data.get('tag_name')

            if tag_name.startswith('v'):
                tag_name = tag_name[1:]

            return tag_name


def is_newer_version(v1: str, v2: str) -> bool:
    try:
        v1_parts = list(map(int, v1.split('.')))
        v2_parts = list(map(int, v2.split('.')))

        while len(v1_parts) < 3:
            v1_parts.append(0)
        while len(v2_parts) < 3:
            v2_parts.append(0)

        for i in range(3):
            if v1_parts[i] > v2_parts[i]:
                return True
            elif v1_parts[i] < v2_parts[i]:
                return False

        return False
    except (ValueError, AttributeError):
        return False


def check_updates() -> bool:
    version_current = get_local_version()
    version_latest = get_latest_version()

    return is_newer_version(version_latest, version_current)


@app.command('reload', help='Reload hyprland and waybar')
def reload(services: List[Service] = typer.Option(None, '--service', '-s')):
    try:
        if services:
            UBM.reload(services)
            return typer.Exit(1)

        UBM.reload()
    except subprocess.CalledProcessError as e:
        typer.echo(f'Filed to reload ubm-dots: {e}')
        typer.Exit(1)


@app.command('exit', help='Close user session')
def exit():
    try:
        UBM.hyprland.exit()
    except subprocess.CalledProcessError as e:
        typer.echo(f'Filed to close session: {e}')
        typer.Exit(1)


@app.command('update')
def update(check: bool = typer.Option(False, '--check', '-c')):
    if check and check_updates():
        typer.echo('New version!')
        typer.Exit(1)

    github = Github('deeerain', 'ubm-dots')
    lat_rel = github.get_latest_release_info()

    print(lat_rel)

    if lat_rel:
        assets = github.list_assets(lat_rel)
        print(assets)


if __name__ == '__main__':
    app()

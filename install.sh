#!/bin/bash

packages=(
  "hypr"
  "hyprpaper"
  "hyprlock"
  "exe"
  "zsh"
  "btop"
  "wofi"
  "waybar"
  "kitty"
  "fastfetch"
  "git"
  "nwg-look"
  "udiskie"
)

pm=""
missing_packages=()
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

print() {
  local msg="$1"
  echo -e "${GREEN}$msg${NC}"
}

eprint() {
  local msg="$1"
  echo -e "${RED}$msg${NC}"
}

get_pm() {
  if command -v apt >/dev/null 2>&1; then
    pm="apt"
  elif command -v dnf >/dev/null 2>&1; then
    pm="dnf"
  elif command -v yum >/dev/null 2>&1; then
    pm="yum"
  elif command -v pacman >/dev/null 2>&1; then
    pm="pacman"
  elif command -v zypper >/dev/null 2>&1; then
    pm="zypper"
  elif command -v emerge >/dev/null 2>&1; then
    pm="emerge"
  else
    eprint "Package manager not found"
    return 1
  fi
}

check_package() {
  local package="$1"

  case "$pm" in
  "apt")
    if dpkg -l | grep -q "^ii $package "; then
      print "Package: $package - installed"
    else
      eprint "Package: $package - NOT installed"
      missing_packages+=("$package")
    fi
    ;;
  "dnf" | "yum")
    if rpm -q "$package" >/dev/null 2>&1; then
      print "Package: $package - installed"
    else
      eprint "Package: $package - NOT installed"
      missing_packages+=("$package")
    fi
    ;;
  "pacman")
    if pacman -Qs "$package" >/dev/null 2>&1; then
      print "Package: $package - installed"
    else
      eprint "Package: $package - NOT installed"
      missing_packages+=("$package")
    fi
    ;;
  "zypper")
    if zypper search --installed-only "$package" >/dev/null 2>&1; then
      print "Package: $package - installed"
    else
      eprint "Package: $package - NOT installed"
      missing_packages+=("$package")
    fi
    ;;
  "emerge")
    if qlist -I "$package" >/dev/null 2>&1; then
      print "Package: $package - installed"
    else
      eprint "Package: $package - NOT installed"
      missing_packages+=("$package")
    fi
    ;;
  esac
}

install_packages() {
  case "$pm" in
  "apt")
    sudo apt install "$@"
    ;;
  "pacman")
    sudo pacman -S "$@"
    ;;
  "zypper")
    zypper install "$@"
    ;;
  "emerge")
    emerge "$@"
    ;;
  esac
}

check_dependensies() {
  for package in "$@"; do
    check_package "$package"
  done
}

copy_config_files() {
  cp -r ./hypr ~/.config/
  cp -r ./fastfetch ~/.config/
  cp -r ./hypr ~/.config/
  cp -r ./kitty ~/.config/
  cp -r ./waybar/ ~/.config/
  cp -r ./wofi ~/.config/
  cp ./.zshrc ~/
  sudo cp -r ./Catppuccin-Dark-Frappe /usr/share/themes/
}

main() {
  echo -e "\tGet package manager...\n"

  get_pm

  print "Using package manager: $pm\n"

  echo -e "\tCheck packages...\n"

  check_dependensies "${packages[@]}"

  if [ ${#missing_packages[@]} -eq 0 ]; then
    echo "\tPackages allready installed!"
  else
    eprint "\nMissing packages: $missing_packages\n"
    read -e -p "Install missing packages? (default y, n): " -i "y" answer
    case "$answer" in
    "y" | "Y") install_packages "${missing_packages[@]}" ;;
    *) ;;
    esac
  fi

  echo -e "Copy configuration files...\n"

  copy_config_files

  print "\tDone!\n"
}

clear

echo -e '\033[0;35m'
echo -e "\t####################"
echo -e "\t# Dots by Deeerain #"
echo -e "\t####################"
echo -e "${NC}"

sleep 1

read -e -p "Install dots? [y, (Default) n]: " -i "n" answer

case "$answer" in
"y" | "Y") main ;;
*) ;;
esac

pkgname=ubm-dots
pkgver=0.0.3
pkgrel=2
pkgdesc="Personal dotfiles for Arch + Hyprland"
arch=('any')
url="https://github.com/Deeerain/ubm-dots"
makedepends=('git')
depends=(
  'hyprland>=0.53.0'
  'hyprpaper'
  'hyprlock'
  'mako'
  'btop'
  'git'
  'grim'
  'slurp'
  'zsh'
  'zsh-autosuggestions'
  'zsh-syntax-highlighting'
  'exa'
  'nwg-look'
  'kitty')
optgepends=(
  'catppuccin-gtk-theme-frappe: Gtk theme (AUR)'
  'gdm: Gnome Display Manager'
  'cassette: Yandex Music Clinet (AUR)')
source=("git+https://github.com/deeerain/ubm-dots.git#tag=v$pkgver")
sha256sums=('SKIP')
install=ubm-dots.install

package() {
  cd "$srcdir/$pkgname"

  local install_dir="$pkgdir/etc/skel"

  install -dm755 "$install_dir/.config/hypr"
  install -dm755 "$install_dir/.config/waybar"
  install -dm755 "$install_dir/.config/wofi"
  install -dm755 "$install_dir/.config/mako"
  install -dm755 "$install_dir/.config/fastfetch"
  install -dm755 "$install_dir/.config/kitty"

  cp -r dots/hypr "$install_dir/.config"
  cp -r dots/waybar "$install_dir/.config"
  cp -r dots/wofi "$install_dir/.config"
  cp -r dots/mako "$install_dir/.config"
  cp -r dots/fastfetch "$install_dir/.config"
  cp -r dots/kitty "$install_dir/.config"

  install -Dm664 dots/.zshrc "$install_dir"
}

pkgname=my-dots
pkgver=0.1.0
pkgrel=1
pkgdesc="Personal dotfiles for Arch + Hyprland"
arch=('any')
url="https://github.com/Deeerain/my-dots"
makedepends=('git')
depends=('hyprland'
  'hyprpaper'
  'mako'
  'btop'
  'git'
  'grim'
  'slurp'
  'zsh'
  'zsh-autosuggestions'
  'zsh-syntax-highlighting'
  'exa'
  'nwg-look')
optgepends=('catppuccin-gtk-theme-frappe: Gtk theme (AUR)')
source=("git+https://github.com/deeerain/my-dots.git")
sha256sums=('SKIP')
install=my-dots.install

package() {
  cd "$srcdir/$pkgname"

  # Hyprland and Hyprpaper
  install -dm755 "$pkgdir/etc/skel/.config/hypr"
  cp -r dots/hypr/* "$pkgdir/etc/skel/.config/hypr"

  # Waybar
  install -dm755 "$pkgdir/etc/skel/.config/waybar"
  cp -r dots/waybar/* "$pkgdir/etc/skel/.config/waybar"

  # Zsh
  cp -r dots/.zshrc "$pkgdir/etc/skel/"
}

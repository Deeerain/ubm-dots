export ZSH="$HOME/.oh-my-zsh"
export SUDO_EDITOR=vim

ZSH_THEME="alanpeabody"

plugins=(
  git
  zsh-autosuggestions
  zsh-syntax-highlighting
  sudo
  history
)

source $ZSH/oh-my-zsh.sh

alias vim='nvim'
alias vi='nvim'

alias top='btop'

# ls aliases
alias ls='exa --icons'
alias ll='exa -l --icons'
alias la='exa -la --icons'

# git aliases
alias gs='git status'
alias gc='git commit'
alias gps='git push'
alias gpl='git pull'


## [Completion]
## Completion scripts setup. Remove the following line to uninstall
[[ -f /home/deerain/.config/.dart-cli-completion/zsh-config.zsh ]] && . /home/deerain/.config/.dart-cli-completion/zsh-config.zsh || true
## [/Completion]

# FastFetch при запуске терминала
if command -v fastfetch &> /dev/null && [ -z "$FASTFETCH_DISABLED" ]; then
    fastfetch
fi

# Включить автодополнение
autoload -U compinit && compinit

# Чувствительное к регистру автодополнение
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'

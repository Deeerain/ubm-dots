#!/bin/bash

style="~/.config/wofi/style.css"
USER=$(whoami)

menu() {
  echo " Выключить"
  echo " Перезагрузить"
  echo " Выйти"
  echo " Спящий режим"
  echo "  Режим гибернации"
  echo " Заблокировать"
  echo " Отмена"
}

choice=$(
  menu | wofi --show dmenu \
    --prompt "Выберите действие:" \
    --width 400 \
    --height 300 \
    --location center \
    --hide-scrollbar \
    --cache-file /dev/null
)

case "$choice" in
" Выключить")
  confirm=$(echo -e "Да\nНет" | wofi --show dmenu --prompt="Выключить компьютер?")
  [[ "$confirm" == "Да" ]] && systemctl poweroff
  ;;
" Перезагрузить")
  confirm=$(echo -e "Да\nНет" | wofi --show dmenu --prompt="Перезагрузить компьютер?")
  [[ "$confirm" == "Да" ]] && systemctl reboot
  ;;
" Выйти")
  confirm=$(echo -e "Да\nНет" | wofi --show dmenu --prompt="Выйти из системы?")
  [[ "$confirm" == "Да" ]] && pkill -u $USER
  ;;
" Спящий режим")
  systemctl suspend
  ;;
" Режим гибернации")
  systemctl hibernate
  ;;
" Заблокировать")
  hyprlock
  ;;
*)
  exit 0
  ;;
esac

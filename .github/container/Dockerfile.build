FROM archlinux:latest

# Устанавливаем зависимости
RUN pacman -Syu --noconfirm --needed \
    base-devel \
    git \
    sudo \
    namcap \
    devtools \
    && pacman -Scc --noconfirm

# Создаем пользователя для сборки
RUN useradd -m -G wheel -s /bin/bash builder && \
    echo "builder ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Рабочая директория
WORKDIR /build

# Копируем файлы
COPY . .

# Меняем владельца
RUN chown -R builder:builder .

# Собираем пакет
USER builder
RUN makepkg --syncdeps --noconfirm --clean --cleanbuild

# Копируем готовые пакеты
USER root
RUN mkdir -p /output && \
    find . -name "*.pkg.tar.*" -exec cp {} /output/ \;

FROM archlinux:latest

# Мета-информация
LABEL name="ubm-dots-builder"
LABEL version="1.0"
LABEL description="Builder for ubm-dots package"

# Обновляем и устанавливаем зависимости
RUN pacman -Syu --noconfirm --needed \
    base-devel \
    git \
    && echo "Кеш очищен" && \
    pacman -Scc --noconfirm

# Создаем пользователя с UID 1000 (совместимость с хостовой системой)
ARG USER_ID=1000
ARG GROUP_ID=1000

RUN groupadd -g ${GROUP_ID} builder && \
    useradd -m -u ${USER_ID} -g builder -s /bin/bash builder && \
    echo "builder ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Настраиваем git (убираем проблемный конфиг)
RUN git config --global --unset-all http.https://github.com/.extraheader 2>/dev/null || true

# Рабочая директория
WORKDIR /home/builder/ubm-dots

# Копируем исходники
COPY . .

# Исправляем права
RUN chown -R builder:builder /home/builder

# Переключаемся на пользователя
USER builder

# Проверяем PKGBUILD
RUN echo "=== Проверка PKGBUILD ===" && \
    if [ -f "PKGBUILD" ]; then \
        echo "✅ PKGBUILD найден" && \
        echo "Имя пакета: $(grep '^pkgname=' PKGBUILD | cut -d= -f2)" && \
        echo "Версия: $(grep '^pkgver=' PKGBUILD | cut -d= -f2)" && \
        echo "Ревизия: $(grep '^pkgrel=' PKGBUILD | cut -d= -f2)"; \
    else \
        echo "❌ PKGBUILD не найден" && exit 1; \
    fi

# Команда для сборки (с отключенной проверкой зависимостей)
CMD makepkg \
    --syncdeps \
    --noconfirm \
    --clean \
    --cleanbuild \
    --skipinteg \
    --nodeps \
    --nocheck

FROM "debian"

RUN apt-get update && \
    apt-get -y install xvfb xserver-xephyr x11-utils python3-pip python3-tk python3-dev scrot && \
    python3 -m pip install pyvirtualdisplay pillow EasyProcess python3-xlib pyautogui

# for testing
# RUN apt-get -y install firefox-esr
RUN apt-get -y install default-jre libgbm1 libgdk-pixbuf2.0-0 libgtk-3-0 xdg-utils libcurl4 wget && \
    wget https://launcher.mojang.com/download/Minecraft.deb && \
    dpkg -i Minecraft.deb

ENTRYPOINT ["/bin/bash"]

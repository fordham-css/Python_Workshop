#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See https://go.microsoft.com/fwlink/?linkid=2090316 for license information.
#-------------------------------------------------------------------------------------------------------------
FROM debian:stretch-slim

# This Dockerfile adds a non-root 'vscode' user with sudo access. However, for Linux,
# this user's GID/UID must match your local user UID/GID to avoid permission issues
# with bind mounts. Update USER_UID / USER_GID if yours is not 1000. See
# https://aka.ms/vscode-remote/containers/non-root-user for details.
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
		biber \
		latexmk \
		make \
		texlive-full \
	&& rm -rf /var/lib/apt/lists/*


RUN apt-get update && apt-get install -y git
# Install git, bash, dependencies, and add a non-root user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # [Optional] Add sudo support for the non-root user
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
    && chmod 0440 /etc/sudoers.d/$USERNAME

RUN apt-get install wget -y
RUN apt-get install -y gnupg2
# Add Fish
RUN echo 'deb http://download.opensuse.org/repositories/shells:/fish:/release:/3/Debian_9.0/ /' > /etc/apt/sources.list.d/shells:fish:release:3.list
RUN wget -nv https://download.opensuse.org/repositories/shells:fish:release:3/Debian_9.0/Release.key -O Release.key
RUN apt-key add - < Release.key
RUN apt-get update
RUN apt-get install fish -y

# Set up fish config
WORKDIR /home/vscode/.config/fish
RUN wget https://gist.githubusercontent.com/ThoolooExpress/e78e30ea9384fb833ed9defc269f04f1/raw/74b6f3c342db7552afba1ca48ccb5e56fd20dacd/config.fish

# SSH-Agent fix
RUN echo "\neval (ssh-agent -c)" >> /home/vscode/.config/fish/config.fish
RUN echo "\nssh-add ~/.ssh/id_rsa" >> /home/vscode/.config/fish/config.fish

# Add conda initialization to fish config
RUN echo "\nsource /opt/conda/etc/fish/conf.d/conda.fish" >> /home/${USERNAME}/.config/fish/config.fish


# Fix permissions
RUN chown -R $USERNAME:$USERNAME /home/$USER

# Install Conda (Weird global install, please don't copy these commands if you
# want to work on this outside of a dockerfile FFS)
# Note that there are some duplicate apt-get entries, but it really doesn't
# matter and I didn't feel like either messing with Conda's commands or
# busting the cache by deleting them up above and waste 20 mins

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda2-4.5.11-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

RUN apt-get install -y procps

# Install conda packages here so they'll get cached if this isn't the first build
# Copy environment.yml (if found) to a temp locaition so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no environment.yml exists.
COPY environment.yml* .devcontainer/noop.txt /tmp/conda-tmp/

USER $USERNAME
# Install Conda Environment
RUN if [ -f "/tmp/conda-tmp/environment.yml" ]; then /opt/conda/bin/conda env create -f /tmp/conda-tmp/environment.yml; fi

# Remove temp directory to avoid confusion
USER root
RUN rm -rf /tmp/conda-tmp

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=
ENTRYPOINT [ "/usr/bin/tini", "--" ]
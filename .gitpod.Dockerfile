FROM gitpod/workspace-python-3.11:latest

# Install & configure Doppler CLI
RUN (curl -Ls --tlsv1.2 --proto "=https" --retry 3 https://cli.doppler.com/install.sh || wget -t 3 -qO- https://cli.doppler.com/install.sh) | sudo sh
# Install temporal 
RUN curl -sSf https://temporal.download/cli.sh | sh
RUN echo export PATH="\$PATH:/home/gitpod/.temporalio/bin" >> ~/.bashrc
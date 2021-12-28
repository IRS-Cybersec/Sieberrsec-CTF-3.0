FROM ubuntu:20.04

RUN echo "pls update"
RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get install -y libncurses5 openssh-server

RUN DEBIAN_FRONTEND=noninteractive apt install -y tzdata

RUN useradd -ms /bin/bash rock_farming_simulator
RUN passwd -d rock_farming_simulator

WORKDIR /home/rock_farming_simulator
RUN ls /home/rock_farming_simulator -la

COPY ./bin/ /home/rock_farming_simulator/
RUN chown -R root:rock_farming_simulator /home/rock_farming_simulator && \
    chmod -R 750 /home/rock_farming_simulator && \
    chmod 740 /home/rock_farming_simulator/flag
COPY ./chal /usr/bin/chal
RUN chmod +x /usr/bin/chal

RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PermitEmptyPasswords no/PermitEmptyPasswords yes/' /etc/ssh/sshd_config
RUN sed -i 's/X11Forwarding yes/X11Forwarding no/' /etc/ssh/sshd_config
RUN sed -i 's/#AllowTcpForwarding yes/AllowTcpForwarding no/' /etc/ssh/sshd_config
RUN sed -i 's/#AllowAgentForwarding yes/AllowAgentForwarding no/' /etc/ssh/sshd_config
RUN sed -i 's/#PermitTunnel no/PermitTunnel no/' /etc/ssh/sshd_config
RUN sed -i '$aMatch User rock_farming_simulator' /etc/ssh/sshd_config
RUN sed -i '$a\\tForceCommand /usr/bin/chal' /etc/ssh/sshd_config 
RUN service ssh start

CMD ["/usr/sbin/sshd", "-D", "-p", "22"]

EXPOSE 22

# Verne
Verne is the second generation data collection and logging software for the VIP team Lightning from the Edge of Space at the Georgia Institute of Technology.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The software is designed to be run on a Docker container where a number of software libraries will be installed. As a result, the docker-ce package is required. Run the following command to install Docker:

```bash
curl -sSL https://get.docker.com | sh
```

### Building the Image

The Docker image is not available at the moment on the Docker hub, as a result, you need to compile it using the following command:

```bash
docker build -t gtviples/verne .
```

### Installing and Running

#### Easy, automated setup:

* The docker image can be built using `sudo ./scripts/build-image.sh`
* The container can be created using `sudo ./scripts/create-container.sh`
* The startup settings can be configured using `sudo ./scripts/startup-config.sh`

#### Manual setup:

To run the project, a container must be created with this image and the correct parameters. For example:

```bash
docker create \
    --name=verne
    --device /dev/ttyAMA0 \
    --device /dev/i2c-1 \
    -v /home/pi/vernedata:/data \
    gtviples/verne
```

Then, the container can be started and stopped using the `docker start verne` and `docker stop verne` commands.

Note that we are not running this container with a restart policy because of the fact that we want the code to run just once.
As a result, we need another way of making sure that the container is started on startup.

We start by making sure that the responsibility of starting docker is on systemd and not on upstart:

```bash
echo manual | sudo tee /etc/init/docker.override
sudo systemctl enable docker
```

We will use a systemd service setup to ensure that our container is run on boot. Create a file `/etc/systemd/system/verne.service` with the following contents:
```
[Unit]
Description=Verne
Requires=docker.service
After=docker.service

[Service]
Restart=no
ExecStart=/usr/bin/docker start -a verne
ExecStop=/usr/bin/docker stop -t 5 verne

[Install]
WantedBy=default.target
```
For convenience, this file is provided in the repository so that you can just copy and paste it.

To run the service, do the following:
```
systemctl daemon-reload
systemctl start verne.service
```

And to set it to start on startup, do the following:
```bash
systemctl enable verne.service
```


## Built With

* [Docker](https://www.docker.com/) - The container-based deployment system
* [PySerial](https://pythonhosted.org/pyserial/) - A library for interfacing with UART Serial devices
* [RTIMULib2](https://github.com/RTIMULib/RTIMULib2/) - A library for interfacing with Inertial Measurement devices

## Contributing

Please branch the code and create pull requests instead of merging or committing on the the master branch yourself. These pull requests will be reviewed by the lead developers before merging. As an overall principle, only production-ready code should be on the master branch.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/VIP-LES/Verne/tags). 

## Authors

* **Cem Gokmen** - *Initial work* - [skyman](https://github.com/skyman)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

This project was named after French author Jules Verne whose novel *Cinq semaines en ballon* was what first introduced the project's developer to the concept of aerostats.

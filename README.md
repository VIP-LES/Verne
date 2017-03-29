# Verne
Verne is the second generation data collection and logging software for the VIP team Lightning from the Edge of Space at the Georgia Institute of Technology.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The software is designed to be run on a Docker container where a number of software libraries will be installed. As a result, the docker-ce package is required. Run the following command to install Docker:

`curl -sSL https://get.docker.com | sh`

### Building the Image

At the moment, the Docker image is present on the Docker Hub as gtviples/verne, with the :latest tag pointing to the latest stable version here on master branch the repository and the :develop branch pointing to the develop branch. However, if you choose the build the image yourself from source, you may do so using the following command in the repository directory:

`docker build -t gtviples/verne .`

Note that this step is completely optional and that it should be done only if no internet connectivity is available.

### Installing and Running

To run the project, a container must be created with this image and the correct parameters, including the unless-stopped restart policy and the correct volume links to any devices. For example:

```
docker create \
    --name=verne
    --device /dev/ttyAMA0 \
    --device /dev/i2c-1 \
    -v /home/pi/vernedata:/data \
    --restart=unless-stopped \
    gtviples/verne
```

Then, the container can be started and stopped using the `docker start verne` and `docker stop verne` commands.

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

# Verne
Verne is the second generation data collection and logging software for the VIP team Lightning from the Edge of Space at the Georgia Institute of Technology.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The software is designed to be run on a Docker container where a number of software libraries will be installed. As a result, the docker-ce package is required. [Click here](https://docs.docker.com/engine/installation/linux/ubuntu/#install-docker) for details about installing Docker on Raspbian.

### Building the Image

At the moment, the Docker image is not present on the Docker Hub, as a result, it needs to be built on the host device. Build instructions will be added here shortly.

### Installing and Running

Once the image is built, a container must be created with this image and the correct parameters, including the unless-stopped restart policy and the correct volume links to any devices. Instructions will be added here shortly.

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

* Under construction

# VPN Service

A test task for imitating a VPN service.

## Run with Docker

**Docker must already be installed!**

```shell
git clone https://github.com/vitalii-babiienko/tt_vpn_service.git
cd tt_vpn_service
```

Create a **.env** file by copying the **.env.sample** file and populate it with the required values.

```shell
docker-compose up --build
```

## Get access

* Create a new user via [accounts/login/](http://localhost:8000/accounts/login/).
* Manage sites via [vpn/sites/](http://localhost:8000/vpn/sites/). 
* Get statistic via [vpn/statistics/](http://localhost:8000/vpn/statistics/). 

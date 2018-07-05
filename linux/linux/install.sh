#!/bin/bash
echo "##### Start pulling dependency packages... #####"
docker pull rethinkdb || echo "rethinkdb download failure" >insshi.log ; date > insshi.log ; echo "--------------------" > insshi.log 
docker pull microbox/etcd || echo "microbox/etcd pull failure" >insshi.log ; date > insshi.log ; echo "--------------------" > insshi.log
docker pull shipyard/docker-proxy || echo "shipyard/docker-proxy pull failure" >insshi.log ; date > insshi.log ; echo "--------------------" > insshi.log
docker pull swarm || echo "swarm pull failure" >insshi.log ; date > insshi.log ; echo "--------------------" > insshi.log 
docker pull dockerclub/shipyard || echo "dockerclub/shipyard pull failure" >insshi.log ; date > insshi.log ; echo "--------------------" > insshi.log && echo "#####  All dependency packages pulled successful! #####"

echo "##### Start install shipyard... #####"
sh deploy && echo "##### Install shipyard successful! #####"



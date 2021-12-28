if [ "$#" -eq 0 ] 
then    echo './setup.sh PORT EXECUTABLE_NAME DOCKER_NAME'
    exit 67
fi
if [ "$1" = "" ]
then	echo 'err: no port given'
	exit 67
fi
if [ -z "$3" ]
then    echo 'err: no docker image name given (make up a name related to your challenge)'
fi

# bin/ checking
executable="$2" # this is the basename of the executable
if [ -f "$executable" ] # bin/executable was given
then    executable="$(basename "$executable")"
elif ! [ -f "bin/$executable" ] # neither bin/$executable nor $executable are files
then	echo 'err: no executable given'
    exit 67
fi
if ! [ -f "bin/flag" ]
then	echo 'WARNING: no flag file found in bin/flag'
fi

[ -f "rebuild.sh" ] || echo "./setup.sh '$1' '$2' '$3'" > rebuild.sh # this might break
chmod +x rebuild.sh

sed -i "s,helloworld,$executable," ctf.xinetd
docker stop "$3"
docker rm "$3"
docker build -t "$3" .
docker run -m 512m --cpus .5 --restart unless-stopped -d -p "0.0.0.0:$1:9999" -h "$3" --name="$3" "$3"

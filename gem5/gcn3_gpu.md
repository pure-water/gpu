# Running GCN3 GPU docker image
It is based on this but with my own work   https://gem5.googlesource.com/public/gem5-resources/+/refs/heads/stable/src/gpu/square/

### Pull Docker image
        docker pull --disable-content-trust gcr.io/gem5-test/gcn-gpu:v21-2
 
### Get the GEM5 resource
        git clone https://gem5.googlesource.com/public/gem5

### GCN3-Test Resource
        git clone https://gem5.googlesource.com/public/gem5-resources

### Compile the Sqrt with the docker
        cd src/gpu/square
        docker run --rm -v ${PWD}:${PWD} -w ${PWD} -u $UID:$GID gcr.io/gem5-test/gcn-gpu:v21-2 make


### Compile the GEM5 with the docker
        git clone https://gem5.googlesource.com/public/gem5
        cd gem5
        docker run -u $UID:$GID --volume $(pwd):$(pwd) -w $(pwd) gcr.io/gem5-test/gcn-gpu:v21-2 scons build/GCN3_X86/gem5.opt -j <num cores>



### Run the SQRT with GCN architcture on the docker
        docker run -u $UID:$GID --volume $(pwd):$(pwd) -w $(pwd) gcr.io/gem5-test/gcn-gpu:v21-2 gem5/build/GCN3_X86/gem5.opt gem5/configs/example/apu_se.py -n 3 -c bin/square


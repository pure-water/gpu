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



### Topology

#### CU Part
![image](https://user-images.githubusercontent.com/2059536/147867096-ade0e529-38ee-4ed2-a67f-3c587534981b.png)

#### CPU Part
![image](https://user-images.githubusercontent.com/2059536/147867123-745d0df5-58e4-4d27-b6f6-f2ac268c4df6.png)

#### Whole Picture
![image](https://user-images.githubusercontent.com/2059536/147867140-8af19bb1-6fac-40cc-ad92-3b6e3194d176.png)

#### Host Side
![image](https://user-images.githubusercontent.com/2059536/147867161-296eaf60-334a-4123-9f14-8e56967a65d6.png)


#### Topology
![image](https://user-images.githubusercontent.com/2059536/147867253-df4fa891-aaaf-4539-831d-fd38f33cd4f4.png)
![image](https://user-images.githubusercontent.com/2059536/147867287-126ad095-249b-4316-a4e7-f9ca9b777f44.png)


### Workload
![image](https://user-images.githubusercontent.com/2059536/147867408-118a9d03-354e-4b2e-8d3f-8a16359a1927.png)


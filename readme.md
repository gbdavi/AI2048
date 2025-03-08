# Create image
docker build -t rl-ai-jupyter .

# Run container
docker run --name tf -p 8888:8888 -v ${PWD}:/app -it rl-ai-jupyter

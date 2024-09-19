export GENERATED_KEY=$(echo 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef | fold -w1 | shuf | tr -d '\n')
docker-compose build
docker-compose up

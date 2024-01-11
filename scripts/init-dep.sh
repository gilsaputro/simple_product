function main() {
  init_vault_dir=$1
  schema_vault_dir=$2
  init_es_dir=$3
  schema_es_dir=$4

  echo "INFO: checking redis instance..."
  test_redis_env "product_redis_local" "localhost" "redislocal" 2

  echo "INFO: checking postgres instance.."
  test_postgres_env "product_postgres_local" "product_postgres_local" 2

  echo "INFO: checking vault instance..."
  wait_for_http "hashicorp_vault" "localhost:8200/v1/sys/health" 2

  echo "INFO: storing secret to vault..."
  python $init_vault_dir/app.py $schema_vault_dir

  echo "INFO: all depedency up"
}

function wait_for_http() {
  name=$1
  addr=$2
  sleep_time=$3

  while [[ true ]]; do
    local code=`curl -s -o /dev/null -w "%{http_code}" $addr`
    if [ "$code" -eq "200" ]; then
      echo "INFO: $name is ready"
      break
    fi
    echo "INFO: $name is not ready...sleeping for a while before checking again"
    sleep $sleep_time
  done
}

function test_redis_env() {
  name=$1
  addr=$2
  password=$3
  sleep_time=$4

  while [[ true ]]; do
    local code=`docker exec $name redis-cli -h $addr -a $password ping`
    echo "docker exec $name redis-cli -h $addr -a $password ping"
    if [ "$code" == "PONG" ]; then
      echo "INFO: $name is ready"
      break
    fi
    echo "INFO: $name is not ready...sleeping for a while before checking again"
    sleep $sleep_time
  done
}

function test_postgres_env() {
  name=$1
  container=$2
  sleep_time=$3

  while [[ true ]]; do
    local code=`docker exec $container pg_isready`
    if [[ "$code" == *"accepting connections"* ]]; then
      echo "INFO: $name is ready"
      break
    fi
    echo "INFO: $name is not ready...sleeping for a while before checking again"
    sleep $sleep_time
  done
}

main "$@"
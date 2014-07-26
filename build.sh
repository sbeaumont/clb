export PYTHONPATH=$PYTHONPATH:./lib/requests

while getopts ":c:t" opt; do
  case $opt in
    c)
      find . -name "*.pyc" -delete
      ;;
    t)
      python -m tabnanny test
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

python -m unittest discover
# create integration folder for scraper component
rm -r scapres
mkdir scapres

# scraper code
rsync -a --exclude=integration ../* scapres/.

# server utils code
cp -r ../../server_utils scapres/.

# run shell file
cp run.sh scapres/.

# environment variables file
cp env scapres/.

# dockerfile
cp Dockerfile scapres/.

# requirement file
cp ../../requirements.txt scapres/.

echo "Done scraper prepare for integration"
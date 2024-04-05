
ARCH=$(uname -m)
echo "System architecture is: $ARCH"

if [ $ARCH == "x86_64" ]; then
	SCALADOWNLOAD=https://github.com/coursier/coursier/releases/latest/download/cs-x86_64-pc-linux.gz
elif [ $ARCH == "arm64" ]; then
	SCALADOWNLOAD=https://github.com/VirtusLab/coursier-m1/releases/latest/download/cs-aarch64-pc-linux.gz
fi

echo "Downloading from: $SCALADOWNLOAD"
# this command never works properly
curl -fL "$SCALADOWNLOAD" | gzip -d > cs && chmod +x cs && ./cs setup

chmod +x cs && ./cs setup
cs install scala:2.12.8
printf "Installed scala and sbt with coursier cli\n"
printf "Scala version:"
echo scala -version
printf "Sbt version:"
echo sbt -version 
echo export PATH="$PATH:/home/benchmarker/.local/share/coursier/bin" >> ~/.bashrc

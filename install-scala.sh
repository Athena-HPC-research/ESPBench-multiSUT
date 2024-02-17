curl -fL https://github.com/coursier/coursier/releases/latest/download/cs-x86_64-pc-linux.gz | gzip -d > cs
chmod +x cs && ./cs setup
cs install scala:2.12.8
printf "Installed scala and sbt with coursier cli\n"
printf "Scala version:"
echo scala -version
printf "Sbt version:"
echo sbt -version 
echo export PATH="$PATH:/home/benchmarker/.local/share/coursier/bin" >> ~/.bashrc

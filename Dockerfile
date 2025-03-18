FROM python:3.14-rc-bookworm

RUN apt-get update -y && apt-get install -y git vim

# Copy requirements 
COPY requirements.txt /tmp/

# Install dependencies 
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy all project files into /dev
WORKDIR /dev
COPY . .

# Keep the container running with an interactive shell
CMD ["bash"]


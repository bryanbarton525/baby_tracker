FROM python:3.6

# Install requirements
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN rm -rf requirements.txt

# Create User
RUN useradd tracker
WORKDIR /home/tracker


# Copy files
COPY classes classes
COPY configs configs
COPY web_gui web_gui
COPY launch_site.py launch_site.py

# change ownership and run
RUN chown -R tracker:tracker ./
USER tracker

CMD ["python", "launch_site.py"]
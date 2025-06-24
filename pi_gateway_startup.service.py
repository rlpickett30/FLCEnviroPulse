[Unit]
Description=EnviroPulse Gateway Startup Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/enviroPulse/gateway/gateway_startup.py
WorkingDirectory=/home/pi/enviroPulse/gateway
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target

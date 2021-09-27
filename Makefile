STREAM_URI=rtsp://ryder:ryder@10.0.0.186/live
PI_IP_ADDRESS=10.0.0.86

.PHONY: run
run:
	@echo "Starting Script"
	@. env/bin/activate && export STREAM_URI=$(STREAM_URI) && export RASPBERRY_PI_HOST=$(PI_IP_ADDRESS) && cd src && python app.py

.PHONY: install
install:
	@cd scripts && bash install_pi.sh

.PHONY: copy
copy:
	@rsync -a --exclude env ./ pi@$(PI_IP_ADDRESS):/home/pi/halloween_mannequin_head/

.PHONY: shell
shell:
	@ssh pi@$(PI_IP_ADDRESS)

.PHONY: server
server:
	@echo "Starting Server"
	@. env/bin/activate && cd src && python server.py

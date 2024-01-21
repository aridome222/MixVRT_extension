clean:
	sudo rm -rf app/base_dir app/diff_dir
	sudo rm -rf app/disp/static/images/diff_html_png
	sudo rm -rf app/disp/static/images/diff_img_png
	sudo rm -rf app/disp/static/images/original_png
	sudo rm -rf app/disp/static/images/sub_effect_png

save:
	rm -rf app/base_dir/current
	cp -r app/base_dir/latest app/base_dir/current

run:
	docker exec -it zenn_selenium-python-1 python3 app/MixVRT.py $(URL)
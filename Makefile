clean:
	sudo rm -rf python/app/base_dir python/app/diff_dir
	sudo rm -rf python/app/disp/static/images/diff_html_png
	sudo rm -rf python/app/disp/static/images/diff_img_png
	sudo rm -rf python/app/disp/static/images/original_png
	sudo rm -rf python/app/disp/static/images/sub_effect_png

save:
	sudo rm -rf python/app/base_dir/current/
	sudo cp -r python/app/base_dir/latest/ python/app/base_dir/current/

test:
	docker exec -it zenn_selenium-python-1 python3 python/app/MixVRT.py $(URL)
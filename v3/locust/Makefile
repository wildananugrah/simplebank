run-locust:
	@locust -f simple_locust.py -u 2 -r 1

run-locust-100:
	@locust -f 100_users_normal_all_locust.py -u 2 -r 1

run-headless-locust:
	@locust -f simple_locust.py -u 1 -r 1 --host http://45.113.235.79:3000 --headless
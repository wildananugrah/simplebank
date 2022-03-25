run-locust:
	@locust -f simple_locust.py -u 2 -r 1

run-locust-100:
	@locust -f 100_users_normal_all_locust.py -u 100 -r 1

run-locust-1000:
	@locust -f 1000_users_normal_all_locust.py -u 1000 -r 1

run-locust-10000:
	@locust -f 10000_users_normal_all_locust.py -u 10000 -r 1

run-locust-20000:
	@locust -f 20000_users_normal_all_locust.py -u 20000 -r 1


run-headless-locust:
	@locust -f simple_locust.py -u 1 -r 1 --host http://45.113.235.79:3000 --headless
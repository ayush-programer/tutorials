#include <iostream>
#include <thread>
#include <future>
#include <chrono>

namespace PromiseEx {

	static std::promise<bool> test;

	static void threadHandler(const int seconds) {
		std::this_thread::sleep_for(std::chrono::seconds(seconds));

		test.set_value(true);
	}

	static void startTestRaw(const int seconds) {
		std::future<bool> test_future { PromiseEx::test.get_future() };

		std::thread testThread(PromiseEx::threadHandler, seconds);

		if (test_future.get())
			std::cout << "Promise value properly set." << std::endl;

		testThread.join();
	}

	static void startTest(const int seconds) {

		if (seconds <= 0)
			throw std::invalid_argument("Please provide proper "
						    "integer greater than zero "
						    "as number of seconds.");
		startTestRaw(seconds);
	}
}

int main(const int argc, const char* argv[]) {

	try {
		if (argc < 2)
			throw std::invalid_argument("Please provide number "
						    "of seconds.");

		PromiseEx::startTest(std::stoi(argv[1]));
	}
	catch (std::invalid_argument& ex) {
		std::cout << "Error: ";
		std::cout << ex.what() << std::endl;

		return 1;
	}
	catch (...) {
		std::cout << "Error: Unforeseen consequences." << std::endl;

		return 2;
	}

	return 0;
}

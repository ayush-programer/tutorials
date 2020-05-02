#include <iostream>
#include <thread>
#include <chrono>
#include <future>
#include <vector>
#include <string>

namespace AsyncEx {

	static int test {};
	std::mutex mutex;

	static int produce() {

		std::this_thread::sleep_for(std::chrono::seconds(2));
		std::lock_guard<std::mutex> guard(mutex);

		return test++;
	};

	static void throw_arg_error() {

		throw std::invalid_argument("No numeric value provided. "
					    "Skipping pre-produce...");
	}

	static void preProduceRaw(int count) {

		std::vector<std::future<int>> preFutures;
		bool hashTable[count] { false };
		auto begin { std::chrono::steady_clock::now() };
		std::mutex hash_mutex;

		for (size_t i = 0; i < count; i++) {
			preFutures.push_back(std::async(std::launch::async,
					     AsyncEx::produce));
		}

		for (auto& preFuture: preFutures) {
			auto el = preFuture.get();

			std::lock_guard<std::mutex> guard_lock(hash_mutex);
			if (hashTable[el])
				throw std::logic_error("Hash collision!");
			hashTable[el] = true;
		}

		std::cout << "Pre-produced " << count << " in: " << std::chrono::duration <double, std::ratio<1, 1>> (std::chrono::steady_clock::now() - begin).count() << "s" << std::endl;
	}

	static void preProduce(int count) {

		if (count == 0)
			throw_arg_error();

		std::cout << "Pre-producing..." << std::endl;

		preProduceRaw(count);
	}
};

int main(int argc, char* argv[]) {

	std::future<int> res {};

	std::cout << "Press CTR+C to stop any time..." << std::endl;

	try {
		if (argc != 2)
			AsyncEx::throw_arg_error();

		AsyncEx::preProduce(std::stoi(argv[1]));

	}
	catch (const std::logic_error &ex) {
		std::cout << ex.what() << std::endl;
	}
	catch (const std::exception &ex) {
		std::cout << "Error: ";
		std::cout << ex.what() << std::endl;
	}

	while(true) {
		res = std::async(std::launch::async, AsyncEx::produce);

		std::cout << "Got: " << res.get() << std::endl;
	}

	return 0;
}

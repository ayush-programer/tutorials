#include <iostream>
#include <thread>
#include <chrono>
#include <future>
#include <vector>
#include <string>

namespace AsyncEx {

	static int produce(const int seconds) {
		static int test {};
		static std::mutex mutex;

		std::this_thread::sleep_for(std::chrono::seconds(seconds));
		std::lock_guard<std::mutex> guard(mutex);

		return test++;
	};

	static void preProduceRaw(const int count, const int seconds) {
		std::vector<std::future<int>> preFutures;
		bool hashTable[count] { false };
		std::mutex hash_mutex;
		auto begin { std::chrono::steady_clock::now() };

		for (size_t i = 0; i < count; i++)
			preFutures.push_back(std::async(std::launch::async,
					     AsyncEx::produce, seconds));

		for (auto& preFuture: preFutures) {
			auto el = preFuture.get();

			/* check returned element consistency */
			std::lock_guard<std::mutex> guard_lock(hash_mutex);

			if (hashTable[el])
				throw std::logic_error("Hash collision!");

			hashTable[el] = true;
		}

		std::cout << "Produced " << count << " in: "
			  << std::chrono::duration <double, std::ratio<1, 1>>
			    (std::chrono::steady_clock::now() - begin).count()
			  << "s" << std::endl;
	}

	static void preProduce(const int count, const int seconds) {

		if (count == 0)
			throw std::invalid_argument("Please provide numeric "
						    "argument greater than zero.");

		if (seconds == 0)
			throw std::invalid_argument("Seconds should be an integer "
						    "greater than zero.");

		std::cout << "Producing... ";
		std::cout << "Press CTR+C to stop any time..." << std::endl;

		preProduceRaw(count, seconds);
	}
};

int main(int argc, char* argv[]) {

	try {
		if (argc == 1)
			throw std::invalid_argument("No numeric value provided.");

		AsyncEx::preProduce(std::stoi(argv[1]),
				    argc == 3 ? std::stoi(argv[2]) : 2);

	}
	catch (const std::invalid_argument &ex) {
		std::cout << "Error: ";
		std::cout << ex.what() << std::endl;

		return 1;
	}
	catch (const std::logic_error &ex) {
		std::cout << ex.what() << std::endl;

		return 2;
	}
	catch (const std::exception &ex) {
		std::cout << "Error: ";
		std::cout << ex.what() << std::endl;

		return 3;
	}

	return 0;
}
